---
tags:
  - seed
  - type/project
aliases: []
created: 2026-08-02
---

[20260729 ~ 20260805]
### 컴파일 및 디버깅 관련 문제
- [ ] **치명**   CartItem   컴파일 실패:   CartItemResponseDTO   import 누락으로   cannot find symbol   발생 → DTO import 추가 필요.
- [ ] **중간** 장바구니 합계 계산 NPE 위험:   isEmpty()  가 null 체크보다 먼저 실행됨 → null 체크를 앞에 두도록 조건 순서 변경 필요.
- [ ] **중간** 전역 예외/응답 포맷 미적용 상태에서 디버깅 비효율: 예외 타입별 응답 형식 불일치로 원인 추적 비용 증가 →   @RestControllerAdvice   + 공통 에러 포맷 매핑 필요.
- [ ] **경미** Validation 실패 응답 비표준 가능성: 필드 에러 구조가 엔드포인트마다 달라질 수 있음 →   field/reason/rejectedValue   고정 포맷 필요.
- [ ] **경미** 주문/재고 로직 사전 테스트 포인트 부재: 동시성/재고 차감 오류 발견이 늦어질 위험 → 주문 생성/재고 차감/취소 복구 테스트를 초기부터 포함 필요.
- [ ]  **D1~D2(긴급 안정화)**   CartItemResponseDTO   import 누락/합계 계산 NPE 위험을 즉시 수정하고, 장바구니 조회·합계 계산·주문 전환 직전 경로를 우선 점검.
- [ ]  **D2~D3(에러 관측성 개선)**   @RestControllerAdvice   + 공통   ErrorResponse  를 적용해 예외 타입별 응답 형식을 통일하고, Validation 실패를   field/reason/rejectedValue   포맷으로 고정.
- [ ]  **D6~D7(회귀 방지)** 주문/재고/취소 핵심 시나리오를 중심으로 디버깅 로그 포인트와 재현 테스트 케이스를 정리해 이후 기능 확장 시 회귀 탐지를 빠르게 할 수 있도록 준비.
- [ ] **치명** 컴파일 실패:   OrderDetailController  가   TableNames.orderDetailTableName  를 참조하지만   TableNames  에는   orderItemTableName  만 존재하여   cannot find symbol   발생.
- [ ]  **중간** 예외 응답 표준 미완성:   GlobalExceptionHandler  가   ApiResponse.error(message)  만 반환해   ErrorCode  /필드 단위 Validation 상세(  field/reason/rejectedValue  )가 응답에 포함되지 않음.
- [ ]  **중간** 서비스 계층 미구현:   OrderService  가 비어 있어 주문 유스케이스 디버깅 포인트(입력 검증/상태 전이/재고 실패 지점)가 컨트롤러 레벨에서 분산될 위험이 큼.

### 구현 기능 관련 문제점
1. **치명** 주문 라인아이템 구조 부재:   Order.productId   단일 컬럼 + 비어 있는   OrderDetail  로 다건 상품 주문 처리 곤란 →   Order  -  OrderDetail   관계 및 FK 명시 필요.
2. **치명** 찜 기능 모델 미완성:   Like  가   id  만 보유해 사용자-상품 매핑 불가 →   userId  ,   productId  , 유니크 제약 필요.
3. **치명** PK 전략 불일치:   User/Product  의   String id  와   IDENTITY   전략 충돌 가능 → 정수 PK 또는 UUID 전략으로 통일 필요.
4. **중간** 최근 본 상품 확장성 부족: 단일   recentWatchingProductId  로 목록/정렬 기능 한계 → 별도 이력 테이블 설계 필요.
5. **중간** 주문 이력 재현성 부족: 주문 시점 가격/수량 스냅샷 부재 →   OrderDetail  에 주문 당시 금액/수량 컬럼 필요.
6. **중간** 재고 무결성 경계 부재: 결제/취소 시점 재고 정합성 깨질 가능성 → 재고 차감/복구를 하나의 트랜잭션 경계로 처리 필요.
7. **중간** 운영 표준 계층 미완성: 공통 에러코드/응답계약/로깅 추적 미통일 → API 응답/예외/traceId 표준화 필요.
8. **중간** 직렬화/시간대 정책 부재: 날짜 포맷·타임존이 환경별로 달라질 수 있음 → Jackson ISO-8601 포맷 및 타임존 정책 고정 필요.
9. **경미** CORS 정책 산재 위험: 컨트롤러 단위 분산 설정 시 운영 실수 가능 → 글로벌 CORS + 프로파일별 허용 도메인 분리 필요.
10. **D1~D3(데이터 모델 정비)**   Order  -  OrderDetail   관계/FK/스냅샷 컬럼(주문시점 가격·수량)을 우선 확정해 다건 주문과 주문 이력 재현성을 확보.
11. **D2~D4(식별자/무결성 정합화)**   User/Product   PK 전략을 단일 정책(정수 PK 또는 UUID)으로 통일하고,   Like(userId, productId)   유니크 제약을 포함한 찜 모델을 완성.
12. **D3~D5(확장성 보강)**   recent_watching(userId, productId, viewedAt)   이력 테이블로 최근 본 상품을 정규화하고, 목록·정렬 요구사항 대응 기반을 마련.
13. **D4~D6(트랜잭션 경계 확립)** 결제 시 재고 차감/취소 시 복구를 하나의 트랜잭션 경계로 묶고, 동시성 충돌 시 처리 전략(락/버전)을 도입.
14. **D5~D7(운영 표준 마감)** API 응답 계약·에러코드·traceId 로깅·Jackson 시간대 정책·글로벌 CORS를 통일해 운영 환경 편차를 최소화.
15. **부분 달성** 주문 모델 정비는 진전됨:   Order  -  OrderItem   1:N 관계와 주문 시점 가격/수량(  curOrderItemPrice  ,   quantity  ) 스냅샷은 반영됨.
16. **범위 외(차주 목표)** 장바구니→주문 전환 API:   OrderCreateDTO  /  OrderItemCreateDTO  는 준비되어 있으나 서비스/컨트롤러 유스케이스는 다음 주 구현 범위로 이관.
17. **범위 외(차주 목표)** 재고 트랜잭션 경계:   @Transactional  , 락(  PESSIMISTIC_WRITE  /  FOR UPDATE  ), 조건부 재고 차감/복구 로직은 서비스 레이어 구현과 함께 다음 주 진행.
18. **미달성** 찜 기능 정규화 미완성:   Like   엔티티가   id  만 보유하고   userId  ,   productId  , 유니크 제약이 없음.
19. **미달성** 최근 본 상품 정규화 미완성:   recent_watching   이력 엔티티/테이블 및 조회 정렬 기반 컬럼(  viewedAt  )이 없음.
20. **범위 조정 필요** 운영 표준 설정: 글로벌 CORS/Jackson/traceId는 애플리케이션 레이어 성격이 강하므로 스키마 작업 이후 우선순위 재배치 권장.

[20260811 ~ 20260818]

### 이번주 구현 목표
- [x] 1. 주문 모델 기본 구조(`Order - OrderItem` 관계, 주문 시점 가격/수량 스냅샷) 반영 상태 확인.
- [ ] 2. 서비스/컨트롤러 구현 완료(주문/장바구니/재고/결제): Cart는 완료(`CartService` 전체 구현). Order는 `createOrder`/`authTossPayment`만 구현되고 `getOrders`/`getOrdersWithUserId`/`getOrderWithUserId`/`patchOrder`/`putOrder`/`deleteOrder`는 스텁으로 남아 부분 완료. 재고 차감 로직은 미구현.
- [x] 3. TossPayments 연동 방식 학습 및 설계 착수: `TossClient`/`TossPaymentConfig`/`OrderService.authTossPayment()`/결제 승인 엔드포인트까지 실구현되어 목표 초과 달성.
- [x] 4. JWT 발급/검증 인프라(`JwtProvider`) 및 Spring Security Servlet Filter(`JwtAuthenticationFilter`) 구현 완료(헤더+쿠키 토큰 추출, AuthenticationEntryPoint 연결까지 확인됨).
- [ ] 5. Redis 기반 refresh token 저장/조회/대조(`RefreshTokenRepository`)는 완료. 블랙리스트는 애초에 이번 주 범위가 아니었음(CI/CD 이후 추가 기능 단계로 재확인, 아래 다음 주 계획에서 제외 처리).
- [ ] 6. 이번주 주요 목표: TossPayments 연동 + JWT 구현은 완료. 컨트롤러 엔드포인트의 JWT 연동(`@AuthenticationPrincipal`, role 기반 인가)까지 완료됐으나 2번의 Order 잔여 작업 때문에 전체 완료로는 미체크.

### 컴파일 및 디버깅 관련 문제
- [ ] 1. 미구현 서비스/컨트롤러 경로에서 요청 처리 시점 예외(NPE/미지원 동작) 위험이 남아 있음.
- [ ] 2. 결제 승인 전후 주문 상태 전이 검증 로직이 없어 디버깅 시 결제-주문 정합성 추적이 어려움.

### 구현 기능 관련 문제점
- [ ] 1. 주문 관련 핵심 유스케이스(`placeOrder`, `cancelOrder`, 결제 승인 후 상태 반영)가 서비스 계층에 완결되지 않음.
- [ ] 2. TossPayments 승인/취소 API와 내부 `OrderStatus` 매핑 규칙이 정의되지 않아 구현 방향이 불명확함.
- [ ] 3. 결제 성공/실패 콜백(리다이렉트 또는 웹훅) 처리와 멱등성 기준(orderId 중복 승인 방지)이 미정의 상태임.
- [ ] 4. 일정 리스크: 8/24~8/25 해커톤 일정으로 다음 주(20260819~20260825) 실질 가용 개발일이 7일 중 5일(8/19~8/23)로 축소됨 → 다음 주 목표 범위를 5일 기준으로 재조정 필요.

### 다음 한 주 동안 개발할 기능
- [ ] 1. TossPayments 연동 목표 1: 결제 요청 파라미터(`orderId`, `amount`, `orderName`, 고객 식별자) 생성 규칙과 성공/실패 URL 엔드포인트를 확정.
- [ ] 2. TossPayments 연동 목표 2: 서버 결제 승인 API(`paymentKey`, `orderId`, `amount` 검증 → Toss 승인 호출) 구현.
- [ ] 3. TossPayments 연동 목표 3: 승인 결과를 주문 상태 전이(`PAY_PENDING → PAID / PAY_FAILED`)와 재고 처리 트랜잭션에 연결.
- [ ] 4. TossPayments 연동 목표 4: 중복 승인 방지를 위한 멱등 키/중복 요청 차단 로직 및 실패 재시도 정책 정의.
- [ ] 5. 서비스/컨트롤러 마감 목표: 주문·결제 관련 미구현 Service/Controller 메서드를 우선 완성하고 통합 시나리오로 점검.
- [ ] 6. (필수, 사용자 직접 구현) `OrderService`의 스텁 메서드(`getOrderWithUserId` 등)를 본인 소유 주문 검증 로직 포함해서 완전하게 구현 — 담당자가 직접 진행하기로 확정.
- [ ] 7. ~~(필수, 8/20) 결제-재고 트랜잭션 경계 설계~~ → 범위 조정: 재고 처리 로직은 CI/CD 이후 추가 기능 단계 목표로 재확인됨. 이번 5일(8/19~8/23) 계획에서 제외.
- [ ] 8. ~~(필수, 8/21) Toss 결제 승인 성공 시 재고 차감/복구 트랜잭션~~ → 7번과 동일하게 CI/CD 이후로 이월.
- [ ] 9. ~~(필수, 8/22) access token 블랙리스트~~ → 범위 조정: 블랙리스트 관리는 CI/CD 이후 추가 기능 단계 목표로 재확인됨. 이번 5일 계획에서 제외.
- [ ] 10. (필수, 8/23 · 해커톤 전날) 회원가입 → 로그인 → JWT 발급 → 인증된 cart/order API 호출 → Toss 결제 → 주문 상태 반영까지 수동 E2E 시나리오 점검. 새 기능 착수보다 확인/마무리 위주로 진행.
- [ ] 11. (스트레치, 우선순위 최하위) Next.js 웹서버 프로젝트 뼈대 착수 — 해커톤으로 가용일이 5일로 줄어 이번 주 필수 범위에서 제외, 8/19~8/23 중 시간이 남는 경우에만 시도.

