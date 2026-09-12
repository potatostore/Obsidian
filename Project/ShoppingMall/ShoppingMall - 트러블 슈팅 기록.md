---
tags:
  - seed
aliases: []
created: 2026-08-07
---

# 20260729 ~ 20260804
전체적인 흐름을 잡았다.

기본적으로 backend 구현은 spring boot를 통해 직접구현을, frontend구현은 추후에 claude와 같은 ai agent를 통해 구현을 할 계획이다.

따라서 6개월의 기간을 목표로 잡고, backend -> frontend -> test -> 배포의 과정을 거칠 계획이다.

#### 금주 할일
- [x] harness rule setting : copilot-cli는 github student pack을 가입한 github pro 사용자들에게 무료로 제공되는 토큰이 존재한다. 이는 적은 양이지만 성능이 꽤 좋은 편이라고 생각해서 전반적으로 주간 스케줄을 작성하고, 구현에 이상이 존재하는지 등을 부트캠프의 강사 입장에서 확인할 수 있도록 설정하였다.
- [x] Data structure : 쇼핑몰에서 기본이 되는 user, cart, product, order의 데이터 스키마를 설계하고, 이를 entity class로 표현하는 것을 목표로 둔다.
- [x] DTO structure : 위 데이터 스키마 설계에서는 중요한 user, cart, product, order 데이터의 뼈대를 설계하였는데, 추가적으로 api를 통해 json파일을 받을 때, 응답을 할 때 등의 과정에서 필요한 dto를 설계하였다.
- [x] global config : Global Exception Handler와 ErrorCode를 통해 발생가능한 예외상황을 정의하고, HttpStatus를 상황별로 고정시켜 반환할 수 있도록 구현
- [x] API Response : API 요청이 들어온 경우, 정해진 양시에 따라 응답을 할 수 있도록 ApiResponse 클래스 작성
- [x] Constant : 테이블 이름과 같은 상수를 따로 저장하고, 추후 필요에 따라 컬럼의 이름을 기존 엔티티 필드와 다르게 설정할 경우 매핑될 수 있도록 작성할 것인지 판단, api url을 상수로 뺄 것인지도 판단.
- [x] 추가) CheckConfig : 앞선 엔티티 구현에서 NPE체크, 문자열의 경우 Blank 확인, 수량과 같은 정수는 음수 확인 등 값들의 확인이 중복되는 것을 확인하고, 이를 CheckConfig에 메서드로 정의하여, 통합된 방식으로 확인

#### 트러블
1. NPE : null pointer exception이라는 뜻으로, db에 table을 생성할때, column을 정하게 되는데, 이때 column 어노테이션과 nullable의 조합으로 해당 컬럼에 null을 허용할 것인지 쿼리를 자동 설정할 수 있다. 그 외에도 dto -> entity로 데이터 변환 작업이 이뤄질 경우, null에 대한 참조가 발생할 때, null pointer 참조에 대한 예외처리를 확실하게 하여 서버가 다운되는 일을 방지한다. (때때로 dto에 null을 의도적으로 허용하여 dto가 원하는 데이터를 담을 수 있도록 설정한 경우도 존재하기에 꼼꼼하게 살핌)
2. Harness file : 하네스 파일은 ai agent가 작업을 실행할 때, 어떤 작업을 어떤 위치에서 실행하는지 등을 정확하고 상세하게 명시해주는 것이 좋다. 이때 너뭄 세세하게 명시하다 보면 충돌이 일어나는 개념이 존재할 수 있는데, 내가 작성한 하네스 파일을 예시삼으면, 저번주 목표 기술적 문제 확인 -> 기능적 문제 확인 -> 전체적인 흐름에 따른 다음 한주 동안 목표 설정의 과정을 obsidian vault내부 copilot-addendum.md파일에 서술하라고 명시하였는데, 이때 날짜를 위에서는 하루단위로 설정하고, 밑에서는 1주일의 단위로 설정하니 혼돈이 생겨서 어쩔때는 하루 단위, 어쩔때는 일주일의 단위로 설정되는 것을 확인 할 수 있었다. 따라서 본인의 의도대로 ai agent를 작동시키기 위해서는 전체적으로 서술을 한 후, 자신의 의도가 다 담겨있는지 확인한 후, 충돌되는 부분이 존재하는지 확인한 후, 시험삼아 몇 번 돌려보는 것이 좋은 것 같다.
3. Data type : 기존 정수의 타입을 Integer로 통일을 했었는데, 이를 Long으로 바꾸게 되었다.
	1. 데이터의 범위가 Integer은 약 21억까지 지원을 하기에 충분할 것으로 생각을 하였는데, 주문정보나 장바구니에 담는 물건 정보등은 Integer로 설계될 경우 빠르게 찰 것으로 생각되어 Long으로 바꾸게 되었다.
	2. JPA 및 Spring Data JPA의 기본 예제와 표준 엔티티 인터페이스에 따르면 Long타입으로 작성이 되었다.
	3. 외부 PG사와의 결제 기능을 추후에 넣을 예정인데, 이때 Long/BigInt를 기준으로 삼는 시스템이 많다.
	4. MySQL의 BIGINT타입과 Long타입이 1:1로 대응된다.
