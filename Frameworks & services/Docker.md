---
tags:
  - seed
aliases: []
created: 2026-08-22
---

Docker는 "이 애플리케이션이 필요로 하는 실행 환경 전체(코드, 런타임, 라이브러리, 설정)를 하나의 패키지(이미지)로 묶어서, 어디서 실행하든 완전히 동일하게 동작하게 만드는" 컨테이너 가상화 기술이다.

# 0. Docker가 해결하려는 문제
지금까지 이 프로젝트를 진행하면서 이미 겪은 문제들이 사실 Docker가 정확히 해결하는 문제다.

- MySQL을 로컬(Homebrew)로 설치해서 쓰다가 포트 충돌/PID 문제를 겪었던 것 (ShoppingMall - 트러블 슈팅 기록.md에도 기록되어 있음) — "내 컴퓨터에 이미 설치된 MySQL"과 "이 프로젝트가 원하는 MySQL 설정"이 충돌한 경우다.
- Redis를 Homebrew로 로컬에 띄워놓고 그게 우연히 떠있어서 앱이 동작하는 상태 (실제로 docker-compose에 redis 서비스가 빠져있다는 걸 이전에 지적한 적이 있다) — "내 컴퓨터에만 있는 어떤 것" 때문에 우연히 되는 상태.

Docker는 이런 "내 컴퓨터에만 있는 상태" 자체를 없앤다. 컨테이너 안에는 이 애플리케이션이 필요로 하는 것만 정확히 들어있고, 호스트 컴퓨터에 뭐가 설치되어 있는지와 무관하게 항상 똑같이 동작한다.

# 1. 컨테이너 vs 가상머신(VM) — 그리고 가상 메모리와의 관계
이 부분이 원리적으로 가장 중요하고, 컴퓨터공학적으로 정확히 이해해야 하는 부분이다.

## 1-1. VM의 원리
전통적인 가상머신(VirtualBox, VMware 등)은 *하이퍼바이저(Hypervisor)* 가 물리 하드웨어를 통째로 가상화해서, 그 위에 *완전히 별개의 커널을 가진 게스트 OS*를 통째로 하나 더 띄운다.

- 호스트 OS 위에 하이퍼바이저가 있고, 그 위에 게스트 OS(자체 커널 포함)가 통째로 하나 더 돌아간다.
- 이때 메모리 관점에서 무슨 일이 일어나냐면: 원래 OS는 프로세스마다 *가상 주소(virtual address)를 물리 주소(physical address)로 변환*하는 페이지 테이블을 커널이 관리하고, CPU의 MMU(Memory Management Unit)가 이 변환을 하드웨어적으로 수행한다. 그런데 VM 환경에서는 *게스트 OS도 자기 나름의 페이지 테이블(게스트 가상주소 → 게스트가 "물리주소"라고 믿는 주소)을 가지고 있고*, 그 게스트의 "물리주소"는 사실 진짜 물리주소가 아니라 하이퍼바이저가 관리하는 또 다른 가상의 주소 공간이다. 그래서 실제 물리 메모리에 도달하려면 *주소 변환을 두 번* 거쳐야 한다 (게스트 가상주소 → 게스트 물리주소 → 호스트 물리주소).
- 이걸 예전에는 하이퍼바이저가 소프트웨어적으로 흉내내는 *섀도우 페이지 테이블(Shadow Page Table)* 방식으로 처리했는데 느렸고, 요즘 CPU는 이 2단계 변환을 하드웨어가 직접 지원한다 (Intel의 *EPT, Extended Page Table* / AMD의 *NPT, Nested Page Table*). 그래도 결국 "주소 변환을 두 번 하는" 근본적인 오버헤드는 여전히 있다.

정리하면: *VM은 커널 자체를 통째로 하나 더 돌리고, 그 커널이 쓰는 가상 메모리 체계를 하이퍼바이저가 한 번 더 가상화(2단계 주소변환)한다.* 그래서 VM은 무겁고(자체 커널 부팅 필요), 느리게 시작되고(수십 초~수 분), 메모리도 게스트 OS 커널 몫만큼 추가로 먹는다.