[20260819 ~ 20260825]

### 이번주 구현 목표
- [x] 1. E2E 시나리오 점검: 회원가입 → 로그인 → JWT 발급 → 인증된 cart/order API → Toss 결제 → 주문 상태 반영까지 전체 흐름 확인. **20260821 완료** — 주문 생성(`orderUid` 자동 생성 포함) → Toss 결제창 → 백엔드 `authTossPayment` confirm → `orderStatus` PAID 반영까지 실제 응답으로 검증됨(아래 컴파일/디버깅·구현 문제 항목들이 이 과정에서 순차적으로 발견·수정됨).
- [ ] 2. Next.js를 통한 웹서버 뼈대 구축: 기존 뼈대 기준으로 구현된 기능을 노출할 UI/UX 및 URL 엔드포인트 기획·구현. (지난주엔 스트레치로 분류했으나, 트러블 슈팅 기록에서 이번 주 핵심 목표로 격상 확정됨) **20260821 진행 상황**: 메인페이지(네비/배너/백엔드 연동 상품 그리드, Server Component), 상품 목록 페이지(`/products`), 로그인 페이지 CORS(`AuthController` `@CrossOrigin` 누락)·필드명 불일치(`signInPassword`→`logInPassword`, `signUpBirthday`→`signUpBirthDay`) 버그까지 수정 완료해 로그인 E2E 성공 확인. 남은 것(로그인 성공 시 메인 리다이렉트, 상품 상세 동적 라우트, 장바구니 담기/조회/결제)은 내일(20260822)부터 이어서 진행 — UI/UX 스타일링은 기능 완성 이후로 의도적으로 미룸(사용자 확정, 구조 변경 중 반복 스타일링 낭비 방지).
- [ ] 3. (스트레치) 1, 2번 우선 완료 후 시간이 남는 경우에만 JS/TS 학습 보강 — 정식 구현 목표가 아닌 개인 학습 목적, 이번 주(8/19~8/23, 해커톤으로 5일) 범위 내 조건부 항목.

### 컴파일 및 디버깅 관련 문제
- [x] 1. **치명** 주문 생성 시 SQL 문법 에러(`SQLSyntaxErrorException`, `insert into order (...)` 근처): `TableNames.orderTableName = "order"`가 MySQL 예약어(`ORDER BY`)와 충돌 → `userTableName`이 이미 동일한 이유로 `"users"`로 우회해놓은 전례가 있음. `orderTableName`을 `"orders"`로 수정 완료(`likeTableName`은 찜 기능 미구현이라 아직 미적용, 착수 시 `"likes"`로 같이 변경 필요).
- [x] 6. **치명** `orders` 테이블에 `order_id` 컬럼 없음(`Unknown column 'o1_0.order_id'`): 위 테이블명 변경 이전에 아주 오래된 스키마(`id`/`productId`/`userId`/`orderDate` 컬럼, 현재 엔티티와 불일치)로 이미 `orders` 테이블이 존재했음 → `ddl-auto: update`는 기존 테이블의 PK 컬럼을 못 바꿔서 `order_id`가 끝내 안 생김. 정크 데이터(2건)뿐이라 `orders` 테이블 및 정체불명 플레이스홀더 테이블(`${mallDB.order.url}` 등 3개, 과거 프로퍼티 치환 실패 잔재로 추정) 전부 DROP 후 재기동으로 정상 스키마 재생성해서 해결.
- [x] 7. **치명** Toss confirm 브라우저 호출이 CORS로 "Failed to fetch": `SecurityConfig`에 `.cors(...)` 설정이 아예 없어서, Spring Security가 `/orders/**`(`authenticated()`)에 대한 preflight `OPTIONS` 요청까지 401로 막아버림(`@CrossOrigin`의 `allowCredentials`만으론 해결 안 됨 — Security 필터가 MVC 도달 전에 먼저 차단). `curl -X OPTIONS`로 401 및 CORS 헤더 부재 직접 확인. `.cors(Customizer.withDefaults())` 추가로 해결.
- [x] 8. **경미** `TossPaymentRequestDTO.orderId`를 `Long`으로 타입 변경하면서 `@NotBlank`(String 전용 검증) 어노테이션이 그대로 남아있어 Bean Validation 시 `UnexpectedTypeException` 위험 → `@NotNull`로 수정.
- [ ] 9. **경미(미해결, 참고용)** `OrderService.authTossPayment`가 Toss의 실제 에러(`TossError.code()`/`.message()`, 예: `ALREADY_PROCESSED_PAYMENT`)를 버리고 자체 `PA001`(뭉뚱그린 메시지)로 덮어써서 던짐 → 디버깅 중 원인 파악이 어려웠던 원인. 나중에 Toss 원본 에러 코드/메시지를 로그에 남기거나 응답에 포함하는 개선 권장(지금 당장 급한 건 아님).

### 구현 기능 관련 문제점
- [ ] 1. **중대** 주문 가격/재고 무결성 미검증: `OrderItemCreateDTO`(`productId`, `curOrderItemPrice`, `quantity`)가 클라이언트 값을 그대로 받고, `OrderService.createOrder` / `Order.addOrderItem`에서 `Product` 엔티티를 재조회해 가격을 검증하는 로직이 전혀 없음(코드상 `productRepository` 참조 자체가 없음). API를 UI 없이 직접 호출하면 `curOrderItemPrice`를 임의값(예: 0)으로 조작해 주문 생성 가능 → `productId` 목록을 모아 `productRepository.findAllById()` 1회(IN 절) 조회로 서버가 `curOrderItemPrice`를 직접 채우도록 수정 필요. 애초에 클라이언트 입력값(카트에 표시된 가격)을 그대로 전달해 DB 조회를 없애려던 설계(“db조회 쿼리 최소화”)는 이 경로에서는 채택하지 않기로 확정 — 가격 무결성이 쿼리 1회 절감보다 우선. 기존 재고 차감 TODO(`OrderService.java` 49행)와 같은 조회에 묶어서 처리 권장.
- [x] 5. ~~**중간** Toss 결제 승인 엔드포인트 소유권 검증 누락~~ → **정정(같은 날 번복, 사용자 확인)**: 처음엔 `authTossPayment`에 `userId` 받아서 `patchOrder`처럼 소유권 검증을 추가하자고 제안했으나, 사용자가 Bruno에서 로그인 쿠키 없이 호출 시 401로 막히는 걸 확인하고 "애초에 이 엔드포인트는 인증 자체를 빼야 하지 않냐"고 재질문 → Copilot 재검토 결과 인증 제거가 더 합리적이라고 결론 변경. 근거: `paymentKey`(Toss가 실제 결제 시도 후에만 발급) + `OrderService.authTossPayment`의 amount vs `Order.totalOrderPrice` 대조(71-73행) + `TossClient.confirm()`의 서버 간 secretKey 인증(Basic Auth)이 이미 3중으로 진위를 검증하므로, 자체 로그인 세션 요구는 보안적으로 더해주는 게 적고, 오히려 외부 도메인(Toss) 왕복 리다이렉트에서 쿠키 유실 마찰만 유발. `SecurityConfig`에 `POST /orders/toss/payment/auth`를 `permitAll()`로 별도 매처 추가(넓은 `/orders/** authenticated()` 규칙보다 앞 순서 필수) 권장. 소유권 검증(userId 비교) 제안은 철회.
- [x] 4. **치명** CORS 설정 불일치: `OrderController.java:18`의 `@CrossOrigin(origins = "https://localhost:3000")`만 `https`이고, `ProductController`/`CartController`/`UserController`는 전부 `http://localhost:3000` → Next.js dev 서버(기본 http)에서 주문/Toss 결제 승인(`/orders/toss/payment/auth`) API 호출 시 CORS로 막힘. `http`로 수정 완료 + `allowCredentials = "true"` 추가(쿠키 기반 인증 유지 결정에 따라 필요) + `SecurityConfig`의 `.cors(...)` 누락(위 디버깅 항목 7번)까지 같이 고쳐야 최종적으로 브라우저에서 정상 동작 확인됨.
- [x] 10. **신규 구현(사용자 요청)** `Order.orderUid` 도입: Toss `orderId` 제약(6자 이상 문자열) 때문에 내부 PK(`orderId`, 순차 증가라 1자리부터 시작)를 그대로 못 씀 → `Order` 생성자 내부에서 `ThreadLocalRandom`으로 6~12자리 랜덤 `Long`을 자동 생성(호출부에서 별도 주입 불필요), `@Column(unique = true, nullable = false)`. `OrderRepository.findByOrderUid` 추가, `authTossPayment`가 PK `findById` 대신 이걸로 조회하도록 변경, `OrderResponseDTO`에도 노출. 충돌 시 재시도 로직은 값 공간(최대 10^12)이 커서 지금 규모엔 과설계로 판단해 보류.
- [ ] 2. **경미** 카트→주문 DTO 구조 후보로 `List<Map<ProductId, Quantity>>`가 제안됐으나 비채택: 기존 `List<OrderItemCreateDTO>`(productId+quantity)가 Bean Validation/타입 안정성/확장성에서 이미 우위이고, 체크박스로 일부 선택 + 수량 조절 시나리오도 이 구조로 그대로 커버 가능(체크된 CartItem만 골라 매핑해서 전송) → 구조 변경 불필요, item 1의 가격 서버 재조회만 반영. 단, 부분 주문 후 장바구니 처리 정책(주문한 CartItem 삭제 vs 수량 차감)이 아직 미정 → `OrderService.createOrder` 후속 로직 설계 시 확정 필요.
- [ ] 11. **미해결(관찰됨, 참고용)** `authTossPayment` 멱등성 부재: 같은 주문에 confirm이 두 번 이상 호출되면(테스트 중 실수로 재시도 등) 두 번째 호출이 Toss로부터 `ALREADY_PROCESSED_PAYMENT` 에러를 받고, `Order.failPayment()`가 실행돼 **이미 정상 결제(PAID)된 주문이 FAILED로 덮어써질 위험**이 있음. 오늘 디버깅 중 실제로 이 에러 코드가 재현됐지만(다른 주문에 대해), 다행히 최종 성공 테스트는 새 주문으로 진행해 실제 데이터 오염은 없었음. `orderStatus`가 이미 `PAID`면 confirm을 재시도하지 않고 바로 성공 응답을 반환하는 가드 추가를 향후 개선 항목으로 권장(급한 건 아님).
- [x] 3. **범위 조정(사용자 확정)** `OrderCreateDTO`에서 `userId` 제거하고 JWT(`@AuthenticationPrincipal Long userId`)로 대체 완료 확인 — `CartController` 기존 패턴과 일치, `JwtAuthenticationFilter`가 principal로 `Long userId`를 직접 넣는 구조와도 정합성 확인됨. 컨트롤러/서비스 시그니처도 `List<OrderItemCreateDTO>` 대신 `OrderCreateDTO` 단일 파라미터로 정리 완료. 다만 item 1(가격 서버 재조회)은 이번 변경에 포함되지 않음 — 재고 컬럼 자체가 아직 없어 재고 확인/차감 로직 전체를 CI/CD 이후 "추가 기능" 단계로 미루기로 확정했고, 가격 검증도 재고 트랜잭션 작업과 묶어서 그 단계에 같이 처리하기로 사용자가 명시적으로 결정함(작은 변경이라 지금 반영 가능하다고 제안했으나 반려). 이번 주 범위는 주문 생성 API + TossPayments 결제 흐름 연결 확인으로 한정.

