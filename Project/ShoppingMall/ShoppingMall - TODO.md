---
tags:
  - seed
  - type/project
aliases: []
created: 2026-11-02
---
# ShoppingMall - TODO

- 기준: main 1e1e7f3 (PR 23 머지, 2026-11-02). 백엔드 테스트 133개 통과 (로컬 clean test, GitHub Actions 모두 성공)
- 로드맵: Spring Boot + MySQL → CI(테스트 코드) + Web Server → JWT 인증 심화(로그인/로그아웃) → Grafana/Prometheus + Mock Data → Deploy(CD 포함)
- 현재 단계: 컨트롤러 예외/인가 테스트 마무리 → 끝나면 JWT 인증 심화로 전환
- 우선순위: 높음(돈·데이터 문제) / 중간(기능 결함·사용성) / 낮음(정리). "미확인"은 코드로 추론했고 실행해서 확인하지 않은 항목
- 자세한 근거: ShoppingMall 저장소 docs/claude-work-log/ 의 20261102_work-log.md(변경 내역·API 변경 목록), 20261102_unimplemented.md(미구현 상세)

## 0. PR 23 머지 후 바로 할 일

- [ ] 로컬 DB의 orders, order_item 테이블 drop (주문 상태를 숫자 → 문자열로 저장하도록 바꿨는데 ddl-auto update는 기존 컬럼 타입을 바꾸지 않음)
- [ ] 기존 상품에 재고 지정: PATCH /products/{id} 로 stock 입력 (컬럼이 새로 생기면 0 = 품절)
- [ ] ADMIN 계정은 DB에서 role을 ADMIN으로 직접 수정 (회원가입은 항상 USER)
- [ ] application.yml access-token-expiration-ms 를 1800000(30분)으로 원복 (현재 7일)
- [ ] 수동 E2E: 가입 → 로그인 → 같은 상품 두 번 담기 → 장바구니 수정 → 주문 → 토스 결제 → 승인 → 장바구니에서 결제 상품만 빠졌는지, 재고가 줄었는지 → 결과 페이지 새로고침해도 PAID 유지되는지
- [ ] access token 만료를 짧게(60000) 바꿔 재발급(POST /auth/reissue) 흐름 확인 후 원복
- [ ] [[ShoppingMall - API 명세서]] 갱신: POST /auth/reissue, GET /users/find-id 추가, signup·orders·products 요청/응답 변경, 403 바디, 새 ErrorCode(O003, A001)
- [ ] [[copilot-addendum]] 에 20261102 블록 반영 (저장소 docs/claude-work-log/20261102_copilot-addendum-block.md 그대로 붙여넣기)
- [ ] 검증 규칙 결정
	- 회원 이름 ^[가-힣]{3,5} : 2글자 이름(예: 김구), 6글자 이상, 외국인 이름 가입 불가
	- 상품 이름 [a-z]{3,20}|[가-힣]{3,20} : 대문자·숫자·공백 불가("감자 1kg", "Apple" 거부). 수정 DTO에만 있어서 등록은 되는데 같은 이름으로 수정은 안 됨 → 등록·수정 규칙 통일 필요

## 1. 현재 단계: 컨트롤러 예외·인가 테스트 마무리 (Phase 2)

- [ ] (중간) SecurityConfig 인가 매트릭스 테스트: 공개 200 / 비로그인 401 / USER 403 / ADMIN 200을 엔드포인트별로 고정. 새로 생긴 공개 경로 POST /auth/reissue, GET /users/find-id 포함. 지금은 401·403 응답 형식만 확인(SecurityErrorResponseTest)
- [ ] (중간) 컨트롤러 예외 매핑 테스트: 서비스가 던진 예외(thenThrow)가 GlobalExceptionHandler를 거쳐 올바른 상태코드·메시지로 나가는지. 현재 AuthControllerTest에만 있고 Cart·Order·Product·User 컨트롤러는 400 검증 테스트만 있음 (404 NOT_FOUND, 400 OUT_OF_STOCK, 400 ORDER_STATUS_INVALID 등)
- [ ] (낮음) 기존 테스트 정리: any() → eq()와 verify, SecurityContextHolder 직접 설정 → .with(authentication(...)) 통일, 매직값 상수화

## 2. 다음 단계: JWT 인증 심화 (Phase 5)

