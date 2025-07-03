Amazon Elastic Compute Cloud(EC2)

EC2는 가상서버로 고가용성과 내결함성을 갖고 유연한 확장성(OnDemand)을 갖는다.

물리서버의 한계를 인식

*AMI에 어떤 인스턴스를 넣을 건지 결정*

bucket

access key

s3 역할 부여를 통해 인스턴스에서 접근 권한을 부여

인스턴스를 생성하게 되면 virtual machine에 자동으로 IP가 붙음 -> (IPv4 /  IPv6 설정)

# EC2
- EC2
	- AWS Cloud에서 필요한 만큼의 가상 서버(인스턴스)를 손쉽게 생성, 관리할 수 있게 해주는 서비스
	- 가상 서버
		
		물리 서버의 한계점
		
		- OS가 하드웨어와 같은 계층으로 존재하여 이식이 불가능함
		- 서버 문제시 리소스 활용 불가능
		- 높은 비용, 확장성 제약, 배포 시간이 김
	- 온디맨드 확장 가능성
	- 고가용성 & 내결함성
	- 인스턴스 생성
		- Amazon Linux > AMI 설정(프리 티어 사용 가능)
		
		- 인스턴스 유형 > t2.micro 선택
		
		- 키 페어 > 키 페어 생성(이름은 루트 계정 별칭+지역)
		
		- 네트워크 설정 > 편집 > 방화벽(보안 그룹)
		
		- Window도 마찬가지로 생성 (AMI Microsoft 설정, 보안 그룹 WebAccessAuth로 변경)
	- 인스턴스 연결
		- 리눅스: EC2 인스턴스 연결 > 퍼블릭 IP(35.79.225.188) 사용 연결
		- IP 할당 확인 명령어(ifconfig)
		
		![image.png](attachment:dad2cb3b-824f-4d86-8140-4828a8a29410:image.png)
		
		- 윈도우: RDP 클라이언트 연결(아이디: Public DNS, 비번: 암호 가져오기)
		
		![image.png](attachment:b3cc087a-6231-43fc-b50b-cd36646e2165:image.png)
		
		- 원결 데스크톱 파일 다운로드 > 실행 > 암호 입력
		
		![image.png](attachment:9b68cb4f-b96d-4b39-ae52-b9b572a02138:image.png)
		
		- 액세스 키 만들기 > 액세스 키 / 비밀 액세스 키
		
		![image.png](attachment:a4f38116-dc82-446b-a415-44393fc484eb:image.png)
		
	- 인스턴스 권한 부여 방식
		- 액세스 키(리눅스 명령어)
			- aws s3 ls: 생성된 bucket 출력 명령어
				- s3는 데이터 저장소, 데이터 개수 제한 X
			- pwd: 현재 위치 출력 명령어
			- aws configurt: 권한 부여 명령어
				- 액세스 키 ID / 비밀번호 / 지역 이름(ap-northeast-1)
			- aws s3 mb s3://유일한 bucket이름: bucket 생성 명령어
			- cat config / cat credentials : 이 명령어들은 각각 지역 이름, 액세스 키 ID, 비밀번호와 같은 민감한 보안 정보를 노출 시켜 보안에 취약점을 만들 수 있음
				- rm -rf ~/.aws/*: 위 정보를 삭제하는 명령어
				- 액세스 키 비활성화 or 삭제
		- 역할 생성
			- 보안 상 역할 생성 후 부여해주는 방식이 안전함
			- AmazonS3ReadOnlyAccess: s3는 데이터 접근만 가능해도 충분(보안 상 선택)
			- EC2 > 인스턴스 > 작업 > 보안 > IAM 역할 수정
			- 계정에 역할을 부여하는 것이 아닌 AWS 서비스로 IAM 역할을 부여하는 것 (알아서 분류 해줌)
			
			![image.png](attachment:7598869a-a28b-46ab-ab82-5b5e55c837b5:image.png)