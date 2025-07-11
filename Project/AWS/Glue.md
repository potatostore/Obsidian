# Job

- ETL 파이프라인이 자동으로 실행되는 단위
#### ETL
- Extract : 데이터 추출
- Tranfer : 데이터 변환
- Load : 데이터 적재

# Data Catalog

- AWS에서 데이터베이스 내에 여러 데이터베이스와 유사한 catalog가 존재하도록 설계
- 각 데이터베이스 catalog는 여러 테이블로 구성
- 따라서 

#### metadata
- 소스타입, 데이터포멧, 컬럼정보를 담고있는 데이터

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

크롤러의 역할은 데이터를 읽고, 메타데이터를 생성해서, 쓰기를 해야 한다. 위 동작을 하기 위해서는 크롤러에 권한을 부여해야 하는데, 이는 IAM Role을 통해 부여하게 된다.

