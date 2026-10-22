---
tags:
  - seed
aliases:
  - Flyway
  - DB Migration
created: 2026-10-20
---

Flyway는 "DB 스키마의 변경 이력을 SQL 파일(버전) 단위로 코드 저장소에 남기고, 애플리케이션이 뜰 때 아직 적용되지 않은 버전만 순서대로 DB에 적용해 주는" DB 마이그레이션 도구다. 쉽게 말해 DB 스키마를 위한 Git이다.

# 사용 목적

우리가 사용한다는 redis, mysql, postgresql등은 dbms로 데이터베이스를 관리해주는 시스템이지 실질적으로 db자체를 의미하는 바는 아니다. 즉 다양한 환경이나, 다른 다른 사람들과 작업을 하다가 보면 동일한 dbms를 사용하더라도 다른 db 스키마로 인하여 동일한 테이블로 개발을 진행하지 않을 수도 있고, 심하면 충돌이 발생할 수 있다. 또한 테스트 데이터처럼 모두가 동일한 테스트를 진행해야 하는 부분에 대해 다른 테스트 데이터를 db에 설정할 경우 설정 오류가 발생할 수밖에 없다. 따라서 dbms가 아닌 db자체에서 데이터 및 스키마를 통일하기 위해 db migration(복제)가 필요하고, 이는 spring boot 내장 의존성인 flyway를 통해 쉽게 진행할 수 있다. 

> [!note] 보충 / 정정
> 1. migration은 "복제"가 아니다. 복제(Replication)는 한 DB의 데이터를 다른 DB로 실시간 복사하는 것(Primary-Replica)이고, migration은 "스키마를 버전 A 상태에서 버전 B 상태로 옮기는(이행하는) 작업"이다. Flyway가 다루는 것은 데이터 복사가 아니라 스키마 변경 이력의 순차 적용이다.
> 2. Flyway는 Spring Boot "내장" 의존성이 아니다. Spring Boot는 Flyway의 버전 관리(dependency management)와 자동 설정(FlywayAutoConfiguration)만 제공하고, 실제 라이브러리는 build.gradle에 직접 추가해야 동작한다. 버전을 적지 않아도 되는 것일 뿐, 처음부터 들어 있는 것은 아니다.
> 3. 핵심 가치는 "모든 환경(내 로컬, 다른 기기, CI, 운영)의 스키마가 같은 SQL 파일들로부터 같은 순서로 만들어진다"는 재현성이다. 스키마가 코드와 함께 Git으로 리뷰/버전 관리된다는 것이 JPA ddl-auto와의 가장 큰 차이다.

# 0. 왜 ddl-auto: update로는 부족한가

지금 프로젝트는 spring.jpa.hibernate.ddl-auto: update로 엔티티를 보고 Hibernate가 테이블을 알아서 만들고 고친다. 개발 초기에는 편하지만 운영 관점에서는 다음 문제가 있다.

1. 컬럼 이름 변경을 "추가"로 처리한다. 엔티티 필드명을 바꾸면 기존 컬럼은 남고 새 컬럼이 생긴다. 데이터는 옛 컬럼에 그대로 남는다.
2. 컬럼/테이블 삭제, 타입 축소, 제약조건 변경은 거의 반영하지 않는다. 결과적으로 기기마다 "쓰레기 컬럼"이 다르게 쌓여 스키마가 갈라진다.
3. 무엇이 언제 바뀌었는지 기록이 남지 않는다. 리뷰도, 롤백 계획도 불가능하다.
4. 인덱스, 데이터 이관(예: 기존 행에 기본값 채우기) 같은 작업을 표현할 수 없다.
5. 운영 DB에 애플리케이션이 임의로 DDL을 실행하는 것은 실무에서 사실상 금지다.

그래서 실무 표준은 "스키마 변경은 Flyway(또는 Liquibase) 스크립트로만, JPA는 ddl-auto: validate로 엔티티와 스키마가 일치하는지 검사만" 하는 구조다.

