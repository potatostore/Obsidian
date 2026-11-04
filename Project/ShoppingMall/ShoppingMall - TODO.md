---
tags:
  - seed
  - type/project
aliases: []
created: 2026-11-02
---
# ShoppingMall - TODO

- 기준: main 1e1e7f3 (PR 23 머지, 2026-11-02). 백엔드 테스트 133개 통과 (로컬 clean test, GitHub Actions 모두 성공)
- 갱신: 4번 기능 개발 전체를 PR 25(claude/hopeful-mccarthy-6y31xt)로 구현, 테스트 191개 통과. PR 25 머지 후 할 일을 1번에 추가
- 갱신(2026-11-03): PR 25 머지(main db7ba07, 테스트 191개·CI 통과 확인). 타사 쇼핑몰 비교로 7번 "기능 개발 2차" 추가, 1~5번 기능 뼈대를 PR 26으로 올림
- 갱신(2026-11-04): API 명세서를 main 1cb7a0a 기준으로 전체 갱신(1번 항목 2개 완료), copilot-addendum에 20261102 블록 반영. 프론트 잡지형 메인 화면을 PR 29(dev/ui-cntwa2)로 올림, 8번 "프론트 UI" 추가
- 로드맵: Spring Boot + MySQL → CI(테스트 코드) + Web Server → JWT 인증 심화(로그인/로그아웃) → Grafana/Prometheus + Mock Data → Deploy(CD 포함)
- 현재 단계: 컨트롤러 예외/인가 테스트 마무리 → 끝나면 JWT 인증 심화로 전환
- 구성: 작업 성격별로 나눔. 1 바로 할 일(운영·문서) / 2 결정 필요(정해야 진행 가능) / 3 테스트 / 4 기능 개발(완료) / 5 인프라·데이터 / 6 정리 / 7 기능 개발 2차(다음 구현 대상) / 8 프론트 UI
- 우선순위: 높음(돈·데이터 문제) / 중간(기능 결함·사용성) / 낮음(정리). "미확인"은 코드로 추론했고 실행해서 확인하지 않은 항목
- 자세한 근거: GitHub PR 22·23·25·29 설명(변경 사항·변경 이유·검증). 저장소의 docs/claude-work-log/는 PR 26에서 삭제했으므로, 문서 원문이 필요하면 PR 25 머지 커밋(db7ba07) 시점의 파일을 git 이력에서 확인

## 1. 바로 할 일 (운영·문서)

- [ ] 로컬 DB의 orders, order_item 테이블 drop (주문 상태를 숫자 → 문자열로 저장하도록 바꿨는데 ddl-auto update는 기존 컬럼 타입을 바꾸지 않음)
- [ ] 기존 상품에 재고 지정: PATCH /products/{id} 로 stock 입력 (컬럼이 새로 생기면 0 = 품절)
- [ ] ADMIN 계정은 DB에서 role을 ADMIN으로 직접 수정 (회원가입은 항상 USER)
- [ ] application.yml access-token-expiration-ms 를 1800000(30분)으로 원복 (현재 7일)
- [ ] access token 만료를 짧게(60000) 바꿔 재발급(POST /auth/reissue) 흐름 확인 후 30분으로 원복
- [ ] 수동 E2E: 가입 → 로그인 → 같은 상품 두 번 담기 → 장바구니 수정 → 주문 → 토스 결제 → 승인 → 장바구니에서 결제 상품만 빠졌는지, 재고가 줄었는지 → 결과 페이지 새로고침해도 PAID 유지되는지
- [x] [[ShoppingMall - API 명세서]] 갱신 (2026-11-04 완료): POST /auth/reissue, GET /users/find-id 추가, signup·orders·products 요청/응답 변경, 403 바디, 새 ErrorCode(O003, A001)
- [x] [[copilot-addendum]] 에 20261102 블록 반영 (2026-11-04 완료) (블록 원문: 저장소 git 이력 db7ba07의 docs/claude-work-log/20261102_copilot-addendum-block.md, PR 26에서 파일 삭제)

