[20260729 ~ 20260805]
### 컴파일 및 디버깅 관련 문제
- [x] **치명**   CartItem   컴파일 실패:   CartItemResponseDTO   import 누락으로   cannot find symbol   발생 → DTO import 추가 필요.
- [x] **중간** 장바구니 합계 계산 NPE 위험:   isEmpty()  가 null 체크보다 먼저 실행됨 → null 체크를 앞에 두도록 조건 순서 변경 필요.
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

### 다음 한 주 동안 개발할 기능
1. **Global Config 최소 골격 구현**:   ApiResponse<T>  ,   ErrorResponse  ,   ErrorCode  ,   GlobalExceptionHandler  , Validation 에러 매핑을 먼저 고정.
2.  **주문 코어 도메인 구현** :   Order  -  OrderDetail   관계, 주문 상태, 주문 시점 가격/수량 스냅샷 컬럼 도입.
3. **장바구니→주문 전환 API 구현**: CartItem 다건 주문 생성, 총액 검증, 주문 저장 처리.
4. **재고 처리 구현**: 결제 시 재고 차감/취소 시 복구, 동시성 충돌 대응(락/버전 전략).
5. **찜/최근본 정규화 구현**:   Like(userId, productId)   유니크 제약 및   recent_watching(userId, productId, viewedAt)   이력 테이블 추가.
6. **1주차 목표 1(기반 완성)** Global Config(  ApiResponse  ,   ErrorResponse  ,   ErrorCode  ,   GlobalExceptionHandler  )와 Validation 에러 매핑을 먼저 고정.
7. **1주차 목표 2(주문 코어 완성)**   Order  /  OrderDetail   리팩터링과 장바구니→주문 전환 API를 연결하고, 총액 검증 규칙을 명시.
8. **1주차 목표 3(재고 정합성 확보)** 결제/취소 재고 처리와 동시성 대응을 구현해 주문 라이프사이클 무결성을 확보.
9. **1주차 목표 4(사용자 기능 정규화)** 찜/최근본 모델을 정규화하고 제약조건(유니크/FK/인덱스)을 적용.
10. **1주차 목표 5(안정화 점검)** 주문 생성·재고 차감·취소 복구·예외 응답 형식까지 포함한 통합 점검 시나리오를 완료.
11. **트랜잭션 경계 적용 5단계**: 1) placeOrder/cancelOrder를 유스케이스 단위 @Transactional 메서드로 고정, 2) 재고 조회 시   PESSIMISTIC_WRITE   또는   SELECT ... FOR UPDATE  로 행 잠금, 3)   qty >= 요청수량   조건부 차감/복구 쿼리로 원자성 보장, 4) 주문 상태 전이(  PENDING→PAID  ,   PAID→CANCELED  )를 화이트리스트 검증, 5) 중간 실패 시 예외 전파로 전체 롤백 보장.
12.   OrderDetailController   라우팅 상수 오타(  orderDetailTableName  )를   orderItemTableName  로 즉시 수정해 컴파일을 먼저 복구.
13.   ErrorResponse   구조를 도입하고   GlobalExceptionHandler  에서   ErrorCode  /Validation 상세 필드를 공통 포맷으로 반환.
14.   OrderService  에   placeOrder  /  cancelOrder   유스케이스를 구현하고 유스케이스 단위   @Transactional   경계를 고정.
15. 재고 차감/복구를 조건부 업데이트 + 락 전략으로 구현해 동시성 충돌 시 음수 재고를 방지.
16.   Like(userId, productId)   유니크 제약 및   recent_watching(userId, productId, viewedAt)   이력 모델을 추가해 사용자 기능 정규화를 완료.
