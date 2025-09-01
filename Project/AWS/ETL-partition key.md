ETL을 통해 partition key를 지정하는 순간, partition key가 된 컬럼은 중복하여 존재할경우 중복제거에 의해 통째로 날라갈 수 있다. 따라서 이를 방지하기 위해 aws에서는 partition키로 지정한 컬럼은 자동으로 삭제한다.

그렇기에 이를 복제하여 새로운 컬럼을 만들어 partition key year column과 normal year column으로 같은 정보를 담는 두 column을 생성하는게 목적이다.

# partition key column copy

1. s3 bucket 지정시, partition key를 복제하는 방식을 선택 : 해당 파티션 키가 존재한다는 사실을 스키마에 담아 db에 복제하는 방법(option 2)과 아예 새로운 컬럼을 복제하여 붙이는 방식(option 3)이 존재하는데, 둘 다 bucket이 아닌 db에 들어가므로 비추
2. custom transform 사용 : custom transform을 통해 복제를 시도하는 방식인데, 복제가 끝난 후 해당 데이터셋이 collection으로 간주되어 bucket에 담기지 못하는 현상 발생 -> Select From Collection ETL Node를 선택하여 collection을 dataset으로 바꿔줌. 이후에 s3에 저장하면 정상적으로 저장된다.