## 1-2. 컨테이너(Docker)의 원리
Docker 컨테이너는 *커널을 하나 더 안 돌린다.* 호스트 OS의 커널을 컨테이너들이 *그대로 공유*한다. 그럼 격리는 어떻게 하냐면, 리눅스 커널이 원래 제공하는 두 가지 기능만으로 격리를 흉내낸다.

1. *Namespace (무엇이 "보이는지"를 격리)*: 리눅스 커널은 프로세스별로 "이 프로세스한테는 어떤 자원이 보이는가"를 나누는 기능을 여러 종류 제공한다.
   - PID namespace: 컨테이너 안에서는 자기 프로세스가 PID 1번부터 보인다 (실제 호스트에서는 다른 번호를 갖고 있어도).
   - NET namespace: 컨테이너 전용 네트워크 인터페이스/IP를 가진 것처럼 보인다.
   - MNT namespace: 컨테이너 전용 파일시스템 마운트 트리를 가진 것처럼 보인다 (그래서 컨테이너 안에서 /를 봐도 호스트의 /가 안 보이고 이미지 안의 파일들만 보인다).
   - UTS namespace: 컨테이너 전용 호스트네임을 가진 것처럼 보인다.
   - IPC namespace, USER namespace 등도 비슷한 원리.
2. *cgroups (Control Groups, 얼마나 "쓸 수 있는지"를 제한)*: 이 프로세스 그룹이 CPU를 몇 %까지, 메모리를 몇 MB까지, 디스크 I/O를 얼마나까지 쓸 수 있는지 커널 레벨에서 제한한다. (docker run --memory=512m 같은 옵션이 결국 이 cgroup 설정을 대신 해주는 것이다.)

## 1-3. 그래서 가상 메모리 관점에서 정확히 무슨 차이인가
이게 핵심이다 — *컨테이너는 새로운 가상 메모리 계층을 추가하지 않는다.*

호스트 OS 위에서 돌아가는 "일반 프로세스"는 원래부터 자기만의 독립된 가상 주소 공간을 갖는다 (이건 컨테이너와 무관하게, 리눅스/유닉스 프로세스라면 원래 다 그렇다 — 프로세스 A와 B가 똑같이 0x00400000 주소를 쓴다고 해도 서로 다른 물리 메모리를 가리키는 이유가 이것이다). 즉 *"프로세스마다 독립된 가상 주소 공간"이라는 격리는 컨테이너가 있기 전부터 호스트 커널의 MMU + 페이지 테이블이 이미 제공하던 기능*이다.

Docker 컨테이너 안의 프로세스는 그냥 *호스트 커널 입장에서는 평범한 프로세스 하나*다. 그 프로세스가 갖는 가상주소 → 물리주소 변환도 호스트 커널이 관리하는 *단 하나의 페이지 테이블 체계* 안에서 그대로 이루어진다 (VM처럼 2단계 변환이 없다). Docker가 하는 일은:

- namespace로 "이 프로세스한테 다른 프로세스나 파일시스템이 안 보이게" 시야를 가리고
- cgroup으로 "이 프로세스가 페이지(메모리)를 얼마나 확보할 수 있는지" 상한선을 그어주는 것

뿐이다. 새로운 메모리 관리자를 만드는 게 아니라, *원래 있던 프로세스 격리 체계에 "안 보이게" + "제한하기"라는 두 겹의 규칙만 얹은 것*이다.

*이게 바로 컨테이너가 VM보다 압도적으로 가볍고 빠른(수백 ms 안에 시작되는) 근본적인 이유다.* 새 커널을 부팅할 필요도 없고, 주소 변환을 두 번 할 필요도 없다 — 그냥 호스트 커널이 관리하는 프로세스 목록에 프로세스 하나가 더 추가되는 것뿐이고, 그 프로세스가 보는 세상(파일시스템, 네트워크, 프로세스 목록)만 커널이 눈속임을 해주는 것이다.