| 구분 | ddl-auto: update | Flyway |
| --- | --- | --- |
| 스키마의 근거 | 엔티티 클래스 | 버전별 SQL 파일 |
| 변경 이력 | 없음 | flyway_schema_history 테이블 + Git |
| 컬럼 rename/drop | 사실상 불가 | SQL로 명시 |
| 데이터 이관 | 불가 | UPDATE/INSERT 가능 |
| 환경 간 재현성 | 낮음 (실행 이력에 따라 달라짐) | 높음 (같은 파일, 같은 순서) |
| 운영 사용 | 비권장 | 표준 |

# 1. 동작 원리

Flyway의 원리는 단순하다. "DB 안에 이력 테이블을 하나 두고, 파일 목록과 이력을 비교해서 빠진 것만 실행한다."

1. 애플리케이션 시작 시 Flyway가 DB에 접속해 flyway_schema_history 테이블을 찾는다. 없으면 만든다.
2. classpath:db/migration 아래의 마이그레이션 파일들을 스캔해 버전 순으로 정렬한다.
3. 이력 테이블에 기록된 버전과 비교해, 이미 적용된 파일은 체크섬(CRC32)이 그대로인지 검증(validate)한다.
4. 아직 적용되지 않은 버전만 순서대로 실행(migrate)하고, 각각의 결과를 이력 테이블에 한 행씩 기록한다.
5. 여기까지 끝나야 JPA(EntityManagerFactory)가 초기화된다. Spring Boot가 "JPA는 Flyway에 의존한다"는 순서를 자동으로 보장하기 때문에, Hibernate가 validate할 시점에는 이미 스키마가 최신이다.

flyway_schema_history의 주요 컬럼:

| 컬럼 | 의미 |
| --- | --- |
| installed_rank | 적용된 순서 |
| version | 파일 이름의 버전 (V3__xxx.sql → 3) |
| description | 파일 이름의 설명 부분 |
| type | SQL, JDBC(Java 마이그레이션), BASELINE 등 |
| script | 파일 이름 |
| checksum | 파일 내용의 CRC32 값. 파일이 수정되면 값이 달라져 validate가 실패한다 |
| installed_on / execution_time | 적용 시각 / 소요 시간(ms) |
| success | 성공 여부 (1/0) |

가장 중요한 규칙이 여기서 나온다. 한 번 적용된(특히 다른 환경과 공유된) 마이그레이션 파일은 절대 수정하지 않는다. 고치고 싶으면 새 버전 파일을 추가한다. 수정하면 체크섬이 달라져서 다른 환경에서 애플리케이션이 아예 기동하지 않는다.

# 2. 파일 이름 규칙

기본 위치: src/main/resources/db/migration (Spring Boot 기본값 classpath:db/migration)

```
V1__init_schema.sql
V2__add_index_on_orders_user_id.sql
V2_1__add_column_users_phone.sql
R__create_view_order_summary.sql
```

1. 접두사: V = Versioned(한 번만 실행), R = Repeatable(체크섬이 바뀔 때마다 재실행), U = Undo(유료 에디션 전용, 무료에서는 사용 불가).
2. 버전: 숫자이며 _ 또는 .으로 구분하면 소수 버전이 된다. V2_1은 2.1로 해석되어 V2와 V3 사이에 정렬된다. 문자열 정렬이 아니라 숫자 정렬이므로 V10이 V9 뒤에 온다.
3. 구분자: 밑줄 두 개(__). 하나만 쓰면 인식하지 못하거나 잘못 파싱된다. 가장 흔한 실수다.
4. 설명: 밑줄은 공백으로 바뀌어 description에 저장된다. 무엇을 하는 파일인지 동사로 쓴다.
5. 같은 버전이 두 파일에 있으면 기동 시 에러가 난다.