### PR 25 머지 후
- [x] PR 25 리뷰·머지 (2026-11-02, main db7ba07에서 테스트 191개·CI 통과 확인)
- [ ] 로컬 DB: ALTER TABLE orders MODIFY order_status VARCHAR(20) NOT NULL; (PR 23 이후 새로 만든 orders 테이블은 MySQL enum 타입이라 CANCELED·EXPIRED 저장이 실패함)
- [ ] 로컬 DB: likes 테이블이 비어 있는지 확인 (user_id·product_id NOT NULL 컬럼 추가가 기존 행이 있으면 실패)
- [ ] 수동 E2E
	- 로그아웃 후 같은 access token으로 GET /users/me → 401
	- access token 만료 상태로 /profile, /orders 진입 → 자동 재발급 후 정상 표시
	- 결제 후 주문 내역에서 취소·환불 → 토스 테스트 결제 내역에서 취소 확인, 재고 복구 확인
	- 주문만 만들고 결제창 닫기 → 만료(EXPIRED)·재고 복구 확인 (테스트 시 order.pending-expiration-minutes=1)
	- 상품 검색·정렬·페이지 이동, 찜하기·찜 목록
- [x] [[ShoppingMall - API 명세서]] 에 PR 25 변경 반영 (2026-11-04 완료): GET /products 페이지 응답, 주문 취소, 찜 API 4개, 로그인 401 통일, 주문 응답 orderStatus·productName, 장바구니 productName·productPrice, ErrorCode U006·PA002, TOSS_SERVER_ERROR 502
- [ ] PR 25 이전에 결제된 주문은 paymentKey가 없어 API 환불 불가(400) → 필요하면 토스 개발자센터에서 수동 환불

## 2. 결정 필요 (정해야 진행 가능)

- [ ] (중간) 검증 규칙
	- 회원 이름 ^[가-힣]{3,5} : 2글자 이름(예: 김구), 6글자 이상, 외국인 이름 가입 불가
	- 상품 이름 [a-z]{3,20}|[가-힣]{3,20} : 대문자·숫자·공백 불가("감자 1kg", "Apple" 거부). 수정 DTO에만 있어서 등록은 되는데 같은 이름으로 수정은 안 됨 → 등록·수정 규칙 통일 필요
- [ ] (중간) 멀티 디바이스 정책: 지금은 사용자당 refresh token 1개라 다른 기기에서 로그인하면 이전 기기는 다음 재발급에서 401
	- 정책이 정해지면 같이 진행: 기기별 키로 저장, 재사용 감지(이미 교체된 토큰이 다시 오면 세션 강제 종료), 여러 탭 동시 재발급 시 직전 토큰 짧은 유예
- [ ] (높음, 미확인) 회원 탈퇴·상품 삭제 정책
	- 회원 탈퇴: orders가 users를 FK로 참조해 주문이 있는 회원 탈퇴 시 500 예상, 장바구니는 고아로 남음
	- 상품 삭제: cart_item이 product를 FK로 참조해 장바구니에 담긴 상품 삭제 시 500 예상
	- 선택지: soft delete(상태 컬럼, 개인정보 마스킹, 판매 중지) 권장. 주문 기록 보존 기간 등 정책 결정 필요
- [ ] (중간) 비밀번호 찾기 방식: 현재 프론트 설계(이메일+이름+전화번호만 맞으면 즉시 변경)는 계정 탈취 위험. 메일 인증 + Redis 재설정 토큰(TTL) 방식 권장, spring-boot-starter-mail 의존성 추가 필요(사용자 담당). 그 전까지 로그인 화면의 비밀번호 찾기 링크 숨김 권장 (지금은 비로그인 시 401)
- [ ] (낮음) 토스 승인 요청의 주문 소유자 확인 여부 (20260826 결정으로 보류 중)
- [ ] (낮음) Swagger 공개 범위: 지금은 ADMIN 전용. 개발 편의가 필요하면 local 프로파일에서만 공개

## 3. 테스트 (현재 단계, Phase 2)