| | VM | Docker 컨테이너 |
|---|---|---|
| 커널 | 게스트 OS가 자체 커널을 새로 부팅 | 호스트 커널을 그대로 공유 |
| 격리 방식 | 하드웨어 가상화(하이퍼바이저) | 커널의 namespace + cgroup |
| 가상 메모리 | 2단계 주소변환 (게스트 가상→게스트 물리→호스트 물리) | 호스트가 원래 하던 1단계 변환 그대로 (새 계층 없음) |
| 시작 속도 | 수십 초~수 분 (OS 부팅) | 수백 ms (프로세스 하나 fork/exec) |
| 자원 오버헤드 | 게스트 커널 몫만큼 추가 소모 | 거의 없음(프로세스 하나 수준) |
| 격리 강도 | 강함(커널 자체가 다름) | 상대적으로 약함(커널을 공유하므로 커널 취약점에 같이 노출될 수 있음) |

# 2. Docker 이미지의 원리 — 레이어와 Union File System
Docker 이미지는 하나의 큰 파일이 아니라, *읽기 전용 레이어(layer)를 여러 겹 쌓아올린 것*이다. 이걸 가능하게 하는 게 *OverlayFS*(Union File System의 한 구현체)다.

- Dockerfile의 명령어(FROM, RUN, COPY 등) *한 줄마다 레이어 하나*가 생긴다고 생각하면 된다.
- 이미지를 실제로 컨테이너로 *실행*할 때는, 이 읽기 전용 레이어들 맨 위에 *쓰기 가능한 레이어(container layer)* 를 하나 추가로 얹는다. 컨테이너 안에서 파일을 수정/생성하면 전부 이 맨 위 쓰기 레이어에만 기록된다 (아래 읽기 전용 레이어는 절대 바뀌지 않는다).
- 이 방식을 *Copy-on-Write(CoW)* 라고 한다 — 아래 레이어의 파일을 수정하려고 하면, 그 파일을 통째로 맨 위 쓰기 레이어로 복사해온 뒤 그 복사본을 수정한다.
- 컨테이너를 삭제하면 이 맨 위 쓰기 레이어도 통째로 사라진다 — *컨테이너는 기본적으로 휘발성(stateless)* 이라는 원칙이 여기서 나온다. (그래서 DB처럼 데이터가 남아있어야 하는 건 뒤에서 다룰 *Volume*을 반드시 써야 한다.)
- 레이어는 *캐시되고 재사용된다*: 같은 레이어(같은 명령어 + 같은 이전 레이어 상태)는 다시 만들지 않고 캐시를 그대로 쓴다. 이게 Dockerfile 작성 순서가 중요한 이유다 (아래 3번에서 설명).

# 3. Dockerfile 작성법
Spring Boot(Gradle) 프로젝트 기준 예시:

```dockerfile
# 1단계: 빌드 전용 환경 (최종 이미지에는 안 남음 — 아래 4번 멀티스테이지 참고)
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app

# 의존성 파일만 먼저 복사 (소스코드보다 먼저!)
COPY build.gradle settings.gradle gradlew ./
COPY gradle ./gradle
RUN ./gradlew dependencies --no-daemon

# 이제 소스코드 복사 & 빌드
COPY src ./src
RUN ./gradlew build --no-daemon -x test

# 2단계: 실제 실행 환경 (훨씬 가벼움)
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

각 명령어의 의미:

- FROM: 베이스 이미지 지정. 모든 Dockerfile의 첫 줄이며, 이 이미지의 레이어들 위에 내 레이어를 쌓기 시작한다.
- WORKDIR: 이후 명령어들이 실행될 기준 디렉터리 (없으면 자동 생성).
- COPY: 호스트(빌드하는 내 컴퓨터 또는 CI 서버)의 파일을 이미지 안으로 복사.
- RUN: 이미지를 빌드하는 시점에 실행되는 명령. 결과가 레이어로 남는다.
- ENV: 컨테이너 실행 시 환경변수 기본값 설정.
- EXPOSE: 이 컨테이너가 몇 번 포트를 쓰는지 "문서화"하는 용도 (실제로 포트를 열어주는 건 아니고, docker run -p로 실제 매핑을 해줘야 함).
- ENTRYPOINT vs CMD: 둘 다 "컨테이너 시작 시 실행할 명령"을 정하지만, ENTRYPOINT는 고정된 진입점(웬만하면 안 바뀜), CMD는 기본 인자(실행 시 덮어쓰기 쉬움)라는 성격 차이가 있다. 실행 파일이 하나로 고정된 경우(지금처럼 java -jar app.jar)엔 ENTRYPOINT를 쓰는 게 일반적이다.

## 3-1. 왜 의존성 설치를 소스코드 복사보다 먼저 하는가 (레이어 캐싱 실전 팁)
위 Dockerfile에서 COPY build.gradle ... → RUN ./gradlew dependencies를 COPY src ...보다 먼저 둔 이유가 있다. Docker는 *레이어를 위에서부터 순서대로 캐시 검사*하는데, 어떤 레이어를 만드는 명령어와 그 입력(이전 레이어 + 복사되는 파일 내용)이 이전 빌드와 완전히 같으면 그 레이어를 다시 만들지 않고 캐시를 그대로 쓴다.

- 소스코드(src/)는 코드를 한 줄만 고쳐도 매번 바뀐다. 만약 COPY src → COPY build.gradle처럼 *소스코드 복사를 의존성 설치보다 먼저* 둔다면, 소스코드가 한 글자만 바뀌어도 그 뒤에 있는 "의존성 다운로드" 레이어까지 전부 캐시가 깨져서 매번 처음부터 다시 다운로드하게 된다.
- 반대로 지금처럼 *거의 안 바뀌는 것(의존성 목록)을 먼저, 자주 바뀌는 것(소스코드)을 나중에* 두면, 코드만 고쳤을 때는 의존성 다운로드 레이어는 캐시를 그대로 재사용하고 소스코드 이후 레이어만 새로 빌드한다 — 빌드 시간이 훨씬 짧아진다.

이건 CI/CD 노트에서 다룬 actions/cache의 캐시 히트/미스 원리, 그리고 Redis 노트의 캐싱 원리와도 본질적으로 같은 이야기다: *"자주 안 바뀌는 것과 자주 바뀌는 것을 분리해서, 안 바뀌는 부분은 재계산하지 않는다."*

## 3-2. .dockerignore — 이미지에 넣으면 안 되는 것을 걸러내기
COPY . .처럼 현재 디렉터리를 통째로 복사하는 경우, .git/, node_modules/, IDE 설정 파일, 로컬 .env 파일까지 전부 이미지 안에 들어가 버릴 수 있다. .gitignore와 똑같은 문법으로 .dockerignore 파일을 만들어두면 COPY/ADD 시점에 해당 경로들을 아예 빌드 컨텍스트에서 제외한다.

```
# .dockerignore (프로젝트 루트)
.git
node_modules
build
.gradle
.env
*.md
```

이게 왜 중요하냐면:
1. *이미지 용량/빌드 속도*: 불필요한 파일까지 복사하면 레이어 크기가 커지고, 빌드 컨텍스트를 Docker 데몬으로 전송하는 시간도 늘어난다.
2. *보안*: .env처럼 실제 비밀번호/키가 든 파일이 실수로 이미지 안에 그대로 박제되는 걸 막는다 — 이미지는 나중에 레지스트리에 올라가고 다른 사람도 pull 받을 수 있으므로, 한 번 들어간 민감정보는 이미지를 지워도 이미 퍼졌을 수 있다.
3. *캐시 효율*: node_modules처럼 빌드 때마다 새로 만들어지는 디렉터리를 호스트에서 그대로 복사해오면, 3-1번에서 설명한 레이어 캐싱이 오히려 방해받는다 (내용이 계속 바뀌니 캐시가 계속 깨짐).

# 4. 멀티스테이지 빌드 (Multi-stage build)
위 Dockerfile에서 FROM ... AS build와 두 번째 FROM이 나뉜 게 멀티스테이지 빌드다.

- *왜 필요한가*: Gradle로 빌드하려면 JDK 전체(컴파일러 등, 용량이 큼)가 필요하지만, 빌드된 jar를 *실행*만 하는 데는 JRE(실행 환경만, JDK보다 훨씬 작음)면 충분하다. 만약 하나의 스테이지로만 만들면, 최종 이미지 안에 필요도 없는 JDK/Gradle 캐시/소스코드까지 전부 남아서 이미지 용량이 커진다 (배포/전송 속도, 공격 표면 모두에 안 좋다).
- *원리*: FROM ... AS build로 이름 붙인 스테이지에서 빌드까지 마치고, 그 다음 FROM eclipse-temurin:21-jre로 *완전히 새로운 이미지*를 시작한 뒤, COPY --from=build로 *빌드 결과물(jar 파일)만* 콕 집어서 가져온다. 앞 스테이지의 나머지 레이어(JDK, 소스코드, 중간 산출물)는 최종 이미지에 전혀 포함되지 않는다.
- 결과적으로 "빌드에 필요한 무거운 도구들"과 "실행에 필요한 가벼운 런타임"을 완전히 분리해서, 최종 이미지는 실행에만 필요한 것만 남는다.

# 5. Docker Compose — 여러 컨테이너를 함께 정의하기
실제 이 프로젝트는 컨테이너 하나가 아니라 *백엔드 + MySQL + Redis + 프론트엔드*, 최소 4개의 컨테이너가 함께 떠야 동작한다. 이걸 매번 docker run 명령어로 하나씩 띄우면 옵션이 너무 많고 실수하기 쉽다. *Docker Compose*는 이 여러 컨테이너의 구성을 YAML 파일 하나로 선언하고, docker compose up 한 번으로 전부 띄워주는 도구다.

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: shopping_mall
    ports:
      - "3306:3306"
    volumes:
      - db-data:/var/lib/mysql   # 컨테이너 삭제돼도 데이터는 남도록

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  backend:
    build: ./backend/shopping-mall-api    # 이 경로의 Dockerfile로 직접 빌드
    depends_on:
      - db
      - redis
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://db:3306/shopping_mall
      SPRING_REDIS_HOST: redis
    ports:
      - "8080:8080"

  frontend:
    build: ./frontend/shopping-mall-web
    depends_on:
      - backend
    ports:
      - "3000:3000"

volumes:
  db-data:   # named volume 선언
```

