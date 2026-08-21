---
tags:
  - seed
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
- [ ] 5. 위 1~4번으로 E2E 프론트 기능 완성, 목표 마감 20260826 전후. 완료되는 대로 바로 CI/CD + Docker/Kubernetes 착수(다음 항목이 아니라 그 다음 사이클로 이월 가능).
- [ ] 6. UI/UX 스타일링은 1~4번 기능이 다 완성된 뒤로 의도적으로 미룸(사용자 확정, 20260821).

### 장기 로드맵 참고 (특정 주차에 배정된 항목 아님, 순서만 확정 — 20260821 순서 정정: SQL 튜닝이 재고 로직 이전→이후로 이동)
- 웹서버(Next.js) E2E 기능 완료(목표 ~20260826) → GitHub Actions + CI/CD + Docker/Kubernetes → access token 블랙리스트 + 주문 무결성 묶음("추가 기능" 단계, 사용자는 "상품 수량 로직"으로 지칭): (a) 상품 재고 차감/복구 트랜잭션, (b) `OrderService.createOrder` 서버 측 가격 재조회(`productRepository`, 클라이언트 `curOrderItemPrice` 미신뢰), (c) (b) 완료 후 `OrderItemCreateDTO.curOrderItemPrice` 필드 제거 → **그다음 SQL 튜닝** (20260821 기준 최종 순서, 이전엔 SQL 튜닝이 이 묶음보다 앞이었으나 사용자가 언급을 빠뜨렸던 것으로 확인되어 정정)
- 각 단계는 이전 단계 완료가 전제 조건.