- [ ] (중간) SecurityConfig 인가 매트릭스 테스트: 공개 200 / 비로그인 401 / USER 403 / ADMIN 200을 엔드포인트별로 고정. 새로 생긴 공개 경로 POST /auth/reissue, GET /users/find-id 포함. 지금은 401·403 응답 형식만 확인(SecurityErrorResponseTest)
- [ ] (중간) 컨트롤러 예외 매핑 테스트: 서비스가 던진 예외(thenThrow)가 GlobalExceptionHandler를 거쳐 올바른 상태코드·메시지로 나가는지. 현재 AuthControllerTest에만 있고 Cart·Order·Product·User 컨트롤러는 400 검증 테스트만 있음 (404 NOT_FOUND, 400 OUT_OF_STOCK, 400 ORDER_STATUS_INVALID 등)
- [ ] (낮음) 기존 테스트 정리: any() → eq()와 verify, SecurityContextHolder 직접 설정 → .with(authentication(...)) 통일, 매직값 상수화

## 4. 기능 개발 (PR 25에서 전부 구현)

### JWT 인증 심화 (Phase 5)
- [x] refresh token 재발급 API(POST /auth/reissue) + rotation, 로그아웃 시 쿠키 만료 (PR 23)
- [x] (중간) 로그아웃 후에도 access token이 만료 전까지 유효 → Redis 블랙리스트(jti, 남은 만료 시간만큼 TTL, Redis 장애 시 401) (PR 25)
- [x] (중간) 서버 컴포넌트(profile, orders 페이지)는 access token 만료 시 재발급하지 못함 → /auth/refresh 페이지로 재발급 후 원래 페이지로 복귀 (PR 25)
- [x] (중간) 로그인 실패 메시지가 "Email not found" / "User password unmatched"로 갈려 가입 여부가 드러남 → 401 "Invalid email or password"로 통일, 응답 시간 차이도 제거 (PR 25)

### 주문·결제
- [x] (높음) PENDING 주문 만료 처리: 30분 지난 PENDING을 1분마다 정리, 토스 조회 후 DONE이면 결제 완료로 복구 / 미결제면 EXPIRED + 재고 복구 (PR 25)
- [x] (높음) 토스 호출 타임아웃·네트워크 오류: 타임아웃 5초/30초, 승인 중 오류 시 결제 조회로 확정, 확정 불가면 PENDING 유지 + 502. 중복 RestClient 빈 삭제 (PR 25)
- [x] (중간) 주문 취소·환불: POST /orders/{orderId}/cancel, PAID는 토스 결제 취소(Idempotency-Key로 재시도 안전), 재고 복구, 주문 내역 화면 취소 버튼 (PR 25)
- [x] (낮음) orderUid 난수 충돌 시 unique 위반 500 → 저장 전 확인 후 최대 5회 재생성 (PR 25)

### 회원·상품
- [x] (중간) 상품 목록 페이지네이션(서버 검색·가격 범위·정렬) + @BatchSize로 N+1 해결 (PR 25)
- [x] (낮음) 찜하기: 찜·취소·내 찜 여부·찜 목록 API, 상품 상세 버튼, /likes 페이지 (PR 25)

## 5. 인프라·데이터 (의존성·설정은 사용자 담당)

- [ ] (중간) Flyway 학습(V/R 마이그레이션, checksum, baseline, validate) → db/migration/V1__init_schema.sql (product.stock, orders.order_status 문자열 반영) → ddl-auto validate + Flyway 활성화, 테스트 프로파일은 Flyway 끔
- [ ] (중간) 목데이터 seed: R__seed_mock_data.sql (고정 ID, 미리 만든 bcrypt 해시 테스트 계정, ADMIN 계정 포함) + application-local.yml
- [ ] (중간) Redis getProduct 캐시: @EnableCaching + RedisCacheManager 직렬화 설정 필요
- [ ] (낮음) Actuator + Prometheus + Grafana, 대량 목데이터로 부하 확인
- [ ] (낮음) Deploy: CD, Nginx 리버스 프록시, CORS 설정을 컨트롤러별 @CrossOrigin(localhost:3000) 대신 한 곳으로, 프론트·API 도메인에 맞춘 쿠키 Secure·SameSite
- [ ] (낮음) 서버를 여러 대 띄울 때 PENDING 만료 스케줄러가 서버마다 돎 → 행 잠금으로 중복 처리는 막히지만 ShedLock 등 단일 실행 장치 검토