문법 요소:

- services: 컨테이너 하나하나를 정의하는 최상위 키. 각 서비스 이름(db, redis, backend, frontend)이 곧 컨테이너를 부르는 이름이자 아래에서 설명할 네트워크상의 호스트명이 된다.
- image: 이미 만들어진 이미지를 그대로 받아서 씀 (MySQL, Redis처럼 내가 직접 빌드할 필요 없는 것들).
- build: 내가 직접 작성한 Dockerfile로 이미지를 빌드해서 씀 (내 애플리케이션들).
- depends_on: 시작 순서를 지정 (단, *컨테이너가 "시작됨"과 "서비스가 실제로 요청을 받을 준비가 됨"은 다르다* — MySQL 컨테이너가 시작은 됐지만 아직 초기화 중이라 backend가 먼저 연결을 시도해서 실패하는 경우가 실제로 자주 생긴다. 정교하게 하려면 healthcheck + condition: service_healthy를 추가로 써야 한다).
- ports: "호스트포트:컨테이너포트": 호스트 컴퓨터의 포트를 컨테이너 내부 포트로 연결(포트 포워딩).
- volumes: 아래 6번에서 설명하는 데이터 영속화.
- environment: 컨테이너 실행 시 주입할 환경변수. ${MYSQL_ROOT_PASSWORD}처럼 .env 파일이나 셸 환경변수를 그대로 참조할 수 있다 (Dockerfile에 비밀번호를 하드코딩하면 안 되는 이유이자, CI/CD 노트의 Secrets와 같은 문제의식).