Repeatable(R__) 파일은 항상 모든 V 파일이 적용된 뒤에 실행된다. 뷰, 프로시저처럼 "현재 정의로 통째로 다시 만들면 되는" 객체에 쓴다. 테이블에는 쓰지 않는다.

# 3. Spring Boot 프로젝트에 추가하기

#### 3-1. 의존성 (Gradle)

```gradle
dependencies {
    implementation 'org.flywaydb:flyway-core'
    runtimeOnly 'org.flywaydb:flyway-mysql'   // MySQL/MariaDB 사용 시 필수
    runtimeOnly 'com.mysql:mysql-connector-j'
}
```

1. 버전을 적지 않는다. Spring Boot의 dependency management가 Boot 버전에 맞는 Flyway 버전을 고른다 (Boot 3.3 기준 Flyway 10.x).
2. Flyway 10부터 DB별 지원이 별도 모듈로 분리되어 있다. flyway-core만 넣고 MySQL에 붙이면 "Unsupported Database: MySQL 8.0" 에러로 기동이 실패한다. MySQL이면 flyway-mysql, PostgreSQL이면 flyway-database-postgresql을 함께 넣는다.
3. classpath에 flyway-core가 있으면 Spring Boot는 자동으로 Flyway를 실행한다(spring.flyway.enabled 기본값 true). 별도 코드가 필요 없다.

#### 3-2. application.yml

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mall_db?serverTimezone=Asia/Seoul
    username: root
    password: root

  jpa:
    hibernate:
      ddl-auto: validate          # 스키마 생성은 Flyway, JPA는 검증만

  flyway:
    enabled: true
    locations: classpath:db/migration   # 기본값이라 생략 가능
    baseline-on-migrate: false          # 기존 DB에 처음 도입할 때만 고려 (5장)
    validate-on-migrate: true           # 기본값. 적용된 파일 변조 시 기동 실패
    clean-disabled: true                # 기본값. 실수로 전체 삭제(clean) 방지
    out-of-order: false                 # 기본값. 낮은 버전이 뒤늦게 추가되면 거부