### 다음 한 주 동안 개발할 기능
- [ ] 1. (20260822부터) 로그인 성공 시 메인페이지로 리다이렉트
- [ ] 2. 메인페이지 상품 클릭 → 상품 상세 페이지(동적 라우트 `products/[productId]`)
- [ ] 3. 장바구니 담기 / 장바구니 페이지 이동
- [ ] 4. 장바구니 → 결제(Toss) 흐름 프론트 연동
- [ ] 5. 위 1~4번으로 E2E 프론트 기능 완성, 목표 마감 20260825(화, 수요일 시작 기준 이번 주 마지막날). 완료되는 대로 바로 CI/CD + Docker/Kubernetes 착수(다음 항목이 아니라 그 다음 사이클로 이월 가능).
- [ ] 6. UI/UX 스타일링은 1~4번 기능이 다 완성된 뒤로 의도적으로 미룸(사용자 확정, 20260821).

### 장기 로드맵 참고 (특정 주차에 배정된 항목 아님, 순서만 확정 — 20260821 순서 정정: SQL 튜닝이 재고 로직 이전→이후로 이동)
- 웹서버(Next.js) E2E 기능 완료(목표 20260825, 화요일 마감) → GitHub Actions + CI/CD + Docker/Kubernetes → access token 블랙리스트 + 주문 무결성 묶음("추가 기능" 단계, 사용자는 "상품 수량 로직"으로 지칭): (a) 상품 재고 차감/복구 트랜잭션, (b) `OrderService.createOrder` 서버 측 가격 재조회(`productRepository`, 클라이언트 `curOrderItemPrice` 미신뢰), (c) (b) 완료 후 `OrderItemCreateDTO.curOrderItemPrice` 필드 제거 → **그다음 SQL 튜닝** (20260821 기준 최종 순서, 이전엔 SQL 튜닝이 이 묶음보다 앞이었으나 사용자가 언급을 빠뜨렸던 것으로 확인되어 정정)
- 각 단계는 이전 단계 완료가 전제 조건.
- (20260908 추가) **빌더 컨벤션 정립 + 리팩터링** — "테스트 코드 + CI/CD + 트래픽 테스트 도구 의존성 확립"이 전부 끝나고 본격 리팩터링 후 기능을 하나씩 추가하는 시점의 항목(특정 주차 미배정, `[20260826~20260901]` 다음 한 주 8번 후순위 조정 지점과 동일 페이즈). 진행 순서: 컨벤션 문서화 → 기존 `@Builder` 배치 전수 점검(엔티티/DTO 전부) → "최소 변경" 원칙 리팩터링. 20260908 세션 확정 방침:
	1. 동일 클래스에 `@Builder` 2개 금지 — 애노테이션마다 `builder()` + `XxxBuilder`를 생성하므로 2개면 컴파일 충돌. `builderMethodName`/`builderClassName`을 따로 주면 컴파일은 되나 엔티티에선 책임 과다 신호로 보고 지양.
	2. 엔티티: `@Builder`는 "생성 시점에 허용할 필드만 받는 생성자" 하나에만. `@NoArgsConstructor(access = PROTECTED)` 동반(JPA 프록시용 기본 생성자 확보 + 무분별한 all-args 차단).
	3. 응답 DTO(예: `OrderResponseDTO`): `@Builder`는 `private`(or package-private) all-args 생성자에. 엔티티→DTO 매핑은 `static from(Entity)` 팩토리 한 곳에 모으고 내부에서 `builder()` 호출. 운영 변환 코드와 테스트가 이 빌더 하나를 공유 — 테스트 전용 생성자를 따로 만들지 않는다(생성 경로 중복 방지).
	4. DTO 필드가 단순하고 테스트에서 부분 조립 빈도가 낮으면 `record DTO(...)` + `from()`만으로 충분, 빌더 미도입 검토.
	5. 점검 근거: `@Builder` 사용 패턴이 이미 제각각 — `Product.builder()`가 `productDetailCreateDTOList(List.of())`에서 검증 위반(위 `[20260826~20260901]` 컴파일/디버깅 7번 ①). 전수 점검 필요.
	6. (20260908 추가) 요청 DTO는 `@NoArgsConstructor` 필수 — Jackson 역직렬화 경로 확보용. `@AllArgsConstructor` 단독은 부족(필드 1개면 인자 1개 생성자가 되어 Jackson이 delegating creator로 오인, JSON object 바인딩 실패). `@Builder`는 테스트 편의용이며 Jackson은 사용하지 않음. 근거: `OrderUpdateDTO` 누락으로 `@RequestBody` 역직렬화가 `InvalidDefinitionException`("no Creators")·HTTP 500 (상세 `[20260902~20260908]` 컴파일/디버깅 1번).

[20260826 ~ 20260901]

### 이번주 구현 목표
- [x] 1. GitHub Actions 워크플로우 파일 정상화: `.github/workflow/` → `.github/workflows/` 경로 수정, `workflow_dispatch: "Run WorkFlow"` 문법 오류 수정. **20260827 완료** — 이후에도 `name`/`run`/`uses` 분리 오타, `cache: gradle` 위치 오류(스텝 최상위가 아니라 `with:` 안에 있어야 함) 등 추가로 여러 차례 발견·수정을 거쳐 최종적으로 `build-and-test` job이 GitHub Actions에서 실제로 초록불(성공)까지 확인됨.
- [ ] 2. GitHub Actions 파이프라인 구현: checkout → 백엔드 빌드/테스트(gradle) → 프론트 빌드(npm) → Docker build & push(Docker Hub) → EC2 배포까지 최소 1회 성공 실행 확인. **20260827 진행 상황**: checkout → JDK 셋업(`actions/setup-java`) → `docker compose up -d db` → `mysqladmin ping` 대기 → `./gradlew test`(working-directory 지정)까지의 "빌드/테스트" 구간만 완성 및 성공 확인. Docker build & push(Docker Hub), EC2 배포 job은 아직 미착수 — 다음 작업 대상.
- [ ] 3. 백엔드 테스트 코드 작성(2번 build-and-test 단계에서 실제로 실행될 대상 확보, 저널 20260826 기록 기준). **20260827 진행 상황**: `UserServiceTest` 완료(createUser/getUser/patchUserInfo/putUserInfo/deleteUser 각각 성공·not-found 케이스, 총 9개 테스트, 전부 통과 확인). 나머지 서비스(`CartService`, `CartItemService`, `OrderService`, `ProductService`, `TossPaymentService`, `AuthService`)는 다음 작업일(20260828 예정)로 이월.
- [x] 4. GitHub Actions 동작 원리 학습 보강(트리거 종류/러너/시크릿 관리 등) — 지난주 자기평가("대충 파악만 함") 기반 보완 목표. **20260827 완료로 판단** — 웹훅 트리거, 러너(VM) 프로비저닝, job 간 격리(파일시스템 미공유, 매 job마다 checkout 필요 이유), `services:` vs `docker compose up` vs Testcontainers 트레이드오프, 멀티스테이지 Docker 빌드에서 테스트 실행이 불가능한 이유, GitHub Secrets, 새 Rulesets UI(Bypass list, Enforcement status) 개념까지 실습 기반으로 학습 완료.
- [ ] 5. (스트레치, 시간 남는 경우) Docker/Kubernetes 학습 착수 — 사용자가 이번 주 일정 여유에 따라 조건부로 명시(저널 20260826 기록). 20260827 기준 미착수.
- [x] 6. **20260901 Copilot 검토 결과**: 3번(백엔드 테스트 코드 작성) 상향 완료 확인 — `CartServiceTest`(13개)·`ProductServiceTest`(10개)·`OrderServiceTest`(14개) 전부 작성 및 실행 통과 확인(`UserServiceTest` 9개는 기존 완료분과 함께 회귀 확인). `CartItemService`/`TossPaymentService`는 실제 메서드가 없는 빈 클래스라 테스트 대상 자체가 없고, `AuthService`(`logIn`/`logOut`)만 테스트 미작성 상태로 남음.
- [x] 7. **20260901** `contextLoads()`가 로컬에서 실패하던 문제(`JWT_SECRET_KEY` placeholder 미해결 → 이후 MySQL dialect 조회 실패로 원인이 바뀌며 재현)를 `src/test/resources/application.yml`(H2 인메모리 DB + 테스트 전용 Base64 JWT 더미키)로 해결. 해당 더미 시크릿이 GitGuardian에 false positive로 걸려 예외 처리(allow)까지 진행 — 실제 운영 시크릿과 무관한 값이라 값을 앞으로도 그대로 고정 유지 권장(바뀌면 재탐지 가능성 있음).