# 6. Volume — 컨테이너는 휘발성이라는 원칙과 데이터 영속화
2번에서 설명했듯 컨테이너의 쓰기 레이어는 컨테이너를 삭제하면 사라진다. MySQL 컨테이너를 재시작할 때마다 데이터가 날아가면 안 되므로, *컨테이너의 파일시스템과 무관하게 살아남는 저장 공간*이 필요하다. 이게 Volume이다.

- *Named volume* (db-data:/var/lib/mysql): Docker가 관리하는 별도의 저장 영역을 만들어서 컨테이너 내부의 특정 경로에 마운트한다. 컨테이너를 삭제해도 이 volume 자체는 별도로 남아있고, 새 컨테이너를 만들 때 같은 volume을 다시 연결하면 데이터가 그대로 이어진다.
- *Bind mount* (./local-folder:/app/data): 호스트의 실제 디렉터리를 컨테이너 안에 그대로 연결. 로컬 개발 중 코드를 수정하면 바로 컨테이너에 반영되게 하고 싶을 때 주로 쓴다.

트러블슈팅 기록에 있던 "MySQL이 pid로 백그라운드에서 포트를 물고 있어서 어려웠다"는 문제는, 결국 *로컬에 직접 설치한 MySQL과 컨테이너 안의 MySQL이 같은 3306 포트를 두고 충돌*하는 상황이었을 가능성이 높다 — Docker로 완전히 옮기면 이런 충돌 자체가 원천적으로 사라진다(로컬에 아예 MySQL을 설치할 필요가 없어지므로).

