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
- [ ] 5. 위 1~4번으로 E2E 프론트 기능 완성, 목표 마감 20260825(화, 수요일 시작 기준 이번 주 마지막날). 완료되는 대로 바로 CI/CD + Docker/Kubernetes 착수(다음 항목이 아니라 그 다음 사이클로 이월 가능).
- [ ] 6. UI/UX 스타일링은 1~4번 기능이 다 완성된 뒤로 의도적으로 미룸(사용자 확정, 20260821).

### 장기 로드맵 참고 (특정 주차에 배정된 항목 아님, 순서만 확정 — 20260821 순서 정정: SQL 튜닝이 재고 로직 이전→이후로 이동)
- 웹서버(Next.js) E2E 기능 완료(목표 20260825, 화요일 마감) → GitHub Actions + CI/CD + Docker/Kubernetes → access token 블랙리스트 + 주문 무결성 묶음("추가 기능" 단계, 사용자는 "상품 수량 로직"으로 지칭): (a) 상품 재고 차감/복구 트랜잭션, (b) `OrderService.createOrder` 서버 측 가격 재조회(`productRepository`, 클라이언트 `curOrderItemPrice` 미신뢰), (c) (b) 완료 후 `OrderItemCreateDTO.curOrderItemPrice` 필드 제거 → **그다음 SQL 튜닝** (20260821 기준 최종 순서, 이전엔 SQL 튜닝이 이 묶음보다 앞이었으나 사용자가 언급을 빠뜨렸던 것으로 확인되어 정정)
- 각 단계는 이전 단계 완료가 전제 조건.

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
