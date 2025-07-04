Amazon Elastic Compute Cloud(EC2)
# EC2란
#### AWS Cloud에서 필요한 만큼의 가상 서버(인스턴스)를 손쉽게 생성, 관리할 수 있게 해주는 서비스
- 가상 서버
	물리 서버의 한계점을 보완하기 위해 설계
	- OS가 하드웨어와 같은 계층으로 존재하여 이식이 불가능함
	- 서버 문제시 리소스 활용 불가능
	- 높은 비용, 확장성 제약, 배포 시간이 김
- 온디맨드 확장 가능성
- 고가용성 & 내결함성

# AWS EC2 생성하기

#### 인스턴스 생성
- Amazon Linux > AMI 설정(프리 티어 사용 가능) : AMI를 통해 인스턴스(VM)의 OS를 설정
- 인스턴스 유형 > t2.micro 선택 : OS의 version 선택
- 키 페어 > 키 페어 생성(이름은 루트 계정 별칭+지역) : 이미 생성된 키 페어를 사용해도 됨
- 네트워크 설정 > 편집 > 방화벽(보안 그룹)
- Window도 마찬가지로 생성 (AMI Microsoft 설정, 보안 그룹 WebAccessAuth로 변경)
	
#### 인스턴스 연결
- 리눅스: EC2 인스턴스 연결 > 퍼블릭 IP(35.79.225.188) 사용 연결
- IP 할당 확인 명령어(ifconfig)
- 윈도우: RDP 클라이언트 연결(아이디: Public DNS, 비번: 암호 가져오기)
- 원결 데스크톱 파일 다운로드 > 실행 > 암호 입력
- 액세스 키 만들기 > 액세스 키 / 비밀 액세스 키
	
#### 인스턴스 권한 부여 방식
- 기존 인스턴스를 생성하게 되면 cat credential을 통해 인스턴스의 키 페어등을 쉽게 얻어갈 수 있기에 액세스 키를 부여하거나, 역할 생성을 통해 권한을 부여하는 식으로 하여 접근을 불가능하게 만듦. 
- 액세스 키(리눅스 명령어) : 액세스 키를 통해 접근이 가능하지만, 액세스 키를 저장하고, 숨겨야 하는 번거로움 존재
	- aws s3 ls: 생성된 bucket 출력 명령어
		- s3는 데이터 저장소, 데이터 개수 제한 X
	- pwd: 현재 위치 출력 명령어
	- aws configurt: 권한 부여 명령어
		- 액세스 키 ID / 비밀번호 / 지역 이름(ap-northeast-1)
	- aws s3 mb s3://유일한 bucket이름: bucket 생성 명령어
	- cat config / cat credentials : 이 명령어들은 각각 지역 이름, 액세스 키 ID, 비밀번호와 같은 민감한 보안 정보를 노출 시켜 보안에 취약점을 만들 수 있음
		- rm -rf ~/.aws/*: 위 정보를 삭제하는 명령어
		- 액세스 키 비활성화 or 삭제
	
- 역할 생성 : IAM에서 사용자에게 권한을 부여하여 AWS 접근권한을 부여하는 방식과 동일하게 EC2에 접근권한을 생성하여 해당 역할을 부여하게 되면 해당 인스턴스를 통해 사용가능한 AWS가 제한적이게 됨.
	- 보안 상 역할 생성 후 부여해주는 방식이 안전함
	- AmazonS3ReadOnlyAccess: s3는 데이터 접근만 가능해도 충분(보안 상 선택)
	- EC2 > 인스턴스 > 작업 > 보안 > IAM 역할 수정
	- 계정에 역할을 부여하는 것이 아닌 AWS 서비스로 IAM 역할을 부여하는 것 (알아서 분류 해줌)

# EC2 handling

#### 확장 가능성
- auto scaling
- amazon cloud Watch -> auto Scaling Group
1. 사용가능성 유지(현재 시스템 유지) -> fail된 VM instance를 대체하여 생성
2. 확장(scale-up) -> 트래픽 증가 등의 원인으로 VM instance의 리소스 사용량이 증가 시 추가 생성
가용영역 내 subnet은 복제x, 단일

- ELB(Elastic Load Balancing) : 사용자가 서버에 접속을 하다가 위 과정처럼 instance가 fail이 날 경우 사용자가 접속하고 있는 instance를 다른 instance로 옮겨줌(latency x)
	- 대상 등록에서 동적으로 하기 위해 선택x

automatic-scaling(scale-up) : cloudwatch | intance 개수로 확인

# VPC(Virtual Private Cloud)

#### OSI(Open Systems Interfaces)
- 네트워크를 나누는 L7(OSI 7계층)
	1. Physical layer : 물리적인 단계로, port를 통해 전자적 신호로 2진법으로 바꾸어 송수신
	*switch : 서버에 전자적 신호를 받고, 이를 다른 서버로 보낼 때 물리적 신호로 바꿈
	RJ45 Port : 이더넷 케이블을 연결하는 데 사용되는 표준 8핀 커넥터*
	2. Data Link layer : 근거리 네트워크 통신(LAN)을 다루는 단계
	*mac(media access controler) : IP주소 처럼 하드웨어에 할당된 고유 식별 주소
	Ethernet : LAN의 네트워크 통신 규격으로, 네트워크 간의 통신 규칙, 기준
	802.1x : mac를 식별하고, 확인하여 해당 신호를 들이거나 거부*
	3. Network layer : IP를 통해 통신이 이루어지는 단계
	4. Transport layer : IP를 통해 데이터를 통신하는 단계
	*TCP/IP : 3-Way handshaking을 통해 전송하려는 데이터가 제대로 된 IP에 전송되었는지 연결형 프로토콜을 통해 확인한다. 신뢰성은 높지만 느리다.
	UDP : 비연결형 프로토콜로 데이터를 전송할 때, 통신 주체들끼리의 논리적인 경로가 없는 비연결형 프로토콜로 목적지는 존재하지만 경로가 불확실하여 통신을 상대측에서 받았는지 확인할 수 없다. 빠르지만 신뢰성이 낮다.*
	5. Session layer : 
	*위 transport layer에서 TCP는 전달자 역할이지만, session layer에서는 통신 연결 중간에 조율을 통해 원활한 통신을 이룰 수 있도록 조율자 역할을 함*
	6. Presentation layer : 
	*SSL : 
	SSH : 
	릴레이 서버 : *
	7. Application layer : 