- [x] refresh token 재발급 API(POST /auth/reissue) + rotation, 로그아웃 시 쿠키 만료 (PR 23)
- [ ] (높음) access token 30분 원복 (0번과 같은 항목)
- [ ] (중간) 로그아웃 후에도 access token이 만료 전까지 유효 → Redis 블랙리스트(jti, 남은 만료 시간만큼 TTL)
- [ ] (중간) 멀티 디바이스 정책 결정: 지금은 사용자당 refresh token 1개라 다른 기기에서 로그인하면 이전 기기는 다음 재발급에서 401. 기기별 키로 바꾼 뒤 재사용 감지(이미 교체된 토큰이 다시 오면 세션 강제 종료) 도입
- [ ] (중간) 여러 탭이 동시에 재발급하면 한쪽이 401이 될 수 있음 → 직전 토큰 짧은 유예 기간 검토
- [ ] (중간) 서버 컴포넌트(profile, orders 페이지)는 access token 만료 시 재발급하지 못함 → Next.js middleware 또는 클라이언트 authFetch로 이전
- [ ] (중간) 로그인 실패 메시지가 "Email not found" / "User password unmatched"로 갈려 가입 여부가 드러남 → 하나로 통일

## 3. 주문·결제

- [ ] (높음) PENDING 주문 만료 처리: 재고를 주문 생성 시점에 잡으므로 결제창에서 이탈하면 재고가 계속 묶임 → @Scheduled로 일정 시간(예: 30분) 지난 PENDING을 FAILED 처리 + 재고 복구 (주문 행 잠금 사용)
- [ ] (높음) 토스 호출 타임아웃·네트워크 오류: RestClient에 타임아웃이 없고 오류 시 500 + 주문 PENDING 유지. 토스는 승인했는데 응답만 유실되면 결제·주문 불일치 → 타임아웃 설정 + 토스 결제 조회 API로 실제 상태 확인. RestClientConfig와 TossPaymentConfig의 RestClient 빈 중복도 정리
- [ ] (중간) 주문 취소·환불: CANCELED 상태, 승인 시 paymentKey 저장, PENDING은 바로 취소, PAID는 토스 결제 취소 API 호출, 둘 다 재고 복구
- [ ] (중간, 선택) 토스 승인 요청의 주문 소유자 확인 (20260826 결정으로 보류 중)
- [ ] (낮음) orderUid 난수 충돌 시 unique 위반 500 → 재시도 또는 시간 기반 ID

## 4. 회원·상품

- [ ] (높음, 미확인) 회원 탈퇴: orders가 users를 FK로 참조해 주문이 있는 회원 탈퇴 시 500 예상, 장바구니는 고아로 남음 → soft delete 정책 결정
- [ ] (높음, 미확인) 상품 삭제: cart_item이 product를 FK로 참조해 장바구니에 담긴 상품 삭제 시 500 예상 → soft delete(판매 중지 상태)
- [ ] (중간) 비밀번호 찾기: 이번에 구현 보류. 현재 프론트 설계(이메일+이름+전화번호만 맞으면 즉시 변경)는 계정 탈취 위험 → 메일 인증 + Redis 재설정 토큰(TTL) 방식. 구현 전까지 로그인 화면의 비밀번호 찾기 링크 숨김 권장 (지금은 비로그인 시 401)
- [ ] (중간) 상품 목록 페이지네이션 + 목록 API N+1(상세·주문 항목 지연 로딩) 해결
- [ ] (중간) Redis getProduct 캐시
- [ ] (낮음) 찜하기: Likes 엔티티에 id만 있음

## 5. DB·데이터 (Phase 3~4)

- [ ] (중간) Flyway 학습(V/R 마이그레이션, checksum, baseline, validate) → db/migration/V1__init_schema.sql (product.stock, orders.order_status 문자열 반영) → ddl-auto validate + Flyway 활성화, 테스트 프로파일은 Flyway 끔
- [ ] (중간) 목데이터 seed: R__seed_mock_data.sql (고정 ID, 미리 만든 bcrypt 해시 테스트 계정, ADMIN 계정 포함) + application-local.yml

## 6. 모니터링·배포 (로드맵 후반)

- [ ] Actuator + Prometheus + Grafana, 대량 목데이터로 부하 확인
- [ ] Deploy: CD, Nginx 리버스 프록시
- [ ] 배포 전 정리: CORS 설정을 컨트롤러별 @CrossOrigin(localhost:3000) 대신 한 곳으로, 프론트·API 도메인에 맞춘 쿠키 Secure·SameSite, Swagger 공개 범위(지금은 ADMIN 전용), toss-test 페이지 삭제 또는 개발 전용

## 7. 정리 (낮음)

- [ ] 프론트 eslint 에러 2건: order/page.tsx, toss-test/page.tsx의 useEffect 안 setState (set-state-in-effect)
- [ ] CheckConfig의 IllegalArgumentException이 500으로 나감. 사용자 입력은 DTO 검증으로 막는 원칙 유지

> [!info]- 🔗 위키 연결
> - 상위: [[프로젝트]]
> - 프로젝트: [[ShoppingMall - 트러블 슈팅 기록]] · [[copilot-addendum]] · [[ShoppingMall - API 명세서]]
> - 개념: [[Redis]] · [[트랜잭션]]