4. 데이터 체크 : 데이터를 체크할 때, string의 경우 npe + isblank의 조합으로 유효성 검증, 수량과 같은 정수는 npe + negative 조건문으로 확인 등 데이터 유효성 검증에 코드가 겹치는 경우가 발생하였고, 이를 Exception Handler처럼 따로 데이터 검증 클래스에 메서드로 구현하여 보일러 플레이트 코드를 최소화함.
5. 단방향 / 양방향 매핑 엔티티 : JPA(Hibernate)를 통해 User는 user_id에 1:1매핑되는 카트를 객체로 갖게 하거나, cart는 cartitem을 1:N관계로 양방향 매핑하는 등의 관계를 구현하는 과정에서 필요한 어노테이션(Joincolumn, onetomany, onetoone 등)을 이해하고, orphanremoval과 같은 고아 객체 삭제, cascade 설정을 통한 영속성 전이(cartitem의 수정시 cartitemlist에 영향을 미치도록 설정), fetchtype.lazy를 통한 지연설정 등을 설정하고, 해당 설정 과정에서 totalprice와 같이 product의 업데이트에 따라 cartitem의 curproductitem 필드에 영향을 미쳐 totalprice가 변하는 방식등을 어느 부분에서 이뤄지도록 할 것인지 설정하였다.


# 20260805 ~ 20260811

이번주의 전반적인 목표는 기본적인 Controller + Service를 통해 기본적인 CRUD를 추가하고, 이 과정에서 API URL을 Swagger-ui의존성을 추가하여 설정하는 것이 목표

#### 금주 할일
- [/] Controller & service 구현 : 야그니 원칙에 따라 시나리오를 구상하고, 이에 필요한 4개의 엔티티에 대한 CRUD 기능과 Http method 구현
-> user, product에 대한 구현은 마무리 하였지만, cart/product는 미흡
- [x] Api 명세서 & url 설정 : swagger-ui 의존성 추가와 swagger-ui를 통한 api명세서 확인

#### 트러블
1. 데이터 유효성 : 전 주에 데이터 유효성을 한 클래스에 메서드로 구현하여 보일러 플레이트 코드를 줄이려고 노력했는데, 이전에 구현된 Entity & dto에 적용안된 코드들이 다수 존재했고, 이를 수정함. 따라서 앞으로는 중간에 특정 기능을 대체하는 코드를 구현하게 될 경우, 이전 코드들을 즉각적으로 리펙토링하는 습관이 필요
2. cart 정보 조회 문제 : cart정보를 조회하여 장바구니 확인 -> 주문 생성 + 결제의 흐름으로 시나리오를 설계하였지만, 이 과정에서 문제가 발생함. cart정보를 조회하는 과정에서 cartItem의 curProductPrice와 같은 값들을 productId와 매핑하여 갱신하도록 할 계획이였지만, 이는 큰 딜레이를 가져오게됨. 따라서 redis와 같은 인메모리에 curProductPrice를 직접적으로 저장하는 방식이 아닌, product정보를 올리고, 이를 productId로 조회만 할 수 있도록 하여 CUD의 작업을 최소화하는 방식으로 구현할 수 있도록 목표를 새로 잡았고, redis를 사용해본 경험이 전무하기 때문에, 이를 이해하고, 구현할 수 있도록 다음 주에 진행할 예정(설계의 중요성을 다시 한번 파악함)
3. 결제 방식 : kakaopay, tosspay 등의 PG사의 api를 통한 결제를 진행하도록 목표를 잡았는데, 요청과 받는 응답을 처리하는 기능 등을 구현하는게 너무 복잡함. 따라서 다음 주에는 tosspay를 기준으로 결제를 진행하도록 목표를 잡음.
4. api url 설계 : url은 접근할 자원의 경로를 적어주는 것이기에 create나 get 등의 기능적인 단어를 넣지 않음.
-> 다음주 개발 목표에 redis + tosspay를 추가하고, 기본적인 쇼핑몰의 틀이 잡히게 되면, next.js를 통한 webserver 구현 + ui기본적인 틀을 짜는 방향으로 진행. 이후에는 CI/CD와 docker + kubernetes를 추가하여 백엔드의 추가되는 기능과 이에 대한 ui를 github action으로 배포하는 것을 연습할 계획

# 20260812 ~ 20260818

이번주는 저번주 트러블 슈팅에서 알 수 있듯이 redis 적용 + cartItem 수정, tosspay 결제 방식 추가가 주된 내용이다. 추가적으로 Session방식과 JWT방식을 고민했었는데, 무상태성을 통해 DB의 부담을 줄일 수 있는 JWT를 선택하였다. (물론 추후에 블랙리스트 기능을 추가하게 되면 이는 무상태성에서 벗어난다고 생각은 하지만, 현재 상태성을 구현하는 방식은 JWT로 해결할 수 있을 것 같아 JWT를 선택하게 됨.)

#### 금주 할일
- [x] redis 공부 + 적용하여 cart controller & service 구현 완료하기
- [x] tosspay 결제 방식 도입하여 order controller & service 구현 끝내기
- [x] 모든 controller의 http method 요청 방식을 JWT로 통일시키기

```mermaid title="TossPayment sequence"
sequenceDiagram
    autonumber
    actor Client as 클라이언트
    participant Server as Spring Boot 서버
    participant Toss as 토스 페이먼츠

    Client->>Server: 주문 생성 요청 (상품 ID, 수량)
    activate Server
    Note over Server: DB 금액 계산 & Order 저장<br/>(상태: PENDING)
    Server-->>Client: orderId, amount 반환
    deactivate Server

    Client->>Toss: 토스 SDK 결제창 호출 (orderId, amount 전달)
    activate Toss
    Note over Toss: 유저 비밀번호 입력 및 인증
    Toss-->>Client: paymentKey 발급 및 승인 URL 리다이렉트
    deactivate Toss

    Client->>Server: 최종 결제 승인 요청 (paymentKey, orderId, amount)
    activate Server
    Server->>Server: DB의 orderId 실제 금액 검증
    Server->>Toss: 토스 승인 API 호출 (/v1/payments/confirm)
    activate Toss
    Toss-->>Server: 결제 승인 완료 응답
    deactivate Toss
    Server->>Server: Order 상태 변경 (PAID) & Payment 레코드 저장
    Server-->>Client: 결제 완료 응답
    deactivate Server
```