### 컴파일 및 디버깅 관련 문제
- [x] 1. `.github/workflow/ci-cd.yml` 경로 오타로 워크플로우 자체가 트리거되지 않음(20260827 발견) → `workflows`(복수형)로 수정 완료.
- [x] 2. `workflow_dispatch: "Run WorkFlow"` — 값이 없어야 할 위치에 문자열이 들어가 있어 워크플로우 파싱 실패(invalid workflow) 위험(20260827 발견) → 값 제거로 수정 완료.
- [x] 3. **20260827 발견** `cache: gradle`이 step 최상위 키로 들어가 있어(`with:` 블록 밖) 워크플로우 파싱 실패, 실제 Actions 실행 로그(`This run likely failed because of a workflow file issue`)로 확인 → `with:` 내부로 이동해 해결.
- [x] 4. **20260827 발견** `TOSS_SECRET_KEY`/`JWT_SECRET_KEY`가 GitHub Secrets에 미등록 상태로 워크플로우가 빈 문자열을 주입 → `contextLoads()` 테스트가 `io.jsonwebtoken.security.WeakKeyException`으로 실패(JWT 서명 키가 빈 문자열이라 발생). 두 시크릿을 실제로 등록해 해결.
- [x] 5. **20260827 발견** branch protection을 "Rulesets"으로 새로 설정했는데 `enforcement` 기본값이 `disabled`였음 — 나머지 규칙(PR 필수, status check 필수, bypass list 비움)은 다 맞게 설정했지만 이 스위치를 안 켜서 처음엔 무효 상태였음. `active`로 변경해 해결.
- [x] 6. **20260827 발견 (UserServiceTest 작성 중 실제 버그 3건, `./gradlew test` 직접 실행으로 확인)**: ① `userCreateTest`에서 입력 이메일(`qwer1324@...`)과 검증 이메일(`qwer1234@...`) 오타 불일치로 실패, ② `patchUserNotFoundExceptionTest`에서 `UserUpdateDTO`에 `null`을 넘겨 `CheckConfig.npeCheck`가 `NullPointerException`을 먼저 던져서 의도한 `NotFoundException` 검증 전에 실패, ③ `putUserNotFountTest`가 `userService.putUserInfo(...)` 대신 `userService.deleteUser(...)`를 호출하고 있어 우연히 통과는 하지만 `putUserInfo`의 not-found 경로는 실제로 미검증 상태였음 — 셋 다 수정 후 9개 테스트 전부 통과 확인.
- [x] 7. **20260901 (Copilot 리뷰 세션에서 실제 실행 확인)** `CartServiceTest`/`OrderServiceTest` 작성 과정에서 다수의 Mockito 실사용 버그를 실행 기반으로 발견·수정: ① `Product.builder()`의 `productDetailCreateDTOList(List.of())` 빈 리스트 검증 위반(`IllegalArgumentException`), ② `invocation.getArgument(1)`/`getArgument(2)` 인덱스 오류(단일 인자 메서드인데 잘못된 인덱스 참조 → `ArrayIndexOutOfBoundsException`), ③ 실제 객체(mock 아님)에 `when(...)`을 건 Mockito 오용(`MissingMethodInvocationException`), ④ 서로 다른 인스턴스를 대상으로 한 stub과 실제 호출 인자 불일치(`PotentialStubbingProblem`), ⑤ 코드 경로상 도달 못 하는 stub 다수(`UnnecessaryStubbingException`, not-found 시나리오 두 개를 한 메서드에 몰아넣은 경우 포함). 이 과정에서 `Cart.patchCart()`/`Order.patchOrder()`가 quantity만 갱신하고 `updateTotalCartPrice()`/`updateTotalOrderPrice()`를 안 불러서 총액이 갱신 안 되던 **실제 서비스 로직 버그**도 발견·수정됨(테스트 버그가 아니라 프로덕션 버그였음).

### 구현 기능 관련 문제점
- [ ] 1. 일정 리스크: 토요일(8/29) 결혼식 방문, 월요일(8/31) 기숙사 이사로 실질 가용 개발일이 7일 중 5일로 축소됨(저널 20260826 기록 기준) → 목표 범위를 5일 기준으로 재조정 필요.
- [x] 2. `jobs.build-and-test.steps:` 이하 전체 미구현 상태 — 이번 주 핵심 작업 대상. **20260827 완료**: checkout/JDK/db/wait/test 5개 step 구현 및 실제 성공 실행 확인.
- [ ] 3. Docker Hub 자격증명 등 GitHub Actions 시크릿 관리 방식이 아직 워크플로우에 반영되지 않음 — steps 작성 시 `secrets.*` 참조 설계 필요. (`build-and-test`에는 미해당 없음, `build & push`/`deploy` job 추가 시 여전히 필요)
- [ ] 4. **20260827 신규** branch protection(Rulesets)을 `main`에 설정 완료 — `Require a pull request before merging`(승인 0명), `Require status checks to pass before merging`(`build-and-test` 필수), bypass list 비움(관리자 포함 전원 우회 불가). 단, GitGuardian Security Checks는 별도 GitHub App 체크로 표시만 되고 required 목록엔 없어 현재 병합을 막지는 않음 — 필요시 추후 required로 추가할지 검토.
- [ ] 5. **20260901 (신규, 중간)** `AuthService.logIn`/`logOut`(비밀번호 대조, JWT 발급, Redis refresh token 저장까지 포함하는 인증 핵심 로직)에 테스트 코드가 아직 없음 — 다음 주 테스트 작성 시 최우선 대상으로 권장.
- [ ] 6. **20260901 (신규, 치명)** `SecurityConfig`의 `authorizeHttpRequests` 규칙에 `/products/**`가 아예 매칭되지 않아 `anyRequest().permitAll()`로 빠짐 → 로그인 없이 누구나 상품 생성/수정/삭제(`POST`/`PATCH`/`DELETE /products/**`) 가능한 상태. 같은 이유로 `GET /users`(전체 유저 조회, 컨트롤러 주석엔 "관리자 권한만" 예정이라 적혀있으나 실제 규칙 없음)도 인증 없이 열려있음. Controller 레이어 테스트 계획 수립 중 `SecurityConfig` 재검토로 발견 — 상품 CUD는 `hasRole("ADMIN")`, 유저 전체 조회도 관리자 전용으로 규칙 추가 필요.

### 다음 한 주 동안 개발할 기능
- [ ] 1. (이번 주 내 CI/CD를 다 못 끝낼 경우 이월) Docker/Kubernetes 학습 및 적용.
- [ ] 2. CI/CD 파이프라인 안정화 후 EC2 배포 자동화 반복 검증(재현성 확인).
- [ ] 3. 장기 로드맵상 다음 단계인 "상품 수량 로직"(재고 차감/복구 트랜잭션 + 주문 가격 서버 재조회) 착수 준비.
- [ ] 4. **20260828 예정**: `CartService`/`CartItemService`/`OrderService`/`ProductService`/`TossPaymentService`/`AuthService` 나머지 서비스 테스트 코드 작성 + 추가로 어떤 종류의 테스트(Controller 계층, Repository/`@DataJpaTest` 등)가 더 필요할지 탐색.
- [ ] 5. **트러블 슈팅 일지 기록 리마인더**: 20260827 세션에서 다룬 CI/CD 설정·원리(위 컴파일/디버깅 6건 + GitHub Actions 개념 학습 4번 항목)는 아직 `ShoppingMall - 트러블 슈팅 기록.md`에 상세히 기록되지 않음. 다음 작업 시작 전에 오늘 다룬 내용(워크플로우 문법 함정들, job/step 격리, Rulesets 개념, Mockito 테스트에서 발견한 버그 3종 등)을 자세히 정리해서 남기는 것을 권장.
- [x] 6. **(확정, 20260901) 다음 주(20260902~20260908) 목표: 테스트 코드 + Docker/Kubernetes.** 단, Docker/K8s는 이론 학습에서 그치지 않고 이번 주 미완성으로 남은 CI/CD 파이프라인의 "Docker build & push(Docker Hub) → EC2 배포" 단계를 실제로 완성하는 데 바로 적용하는 방향으로 진행(사용자 확정).
- [ ] 7. 테스트 코드 세부 계획(Controller 레이어 신규 착수 — 5개 컨트롤러 전부 테스트 없음 확인됨, `AuthController`/`CartController`/`OrderController`/`ProductController`/`UserController`):
	1. 공통 준비: `@AuthenticationPrincipal Long userId`가 `UsernamePasswordAuthenticationToken(Long, ...)` 커스텀 구조라 `@WithMockUser`가 안 맞음 — `SecurityMockMvcRequestPostProcessors.authentication(...)` 사용 필요. `@WebMvcTest`는 `SecurityConfig`를 자동 로드하지 않으므로 `@Import(SecurityConfig.class)` 명시 필요(안 하면 인가 규칙 자체가 검증 안 됨).
	2. `AuthController`: 로그인 성공(쿠키 2종 확인)/실패, DTO 검증 실패, 로그아웃 인증 여부.
	3. `UserController`: 회원가입 성공/검증 실패, `GET /users` 전체 조회 인증 갭(위 구현 기능 문제점 6번) 재현, 본인 조회/수정/삭제 인증 필요 확인.
	4. `ProductController`: CRUD 성공/not-found, **CUD 미인증 접근 갭(위 6번) 재현 후 `SecurityConfig` 수정으로 막기**.
	5. `CartController`: 전 엔드포인트 미인증 401 확인, `patchCart` 검증 실패 케이스.
	6. `OrderController`: 전 엔드포인트 미인증 401 확인(단 `authTossPaymentOrder`는 트러블 슈팅 기록상 의도적으로 인증 제외 — 미인증이어도 정상 동작해야 정상). `deleteOrder`에 `userId` 파라미터가 없어 소유권 검증 없이 ADMIN 권한만으로 삭제되는 구조가 의도한 설계인지 재확인 필요.
	7. `AuthService`(`logIn`/`logOut`) 단위 테스트 — 우선순위 상위(위 구현 기능 문제점 5번).
	8. (선택, 우선순위 낮음) `@DataJpaTest` 기반 Repository 테스트 — `orphanRemoval` 실제 DELETE 발생 여부 등 Mockito로는 검증 불가능한 부분에 한정.
- [x] 8. **(일정 조정, 사용자 확정 20260901)** 웹서버 E2E 시나리오 점검은 "테스트 코드 + CI/CD + 트래픽 테스트 도구 의존성 확립"이 전부 끝나고 기능을 하나씩 추가하는 시점으로 후순위 조정. (정정: 지난 리뷰에서 "웹서버 E2E 완료가 CI/CD보다 선행"이라고 로드맵 순서를 언급했었는데, 이는 Copilot이 `[20260819~20260825]` 리뷰 시점에 재정리하며 만든 순서였고 사용자 원본 트러블 슈팅 일지엔 CI/CD가 이미 같은 주에 병행되고 있었음 — 확인 없이 단정적으로 전달했던 부분에 대해 정정함.)

[20260902 ~ 20260908]

### 이번주 구현 목표
- [/] 1. 백엔드 테스트 코드 마저 작성 — **부분 완료(20260909 Copilot 검토)**. 완료: 5개 컨트롤러 happy-path 테스트 25개(`AuthControllerTest` 2, `CartControllerTest` 6, `OrderControllerTest` 7, `ProductControllerTest` 5, `UserControllerTest` 5) 전부 통과 + `AuthServiceTest` 5개 존재(`[20260826~20260901]` 구현 기능 문제점 5번 해소). 미완: 예외 매핑 테스트(서비스가 `NotFoundException` 등 throw → `GlobalExceptionHandler` → status/body), `@Valid` 실패(400) 테스트, 인가 테스트(미인증 401 / non-ADMIN 403), `@DataJpaTest` repository 테스트(선택) — 전부 미작성. 저널엔 `[x]`로 표기됐으나 happy-path 한정이라 `[/]`가 정확.
- [/] 2. Docker & Kubernetes 학습 + 구현 — **사실상 미착수(20260909 Copilot 검토)**. 트러블 슈팅 일지 `[20260902~20260908]` 블록에 Docker/K8s 관련 항목이 0개. 다음 주로 이월 필요.

