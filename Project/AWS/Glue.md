https://github.com/niceguy61/aws_study_glue_athena?tab=readme-ov-file
데이터를 읽고, 분류하여, 저장하는 서비스로 순서는 다음과 같다.
asdf

1. 데이터를 crawler를 통해 읽어온다.
2. 테이블 및 파티션을 생성한다.
3. 위 메타데이터를 저장한다.

위 방식을 통해 만들어진 메타데이터를 Amazon에서 지원하는 RDS, DynamoDB, S3에 저장한다.1

1. IAM 권한이 없는 사용자를 생성한다.
2. S3, RDS, DynamoDB 중 하나에 사용할 데이터를 업로드 한다.
3. glue에서 사용자에 권한을 부여해준다. (사용자에 해당 storage read-only 권한 부여) : 저장소의 데이터를 읽고, 해당 데이터의 스키마를 따서 테이블로 만들어줄 것이기에 쓸 권한은 필요 없다.
4. crawler 세팅
5. crawler run 후에 테이블 확인 : 테이블이 정상적으로 생성 되었으면 성공
6. ETL job을 통해 데이터셋 정규화

5번 과정에서 실행을 했는데 테이블이 생성되지 않는 경우, 
1. policy(권한) : 역할 부여할 때, 권한이 붙게 되는데, 해당 권한이 이전 권한과 연동되어 기존 정책이 붙어다니게 됨 -> json resource에서 다른 권한을 지우던가, read-only같은 정책을 삭제할 경우 권한이 정상적으로 붙는다. 
2. csv 파일의 lock : 사용자가 lock을 지정하지 않게 되어도, excel과 같은 텍스트 편집기를 한번이라도 열게 된다면 os단계에서 파일시스템에 대한 권한 보호를 자동적으로 걸게 된다. 물론 프로그램 닫을 경우 빠른 시간 내에 lock이 풀리지만, 풀리지 않았던 경우 크롤링을 진행해도 
# Job

- ETL 파이프라인이 자동으로 실행되는 단위
#### ETL
- Extract : 데이터 추출
- Tranfer : 데이터 변환
- Load : 데이터 적재

# Data Catalog

- AWS에서 데이터베이스 내에 여러 데이터베이스와 유사한 catalog가 존재하도록 설계(스키마와 유사)
- 각 데이터베이스 catalog는 여러 테이블로 구성
- 따라서 

#### metadata
- 소스타입, 데이터포멧, 컬럼정보를 담고있는 데이터
- 데이터를 설명하기 위한 데이터로 실제 데이터들을 나타내거나, 알려주는 데이터를 의미한다.

# Table 생성방법

1. crawlers
2. 수동생성(콘솔,API를 통해 직접 생성)
3. AWS SDK 
4. Hive Metastore 마이그레이션
5. CloudFormation 등 laC 도구 사용

1번이 가장 많이 사용됨.

# Crawlers

#### Classifier
- custom classifier : 사용자가 직접 식별자를 생성하여 데이터를 가져오는 방식
- built-in classifier : 내장된 식별자로 데이터를 가져오는 방식

만약 두 classifier가 동시에 데이터를 크롤링 해올때, 먼저 온 결과물을 채택

<<<<<<< Updated upstream
크롤러의 역할은 데이터를 읽고, 메타데이터를 생성해서, 쓰기를 해야 한다. 위 동작을 하기 위해서는 크롤러에 권한을 부여해야 하는데, 이는 IAM Role을 통해 부여하게 된다.

크롤러는 기본적으로 재사용이 불가능하다.

#### built-int classifier

- default 생성자처럼 기존에 존재하는 classifier로 특수한 데이터셋을 분석하는데에는 부적합하지만, 정형화되어있는 csv같은 파일을 돌리기에 적합하다.

#### custom classifier



# JDBC


# Table Partition

- 쿼리 성능 향상
- 비용 절감
- 더 쉬운 관리

- 파티션 자동 감지
- 각 파티션 스키마 추론 가능
- Dynamic Frame
=======
크롤러의 역할은 데이터를 읽고, 메타데이터를 생성해서, 쓰기를 해야 한다. 위 동작을 하기 위해서는 크롤러에 권한을 부여해야 하는데, 이는 IAM Role을 통해 부여하게 된다.
>>>>>>> Stashed changes