``` title="tomcat실행 및 spring security를 통한 servlet filter chain 실행 흐름"
[1. 클라이언트 요청] 
  │ (HTTP Request / Port 8080)
  ▼
[2. Tomcat (서블릿 컨테이너)]
  │ - TCP/IP 소켓으로 요청 수신
  │ - Worker Thread 할당 및 HttpServletRequest 객체 생성
  ▼
[3. Tomcat의 서블릿 필터 체인 실행]
  │ - DelegatingFilterProxy 실행
  ▼
[4. Spring Container (Spring Security 영역)]
  │ - DelegatingFilterProxy가 FilterChainProxy(Bean)에게 위임
  │ - SecurityFilterChain 내의 필터들 실행 (JwtAuthenticationFilter, AuthorizationFilter 등)
  │ - 검증 실패 시: 즉시 401/403 예외 응답 반환 및 종료
  ▼ (모든 보안 필터 통과 시)
[5. DispatcherServlet (Spring Front Controller)]
  │ - URL 매핑 확인 후 적절한 @RestController 메서드 호출
  ▼
[6. Controller -> Service -> DB 비즈니스 로직 수행]
  │
  ▼ (응답 생성 후 역순으로 복귀)
[7. DispatcherServlet -> Security Filter (후처리) -> Tomcat -> 클라이언트]
```
#### 트러블
1. redis : redis는 인메모리 dbms로 mysql과 달리 디스크가 아닌 ram에 데이터를 저장, 이때 적은 용량으로 인해 조회를 많이 요구하게 되는 데이터를 주로 넣게 된다. 주로 다음과 같은 패턴을 많이 사용함
	1. cache-asside : 조회 작업에 대해 캐시 메모리(redis)를 우선 조회 후 캐시 미스인 경우 디스크(mysql)를 조회하게 됨.
	2. write-around : CUD작업은 바로 디스크(mysql)에서 작업하고, 캐시에 존재하는 데이터의 수정은 바로 반영되지 않음(patch로 인해 발생하는 비용이 커질수도 있기 때문) -> 데이터의 일관성을 해칠 수 있는데 이는 redis의 TTL설정을 통해 어느정도 보완(TTL이 만료되기 전에 UD작업이 발생한 데이터에 대해 조회가 발생한 경우, 일관되지 않은 데이터를 가져올 수 있기 때문에, redis에서는 어느정도 일관성을 해쳐도 기능에 지장이 생기지 않는 데이터를 보관하는 것을 추천함)
	- 위 두 규칙을 적용하여 product같은 정보를 올려서 보관하려고 했지만, 다음과 같은 문제가 발생할 가능성이 높음 
		1. 수량 관리가 매우 힘듬 : 수량에 민감한 쇼핑몰의 특성상 UD작업을 진행하고 이를 write-around에 따라 저장할 경우, 존재하지 않는 수량에 대한 주문 정보가 생성될 수도 있음
		2. 1.의 이유로 데이터의 일관성이 매우 민감하게 작용
		따라서 현재 단계에서는 jwt-refreshToken만 저장하고, 인증 시에만 조회하도록 설정. 추후에 redis에 올릴 데이터를 고민하고, sql튜닝 이후에 적용할 수 있도록 계획해야함.

2. JWT : jwt를 설정하면서 http 통신에 어떤 정보들이 존재하는지 파악, 이때 통신 방식에 따라 헤더 내 authorization 방식을 달리할 수 있음을 파악함. 현재는 bearer방식(authorization에 "Bearer " + jwt를 보내도록 약속하는 규칙)을 통해 구현.
	- http request는 다음과 같은 구조를 가짐
		- http method : post / get / patch / put / delete
		- url : 접근할 자원의 주소
		- header : 요청을 보내는 주체의 마이데이터를 담은 정보로, 주로 host / authorization / content-type이 존재
		- body : 기능에 필요한 데이터들을 담은 정보

3. Spring Security : 가장 어려운 부분이였는데, 서블렛이라는 개념과 서블렛 필터, 서블렛 필터 체인을 통해 spring security의 동작 방식, HTTP Request가 WAS에 도착했을 때, 전처리/후처리 작업이 어떤식으로 이뤄지는지 파악. 특히 인증의 필요 유무에 따라 public/private method api url을 설정하는 과정이 매우 어려웠음(원리도 어렵고 url을 어떤식으로 설정해야 인증이 필요한 요청만 인증을 요구하도록 필터를 설정하도록 구현하는 것이 어려웠음). 
	- 서블렛 필터 체인 : 서블렛 컨테이너(http request를 받아 http response를 만들어주는 클래스 : 서블렛을 보관해놓은 컨테이너, spring boot에서는 tomcat을 의미)가 http request를 받을 때, 전처리작업과 후처리 작업을 진행하는 것을 서블렛 필터라고 하고, 이를 재귀 함수 형식으로 여러 필터를 연쇄적으로 호출하는데, 이때 후처리는 전처리의 역순으로 이뤄지는 일련의 작업을 서블렛 필터 체인이라고 함.