```

자주 쓰는 프로퍼티:

| 프로퍼티 | 기본값 | 설명 |
| --- | --- | --- |
| spring.flyway.enabled | true | Flyway 자동 실행 여부 |
| spring.flyway.locations | classpath:db/migration | 스캔 위치. 콤마로 여러 개 지정 가능 |
| spring.flyway.baseline-on-migrate | false | 이력 테이블이 없는 비어있지 않은 스키마를 만나면 baseline 생성 |
| spring.flyway.baseline-version | 1 | baseline으로 기록할 버전. 이 버전 이하 파일은 건너뜀 |
| spring.flyway.validate-on-migrate | true | migrate 전에 체크섬 검증 |
| spring.flyway.out-of-order | false | 이미 V5가 적용된 뒤 V4가 새로 생겨도 실행할지 |
| spring.flyway.clean-disabled | true | clean(스키마 전체 drop) 금지 |
| spring.flyway.url / user / password | datasource 값 사용 | 마이그레이션만 DDL 권한 계정으로 돌릴 때 사용 |
| spring.flyway.placeholders.* | - | SQL 안의 ${name} 치환 |

실무 팁: 운영에서는 애플리케이션 datasource 계정에는 DML 권한만 주고, spring.flyway.user에만 DDL 권한 계정을 주는 방식으로 권한을 분리하기도 한다.

#### 3-3. 첫 마이그레이션 작성

src/main/resources/db/migration/V1__init_schema.sql

```sql
CREATE TABLE users (
    id          BIGINT       NOT NULL AUTO_INCREMENT,
    email       VARCHAR(255) NOT NULL,
    password    VARCHAR(255) NOT NULL,
    created_at  DATETIME(6)  NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

(예시 테이블이다. 실제 V1은 현재 엔티티 기준으로 만들어야 한다. 방법은 5장 참고)

#### 3-4. 실행 및 확인

1. 애플리케이션을 실행하면 로그에 다음과 비슷한 줄이 찍힌다.
   ```
   Flyway Community Edition 10.x by Redgate
   Database: jdbc:mysql://localhost:3306/mall_db (MySQL 8.0)
   Successfully validated 1 migration
   Creating Schema History table `mall_db`.`flyway_schema_history` ...
   Current version of schema `mall_db`: << Empty Schema >>
   Migrating schema `mall_db` to version "1 - init schema"
   Successfully applied 1 migration to schema `mall_db`, now at version v1
   ```
2. DB에서 확인한다.
   ```sql
   SELECT installed_rank, version, description, checksum, success
   FROM flyway_schema_history ORDER BY installed_rank;
   ```
3. 다시 실행하면 "Schema `mall_db` is up to date. No migration necessary."가 나와야 정상이다.

# 4. 스키마를 바꿀 때의 작업 흐름

엔티티를 바꾸는 순간, 짝이 되는 마이그레이션 파일도 같은 커밋에 들어가야 한다.

1. 엔티티 수정 (예: User에 phone 필드 추가)
2. 다음 버전 파일 작성: V2__add_phone_to_users.sql
   ```sql
   ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;
   ```
3. 애플리케이션 실행 → Flyway가 V2 적용 → Hibernate validate가 엔티티와 스키마가 맞는지 확인
4. 엔티티와 SQL이 어긋나면 기동 시 "Schema-validation: missing column [phone] in table [users]" 같은 에러가 난다. 이 에러가 나는 것이 안전장치가 정상 동작하는 것이다.
5. 엔티티 + 마이그레이션 파일을 한 커밋/PR로 올린다. 리뷰어는 SQL을 보고 운영 영향(락, 데이터 손실)을 판단한다.

#### 데이터가 있는 테이블을 바꿀 때 (실무 패턴)

1. NOT NULL 컬럼 추가: 한 번에 NOT NULL로 추가하면 기존 행 때문에 실패하거나 의도치 않은 기본값이 들어간다. "NULL 허용으로 추가 → UPDATE로 값 채우기 → NOT NULL로 변경"으로 나눈다.
2. 컬럼 이름 변경: 운영 중인 서비스라면 "새 컬럼 추가 → 양쪽 쓰기 → 데이터 이관 → 코드가 새 컬럼만 읽게 배포 → 옛 컬럼 삭제"(expand and contract)로 여러 버전에 걸쳐 진행한다. 배포 중 구버전 서버와 신버전 서버가 동시에 떠 있을 수 있기 때문이다.
3. 대용량 테이블 ALTER: MySQL 8은 많은 ALTER를 ALGORITHM=INSTANT/INPLACE로 처리하지만 일부는 테이블 복사(COPY)와 락이 걸린다. 운영 규모에서는 gh-ost, pt-online-schema-change 같은 도구를 쓴다. 학습 단계에서는 "ALTER가 락을 잡을 수 있다"는 사실만 기억하면 된다.

# 5. 이미 테이블이 있는 DB에 Flyway 도입하기 (Baseline)

ddl-auto로 이미 테이블이 만들어진 DB에 Flyway를 켜면, Flyway는 "이력 테이블이 없는데 스키마가 비어있지 않다"며 기동을 거부한다 (Found non-empty schema(s) ... but no schema history table). 방법은 두 가지다.

#### 방법 A. 개발 DB를 비우고 V1부터 다시 만든다 (로컬 개발 단계 권장)

1. 현재 스키마를 V1__init_schema.sql로 뽑아낸다.
   ```bash
   docker exec db mysqldump -uroot -proot --no-data --skip-add-drop-table --skip-comments mall_db > V1__init_schema.sql
   ```
   뽑은 파일에서 AUTO_INCREMENT=숫자, /*!40101 ... */ 같은 환경 종속 구문을 정리한다.
2. 또는 Hibernate에게 DDL 스크립트를 파일로 생성하게 해서 참고할 수 있다 (DB에 실행하지 않고 파일만 생성).
   ```yaml
   spring:
     jpa:
       properties:
         jakarta.persistence.schema-generation.scripts.action: create
         jakarta.persistence.schema-generation.scripts.create-target: build/schema.sql
   ```
   생성된 SQL은 그대로 쓰지 말고, 제약조건 이름, 인덱스, charset을 사람이 다듬어서 V1에 옮긴다.
3. 로컬 DB를 비운다 (docker-compose의 mysql_data 볼륨을 지우거나 DROP DATABASE). 지우기 전에 남겨야 할 데이터가 없는지 확인한다.
4. Flyway를 켜고 실행하면 빈 DB에 V1부터 적용된다. 모든 기기에서 같은 절차를 밟으면 스키마가 완전히 같아진다.

#### 방법 B. 기존 데이터를 유지하고 baseline을 찍는다 (데이터를 지울 수 없는 DB)

```yaml
spring:
  flyway:
    baseline-on-migrate: true
    baseline-version: 1
```

1. Flyway가 이력 테이블을 만들고 "버전 1 = BASELINE"이라는 행을 기록한다. 즉 "이 DB는 이미 V1 상태다"라고 선언하는 것이다.
2. V1 파일은 실행하지 않고 건너뛰며, V2부터 적용한다.
3. 전제: 그 DB의 실제 스키마가 V1 파일 내용과 정확히 같아야 한다. 다르면 이후 V2가 엉뚱한 상태 위에 적용된다.
4. baseline-on-migrate는 처음 도입 시점에만 의미가 있다. 이미 이력 테이블이 있으면 무시된다. 도입이 끝나면 false로 돌려두는 편이 안전하다.

# 6. 실패했을 때 (MySQL에서 특히 중요)

1. PostgreSQL은 DDL도 트랜잭션 안에서 롤백되지만, MySQL은 DDL마다 암묵적 커밋(implicit commit)이 일어나 롤백되지 않는다. 그래서 파일 하나에 DDL 3개가 있고 2번째에서 실패하면 1번째는 이미 반영된 반쪽 상태로 남는다.
2. 이때 이력 테이블에는 success=0인 행이 남고, 이후 기동은 "Detected failed migration to version X"로 계속 실패한다.
3. 복구 순서
   1. 반쯤 적용된 변경을 DB에서 수동으로 되돌린다 (또는 나머지를 수동 적용).
   2. SQL 파일을 고친다 (실패한 버전은 성공 기록이 없으므로 이 경우에 한해 수정 가능).
   3. flyway repair로 실패 기록을 제거한다.
   4. 다시 migrate한다.
4. 예방책: MySQL에서는 마이그레이션 파일 하나에 DDL 하나(또는 아주 적게)를 원칙으로 한다. 실패 범위가 작아진다.
5. repair는 "실패 행 삭제 + 현재 파일 기준으로 체크섬 재정렬"을 한다. 체크섬 불일치를 repair로 덮는 것은 "누군가 적용된 파일을 수정했다"는 문제를 숨기는 것이므로, 원인을 확인하기 전에는 쓰지 않는다.

Spring Boot는 기동 시 migrate만 실행한다. repair, info 같은 명령은 다음 중 하나로 실행한다.

1. Flyway CLI 도커 이미지
   ```bash
   docker run --rm --network host -v "$PWD/src/main/resources/db/migration:/flyway/sql" flyway/flyway -url=jdbc:mysql://localhost:3306/mall_db -user=root -password=root info
   ```
   (info 자리에 validate, repair 등. macOS Docker Desktop에서 --network host가 안 되면 localhost 대신 host.docker.internal 사용)
2. Flyway Gradle 플러그인 (org.flywaydb.flyway)
3. Spring Boot Actuator의 /actuator/flyway 엔드포인트로 적용 이력 조회 (조회만 가능)

| 명령 | 하는 일 |
| --- | --- |
| migrate | 미적용 버전을 순서대로 적용 (Spring Boot가 기동 시 실행) |
| info | 파일별 상태(Success, Pending, Failed, Ignored 등) 출력 |
| validate | 적용된 파일과 현재 파일의 체크섬 비교 |
| repair | 실패 기록 삭제, 체크섬 재정렬 |
| baseline | 기존 스키마를 특정 버전으로 표시 |
| clean | 스키마의 모든 객체 삭제. 운영에서는 절대 금지 (기본 비활성화) |

# 7. 여러 사람/여러 기기에서 쓸 때의 규칙

1. 적용된 파일은 수정하지 않는다. 오타라도 새 버전으로 고친다.
2. 버전 번호 충돌: 브랜치 A와 브랜치 B가 각자 V3을 만들면 머지 후 같은 버전이 두 개가 되어 기동이 실패한다. 해결책은 둘 중 하나다.
   1. 머지 직전에 main의 최신 버전을 확인하고 번호를 다시 매긴다 (아직 공유 DB에 적용되지 않았을 때만 가능).
   2. 처음부터 타임스탬프 버전을 쓴다: V20261020_1530__add_phone_to_users.sql. 충돌 가능성이 거의 없어 팀 단위에서 많이 쓴다.
3. out-of-order는 기본 false로 둔다. 켜면 늦게 머지된 낮은 버전도 실행되지만, 실행 순서가 환경마다 달라져 Flyway를 쓰는 의미(재현성)가 약해진다.
4. 마이그레이션 파일은 엔티티 변경과 같은 PR에 넣고, 리뷰 때 SQL을 반드시 읽는다.
5. 시드/테스트 데이터는 스키마 마이그레이션과 위치를 분리한다.
   ```yaml
   # application-local.yml (local 프로필에서만)
   spring:
     flyway:
       locations: classpath:db/migration,classpath:db/seed
   ```
   db/seed 아래 데이터 파일도 버전이 필요하다. 스키마와 번호가 섞이지 않도록 V1000__seed_products.sql처럼 대역을 나누거나, R__seed_*.sql(INSERT IGNORE 등으로 재실행해도 안전하게)로 작성한다. 운영 프로필에는 seed 경로를 넣지 않는다.
6. Flyway와 spring.sql.init(schema.sql, data.sql)을 동시에 쓰지 않는다. 스키마를 만드는 주체가 둘이 되면 순서가 꼬인다.

# 8. 테스트 환경

1. src/test/resources/application.yml은 main의 application.yml을 "덮어쓰는(병합)" 것이 아니라 "대체"한다 (classpath에서 같은 이름의 파일이 test 쪽에서 먼저 발견됨). 따라서 main에서 spring.flyway.enabled를 어떻게 설정했든, 테스트에서는 test 쪽 yml에 적힌 값(없으면 기본값 true)이 적용된다.
2. 테스트가 H2(MODE=MySQL)를 쓰는 경우, MySQL 전용 문법(ENGINE=InnoDB, 일부 ALTER 구문, 함수 등)이 H2에서 실패할 수 있다. 선택지는 다음과 같다.
   1. 테스트에서 Flyway를 끄고 ddl-auto: create-drop 유지: 가장 간단하지만 마이그레이션 SQL 자체는 검증되지 않는다.
   2. 테스트에서도 Flyway를 켜고 H2 호환 SQL만 쓴다: MySQL 전용 기능을 포기해야 한다.
   3. Testcontainers로 실제 MySQL 컨테이너를 띄워 Flyway + ddl-auto: validate로 테스트: 실무에서 가장 권장되는 방식. 운영과 같은 DB로 마이그레이션까지 검증된다.
3. 최소한 CI 어딘가에서는 "빈 MySQL에 V1부터 끝까지 적용 → validate 통과"를 한 번은 검증해야 한다. 이게 없으면 깨진 마이그레이션이 배포 시점에 처음 발견된다.

# 9. 자주 만나는 에러

| 에러 메시지 (요약) | 원인 | 해결 |
| --- | --- | --- |
| Unsupported Database: MySQL 8.0 | flyway-mysql 모듈 누락 | runtimeOnly 'org.flywaydb:flyway-mysql' 추가 |
| Found non-empty schema(s) ... but no schema history table | 기존 테이블이 있는 DB에 처음 도입 | 5장 방법 A 또는 B |
| Validate failed: Migration checksum mismatch for migration version X | 적용된 파일을 수정함 | 파일을 원래대로 되돌리고 새 버전으로 수정. 로컬 DB 한정이면 DB 초기화도 가능 |
| Detected failed migration to version X | 이전 실행에서 X가 실패 | 6장 복구 순서 |
| Found more than one migration with version X | 같은 버전 파일 두 개 (브랜치 머지 충돌) | 번호 재지정 |
| Detected resolved migration not applied to database | 더 높은 버전이 이미 적용된 DB에 낮은 버전 파일이 추가됨 | 번호를 최신 뒤로 옮기거나 (신중히) out-of-order |
| Schema-validation: missing column / wrong column type | 엔티티와 마이그레이션이 어긋남 (ddl-auto: validate) | 빠진 변경을 새 버전 파일로 추가 |
| 파일이 있는데 마이그레이션이 0개로 나옴 | 경로 오타, 밑줄 하나(_), 확장자 오류 | db/migration 경로와 V숫자__설명.sql 형식 확인 |

# 10. 이 프로젝트에서의 현재 상태 (2026-10-20, main 기준)

1. 의존성: build.gradle에 flyway-core, flyway-mysql이 이미 추가되어 있다 (3-1 완료).
2. 설정: application.yml에서 spring.flyway.enabled: false, spring.jpa.hibernate.ddl-auto: update. 즉 Flyway는 들어만 있고 꺼져 있으며, 스키마는 여전히 Hibernate가 만든다.
3. 마이그레이션 파일: src/main/resources/db/migration 폴더와 V1 파일이 아직 없다.
4. 테스트: src/test/resources/application.yml은 H2(MODE=MySQL) + ddl-auto: create-drop이고 flyway 설정이 없다. V1이 생기는 순간 테스트에서는 Flyway가 기본값(true)으로 켜져 H2에 V1을 실행하려 하므로, 8장 선택지 중 하나를 미리 정해야 한다.
5. 로컬 DB는 docker-compose의 mysql:8.0 + ./mysql_data 볼륨이고, 두 기기(Mac mini, MacBook)가 각자 DB를 가진다. ddl-auto: update로 쌓인 스키마가 기기마다 다를 수 있으므로 도입은 5장 방법 A(볼륨 초기화 후 V1부터)가 적합하다.

#### 도입 체크리스트

- [ ] 현재 엔티티 기준으로 V1__init_schema.sql 작성 (mysqldump 또는 Hibernate 스크립트 생성 후 다듬기)
- [ ] spring.flyway.enabled: true, spring.jpa.hibernate.ddl-auto: validate로 변경
- [ ] 테스트 환경 방침 결정 (Flyway off / H2 호환 SQL / Testcontainers)
- [ ] 두 기기 모두 로컬 DB 볼륨 초기화 후 기동하여 flyway_schema_history에 V1 success=1 확인
- [ ] 버전 명명 규칙 결정 (순번 vs 타임스탬프). 두 기기가 다른 브랜치에서 작업하므로 타임스탬프 쪽이 충돌에 안전
- [ ] 이후 엔티티 변경 시 반드시 V(n+1) 파일을 같은 커밋에 포함

# 참고

1. Flyway 공식 문서: https://documentation.red-gate.com/flyway
2. Spring Boot 공식 문서: Database Initialization → Use a Higher-level Database Migration Tool
3. Spring Boot 공통 프로퍼티 목록 (spring.flyway.*): https://docs.spring.io/spring-boot/appendix/application-properties/index.html