## 6. 정리 (낮음)

- [ ] 프론트 eslint 에러 2건: order/page.tsx, toss-test/page.tsx의 useEffect 안 setState (set-state-in-effect). 2026-11-04 재확인 시에도 남아 있음
- [ ] ErrorCode 미사용 8개 정리 (CM000, CM001, U003, U004, U005, P002, C002, C003). 로그인 실패를 U006으로 통일하면서 U004·U005도 미사용
- [ ] toss-test 페이지 삭제 또는 개발 환경 전용
- [ ] CheckConfig의 IllegalArgumentException이 500으로 나감. 사용자 입력은 DTO 검증으로 막는 원칙 유지

## 7. 기능 개발 2차 (타사 쇼핑몰 비교로 추가, 2026-11-03)

- 비교 기준: 쿠팡·무신사·11번가 같은 국내 쇼핑몰에서 흔한 기능 (회사별 세부 기능을 하나씩 확인한 것은 아님)
- 지금 가장 큰 빈자리: 배송. 주문에 배송지·배송 상태가 없어 실제로 물건을 보낼 수 없는 구조
- 아래 1~5는 이 순서로 구현 (배송이 있어야 구매확정이 생기고, 구매확정이 있어야 포인트 적립·리뷰 작성 조건이 성립)
- PR 26: 1~5의 클래스·메서드 뼈대만 추가. 새 클래스에는 @Entity·@Service·@RestController가 없고 리포지토리도 JpaRepository를 상속하지 않아 런타임 영향 없음. 메서드는 UnsupportedOperationException("TODO"), 각 클래스 상단 주석에 구현 시 붙일 애너테이션·쿼리·연결 지점 기록

### 다음 구현 (순서대로)
- [ ] 1. (높음) 배송지·배송 상태
	- 회원 주소록(Address): 등록·조회·수정·삭제·기본 배송지
	- 주문 시 배송지 스냅샷(ShippingInfo, @Embeddable)과 배송 요청사항
	- 배송 상태(DeliveryStatus): READY → PREPARING → SHIPPING → DELIVERED → CONFIRMED, 관리자 상태 변경(건너뛰기·되돌리기 금지), 운송장 번호
	- 구매확정(사용자), 배송 완료 후 일정 기간 지나면 자동 구매확정(만료 스케줄러와 같은 폴링 방식)
	- 주문 취소는 배송 준비(PREPARING) 전까지만 허용하도록 기존 취소 로직과 연결
- [ ] 2. (높음) 비밀번호 변경: 현재 비밀번호 확인 → 새 비밀번호 저장 → refresh token 삭제(다른 기기 로그아웃). 메일 의존성 없이 가능
- [ ] 3. (중간) 쿠폰: 정액·정률(최대 할인액), 최소 주문 금액, 기간, 선착순 발급(조건부 UPDATE + unique 제약, 동시성 테스트), 주문 적용, 취소·결제 실패·만료 시 복구. 로드맵의 부하 테스트 대상으로도 적합
- [ ] 4. (중간) 포인트: 구매확정 시 적립, 주문 시 사용(잔액 부족 400, 동시 사용 시 음수 방지), 취소 시 복구, 이력 조회. 결제 금액 = 상품 합계 - 쿠폰 할인 - 사용 포인트
- [ ] 5. (중간) 리뷰·별점: 구매확정한 주문 항목만, 항목당 1개, 상품별 평균 별점·리뷰 수, 작성자 이름 마스킹

