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
- [ ] 2. 서비스/컨트롤러 구현 완료(주문/장바구니/재고/결제) 목표는 미달성으로 체크.
- [ ] 3. TossPayments 연동 방식 학습 및 설계 착수 목표는 미달성으로 체크.

### 컴파일 및 디버깅 관련 문제
- [ ] 1. 미구현 서비스/컨트롤러 경로에서 요청 처리 시점 예외(NPE/미지원 동작) 위험이 남아 있음.
- [ ] 2. 결제 승인 전후 주문 상태 전이 검증 로직이 없어 디버깅 시 결제-주문 정합성 추적이 어려움.

### 구현 기능 관련 문제점
- [ ] 1. 주문 관련 핵심 유스케이스(`placeOrder`, `cancelOrder`, 결제 승인 후 상태 반영)가 서비스 계층에 완결되지 않음.
- [ ] 2. TossPayments 승인/취소 API와 내부 `OrderStatus` 매핑 규칙이 정의되지 않아 구현 방향이 불명확함.
- [ ] 3. 결제 성공/실패 콜백(리다이렉트 또는 웹훅) 처리와 멱등성 기준(orderId 중복 승인 방지)이 미정의 상태임.

### 다음 한 주 동안 개발할 기능
- [ ] 1. TossPayments 연동 목표 1: 결제 요청 파라미터(`orderId`, `amount`, `orderName`, 고객 식별자) 생성 규칙과 성공/실패 URL 엔드포인트를 확정.
- [ ] 2. TossPayments 연동 목표 2: 서버 결제 승인 API(`paymentKey`, `orderId`, `amount` 검증 → Toss 승인 호출) 구현.
- [ ] 3. TossPayments 연동 목표 3: 승인 결과를 주문 상태 전이(`PAY_PENDING → PAID / PAY_FAILED`)와 재고 처리 트랜잭션에 연결.
- [ ] 4. TossPayments 연동 목표 4: 중복 승인 방지를 위한 멱등 키/중복 요청 차단 로직 및 실패 재시도 정책 정의.
- [ ] 5. 서비스/컨트롤러 마감 목표: 주문·결제 관련 미구현 Service/Controller 메서드를 우선 완성하고 통합 시나리오로 점검.