4. Authorization : 위에서 필터를 통해 토큰의 유효를 전처리로 확인했었는데, 이때 jwtprovider를 통해 토큰의 유효를 secret key와 대조하여 확인하게 함. 중요한 것은 추후에 http 요청방식을 사용하지 않은 곳에서도 jwtprovider을 통해 token의 인증을 요구할 수도 있기 때문에 전적으로 httpservletrequest에서 뽑은 access token을 문자열로 받아 판별 및 예외처리만 하는 로직을 작성

5. Cookie : 매번 jwt를 보관 및 인증이 필요한 요청 시 보내주는 것은 때때로 오류를 일으킬 수도 있기 때문에, 자동으로 jwt를 보내도록 웹 브라우저 측에서 관리하는 방식이 cookie이고, 이는 자동으로 보내준다는 이점이 존재함. 필터의 입장에서는 쿠키로 받는 경우도 존재하지만, 쿠키 설정 허용을 하지 않은 사용자는 jwt를 수동으로 보내주게 되고, 따라서 쿠키로 토큰을 뽑는 방식과 header에서 바로 토큰을 뽑는 두 가지의 방식을 모두 지원해야됨. 따라서 extractToken에서 cookie에서 추출 방식 + Bearer에서 추출하는 방식을 모두 지원하도록 변경
6. 권한 부여 : 권한(현재는 관리자 / 사용자로만 분류)을 통해 접근가능한 기능들을 분류해야만 하고, 이는 securityconfig에서 url별 필터적용이 필요하다고 생각함(추후에 권한이 추가되거나, 권한별 기능을 세세하게 분류하게 되어야 할 경우, 주의해서 설정해야 함)
7. Repository : 현재 모든 repository는 Jparepository를 상속하여 기본적인 crud기능을 jpa가 자동으로 매핑할 수 있도록 설정하였는데, return type에 optional로 감쌀 것인지 판단하는 방식을 배움. -> 기본적으로 단일 Entity 객체를 반환하는 경우 찾지 못한 경우 null값처럼 없음을 표현하는 값을 반환해야하고, 이때 java에서는 기본 타입에 Null이 적용되지 않고, 기본값이 적용됨. 만약 Entity의 기본생성자를 통해 모든 필드를 null로 채웠을 경우(물론 개발자가 noargsconstructor 어노테이션이나 기본생성자를 구현했다는 가정이 필요), column 어노테이션 nullable 속성을 통해 null값을 허용하지 않으므로 오류가 발생, 허용한다고 해도 추후에 getter을 통해 조회할 경우 npe problem이 발생할 수 있기 때문에 optional에 감싸 개발자가 orelsethrow를 통한 예외 던지기를 강제구현하게 함. 하지만 findall과 같이 list 래퍼 객체는 빈 리스트라는 null을 표현가능한 대체재가 존재하기 때문에 optional로 감쌀 필요가 존재하지 않고, 감싸더라도 jpa가 자동으로 db 조회 쿼리 결과로 null을 받으면 빈 리스트를 만들기 때문에 orelsethrow가 실행되지 않음.
-> 0/1개의 반환타입만 존재하면(단일 entity 객체 반환형) Optional로 감싸고, 0...n개의 반환타입(List T 반환형)인 경우 optional 불필요.(실제로 findAll()은 jparepository내부에서 List T 반환형으로 구현).
8. servlet container prefix url : application.yml 설정 파일에 prefix url을 설정(/api/v1과 같이 웹서버와 분류하는 url을 prefix로 구현하여 서버를 나누기 위함). 추가적으로 context-path를 통해 WAS에 들어오는 prefix url을 설정했는데 이는 requestmapping시 prefix url을 제거하고 뒤에 url을 제공한다는 의미이다. sercurityconfig에서 request machers를 사용할 때, prefix url을 제거해야 실질적으로 api url을 매핑시킬 수 있기 때문에 (제거하지 않은 경우 prefix url + prefix url + api url로 들어온다고 machers는 간주하는 것이다.) 이를 제거.
9. payment : 가장 어려운 것은 Toss api를 통해 결제를 진행해야 하는데 어떻게 흘러가는지 파악하는 것이였다. 특히 결제 성공 후 product 수량을 컨트롤하거나, 결제 이전에 수량이 존재하는지 등을 체크하고, 결제 내역과 결제 금액등을 api url로 어떻게 요청해야하는지 자세히 몰라 한참을 toss dev 사이트 내 게시된 결제 관련 api 글을 읽어야 했다. 경험으로 느낀 바를 말하자면, 대부분의 PG사 결제 방식은 위 시퀀스 다이어그램의 방식대로 흘러갈 것이고, WAS를 개발하는 입장에서는 다음과 같은 주의사항을 바탕으로 구현 순서를 정하는 것이 중요하다고 생각한다.
	1. 처음 주문을 생성해서 결제 이전의 상태로 orderId + amount(결제 금액)을 반환할 때, 제품의 수량을 확인하는 로직을 작성해야함(이때문에 product 조회가 많아 redis에 올리는 것을 고민하게 되었다.)
	2. 이후 웹서버 측에서 paymentkey + 승인 url을 받아오게 되면(실제로는 사용자 입장에서 인증 + 결제까지 끝난 상태이다.) WAS에서는 결제를 확정짓기 전에, 결제 금액이 일치하는지 확인을 진행해야함. 이때 받아온 paymentkey를 통해 toss에 결제 정보 조회 api 요청을 날림. 
	3. 결제를 확정(상태를 결제 확정 상태로 변경)한 후 저장
	위 주의사항을 바탕으로 다음과 같은 순서로 개발하는 것이 매우 편했다.
	- dto 구현 : toss dev api guide에 따르면 결제가 성공했을때에는 payment, 실패한 경우는 error 객체를 반환하니까, 가이드에 따라 record를 만들어 관리
	- api key 발급 및 url 적용 : api key를 발급받아 환경변수에 적용하고, 가이드에 따른 url을 설정한다.
	- 기능 개발 : 결제 과정에서 WAS가 진행해야 하는 기능들을 기능별로 service 레이어에 구현. 현재 수량 차감 기능이 구현되지 않았는데, 추후에 리펙토링하면서 수량 차감 기능을 트랜잭션으로 구현해야 함.
	payment과정을 진행하면서 흐름을 알더라도 암호화나 각 흐름별 기능들을 어떤식으로 구현해야 하는지 막막했고, 이는 LLM의 도움을 적극적으로 받음. 추후에 다른 PG사와의 결제 연동을 구현할 때(kakaopay, naverpay 등), 카피코드를 통해 얻은 경험으로 적은 LLM의 도움으로 구현할 수 있을거라고 판단했기 때문이다.