### 그다음 (바로 구현 가능)
- [ ] (중간) 카테고리: 계층형 카테고리, 상품 목록 검색 조건에 카테고리 추가
- [ ] (중간) 상품 옵션(사이즈·색상별 재고): 재고 단위가 상품 → 옵션으로 바뀌어 장바구니·주문·재고 차감 전부 영향, 큰 작업
- [ ] (낮음) 인기순 정렬(판매량·찜 수), 최근 본 상품(Redis)
- [ ] (낮음) 부분 취소, 교환·반품, 배송비 정책

### 의존성·인프라·정책이 필요한 것 (사용자 담당 또는 결정 필요)
- [ ] 상품 이미지 업로드: 파일 저장소(로컬 또는 S3)와 업로드 설정 필요. 지금은 상품명 첫 글자로 대신 표시
- [ ] 소셜 로그인(카카오·구글): OAuth2 client 의존성, 플랫폼 앱 등록 필요. 화면에는 "준비 중" 버튼만 있음
- [ ] 메일·알림: 비밀번호 찾기(2번 결정 필요 항목), 주문·배송 알림, 재입고 알림
- [ ] 관리자 화면: 상품 등록·주문 처리·배송 상태 변경·매출 통계. 지금은 API만 있음 (Manager 엔티티는 비어 있음)

## 8. 프론트 UI (잡지형 화면)

- 방향: 흰색·검정 톤의 "잡지 같은 웹". 메인은 모델 사진을 넘겨 보는 잡지, 사진 속 옷에서 상품 상세로 이동
- PR 22(머지): 로그인·회원가입·상품 상세 리디자인, FormField 공통 컴포넌트, 비밀번호 마스킹, Enter 제출, 인라인 에러
- PR 28(dev/ui, 미머지): 잡지 메인 1차(표지·뒤표지, 책장 넘김, = 토글 메뉴, 고객센터 /support)
- PR 29(dev/ui-cntwa2, 미머지, PR 28 포함): 사용자 요구 8개 반영한 최종 레이아웃
	- 가로가 세로 이상이면 펼침면 두 쪽(왼쪽·오른쪽 모델 사진 한 장씩), 세로가 긴 화면은 한 쪽씩 넘김
	- 옷마다 제품명·가격 메모를 모델 옆 배경에 두고 0.6px 실금으로 옷의 점과 연결, 공간이 없으면 메모를 옷 아래에 배치
	- 표지·제목·쪽 번호 모두 삭제, 회사 연락처는 고객센터 화면에만 표시

- [ ] PR 29 리뷰·머지 후 PR 28 닫기 (29가 28의 커밋을 모두 포함)
- [ ] (높음) 실제 모델 사진 준비 후 content.ts 교체: 사진은 8:5 비율(가운데 4:5 영역에 모델), 옷마다 점 위치 x·y와 메모 방향 side, 사진별 모델 범위 span 조정
- [ ] (높음) 상품 이미지 필드 + 업로드 (7번 의존성 항목과 같음). 잡지 사진·상품 목록·상세 모두 지금은 임시 그림 또는 상품명 첫 글자
- [ ] (중간) 잡지 내용(LOOKS)을 코드 상수에서 API 또는 관리자 등록 데이터로 이동. 지금은 productId·이름·가격이 예시 값이라 실제 상품과 다를 수 있음
- [ ] (중간) 주문 내역 화면에 주문 날짜 표시: OrderResponseDTO에 createdAt 없음
- [ ] (중간) 비밀번호 찾기 화면: 백엔드 API 없음(2번 결정 필요). 결정 전까지 링크 숨김 권장
- [ ] (낮음) 카테고리·브랜드·사이즈·색상 옵션 화면 (7번 카테고리·상품 옵션 구현 후)
- [ ] (낮음) 소셜 로그인 버튼은 "준비 중" 상태 유지 (7번 의존성 항목)

> [!info]- 🔗 위키 연결
> - 상위: [[프로젝트]]
> - 프로젝트: [[ShoppingMall - 트러블 슈팅 기록]] · [[copilot-addendum]] · [[ShoppingMall - API 명세서]]
> - 개념: [[Redis]] · [[트랜잭션]]