# 7. 네트워크 — 컨테이너끼리는 어떻게 서로를 찾는가
Docker Compose로 띄운 서비스들은 기본적으로 같은 *bridge 네트워크*에 자동으로 묶인다. 이 네트워크 안에서는 *서비스 이름 자체가 DNS처럼 동작*한다 — 위 예시에서 backend가 db에 접속할 때 IP 주소를 몰라도 그냥 호스트명 db로 접속하면 된다(jdbc:mysql://db:3306/...).

- 이게 가능한 이유는 Docker가 내장 DNS 서버를 이 네트워크에 자동으로 붙여주기 때문 — 컨테이너 이름을 IP로 알아서 변환(resolve)해준다.
- 반대로 *호스트(내 컴퓨터)에서* 컨테이너에 접속하려면 ports로 열어둔 포트(localhost:8080 등)를 써야 한다 — 컨테이너 이름은 호스트 입장에서는 의미가 없다(호스트는 이 내부 DNS 네트워크 밖에 있으므로).

# 8. 자주 쓰는 명령어 모음
```bash
docker build -t myapp:latest .          # 현재 디렉터리의 Dockerfile로 이미지 빌드
docker images                            # 로컬에 있는 이미지 목록
docker run -p 8080:8080 myapp:latest     # 이미지를 컨테이너로 실행 (포트 매핑)
docker ps                                # 실행 중인 컨테이너 목록
docker ps -a                             # 멈춘 것 포함 전체 목록
docker exec -it <컨테이너ID> /bin/bash    # 실행 중인 컨테이너 내부에 셸로 진입
docker logs -f <컨테이너ID>               # 실시간 로그 확인
docker stop <컨테이너ID>                  # 정지
docker rm <컨테이너ID>                    # 삭제 (정지된 것만 가능)

docker compose up -d                     # compose 파일 기준 전체 서비스 백그라운드 실행
docker compose down                      # 전체 정지 & 컨테이너/네트워크 정리 (volume은 안 지워짐, -v 옵션 추가해야 지워짐)
docker compose logs -f backend           # 특정 서비스 로그만 실시간 확인

docker system prune                      # 안 쓰는 이미지/컨테이너/네트워크 한 번에 정리 (디스크 용량 확보)
docker inspect <컨테이너ID>                # 컨테이너의 상세 설정(환경변수, 네트워크, 마운트 등) JSON으로 확인
```

# 9. 이미지를 레지스트리에 올리고 받기 (실제 배포로 이어지는 흐름)
지금까지는 내 컴퓨터 안에서 이미지를 빌드하고 실행하는 것까지였다. 실제로 *다른 서버(배포 서버)* 에서 이 이미지를 쓰려면, 이미지를 어딘가에 올려두고 그 서버가 받아갈 수 있어야 한다. 이 "어딘가"가 *레지스트리(Registry)* 다 — Docker Hub가 가장 널리 쓰이는 공개 레지스트리이고, GitHub Container Registry(ghcr.io)나 회사 자체 프라이빗 레지스트리를 쓰기도 한다.

```bash
docker login                                          # 레지스트리 로그인 (Docker Hub 기준, 최초 1회)

docker build -t shopping-mall-api .                    # 로컬 이름으로 우선 빌드
docker tag shopping-mall-api myaccount/shopping-mall-api:1.0.0   # 레지스트리 계정/이름 규칙에 맞게 태그를 붙임
docker push myaccount/shopping-mall-api:1.0.0          # 레지스트리에 업로드

# --- 배포 서버 쪽에서 ---
docker pull myaccount/shopping-mall-api:1.0.0          # 레지스트리에서 이미지 내려받기
docker run -d -p 8080:8080 myaccount/shopping-mall-api:1.0.0   # 받은 이미지로 컨테이너 실행
```

- *docker tag가 왜 필요한가*: 로컬에서 편하게 지은 이미지 이름(shopping-mall-api)을, 레지스트리가 요구하는 형식(레지스트리계정/이미지이름:태그)으로 다시 이름 붙이는 것뿐이다. 실제로 이미지를 복사하는 게 아니라 *같은 이미지에 이름표(참조)를 하나 더 붙이는 것*이다 (2번에서 다룬 레이어 구조상 실체는 하나, 이름만 여러 개일 수 있다).
- *태그(:1.0.0) 관리*: :latest만 계속 쓰면 "지금 서버에 떠있는 게 정확히 어떤 버전인지" 추적이 안 된다. 실무에서는 버전 번호나 Git 커밋 SHA(:${{ github.sha }}, CI/CD 노트의 예시 참고)를 태그로 써서 *어떤 코드가 배포되어 있는지 항상 역추적 가능하게* 만든다.
- 바로 이 tag/push/pull 흐름이 CI/CD 노트의 build-and-push-image Job과 deploy Job이 실제로 하는 일이다 — CI 서버에서 build+tag+push까지 하고, 배포 서버는 pull+run(또는 docker compose up -d)만 하는 구조.

# 10. 이 프로젝트에 적용할 그림
로드맵에 따라 최종적으로는 다음과 같은 구조가 된다.

1. backend/shopping-mall-api/Dockerfile — 위 3~4번 예시처럼 멀티스테이지로 Spring Boot 이미지 작성
2. frontend/shopping-mall-web/Dockerfile — Next.js도 비슷하게 npm ci → npm run build 후 next start로 실행하는 멀티스테이지 구성
3. 루트(또는 지정 경로)의 docker-compose.yml — 위 5번 예시처럼 db(MySQL) / redis / backend / frontend 4개 서비스 정의
4. CI/CD(GitHub Actions) 노트의 build-and-push-image Job이 바로 여기서 정의한 Dockerfile들을 빌드해서 레지스트리에 올리고, deploy Job이 배포 서버에서 이 docker-compose.yml을 다시 실행(docker compose up -d)하는 흐름으로 이어진다.

이전 트러블슈팅 기록에서 언급됐던 "redis 서비스가 docker-compose.yml에 아직 없다"(현재는 로컬 Homebrew Redis로 우연히 동작 중)는 부분이, 정확히 5번 예시의 redis 서비스 블록을 실제로 추가해야 하는 지점이다.