### 컴파일 및 디버깅 관련 문제
- [ ] 1. **20260908 발견 (`OrderControllerTest.patchOrder_successTest` 작성 중, `./gradlew test`로 재현)** `OrderUpdateDTO`에 `@NoArgsConstructor`가 없어 `@RequestBody` 역직렬화가 실패, HTTP 500 반환 → `andExpect(status().isOk())`(테스트 275행)에서 실패. 실제 예외: `HttpMessageConversionException: Type definition error [OrderUpdateDTO]` → `Caused by: com.fasterxml.jackson.databind.exc.InvalidDefinitionException: Cannot construct instance of OrderUpdateDTO (no Creators, like default constructor, exist): cannot deserialize from Object value (no delegate- or property-based Creator)`.
	1. 원인: 필드가 1개라 `@AllArgsConstructor`가 만드는 유일한 생성자가 "인자 1개짜리" → Jackson이 이를 delegating creator로 간주(요청 바디를 통째로 `List<OrderItemUpdateDTO>` 한 값으로 바인딩 시도)하는데, 실제 바디는 JSON object(`{"orderItemResponseDTOList":[...]}`)라 불일치. 기본 생성자도 없어 사용 가능한 creator가 전무. `@Builder`는 Jackson이 사용하지 않음.
	2. 대조: `OrderCreateDTO`는 `@NoArgsConstructor` 보유 → `createOrder_successTest` 통과. 프로젝트의 다른 order DTO(`OrderItemUpdateDTO`/`OrderResponseDTO`/`OrderItemResponseDTO`)도 전부 `@NoArgsConstructor` 보유 — `OrderUpdateDTO`만 누락.
	3. `OrderServiceTest.patchOrder_successTest`(서비스 단위 테스트)가 통과했던 이유: 거기선 `new OrderUpdateDTO(List.of(...))`로 직접 생성해 Jackson 미개입. 이 버그는 컨트롤러 테스트의 JSON→DTO 역직렬화 경로에서만 드러남.
	4. 수정: `OrderUpdateDTO`에 `@NoArgsConstructor` 추가(다른 DTO와 동일 패턴). 사용자가 직접 반영 예정.
- [x] 2. **20260909 확인** 위 1번 수정(`OrderUpdateDTO`에 `@NoArgsConstructor` 추가) 반영 완료. `./gradlew test --tests "com.shopping_mall_api.controller.*"` 재실행해 컨트롤러 테스트 25개 전부 통과 확인.

### 구현 기능 관련 문제점
- [ ] 1. **20260908 (컨벤션 확정)** 위 디버깅 1번을 근거로, 빌더/생성자 컨벤션에 "요청 DTO는 `@NoArgsConstructor` 필수(Jackson 역직렬화 경로 확보), `@Builder`는 테스트 편의용" 규칙을 추가. 전체 컨벤션 정립 + `@Builder` 배치 전수 점검은 본격 리팩터링 페이즈(테스트 코드 + CI/CD + 트래픽 테스트 도구 의존성 확립 이후)로 유지 — 상세는 `[20260819~20260825]` "장기 로드맵 참고"의 빌더 컨벤션 항목(20260908 갱신) 참조.
- [ ] 2. **20260909 컨트롤러 테스트 리뷰 — happy-path 편향 (중대)** 25개 테스트가 전부 `*_successTest`. 부재: (a) 서비스가 `NotFoundException`/`PaymentException` throw 시 `@RestControllerAdvice`(`GlobalExceptionHandler`)가 `errorCode.getHttpStatus()`+에러 바디로 매핑하는지 — 컨트롤러 레이어에서 가장 가치 있는 검증인데 0개, (b) `@Valid` 위반 → `MethodArgumentNotValidException` 핸들러 → 400, (c) 미인증 401 / non-ADMIN 403. 컨트롤러당 최소 (a) 1개씩은 추가 권장.
- [ ] 3. **20260909 컨트롤러 테스트 리뷰 — 인가 검증 전무** 5개 테스트 클래스 전부 `@AutoConfigureMockMvc(addFilters = false)` + `@Import(SecurityConfig.class)` 없음. `[20260826~20260901]` 7.1 계획(`@Import(SecurityConfig.class)` + `SecurityMockMvcRequestPostProcessors`)이 미이행 → 알려진 `SecurityConfig` 갭(`/products/**` CUD 무인증, `GET /users` 무인증 — `[20260826~20260901]` 구현 기능 문제점 6번)에 실행 가능한 회귀 테스트가 없음. `UserController`에 `// 관리자 권한만` 주석이 달린 `getUsers`/`deleteUser`도 미검증.
- [ ] 4. **20260909 컨트롤러 테스트 리뷰 — 자잘한 결함**
	1. `ProductControllerTest.getProduct_successTest`: `getProduct`는 `@PathVariable`만 받는데 `UsernamePasswordAuthenticationToken(productId, null, null)`(authorities `null`)을 만들어 `SecurityContextHolder`에 세팅. 읽히지 않는 죽은 코드 + `getAuthorities()` null로 NPE 소지. 제거.
	2. `any(Long.class)`/`any(XxxDTO.class)` 남발 → `@AuthenticationPrincipal userId`·`@PathVariable`가 서비스에 제대로 전달되는지 미검증(컨트롤러가 `null`을 넘기거나 path var를 바꿔도 통과). `verify(service).method(eq(1L), eq(2L), ...)`로 바꾸고 userId≠orderId≠productId처럼 **서로 다른 값** 사용. `CartControllerTest`는 일부에서 `eq(userId)`를 이미 씀(일관성 없음).
	3. `SecurityContext` 셋업 방식이 파일마다 3가지 혼재: 원시 `setAuthentication`만(`Order`/`Product`), 원시+try-finally clear(`Cart`/`Auth`/`User` 일부), 원시+`.with(authentication())` 중복(`UserControllerTest.deleteUser`). 격리는 `WithSecurityContextTestExecutionListener`가 이미 보장하므로(20260908 확인) 정합성 문제. `.with(authentication(auth))` 하나로 통일 권장.
	4. `UserControllerTest.getUser_successTest`: `.andExpect(status().isOk())` 누락(다른 테스트엔 전부 있음).
	5. 매직값이 오독 유발: `AuthControllerTest`의 `maxAge(Duration.ofMillis(2026090301L))`(날짜꼴 숫자 + `maxAge` 미단언), `CartControllerTest`의 `.productId(userId)`/`.quantity(20260907L)`, `.build();;`(더블 세미콜론).
- [ ] 5. **20260909 컨트롤러 코드 자체 이슈 (테스트 아님, 사용자 직접 수정)**
	1. `CartController.addCartItemInCart`의 `@RequestBody CartItemCreateDTO`에 `@Valid` 없음(같은 컨트롤러 `patchCart`엔 있음). 장바구니 담기 요청의 Bean Validation이 조용히 스킵됨.
	2. `SecurityConfig` 갭(`/products/**` CUD → `hasRole("ADMIN")`, `GET /users` → ADMIN) 여전히 미수정. `OrderController.deleteOrder`는 `userId` 파라미터 자체가 없어 소유권 검증 불가(`[20260826~20260901]` 7.6에서 이미 지적).
- [ ] 6. **20260909 주간 리뷰 — 트러블 슈팅 일지 학습 내용 정정** (`[20260902~20260908]` 블록)
	1. item 1 (`throws` vs `throw new`): "메서드 내부에서 고의로 예외 객체를 생성하면 선언부에 `throws`를 안 써도 된다"는 **틀림**. `throws` 필요 여부는 **checked/unchecked**만으로 결정. `throw new NotFoundException(...)`에 `throws`가 불필요한 건 `RuntimeException` 하위(unchecked)라서지 "고의 생성" 때문이 아님. `throw new IOException(...)`은 메서드 안에서 만들어도 `throws`가 강제됨. `throws`와 `throw`는 대체재가 아니라 별개(선언 절 vs 발생 문). 테스트 메서드의 `throws Exception`은 `mockMvc.perform(...)`가 checked `Exception`을 선언하기 때문이고 서비스의 `throw new`와 무관. 실제 메커니즘은 커스텀 예외가 전부 `RuntimeException`이라 콜스택을 타고 올라가 `@RestControllerAdvice`가 잡는 것.
	2. item 3: 오타 `@ExtentWith` → `@ExtendWith`. "Controller에 한해서만 Mockito로 설정"은 부정확 — 컨트롤러는 실제 빈으로 스프링이 생성, 목이 되는 건 그 아래 `Service`뿐.
	3. item 4: "스레드 배정 시점에 context 상자를 동시에 할당"은 부정확. `SecurityContext`는 필터가 만들고 채움(`SecurityContextHolderFilter` → `JwtAuthenticationFilter`), `ThreadLocal` 저장소는 항상 존재하며 "요청마다 할당"되는 게 아님. "MappingHandler" → `HandlerMapping`. "5. 기능이 스레드 하나에 할당됨" → business logic만 별도 배정이 아니라 필터~디스패처~컨트롤러~서비스 전체가 워커 스레드 하나의 콜 스택.
	4. item 5: "MODE_THREAD" → `MODE_THREADLOCAL`. "clear 안 하면 CI에서 다른 테스트로 샌다"는 `@WebMvcTest`에선 성립 안 함 — `spring-security-test`의 `WithSecurityContextTestExecutionListener.afterTestMethod`가 모든 테스트 메서드 뒤에 무조건 `clearContext()` 호출(바이트코드 확인). 수동 clear는 격리 목적으론 중복. 실제 누수는 TestContext 없는 순수 단위테스트에서 `SecurityContextHolder` 직접 조작 시로 한정. CI 특정 문제 아님(원인=Gradle 워커 스레드 재사용). "mock session" 용어도 부정확(세션 아님, `SecurityContext`/`Authentication`).
	5. item 2·6은 대체로 정확. item 6에 이번 `OrderUpdateDTO` 실패(단일 인자 `@AllArgsConstructor` → delegating creator → `InvalidDefinitionException`)를 사례로 넣으면 완결.

### 다음 한 주 동안 개발할 기능
- [ ] 1. **(최우선, 이월)** Docker & Kubernetes 학습 + `[20260826~20260901]` 미완성 CI/CD job("Docker build & push(Docker Hub) → EC2 배포") 실제 완성. 이번 주(`[20260902~20260908]`) 목표였으나 미착수 → 이월.
- [ ] 2. 컨트롤러 테스트 보강(1번과 병행 가능): 예외 매핑 테스트(컨트롤러당 1+), `@Valid` 실패 400 테스트, `@Import(SecurityConfig.class)`+`addFilters=true`로 미인증 401·non-ADMIN 403 테스트(알려진 `SecurityConfig` 갭 회귀), `SecurityContext` 셋업 `.with(authentication(...))`로 통일, `any()` → `eq()`/`ArgumentCaptor`+`verify`. 상세 위 구현 기능 문제점 2~4번.
- [ ] 3. `SecurityConfig` 갭 수정(사용자 직접): `/products/**` CUD·`GET /users` → ADMIN, `CartController.addCartItemInCart`에 `@Valid` 추가. 상세 위 구현 기능 문제점 5번.
- [ ] 4. 위 1번(CI/CD 파이프라인) 완료 후 로드맵 다음 단계인 "상품 수량 로직"(재고 차감/복구 트랜잭션 + 주문 가격 서버 재조회) 착수 준비.

[20260909 ~ 20260915]

