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


#### VPN(Virtual Private Network)

- 가상 사설망으로 공공 네트워크를 통해 마치 개인 네트워크처럼 안전하게 통신하는 기술이다. IP address 마스킹, 데이터 암호화를 통해 공공 네트워크를 사용하여도 개인 정보가 보호되게 만든다.

#### Amazon VPC

AWS(Amazon Web Services)의 전체 인프라스트럭처는 보안 시설로서 클라우드에서 실행되는 사용자의 모든 자원은 높은 보안성을 보장받을 수 있다. 이는 기본적으로 AWS를 사용하는 모든 기업들이 보장받을 수 있는 안정성이다. 이에 Amazon VPC를 구축해서 사용자 수준에서 보안의 수준을 높일 수 있다.

VPC(Virtual Private Cloud)는 클라우드 환경을 퍼블릭과 프라이빗의 논리적으로 독립된 네트워크 영역으로 분리할 수 있게 해준다. 어떤 리소스라도 논리적으로 분리된 영역에 격리할 수 있으며, 사용자가 네트워크 환경 설정에 대한 완전한 통제권을 가질 수 있다.

이는 사용자가 Amazon VPC를 통해 만든 네트워크에서 자체 IP 주소, 퍼블릭 및 프라이빗 서브넷, 라우트 테이블, 네트워크 게이트웨이 등 모든 기능을 활용할 수 있는 것을 의미한다. 즉, Amazon VPC를 활용하면 온프레미스 데이터 센터에서 직접 네트워크 환경을 만드는 것과 같은 방식으로 클라우드 환경에서도 네트워크를 구축할 수 있다.

AWS의 네트워크 서비스를 활용하기 위해서는 네트워크 기본 개념에 대한 학습이 선행되어야 한다.  
  

#### VPC가 만들어진 배경

Amazon VPC는 AWS에서 처음부터 제공하는 서비스는 아니었다. Amazon VPC가 없었을 때는 클라우드에 있는 리소스를 격리할 수 있는 방법이 없었다. 예를 들어, 수천 대의 서버를 클라우드에 배포한 경우 IP 네임스페이스를 정확히 관리해야 했으며, IP 주소 간에 중첩되는 부분이 없어야만 온프레미스에서 구동되는 리소스에 빈틈없이 접근할 수 있었다. 따라서 다음과 같은 문제가 있었다.

- 클라우드에서 어떻게 네트워크를 분리할 것인가?
- 어떻게 애플리케이션 중 일부는 인터넷을 통해 퍼블릭하게 연결하고, 일부는 프라이빗하게 연결할 것인가?
- 동일한 IP 범위를 클라우드로 확장하는 방법이 있는가?
- EC2 인스턴스를 생성하면 32비트 랜덤 IP 주소 체계와 비슷하게 유지할 수 있는 방법이 있는가?

Amazon VPC는 이러한 기존 클라우드 환경이 갖는 문제점을 해결하기 위한 솔루션으로 등장하게 되었다. 앞서 언급한 모든 문제를 해결할 수 있으며, 클라우드에서의 애플리케이션 호스팅, 데이터 센터에서 구동 중인 애플리케이션과 클라우드 자원의 긴밀한 연결을 가능하게 해준다. 3 Tier(Client Tier, Application Tier, Database Tier) 애플리케이션의 경우 Amazon VPC의 퍼블릭 서브넷으로 Client Tier(Web Tier)를 실행하고, 동일한 또는 새롭게 생성한 VPC에서 프라이빗 서브넷으로 Application Tier와 Database Tier를 실행할 수 있게 되었다.  
  

#### VPC로 클라우드 환경에서 할 수 있는 일

Amazon VPC 서비스에서 제공하는 여러가지 기능으로 클라우드 환경에서 다음과 같은 일들을 할 수 있다.

- 애플리케이션 중 일부는 VPC 내 클라우드에서 실행하고, 일부는 온프레미스에서 실행할 수 있다.
- VPC 내에서 인터넷으로부터의 접근을 허용하는 퍼블릭 서브넷과 한정된 접근만을 위한 프라이빗 서브넷을 생성할 수 있다.
- Direct Connect를 이용해 기업 데이터 센터와 VPN을 전용 회선으로 연결할 수 있다.
- 하나 이상의 VPC가 필요하다면 다수의 VPC를 생성한 뒤 VPC 피어링을 통해 서로 연결할 수 있다.

# VPC 설정하기

- 위 지식들을 종합하여 VPC를 설정한 후 인스턴스 내 연결할 수 있도록 만들어주기

[[Create-VPC-custom]]을 기준으로 작성하였다.

1. VPC 생성 : IPv4 / IPv6 설정, 서브넷 내에 인스턴스간의 인터넷 생성을 위해 인터넷 게이트웨이를 설정하고, 이를 라우팅 테이블을 설정하여 서브넷이 다른 인스턴스간의 상호작용이 가능하게 만들어야 하는데, 위 구성들을 한꺼번에 묶어주는 역할을 한다.
2. 서브넷 설정하기 : 서브넷은 private/public으로 설정하는데, 이를 기존에 존재하는 legion AZ로 설정하여 서브넷을 만든다.
3. 인터넷 게이트웨이 설정하기 : 생성 후, 위 VPC에 소속시켜준다.
4. 서브넷에 인터넷 게이트웨이를 설정하고, IP설정해주기
5. 인스턴스를 생성하고, 네트워크를 위 VPC로 설정하여 해당 VPC가 정상적으로 작동하는지 확인

전반적으로 VPC는 네트워크 관련 개념으로, AZ내에 생성된 인스턴스가 정상적으로 작동하고, 보안이 유지되기 위해 설정해주는 장치로 생각하면 된다.