10. Service 레이어 구현 : service레이어에서 다른 service를 참조했는데, 서로를 참조하는 경우가 발생했고, 이때 순환 참조 문제가 발생하며 오류(BeanCurrentlyInCreationException)가 발생했었음. 따라서 service레이어에서 해당 Entity가 아닌 다른 Entity를 건드려야 하는 경우, service를 참조하는것과 repository를 참조하는 것이 BeanCurrentlyInCreationException오류를 유발하고, 성능차이가 발생하지 않는 것을 인지하고, repository를 참조할 수 있도록 구현함.
11. 기타 버그 : patch/delete order에서 소유권 검증(권한 검증 + 사용자 권한이여도 해당 주문내역에 대한 소유권이 존재하는지 판단) 로직이나 securityconfig의 /users/** 추가(모든 개인 정보를 조회하거나 변경하는 작업에 jwt를 통한 인증이 필요하기에 추가), hasRole 규칙 순서를 후순위에 두어 규칙이 무효화된 점을 규칙 순서 교체로 고침 등이 존재함.
→ 굉장히 어려운 한 주였고, 이는 이전에 구현해보지 못한 점들을 구현하고, 그 과정에서 원리는 이해해도 코드로 옮기는 과정도 꽤나 어려웠다고 생각함. 특히 security나 filter, encoding등 알지 못했던 spring security api들을 적용해서 구현하고, http request의 원리를 파악하며 jwt/cookie 세팅하는 것이 어려웠음. 현재 인증이 필요함에도 jwt / cookie가 적용되지 않은 부분들이 존재할 수도 있지만, 다음 주 일정 E2E시나리오 점검(전체적으로 사용자가 쇼핑몰에 적용할 수 있는 주요 기능들의 시나리오를 순서대로 따라가며 구현이 정확하게 되어있는지 확인) + 웹 서버 뼈대 세우기를 진행하고, CI/CD 구현 및 docker/kubernetes를 구현하게 되면, CI/CD로 리펙토링과 추가 기능구현을 할 예정인데, 이때 미뤘던 상품 재고 처리 로직이나 인증 로직 점검을 우선적으로 진행할 계획이다.

# 20260819 ~ 20260825

해커톤 일정이 2일 잡혀있기 때문에 5일의 시간을 기준으로 스케줄을 짰고, 이번주는 웹서버의 본격적이 구현 이전에 뼈대를 세우고, WAS의 현재 구현된 기능들을 전체적인 시나리오를 통해 점검하며 리펙토링을 갖는 기간이 됨. 추가적인 기능은 위에서 언급한 바와 같이 추후에 CI/CD구현 후 구현할 계획.

#### 금주 할 일
- [x] E2E 시나리오 점검 : 회원가입 → 로그인 → JWT 발급 → 인증된 cart/order API → Toss 결제 → 주문 상태 반영 까지의 전반적인 흐름을 파악
- [x] Next.js를 통한 웹서버 뼈대 구축 : 이미 존재하는 뼈대를 기준으로 구현된 기능들을 출력할 ui/ux를 구현하고, url 엔드포인트 등을 설정할 수 있도록 기획할 예정
- [/] CI/CD 구축 초기 : aws EC2에 docker을 통해 서버를 열고, docker hub에 가입 + github actions 연동 및 설정 파일 구현

#### 트러블 슈팅
1. E2E 시나리오 : 사용자 생성부터 결제 진행까지의 일련의 과정을 테스트하며 구현하고자 하는 과정과 동일하게 구현이 되는지 파악. 이때 다양한 부분에서 목적에 맞지 않은 구현을 발견할 수 있었다.
	1. Role 반영 : Role(ADMIN, MANAGER 등) 다양한 역할에 따라 접근 가능한 기능이 존재할 것이고, 따라서 기능별로 역할을 전처리 식으로 파악할 수 있어야 하는데, 그러한 기능을 구현하지 않음
	2. 상품 재고 관리 : 상품 엔티티 컬럼에 재고항목이 존재하지 않고, 특히 결제 진행시 트랜젝션을 통해 재고 처리의 원자성을 보장할 수 있어야 하는데, 트랜잭션 어노테이션을 부여했음에도 재고처리를 하는 로직 자체를 구현하지 않음
	3. jwt : 초반에는 url을 통해 userId를 제공받아 로직을 처리하다가, jwt를 도입한 후, userId를 서블렛 컨테이너 필터 체인을 통해 디코딩하여 얻는 방식으로 바꿨는데, 일부분에서 jwt를 통해 userId를 받는 방식이 아닌 구방식을 유지하는 것을 보임, 따라서 이를 서블릿 컨테이너 체인 필터(spring security의 전처리 부분)을 통해 userId를 얻는 방식으로 통일
	4. user password : 프로필 수정 시 비밀번호도 동시에 수정가능하도록 구현하였는데, 이는 프로필 변경 시 매번 비밀번호를 보내는 행위이므로, 보안상의 이유로 제외하였고, 따라서 비밀번호만 변경 가능한 페이지(혹은 프로필 변경 밑에 칸을 구현할 예정)를 통해 수정할 수 있도록 변경해야 한다.
2. docker : docker 공부를 ci/cd 후순위로 밀어놓고, docker-compose 설정파일을 통해 mysql과 webserver을 간단하게 띄우기만 하는 정도로 작성을 하였다. 이 과정에서 mysql의 dbms의 작동방식(pid를 통한 백그라운드에서 포트를 열고 있어서 초기화를 하지 못해 응답을 받지 못하는 상태가 유지됨)으로 인한 문제가 발생해 어려움을 겪고, docker 설정파일을 LLM의 도움 없이 수동으로 작성하는 방법을 몰라 어려움을 겪음. (추후에 docker와 kubernetes를 학습한 후 설정 파일을 건드리는 작업도 진행할 예정)
3. web-server(Next.js)구축 : 사실 js를 알고, html&css를 알고 있어도, 이걸 직접 코드로 구현하고, 테스트용 쇼핑몰 ui를 만든다는 것은 굉장히 시간이 오래 걸릴 것으로 판단하였다. 특히 ui를 제작하는데 경험이 많지도 않으면서 단순 반복작업이 요구되는 부분들은 claude를 통해 ui(html&css)를 작성할 수 있도록 요구하였고, js코드를 작성할때에도 많은 부분에서 claude의 도움을 받았다. ui는 전적으로 claude에게 맡길 것이며, webserver의 구현 자체는 되도록 꼼꼼히 읽으며 어떤 부분들이 어떤식으로 백엔드와 작동해서 어떤 결과를 만들어 내는지 등을 확인할 계획이다.(ci/cd 및 docker, kubernetes, kafka, redis, prometheus/loki, ngrinder 등 현재 계획된 로드맵과 쇼핑몰의 기능 수정은 손수 코드 구현할 계획)
4. AWS : 간단하게 IAM으로 역할 및 사용자를 설정하고, EC2FullAccess를 줘서 EC2관리용 사용자 계정을 만드려고 했는데, 배운지 1년이 넘도록 한번도 사용하지 않으니 매우 어려웠고, obsidian으로 정리한 [[IAM]]과 claude에게 질문하면서 해결할 수 있었음. 정리 습관을 들인것은 좋은데 좀 더 꼼꼼하게 할 필요가 있다고 느꼈다. 
5. AWS-EC2 속도 : 현재 t4g.small + 20GB volume의 인스턴스에 3개의 서버(webserver + spring server + db server)을 올리려니 속도가 매우 느려지는 것을 확인할 수 있었고, 특히나 사용자 체감시간으로 1초가 넘어가면 큰 불편함으로 다가온다는데, 트래픽을 분당 1000건으로 넣기 시작하면 매우매우 불편할 것으로 판단함. 따라서 로드맵을 일부 수정하여 다음과 같은 로드맵을 거칠 것 같다.
	1. 매주 한 개 이상의 기능에 대한 리펙토링 혹은 개선이 추가됨(다음주는 ci/cd + docker/kubernetes로 인해 다담주부터 진행 될 예정)
	2. (CI/CD -> docker/kubernetes) -> redis -> prometheus/loke -> ngrinder -> sql tuning의 순서를 거치는 것이 좋아보인다. 특히 트래픽이 과부화되었을 경우 aws 오토스케일링 및 로드밸런서 설정을 통해 트래픽 분산 서버를 동적으로 생성하거나, 서버 자체의 로직을 리펙토링(sql 튜닝을 거치거나 등)하여 속도나 서버가 감당할 수 있도록 제작하는 것에 초점을 최대한 두면서 기능을 추가하려고 한다.
6. github actions : ci/cd에서 github actions를 통해 어떤 방식으로 테스트가 이뤄지고, 검증이 이뤄지는지 대충 파악은 하였지만, 좀 더 자세하게 파악할 필요가 있다고 느낌.

# 20260826 ~ 20260901

토요일에 결혼식 방문 예정이고, 월요일은 기숙사에 짐을 실어야 하므로 5일의 상대시간을 확보 가능하고, 지난주에 다 하지 못한 ci/cd 설정과 테스트 코드 작성, github actions원리를 정확하게 파악하는 작업을 중점적으로 진행한 후, 시간이 남는 경우 docker 공부를 하는 것이 좋아 보인다.

#### 금주 할 일
- [x] ci/cd 설정 마무리 
- [/] 테스트 코드 작성
- [x] github actions 원리 파악

#### 트러블 슈팅
1. github actions workflow 이해(내용에 대해서는 [[CI-CD(GitHub Actions)]]참고) : github actions yml을 통해 러너에 올릴 VM에 대한 os image, github webhook trigger을 설정하고, 이는 main 브랜치에 pr을 통해 merge하기 전에 test code를 실행할 수 있도록 트리거를 설정함. 이때 기존에 설정한 docker 설정 파일들을 github에서 가져와 docker container을 띄우게 되는데, spring server같은 경우 db가 존재하지 않은 상태에서 빌드하게 될 경우 런타임 오류가 발생할 수 있기 때문에 db -> backend/frontend의 순서로 실행될 수 있도록 유도하였다. 추가적으로 db를 docker 에서 build한다고 하여도, 실행되지 않은 시점에서 backend서버가 돌아갈 수 있기 때문에, linux 명령어를 통해 지속적으로 db의 상태를 추적 후 실행중일때만 다음 과정(backend 실행)을 할 수 있도록 하였다. 이때 docker에 mysql db만 띄우게 하여 실행하였는데, 이는 db 서버 자체가 backend의 의존성으로 필요하였지만, backend는 단위 테스트를 진행하기 때문에 서버 실행이 필요하지 않아, jdk를 설치한 후 직접 빌드하여 단위 테스트를 실행하였다(추후에 단위 테스트가 아닌 연동 테스트를 검증하게 되는 코드를 작성하게 될 경우, docker을 통해 backend, frontend 서버를 띄울 필요가 있다). 또한 merge직전에 test + gitguardian을 통과해야지 merge할 수 있도록 github repository자체에 제약을 걸었다.
2. ci/cd setting file 작성 : CI-CD 설정 파일은 branch의 웹훅 이벤트를 트리거 형태로 감지하고, 어느 os에서 어떤 흐름으로 파일들을 테스트할 것인지 일일이 설정해주는 파일이다. 특히 VM에서 돌아가는 CI는 테스트의 시간을 길게 가져도 큰 문제가 발생하지는 않지만, 짧을 수록 편의성이 올라가기 때문에 최대한 효율적으로 작성하여 테스트가 원활하게 돌아갈 수 있도록 설정 파일을 작성하였다. 위 github actions workflow에서 언급한 것처럼 docker을 전체적으로 띄우는 것이 아닌, 의존성이 강제되는 부분만 따로 띄우고, 다른 부분들은 단위 테스트가 가능한 경우, 단위 테스트를 최대한 지향하는 방식으로 테스트 코드를 작성하도록 구현할 것이다. 또한 중간에 db가 완전히 실행되어야 backend 단위 테스트를 빌드할 수 있도록 linux kernel 명령어를 작성하였는데, 이러한 부분들은 ai의 도움으로 작성하게 되었다.
3. spring boot test code 구현 : given-when-then의 과정을 통해 mock데이터 설정, repository와 같이 외부에 의존성을 둔 기능들에 해당 목데이터를 반환하는 이벤트 코드의 형식으로 테스트 코드를 작성하였다. 전반적인 test code구현을 목표로 잡았지만, 이번 주차에서는 service 레이어에 대한 테스트 코드들만 작성하였다. 이유는 테스트 코드를 작성할때, 예외 처리에 대한 단위 테스트도 작성을 하여야하고, 이때문에 전반적인 코드의 길이가 실제 구현 코드보다 훨씬 길게 작성되기 때문이였다. 또한 userId와 같은 PK를 ReflectionTestUtils와 같이 직접적으로 필드를 설정해주는 코드를 통해 id 비교 로직들을 서비스에서 원활하게 실행되게 만들거나, jwt secret key, 비밀번호 암호화 등 서비스에 구현된 기능들을 상세하게 테스트하는 코드를 작성하는데 주 목적을 두었기에 꽤나 오랜 시간이 걸렸고, 따라서 다음주에도 test code를 마저 구현하는데 중점을 둘 것이다.

# 20260902 ~ 20260908

이번 주는 지난 주 트러블 슈팅 일지에서 언급하였던 테스트 코드 나머지 작성과 더불어 docker + kubernetes를 공부하는데 최대한 중점을 둘 것이다.

#### 금주 할 일
- [x] 테스트 코드 마저 작성
- [/] docker & kubernetes 공부 + 구현

#### 트러블 슈팅 일지
1. 예외처리 (method에 throws를 붙이는 것과 throw new를 통해 예외를 던지는 것의 차이) : 이전에 new throw를 통해 예외를 서비스 레이어에서 던지도록 구현을 하였었는데, 이때 예외를 던지는 메서드에 throws Exception을 붙이지 않았다. controller test code를 작성하면서 post와 같은 http method를 서블릿 컨테이너에 request형식으로 주입할 때, 예외처리의 주체를 해당 메서드가 아닌 호출한 상위 메서드로 전가하기 때문에 이와 같은 차이를 발생한다고 볼 수 있다.
	- method 선언부에 throws Exception과 같이 정의할 경우, 메서드를 호출한 상위 메서드로 예외의 책임이 전가된다.
	- 만약 메서드 내부에서 고의로 예외 객체를 생성하게 될 경우, 예외 처리의 책임이 메서드 내부에 존재하여 선언부에 작성하지 않아도 된다.
2. authController의 userId 주입 : 쿠키를 통해 서블릿 컨테이너에서 userId를 @AuthenticationPrincipal을 통해 주입을 하게 됨(이는 cookie에서 accessToken을 복호화하여 얻음). 이때 authController에서 Mock Cookie를 제작해서 넣는 행위는 controller의 단위테스트가 아닌 필터의 영역까지 건들기 때문에, authentication을 직접 만들어서 이를 필터의 결과물로서 Spring web mvc에 보내고, mockmvc는 이를 통해 정해진 httpmethod를 실행. 즉, 서블릿 필터를 꺼놨지만, 마치 서블릿 필터를 통해 userId가 주입된 것처럼 보이기 위해 SecurityContextHolder을 통해 Authentication을 mock형식으로 넘겨 컨텍스트를 마치 필터에서 나온 것처럼 유도할 수 있다.(예외로 url을 통해 orderId와 같이 @PathVariable을 주입받는 경우, 이는 http method url을 설정할 때, 넘겨주는 방식이 바람직하다.)
3. service레이어를 mock이 아닌 mockbean으로 주입하는 이유 : 가장 큰 차이는 Spring Context를 통해 의존성을 주입하는가에 따라 달라진다. Service test code에서는 @ExtentWith(MockitoExtension.class)를 통해 Spring Context에서 의존성을 주입하는 것이 아닌, mockito를 통해 mock형식으로 의존성을 주입하도록 설정하여 @Mock 어노테이션으로 의존성을 주입하였다. 하지만 Controller test code에서는 HttpRequest를 Spring Context에 설정하여 실질적으로 Controller에 요청이 들어가 기능을 실행하는지 확인하기 때문에, Controller에 한해서만 Mockito로 설정하고, 나머지 요인들을 Spring Context로 주입을 하게 되고, 따라서 Service를 주입할 때, Spring Context를 통해 주입되기 때문에 @MockBean을 통해 IoC 컨테이너에 존재하는 bean을 주입할 수 있도록 함.
4. 서블릿 필터의 자세한 이해 : http method + session이 서블릿 컨테이너의 소켓을 통해 도착한 이후로부터 filter을 거쳐 컨트롤러에 도착하기까지의 과정을 세세하게 알 필요가 존재함.
	1. http request를 서블릿 컨테이너의 소켓을 통해 받아온다.
	2. 서블릿 컨테이너는 관리하고 있는 thread pool 중 하나를 해당 요청에 할당한다. (이때 context라는 상자를 동시에 할당하여 관련 정보를 저장할 수 있도록 관리함.)
	3. 필터의 전처리 / 후처리를 거치면서 인증이 필요한 요청일 경우, cookie에서 userId와 같은 정보들을 뽑아내어 context로 관리한다.(이때 userId와 같은 정보는 SecurityContextHolder가 관리하고, 다양한 context holder가 존재함)
	4. 필터를 거친 후, MappingHandler을 통해 url에 매핑되는 controller을 호출하게 되는데, controller에서 @AuthenticationPrincipal과 같이 컨텍스트에서 값을 뽑아 주입해주는 어노테이션을 감지하면 Context에서 값을 가져와 할당해준다.
	5. 기능 실행 (기능은 스레드 하나에 할당됨)
	이와 같은 과정을 거치며 filter은 요청의 정당성을 확인하거나, 필요한 정보를 context로 관리하여 추후에 기능에 사용될 수 있도록 스레드에 할당된 메모리(ThreadLocal이라고 함)에 값을 저장한다.
5. securityContextHolder에 mock session을 세팅한 후에 처리 후 clear하는 이유 : 기본 저장 방식인 MODE_THREAD를 통해 mock session이 context에 저장되는 것이 아닌, local thread에 context를 세팅하는 것이기 때문에, 단위테스트를 여러개 돌리는 github actions에서 해당 mock session이 스레드에 남아 다른 단위 테스를 실행하는 문제가 발생할 수 있기 때문 -> 이때문에 항상 try-finally문을 통해 context clear을 실행할 수 있도록 작성
6. 마샬링 / 언마샬링 : 마샬링은 자바의 객체를 json 파일로 매핑하여 응답으로 보내는 등의 용도로 사용되는 과정을 의미한다. 이때 마샬링을 Spring MVC에서 진행하게 되는데, 필요한 과정이 존재한다.
	- 마샬링 : 객체를 json으로 매핑하기 위해서 필드명과 data값을 알아야 하는데, 이때 필요한게 getter 메서드다. getter메서드를 통해 Spring MVC는 data값을 읽고, Json파일 형식으로 매핑해준다.
	- 언마샬링 : json을 다시 객체로 매핑할 때, 기본 생성자가 있어야 객체를 생성하고, 필드를 주입해줄 수 있다. 필드에 값을 주입할때 필드가 존재하는지 확인하기 위해서는 getter, private 필드에 값을 주입하기 위해서는 setter가 필요하다고 이해하고 있었지만, 알고보니 reflection을 통해 java의 private 접근 검사를 끈 후, 값을 주입하고, 원상태로 복구하는 방식을 통해 값을 주입하는 방법이 있어, 여전히 setter의 사용을 지양하는 편이 좋다.
	다만 record와 같이 필드가 final로 선언되는 경우, 필드를 주입하는 것이 아닌, 마샬링/언마샬링의 주체인 Spring MVC Jackson이 생성자를 통해 처음에 값을 전부 넘기기에 getter / noargsconstructor 없이 동작 가능하다.

# 20260909 ~ 20260915
controller test code가 생각보다 길어지고, 특히 저번주까지 구현했던 controller test code가 happy-path(전적으로 성공에만 의존되는 코드)를 작성했기 때문에 400 / 401 / 404와 같은 Exception에 대응되는 테스트 코드를 작성하고, docker & k8s의 공부를 조금이라도 무조건 해나가는 것이 이번주 목표이다.

#### 금주 할 일
- [ ] controller 예외 테스트 코드 작성
- [ ] docker & k8s 공부 조금이라도 하기