### 이번주 구현 목표
- [ ] 1. 컨트롤러 예외 테스트 절반 분량 작성(대략 2~3개 컨트롤러) — 서비스가 `NotFoundException` 등 throw 시 `GlobalExceptionHandler` 매핑 검증(status/에러 바디) + `@Valid` 위반 → 400 테스트. 나머지 절반은 다음 주. 근거: `[20260902~20260908]` 구현 기능 문제점 2번.
- [ ] 2. **(확정, 20260909)** Docker & Kubernetes 공부 착수 — 학기 시작으로 주당 가용 시간이 방학 대비 축소된 점을 반영해, "구현 완성"이 아니라 "이번 주 안에 반드시 학습을 시작"하는 것으로 목표를 하향 조정(사용자 확정). CI/CD job 실제 완성(Docker build & push → EC2 배포)은 학습이 어느 정도 된 이후로 이월.

### 컴파일 및 디버깅 관련 문제
- 없음 (이번 주 진행하며 갱신).

### 구현 기능 관련 문제점
- [ ] 1. **20260909 스케줄 조정(사용자 확정)** 학기 시작으로 주당 가용 개발 시간이 방학 대비 축소됨(사용자 언급). 이에 맞춰 이번 주 범위를 "컨트롤러 예외 테스트 절반 + Docker/K8s 학습 착수"로 축소. 무리한 범위보다 완주 가능한 범위를 우선. 로드맵 순서(테스트 → CI/CD 완성 → 상품 수량 로직 → SQL 튜닝)는 유지하되 각 단계 소요 기간을 늘려 잡음.

### 다음 한 주 동안 개발할 기능
- [ ] 1. 컨트롤러 예외 테스트 나머지 절반 + 인가 테스트(미인증 401 / non-ADMIN 403, `@Import(SecurityConfig.class)` + `addFilters=true`), `SecurityContext` 셋업 `.with(authentication(...))` 통일, `any()` → `eq()`/`verify`.
- [ ] 2. `SecurityConfig` 갭 수정(사용자 직접): `/products/**` CUD·`GET /users` → ADMIN, `CartController.addCartItemInCart`에 `@Valid` 추가.
- [ ] 3. Docker/K8s 학습 진척에 따라 CI/CD job "Docker build & push(Docker Hub) → EC2 배포" 완성.
- [ ] 4. 그 뒤 로드맵: "상품 수량 로직"(재고 차감/복구 트랜잭션 + 주문 가격 서버 재조회).

---

[20260916 ~ 20260922]

### 이번주 구현 목표
- [ ] 1. 컨트롤러 예외/인가 테스트 마무리(이월, `[20260909~20260915]` 미완료 — 예외 매핑 테스트, `@Valid` 400, 미인증 401/non-ADMIN 403).
- [ ] 2. **(신규, 20260917 사용자 확정)** 위 1번 완료 즉시 JWT 로그인/로그아웃 인증 방식 심화(기능 추가 단계)로 전환.

### 컴파일 및 디버깅 관련 문제
- 없음 (이번 주 진행하며 갱신).

### 구현 기능 관련 문제점
- [ ] 1. **(스케줄 조정, 사용자 확정 20260917)** 기존 로드맵 순서(테스트 코드 완료 → Docker/K8s 학습 → CI/CD 파이프라인 "Docker build & push → EC2 배포" 완성 → 상품 수량 로직)에서 **CD(Docker/K8s 포함 배포 자동화) 단계를 현 단계에서 제외**. 근거: 현직 백엔드 개발자 조언(20260916) — 여러 기술을 얕게 아는 것보다 핵심 도메인(인증/보안 등) 하나를 깊게 파는 것이 실무 성장에 유리하다는 취지. 테스트 코드 마무리 후 곧바로 JWT 로그인/로그아웃 인증 방식 심화로 전환하기로 함. CD 자체를 영구 폐기하는 것은 아니며, 최종 "Deploy" 단계에서 재도입 예정(로드맵 순서 변경, 삭제 아님).
- [ ] 2. **(Copilot 지적, 20260917)** 기존에 "post-CI/CD"로 미뤄뒀던 두 항목이 이번 JWT 심화 단계와 직접 연관됨을 확인 필요: ① Redis 기반 access token 블랙리스트(로그아웃 시 즉시 무효화), ② `AuthController.logOut`이 Redis 리프레시 토큰 항목만 삭제하고 `accessToken`/`refreshToken` 쿠키를 `Set-Cookie`로 실제 만료시키지 않는 버그(`logIn`과 달리 반환 타입이 `void`라 헤더 자체를 못 붙임). CD가 뒤로 밀리고 JWT 심화가 다음 단계가 되었으므로, 이 두 항목을 "CD 이후"가 아니라 이번 JWT 심화 단계 범위에 포함할지 사용자 확인이 필요함(현재는 재분류하지 않고 보류 상태 유지 — JWT 심화 착수 시점에 범위 재확정).
- [ ] 3. **(용어 정정, 20260917)** `[20260909~20260915]` 블록 구현 기능 문제점 2번에서 "컨트롤러 테스트에 예외 처리 테스트가 없다"고 지적했던 표현이 "컨트롤러가 예외를 던져야 한다"는 뜻으로 오해될 수 있어 정정. 정확한 의미: 예외는 그대로 서비스 레이어에서 던지는 것이 맞고, 컨트롤러 테스트(`@WebMvcTest`)에서는 `@MockBean` 처리된 서비스가 `thenThrow(...)`로 예외를 던지는 상황을 재현한 뒤, 그 예외가 컨트롤러 콜스택을 빠져나가 `@RestControllerAdvice`(`GlobalExceptionHandler`)까지 전파되어 올바른 HTTP 상태코드+에러 바디로 매핑되는지를 검증해야 한다는 뜻. 이 매핑 로직 자체가 컨트롤러 계층(Spring MVC) 컴포넌트라서 서비스 단위 테스트(`assertThrows`)만으로는 커버되지 않음.

### 다음 한 주 동안 개발할 기능
- [ ] 1. 컨트롤러 예외/인가 테스트 마무리(이월).
- [ ] 2. 테스트 코드 마무리 후 JWT 로그인/로그아웃 인증 방식 심화 착수 — 구체 범위(access token 블랙리스트·로그아웃 쿠키 삭제 버그 포함 여부 등)는 착수 시점에 사용자와 재확정.
- [ ] 3. Docker/Kubernetes 학습 및 CI/CD 배포 자동화는 보류 — 추후 "Deploy" 단계에서 재도입.
---

[20260923 ~ 20260929]

### 이번주 구현 목표
- [/] 1. 컨트롤러 예외/인가 테스트 마무리(`[20260916~20260922]` 이월) — **20260929 확인**: 맥미니 저장소 기준 모든 브랜치(GitHub 원격과 동일)에서 `*ControllerTest.java`가 4줄짜리 빈 클래스. `[20260902~20260908]`에서 통과 확인한 컨트롤러 테스트 25개와 `OrderUpdateDTO` `@NoArgsConstructor` 수정이 **다른 컴퓨터에 커밋/푸시되지 않은 채 남아 있음**(사용자 확인). 이번 주 신규 진척은 확인 불가 → `[20260930~20261006]` Phase 0에서 회수 후 Phase 2에서 마무리.
- [x] 2. **(신규, 20260929)** 맥미니 로컬 개발 환경 구성: Colima 0.10.3 + Docker Compose 5.5.1 설치, `docker-compose.yml`에 `redis` 서비스 추가(`backend`에 `depends_on: redis`, `SPRING_DATA_REDIS_HOST=redis`), `docker compose up -d db redis` 후 MySQL(`mysqld is alive`, `mall_db` 생성)·Redis(`PONG`) 동작 확인, 프론트 `npm ci` 완료. 사용자 요청으로 Copilot이 직접 적용(브랜치 `fix/env`, 미커밋).
- [x] 3. **(신규, 20260929)** 전체 작업 백로그 정리 및 주 단위 페이즈 플랜 확정(사용자 승인) — 상세는 `[20260930~20261006]` 블록.

### 컴파일 및 디버깅 관련 문제
- [x] 1. **20260929** `docker compose up -d db redis` → `unknown shorthand flag: 'd' in -d`. 원인: Homebrew `docker` formula는 CLI만 설치됨. compose 플러그인이 없어 `compose`를 하위 명령으로 인식하지 못하고 `-d`가 docker 본체 옵션으로 파싱됨. 컨테이너 엔진(daemon)도 없음(`/var/run/docker.sock` 연결 실패). 해결: `brew install colima docker-compose` → `~/.docker/config.json`에 `cliPluginsExtraDirs: ["/opt/homebrew/lib/docker/cli-plugins"]` 등록 → `colima start --cpu 2 --memory 4`. 재부팅 후에는 `colima start`를 다시 실행해야 함(자동 시작은 `brew services start colima`, 미적용).
- [x] 2. **20260929** `npm run dev` → `ENOENT ... /Users/potatostore/ShoppingMall/package.json`. 원인: 저장소 루트에서 실행함(`package.json`은 `frontend/shopping-mall-web/`에 있음) + `node_modules` 미설치. 해결: 해당 디렉터리에서 `npm ci`. 참고: npm 11 `allowScripts` 정책으로 `sharp`/`unrs-resolver` install script가 스킵됨(arm64 `sharp` 바이너리는 설치돼 있어 현재 영향 없음).
- [ ] 3. **20260929** `Port 3000 is in use` + `Unable to acquire lock at .next/dev/lock`. 원인: 이전 `npm run dev`를 Ctrl+C가 아니라 **Ctrl+Z(일시정지)**로 멈춤 → `npm`/`next dev`/`next-server` 3개 프로세스가 `STAT T`(Stopped) 상태로 포트와 lock 파일을 계속 점유. 해결: 원래 터미널에서 `fg` 후 Ctrl+C(권장), 또는 `pkill -9 -f "next dev|next-server"`(lock이 남으면 `rm .next/dev/lock`). 3001번으로 뜨면 백엔드 `@CrossOrigin("http://localhost:3000")` 때문에 CORS 실패하므로 반드시 3000번 사용.
- [ ] 4. **20260929 (빌드 실패 예정)** `build.gradle`(fix/env, 미커밋)의 `org.flywaydb:flyway-database-mysql`는 Spring Boot 3.3.11 BOM(`spring-boot-dependencies`)에 없는 아티팩트 → 버전 미지정으로 의존성 해석 실패. 올바른 아티팩트는 `org.flywaydb:flyway-mysql`(Flyway 10부터 MySQL 지원이 `flyway-core`에서 분리됨).
- [ ] 5. **20260929 (기동 실패 예정)** Flyway를 classpath에 올린 채 V1 스크립트 없이 Hibernate가 이미 테이블을 만든 DB에 붙으면 "non-empty schema without schema history table"로 앱 기동 실패. V1 작성 전까지 `spring.flyway.enabled: false` 필요.

### 구현 기능 관련 문제점
- [ ] 1. **(치명, 20260929)** 위 이번주 구현 목표 1번 — 컨트롤러 테스트 25개와 `OrderUpdateDTO` 수정이 다른 컴퓨터에만 존재. 방치 시 유실 위험. Phase 0 최우선.
- [ ] 2. **(20260929) 컴퓨터마다 DB가 달라 목데이터 공유 불가** — 결론: 공유 DB(클라우드·Tailscale)가 아니라 seed as code. Flyway로 스키마를 `db/migration/V__`에서 버전 관리하고, 목데이터는 `db/seed/R__`(반복 실행 파일, idempotent)로 분리해 local 프로파일에서만 실행. 근거: ① 목데이터를 `V__`에 넣으면 운영 DB에도 적용됨, ② `V__`는 적용 후 수정하면 checksum 불일치로 기동 실패, ③ `ddl-auto: update` 상태에서 여러 컴퓨터가 DB 하나를 공유하면 브랜치별 스키마 충돌 발생. MySQL `docker-entrypoint-initdb.d`는 Hibernate가 테이블을 만들기 전에 실행되므로 현 구조에서 사용 불가.
- [ ] 3. **(20260929) Redis 캐싱 대상 결정** — P0: `ProductService.getProduct(id)`(`@Cacheable` + patch/put/delete 시 `@CacheEvict`, TTL 30분). P1: 페이지네이션 도입 후 상품 목록, access token 블랙리스트. P2: 최근 본 상품(List), 최근 검색어·랭킹(Sorted Set). 캐싱 제외: Order/Payment/Cart/User. 적용 시 주의: ① 기본 JDK 직렬화는 DTO에 `Serializable` 필요, `GenericJackson2JsonRedisSerializer`는 `.toList()` 결과(`ImmutableCollections$ListN`) 역직렬화 불가 → 캐시별 `Jackson2JsonRedisSerializer` 사용, ② `transactionAware()`로 evict를 커밋 이후로, ③ `LoggingCacheErrorHandler` + `spring.data.redis.timeout: 500ms`(기본 60초) 없으면 Redis 장애 시 API 전체 장애, ④ `@CachePut` 대신 `@CacheEvict`(아래 4번 버그 때문에 반환 DTO를 신뢰할 수 없음).
- [ ] 4. **(20260929) `Product.patchProduct`/`putProduct` 상세 목록 교체 버그** — 새 `ProductDetail`에 `assignProduct(this)` 미호출로 `product_id`가 null로 저장될 수 있음. `putProduct`는 `orphanRemoval = true` 컬렉션을 불변 `toList()`로 통째로 교체해 Hibernate 예외 가능.
- [ ] 5. **(20260929) Refresh Token 저장 이유 정리 + 관련 결함** — 저장 목적은 무효화(로그아웃, 탈취 대응, 비밀번호 변경 시 전체 세션 종료, rotation 재사용 탐지). stateless refresh면 7일짜리 access token과 보안상 동일. 현재 결함: ① **재발급 API 부재** — `RefreshTokenRepository.matches()` 호출처 0개, 저장만 하고 미사용, 그래서 access token 만료를 7일로 늘려 버티는 구조, ② `logOut`이 쿠키를 만료시키지 않음(기존 지적 재확인), ③ 키가 `refresh-token:{userId}` 하나라 단일 디바이스 정책(의도 여부 결정 필요).
- [ ] 6. **(20260929)** `frontend/shopping-mall-web/src/lib/api.ts`의 `process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080/api/v1"` — compose가 미설정 변수를 빈 문자열로 주입하는데 `??`는 빈 문자열이면 기본값으로 대체하지 않음 → `CLIENT_API_URL = ""` → 요청이 `:3000`으로 가서 404. `||`로 변경 필요. (참고: EC2 IP는 코드에 없고 git 미추적 `.env`에만 있었음 → 로컬 전환에 코드 변경 불필요)
- [ ] 7. **(20260929)** 테스트 소스 `src/test/.../controller/ProductController.java`가 main의 `ProductController`와 FQN이 동일 → `ProductControllerTest`로 이름 변경 필요.
- [ ] 8. **(스케줄 조정, 사용자 확정 20260929)** ① `[20260916~20260922]`에서 확정한 "테스트 → JWT 심화" 순서를 **"테스트 → Flyway 스키마 → 목데이터 → JWT 심화"**로 변경(근거: 로드맵 현재 단계가 "데이터 스키마 작성"이고, JWT 심화는 스키마 변경이 없어 뒤로 가도 충돌 없음). ② 컨트롤러 테스트(예외 매핑·`@Valid` 400·인가 401/403·품질 정리)는 **전부 완료 후** 다음 단계로 진행. ③ 주당 가용 시간 5~10시간 → 1주 = 1페이즈. ④ CD(Docker/K8s)는 계속 Deploy 단계로 보류.

### 다음 한 주 동안 개발할 기능
- [ ] 1. `[20260930~20261006]` 블록의 Phase 0 참조.

---

[20260930 ~ 20261006]

### 이번주 구현 목표
- [ ] 1. **(Phase 0, 최우선)** 다른 컴퓨터에서 `git status`/`git stash list` 확인 → 컨트롤러 테스트 25개 + `OrderUpdateDTO` 수정을 브랜치로 커밋·푸시 → 맥미니에서 `./gradlew test` 전체 통과 확인(Copilot 검증).
- [ ] 2. `build.gradle`의 `flyway-database-mysql` → `flyway-mysql`, `application.yml`에 `spring.flyway.enabled: false`(Phase 3에서 켬).
- [ ] 3. `api.ts`의 `??` → `||`, 테스트 파일명 `ProductController` → `ProductControllerTest`.
- [ ] 4. `fix/env` 커밋(redis compose + 위 2·3번) → PR → CI `build-and-test` 통과 → main 머지.
- [ ] 5. 로컬 E2E 완주: IntelliJ Run Configuration에 `JWT_SECRET_KEY`(`openssl rand -base64 32`)·`TOSS_SECRET_KEY`(프론트 `test_ck_...`와 같은 상점의 `test_sk_...`) 설정 → `npm run dev`(3000번) → Chrome `http://localhost:3000`에서 회원가입 → 로그인 → 상품 등록·수정 → 장바구니 → 주문 → 토스 결제. 실패 지점을 목록으로 남김(Phase 1 입력값).
- [ ] 6. (신규, 20260930 사용자 확정) 기기별 브랜치 분담: 같은 기능을 두 기기에서 번갈아 고치면 diff 파일을 주고받아야 해서, 기기마다 기능과 브랜치를 하나씩 맡기로 함. 맥북 = 컨트롤러 테스트(config/test, Phase 2를 이번 주로 앞당겨 착수), 맥미니 = 환경·Flyway·E2E(fix/env). 맥북 잔여 작업: ① UserControllerTest 컴파일 오류 수정 후 WIP 커밋·푸시(Phase 0 회수 겸함), ② 예외 매핑 테스트 컨트롤러당 1개 이상(Auth는 완료, Cart·Order·Product·User 남음), ③ @Valid 400 테스트(User 작성 중, Cart addCartItemInCart는 컨트롤러에 @Valid가 없어 실패 재현용으로 먼저 작성), ④ 인가 테스트 401/403(기존 클래스와 분리해 필터 활성화), ⑤ SecurityContext 셋업을 .with(authentication(...))로 통일, any() → eq()/verify, 매직값 정리.
- [ ] 7. (신규, 20260930 사용자 확정) Git 작업 방식: 작업 중에는 기기별 브랜치에 WIP 커밋·푸시를 반복(브랜치 전환·main 병합 전 작업 트리 비우기, 백업, 기기 간 이어받기 목적). 작업 완료 시 main 병합 → 테스트 → PR → CI·GitGuardian 통과 → Squash and merge(첫 squash 시 Copilot과 함께 진행). 병합 직후 새 커밋 없이 git reset --hard origin/main + git push --force-with-lease로 브랜치 초기화 후 같은 브랜치 재사용. main ruleset(Merging after CI Rule)은 main에만 적용돼 config/test 강제 푸시 가능 확인.
- 종료 조건: 맥미니에서 `./gradlew test` 전체 통과(컨트롤러 25개 포함) + E2E 결과 목록 확보.

### 컴파일 및 디버깅 관련 문제
- [x] 1. 20260930 PR #19(fix/env) CI 실패: compileJava 단계에서 "Could not find org.flywaydb:flyway-database-mysql:." 발생. 원인: Spring Boot 3.3.11 BOM(spring-boot-dependencies)은 flyway.version=10.10.0 기준으로 flyway-mysql만 관리하고 flyway-database-mysql은 관리 목록에 없음 → 버전이 비어 있는 좌표로 해석 실패(에러 메시지 끝의 "mysql:." 콜론 뒤가 비어 있는 것이 버전 미지정의 표시). Maven Central에도 flyway-database-mysql은 존재하지 않음(404), flyway-mysql 10.10.0은 존재. [20260923 ~ 20260929] 블록 컴파일 4번에서 예고한 실패와 동일.
- [x] 2. 20260930 수정 현황(같은 날 CI 재실행 통과 확인, run 36657314511 success): GitHub Copilot 클라우드 에이전트가 PR #19에 da79f6f 커밋으로 runtimeOnly 'org.flywaydb:flyway-mysql' 적용(검토 결과 올바름. MySQL 모듈은 ServiceLoader로 런타임에만 로드되므로 runtimeOnly가 적절). 단, 봇이 푸시한 커밋이라 CI-CD 워크플로가 action_required(승인 대기) 상태로 아직 실행되지 않음 → PR 화면에서 승인 후 재실행하고 통과 확인 필요. 에이전트 작업이 진행 중이므로 끝난 뒤 fix/env를 받아올 것.
- [ ] 3. 20260930 (CI 통과 후에도 남는 리스크) CI 테스트는 test/resources의 H2 메모리 DB(빈 스키마)를 쓰므로 통과하지만, 로컬 bootRun은 기존 테이블이 있는 mall_db에 붙으면서 "Found non-empty schema(s) but no schema history table"로 기동 실패 예상. 이번 주 구현 목표 2번의 main application.yml spring.flyway.enabled: false를 같은 PR에 포함할 것.
- [ ] 4. 20260930 fbdc1d1 커밋 작성자 이메일이 a0105775135976@gamil.com(gmail 오타). 맥미니 git config user.email 수정 필요(GitHub 계정과 커밋이 연결되지 않음).
- [ ] 5. 20260930 맥북 ./gradlew test 컴파일 실패: UserControllerTest.java 94행 String body = "" 뒤 세미콜론 누락(작성 중인 createUser_inValidTest). 테스트 소스 전체가 컴파일되지 않아 나머지 테스트도 실행 불가. 같은 메서드에 throws Exception이 없어 mockMvc.perform 호출 시 checked exception 컴파일 오류가 이어서 날 예정.
- [ ] 6. 20260930 main 머지 후 config/test에서 pull해도 build.gradle에 flyway가 안 들어온 원인: git pull은 현재 브랜치의 upstream(origin/config/test)만 fetch + merge하므로 main 변경분은 들어오지 않음(origin/main에만 있는 커밋 7개, main이 config/test의 조상 아님 확인). main 반영은 config/test에서 git merge origin/main(IntelliJ: 브랜치 팝업 → main → Merge 'main' into 'config/test')으로 해야 함. 부작용: 미커밋 상태로 IntelliJ Smart Checkout/Update를 반복하는 과정에서 build.gradle의 testImplementation 'org.springframework.security:spring-security-test' 줄이 작업 트리에서 사라짐(unshelve 시 main의 flyway 줄과 같은 위치에서 충돌). 원본은 backend/.idea/shelf/Uncommitted_changes_before_Update_at_2026__9__30__11_09에 보존, 나머지 31개 파일은 유실 없음(대조 확인). UserControllerTest가 authentication()을 쓰므로 해당 줄 복구 필요. 재발 방지: 브랜치 전환·main 병합 전에 WIP 커밋으로 작업 트리를 비울 것.

### 구현 기능 관련 문제점
- [ ] 1. 20260930 Phase 0 위치 확인: 미푸시 컨트롤러 테스트는 맥북(potatostoreMacbook) config/test 브랜치 작업 트리에 있음. 컨트롤러 테스트 5개 파일(@Test 30개), ProductController → ProductControllerTest 이름 변경(이번 주 구현 목표 3번의 백엔드 부분), JpaAuditingConfig 신규, build.gradle에 spring-security-test 추가 등이 전부 미커밋. 맥북에서 먼저 커밋·푸시해야 함.
- [ ] 2. 20260930 머지 충돌 예상: 맥북 build.gradle(spring-security-test 추가)과 fix/env build.gradle(flyway 추가)이 둘 다 spring-boot-starter-data-redis 바로 아래 줄에 삽입 → 두 브랜치를 합칠 때 build.gradle 충돌 발생. 두 줄 모두 살리는 방향으로 해결.
- [/] 3. 20260930 (기기 분담 시 최대 리스크, 같은 날 사용자 요청으로 Copilot이 적용·미커밋: ApiURLNames를 GET /users, GET·PATCH·DELETE /users/me, GET·PATCH·DELETE /carts/me, DELETE /carts/items/{productId}로 변경 + 프론트 orders/page.tsx /orders/user/me → /orders/me. compileJava 통과, 프론트 호출 12곳 전부 백엔드 경로와 일치 확인. 커밋·PR·CI 통과 후 [x]) 프론트-백엔드 URL 계약 불일치: 맥북 ApiURLNames 변경분(/users/find/me, /users/update/me, /carts/update/me, /carts/delete/cart/item/me/{productId}, /orders/me)이 프론트 호출(GET·PATCH /users/me, PATCH /carts/me, DELETE /carts/items/{id}, GET /orders/user/me)과 5곳에서 불일치. 기존 main 값(/users/{userId} 등)도 프론트의 "me"를 Long으로 변환하지 못해 400이므로 맥미니 E2E에서도 실패 예정. 컨트롤러 테스트는 ApiURLNames 상수를 그대로 참조하므로 URL이 바뀌어도 통과해 이 불일치를 잡지 못함. 수정 제안(최소 변경, 현업 관례): URL에 동사(find/update/delete)를 넣지 않고 HTTP 메서드로 구분 → 백엔드 상수를 /users/me, /carts/me, /carts/items/{productId}로 맞추면 프론트는 /orders/user/me 한 줄만 /orders/me로 수정. URL 계약 변경은 백엔드 상수와 프론트 호출을 같은 PR에서 함께 수정.
- [/] 4. 20260930 (같은 날 사용자 요청으로 Copilot이 이름 일괄 변경·미커밋: 패키지 entity.like → entity.likes, 클래스 Like → Likes, 상수 likeTableName → likesTableName) 맥북 TableNames의 like → likes 변경(MySQL 예약어 회피, 올바른 수정)은 스키마 변경이므로 맥미니 Flyway V1__init_schema.sql 작성(Phase 3) 전에 main에 먼저 머지돼야 함. 같은 맥북 변경분의 @EnableJpaAuditing → JpaAuditingConfig 분리도 @WebMvcTest가 JPA 메타모델 없이 뜨게 하는 올바른 수정.
- [ ] 5. 20260930 인가 테스트 작성 시 확인할 SecurityConfig 현황: ① /products/** 규칙이 없어 CUD가 permitAll로 빠짐(기존 지적 유지), ② /users/find(전체 유저 조회)는 /users/** authenticated에만 걸려 로그인만 하면 누구나 조회 가능(ADMIN 제한 없음), ③ [20260826 ~ 20260901] 블록에서 결정한 /orders/toss/payment/auth permitAll 매처가 현재 SecurityConfig에 없음 → /orders/** authenticated에 걸려 미인증 호출 시 401, ④ 중복 matcher 줄 잔존. 인가 테스트는 기존 테스트 클래스(addFilters = false)를 건드리지 않고 별도 클래스로 @Import(SecurityConfig.class) + JwtProvider @MockBean 구성 권장. 권한 문자열은 JwtAuthenticationFilter와 동일하게 ROLE_ 접두사 사용(기존 테스트의 SimpleGrantedAuthority("USER")는 필터를 꺼서 통과할 뿐 hasRole 검사에는 매칭되지 않음).
- [ ] 6. 20260930 기기 분담 운영 규칙 제안: ① 파일 소유권 — 맥북은 src/main의 controller·dto·security와 src/test, 맥미니는 build.gradle·resources·docker-compose·frontend·entity/Flyway. 상대 영역 수정이 필요하면 작은 PR로 main에 먼저 머지하고 상대 기기는 자기 브랜치에서 git merge origin/main. ② 작업 시작 시 git fetch 후 origin/main 병합, 종료 시 WIP 커밋 푸시(CI는 main push와 main 대상 PR에서만 돌기 때문에 브랜치 푸시만으로는 CI가 실행되지 않음). ③ 머지 순서 — fix/env(CI 통과) 먼저 main 머지 → 맥북 브랜치에 main 병합해 build.gradle 충돌을 한 번에 해결.
- [ ] 7. 20260930 GlobalExceptionHandler의 @ExceptionHandler(Exception.class) catch-all이 Spring MVC 표준 예외까지 500으로 바꿈. 근거: DispatcherServlet의 예외 리졸버 순서상 ExceptionHandlerExceptionResolver(@RestControllerAdvice 처리)가 DefaultHandlerExceptionResolver(표준 예외 → 400/405 등)보다 먼저 실행되고, Exception.class는 모든 예외에 매칭됨. 영향: 깨진 JSON 요청(HttpMessageNotReadableException) → 400이 아니라 500, 지원하지 않는 HTTP 메서드(HttpRequestMethodNotSupportedException) → 405가 아니라 500. 수정 제안(최소 변경): GlobalExceptionHandler가 ResponseEntityExceptionHandler를 상속하거나 HttpMessageNotReadableException 등 필요한 표준 예외 핸들러를 추가. 컨트롤러 테스트에서 깨진 JSON 요청 1건으로 먼저 재현 권장. (사용자 질문 "예외는 서비스가 던지는데 왜 컨트롤러 테스트에서 오류 케이스를 검증하나" 재설명 중 발견. 개념 정리는 [20260916 ~ 20260922] 블록 용어 정정 항목과 동일)
	1. (20260930 보완, 사용자 질문 "표준 예외를 전부 개별 처리해야 하나, catch-all을 지워야 하나") 결론: 둘 다 아님. catch-all을 지우면 상태코드는 맞아지지만 표준 예외 응답이 Spring Boot 기본 /error JSON(timestamp·status·error·path)으로 나가 ApiResponse와 형식이 둘로 갈라지고, 진짜 버그(NPE·DB 장애)도 같은 기본 형식으로 나가 공통 로그·형식 통제를 잃음. 개별 처리는 Spring 6.1.19 기준 표준 예외가 20종이라 누락 위험. 권장(현업 정석): GlobalExceptionHandler가 ResponseEntityExceptionHandler를 상속(20종 표준 예외를 올바른 4xx/5xx로 이미 매핑, spring-webmvc 6.1.19 jar로 목록 확인) + handleExceptionInternal 1개 오버라이드로 바디만 ApiResponse.error 형식으로 통일 + 기존 MethodArgumentNotValidException 핸들러는 handleMethodArgumentNotValid 오버라이드로 이동(중복 시 Ambiguous @ExceptionHandler 기동 실패) + GlobalShoppingMallException·Exception.class 핸들러는 유지(Exception.class는 진짜 예상 못 한 버그만 500 + log.error). 주의: 표준 예외의 getMessage()는 JSON 파싱 내부 정보가 담길 수 있어 응답 메시지로 그대로 내보내지 말 것. 직전 제안(개별 핸들러 추가)은 HttpMessageNotReadableException 한 건 기준의 최소 변경이었고, 표준 예외 전체로 범위가 넓어져 상속 방식으로 정정.

### 다음 한 주 동안 개발할 기능
- [ ] 1. **Phase 1 (20261007~20261013) 버그 수정 + 회귀 테스트**: ① `SecurityConfig` 갭(`/products/**` CUD·`GET /users` → ADMIN, 중복 matcher 줄 제거) — 인가 테스트(401/403, `@Import(SecurityConfig.class)`, `addFilters=true`)를 먼저 작성해 실패 재현 후 수정, ② `Product` 상세 목록 교체 버그 — `@DataJpaTest` 회귀 테스트, ③ `CartController.addCartItemInCart`에 `@Valid`, ④ `OrderUpdateDTO`(회수 안 된 경우만), ⑤ Phase 0 E2E 실패 항목. 종료 조건: E2E 상품 수정 단계까지 통과.
- [ ] 2. 이후 확정 로드맵(주차는 진행에 따라 재조정, 순서는 사용자 확정):
	1. **Phase 2 (20261014~20261020)** 컨트롤러 테스트 마무리: 예외 매핑(`thenThrow` → `GlobalExceptionHandler`) 컨트롤러별 1개 이상 + `@Valid` 400, `.with(authentication(...))` 통일, `any()` → `eq()`/`verify`, 매직값 정리. 종료 조건: `[20260902~]`부터 이월된 테스트 항목 전부 `[x]`.
	2. **Phase 3 (20261021~20261027)** Flyway 스키마: V/R·checksum·baseline·validate 학습(트러블 슈팅 일지 → Copilot 정확성 검토) → `db/migration/V1__init_schema.sql`(Phase 1 엔티티 수정 이후 기준) + `ddl-auto: validate` + Flyway 활성화, 테스트 프로파일은 `spring.flyway.enabled: false` 유지(H2 + `create-drop`), 로컬 DB 초기화 후 기동 확인.
	3. **Phase 4 (20261028~20261103)** 목데이터: `db/seed/R__seed_mock_data.sql`(고정 ID + `ON DUPLICATE KEY UPDATE`, 테스트 계정은 미리 만든 bcrypt 해시) + `application-local.yml`의 `spring.flyway.locations`에 seed 포함 + `SPRING_PROFILES_ACTIVE=local`. 종료 조건: 맥미니와 다른 컴퓨터 양쪽에서 같은 데이터로 E2E 통과.
	4. **Phase 5 (20261104~20261117, 2주)** JWT 심화: `POST /auth/reissue` + rotation → access token 30분 원복 → 로그아웃 쿠키 만료 → Redis access token 블랙리스트 → 멀티 디바이스 정책 결정. 각 항목에 테스트 추가.
	5. **Phase 6 이후** Redis `getProduct` 캐시 → 상품 목록 페이지네이션 → 상품 수량 로직 + `deleteOrder` 소유권 → Redis 자료구조 기능 → (Deploy 단계) CD / 모니터링 + 대량 목데이터.
