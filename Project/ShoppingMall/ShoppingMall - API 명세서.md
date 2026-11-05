# ShoppingMall - API 명세서

- 기준: main 1cb7a0a (PR 26 머지, 2026-11-03). PR 23(재발급·아이디 찾기·재고)과 PR 25(취소·환불·만료·찜·페이지네이션) 반영
- 생성: 2026-10-07, springdoc-openapi 2.6.0이 만든 /v3/api-docs를 변환 + 코드 확인으로 권한·에러·비고 보강
- 갱신: 2026-11-04, 컨트롤러·DTO·SecurityConfig·서비스 예외를 main 코드에서 다시 대조해 전체 갱신
- 갱신: 2026-11-05, 소셜 로그인 API(Auth 4번) 추가. 프론트(PR 30)가 정한 계약이며 백엔드는 미구현 ("예정" 표시)
- 갱신: 2026-11-05, 문의 게시판 API(Inquiry 33~36번) 추가. 프론트(PR 31)가 정한 계약이며 백엔드는 미구현 ("예정" 표시)
- Base URL: http://localhost:8080/api/v1
- Swagger UI (앱 실행 후, ADMIN 전용): http://localhost:8080/api/v1/swagger-ui.html
- 코드가 바뀌면 이 노트는 자동으로 갱신되지 않음. 최신 명세는 Swagger UI 기준
- PR 26에서 추가된 Address·Delivery·Coupon·Point·Review 컨트롤러는 뼈대만 있고 @RestController가 없어 엔드포인트가 아님 (이 문서에서 제외)

## 0. 공통 규칙

### 인증
- 로그인·재발급 성공 시 서버가 accessToken, refreshToken 쿠키를 발급 (HttpOnly, Secure, SameSite=Lax, Path=/)
- 만료: access token 현재 7일(application.yml TODO: 30분 1800000으로 원복), refresh token 7일
- 요청 시 JwtAuthenticationFilter가 accessToken 쿠키를 먼저 읽고, 없으면 Authorization: Bearer 헤더를 읽음
- 토큰에 type 클레임(access/refresh)과 jti가 있음. refresh token을 access 자리에 넣으면 인증 실패
- 로그아웃한 access token은 Redis 블랙리스트(jti, 남은 만료 시간만큼 TTL)에 올라 만료 전에도 401. Redis 장애 시에도 안전하게 401
- 브라우저 fetch는 credentials: "include" 필요, 서버 컴포넌트 fetch는 Cookie 헤더를 직접 전달
- 프론트 authFetch(lib/api.ts): 401이면 POST /auth/reissue 한 번(동시 요청은 하나의 재발급을 공유) 후 원래 요청 재시도
- 서버 컴포넌트(profile, orders)는 access token 만료 시 /auth/refresh 페이지로 보내 재발급 후 원래 페이지로 복귀
- userId는 경로가 아니라 토큰에서 꺼냄 (@AuthenticationPrincipal). /me 경로는 항상 본인 데이터

### 권한 등급
| 권한 | 의미 | 실패 시 |
|---|---|---|
| x | 누구나 (permitAll) | - |
| 인증요구 | 유효한 토큰 필요 (authenticated) | 401 "Invalid or missing access token" (WWW-Authenticate: Bearer) |
| ADMIN | ROLE_ADMIN 권한 필요 (hasRole) | 비로그인 401, 로그인했지만 권한 없음 403 "Access denied" (둘 다 ApiResponse 형식) |

- SecurityConfig는 엔드포인트별로 HTTP 메서드까지 지정하고, 목록에 없는 요청은 anyRequest().hasRole("ADMIN")으로 막음 (기본 닫기)
- /error는 공개 (예외 처리 중 재요청이 401로 바뀌지 않도록)
- 회원가입은 항상 USER. ADMIN 계정은 DB에서 role을 직접 수정

### 응답 형식 (ApiResponse)
| 필드 | 타입 | 설명 |
|---|---|---|
| status | String | "success" 또는 "error" |
| message | String | 처리 결과 메시지 |
| data | T | 응답 데이터 (에러·데이터 없음이면 null) |

- 반환 타입이 void인 DELETE API(회원 탈퇴, 장바구니·상품·주문 삭제)는 200 + 빈 바디. 로그아웃도 바디 없음(쿠키만 만료)
- 에러 응답은 status "error" + message만 있음. ErrorCode의 코드 문자열(U001 등)은 바디에 포함되지 않음
- 에러 경로: 비즈니스 예외 → ErrorCode의 HTTP 상태, @Valid 실패 → 400 + 첫 번째 필드 메시지, 표준 예외(깨진 JSON 400, 미지원 메서드 405 등) → 해당 상태, 인증·인가 실패 → 401·403 ApiResponse, 그 외 → 500 "Internal Server Error"

## 1. 엔드포인트 요약

### Auth (인증)

| #   | 메서드    | 경로            | 설명                      | 권한    | 프론트 호출                     |
| --- | ------ | ------------- | ----------------------- | ----- | -------------------------- |
| 1   | POST   | /users/login  | 로그인 (accessToken·refreshToken 쿠키 발급) | x     | login/page.tsx (브라우저)      |
| 2   | POST   | /auth/reissue | 토큰 재발급 (refresh token rotation) | x | lib/api.ts authFetch, auth/refresh/page.tsx |
| 3   | DELETE | /users/logout | 로그아웃 (refresh 삭제, access 블랙리스트, 쿠키 만료) | 인증요구  | ProfileMenu.tsx (브라우저)     |
| 4   | POST   | /auth/oauth/{provider} | 소셜 로그인 (카카오·네이버·구글), 예정 | x | auth/callback/[provider]/page.tsx (브라우저) |

- 컨트롤러는 AuthController. 로그인·로그아웃 경로는 /users 하위 (ApiURLNames.loginURL, logOutURL)
- 4번은 백엔드 미구현. 지금은 기본 닫기 규칙(anyRequest ADMIN)에 걸려 401이고, 프론트 콜백 화면은 "OO 로그인에 실패했습니다"를 표시

### User (회원)

| #   | 메서드    | 경로            | 설명                      | 권한    | 프론트 호출                     |
| --- | ------ | ------------- | ----------------------- | ----- | -------------------------- |
| 4   | GET    | /users        | 전체 유저 조회                | ADMIN | 없음                         |
| 5   | GET    | /users/me     | 내 정보 조회                 | 인증요구  | profile/page.tsx (서버 컴포넌트) |
| 6   | PATCH  | /users/me     | 내 정보 수정                 | 인증요구  | ProfileEditor.tsx (브라우저)   |
| 7   | DELETE | /users/me     | 회원 탈퇴                   | 인증요구  | 없음                         |
| 8   | POST   | /users/signup | 회원가입 (장바구니 동시 생성)       | x     | signup/page.tsx (브라우저)     |
| 9   | GET    | /users/find-id | 아이디 찾기 (마스킹 이메일)     | x     | find-id/page.tsx (브라우저)    |

미구현: 프론트 find-password/page.tsx가 호출하는 POST /users/find-password는 백엔드에 없음 → 기본 닫기 규칙으로 401 (비밀번호 찾기 방식 결정 필요, TODO 2번)

### Cart (장바구니)

| #   | 메서드    | 경로                       | 설명              | 권한    | 프론트 호출                   |
| --- | ------ | ------------------------ | --------------- | ----- | ------------------------ |
| 10  | GET    | /carts                   | 전체 장바구니 조회      | ADMIN | 없음                       |
| 11  | POST   | /carts                   | 장바구니에 상품 담기     | 인증요구  | AddToCartForm.tsx (브라우저) |
| 12  | DELETE | /carts/items/{productId} | 장바구니에서 상품 하나 제거 | 인증요구  | cart/page.tsx (브라우저)     |
| 13  | GET    | /carts/me                | 내 장바구니 조회       | 인증요구  | cart/page.tsx (브라우저)     |
| 14  | PATCH  | /carts/me                | 내 장바구니 수량 수정    | 인증요구  | cart/page.tsx (브라우저)     |
| 15  | DELETE | /carts/me                | 내 장바구니 비우기      | 인증요구  | 없음                       |

### Product (상품)

| # | 메서드 | 경로 | 설명 | 권한 | 프론트 호출 |
|---|---|---|---|---|---|
| 16 | GET | /products | 상품 목록 조회 (검색·가격 범위·정렬·페이지) | x | products/page.tsx (브라우저) |
| 17 | POST | /products | 상품 등록 | ADMIN | 없음 |
| 18 | GET | /products/{productId} | 상품 단건 조회 | x | products/[productId]/page.tsx (서버), orders/page.tsx (서버), order/page.tsx (브라우저) |
| 19 | PATCH | /products/{productId} | 상품 수정 | ADMIN | 없음 |
| 20 | DELETE | /products/{productId} | 상품 삭제 | ADMIN | 없음 |

### Likes (찜)

| # | 메서드 | 경로 | 설명 | 권한 | 프론트 호출 |
|---|---|---|---|---|---|
| 21 | POST | /products/{productId}/likes | 찜하기 | 인증요구 | LikeButton.tsx (브라우저) |
| 22 | DELETE | /products/{productId}/likes | 찜 취소 | 인증요구 | LikeButton.tsx, likes/page.tsx (브라우저) |
| 23 | GET | /products/{productId}/likes/me | 내 찜 여부·찜 수 | 인증요구 | LikeButton.tsx (브라우저) |
| 24 | GET | /users/me/likes | 내 찜 목록 | 인증요구 | likes/page.tsx (브라우저) |

- LikesController는 공통 prefix 없이 전체 경로를 씀 (ApiURLNames.productLikesURL 등)

### Order (주문·결제)

| #   | 메서드    | 경로                        | 설명         | 권한    | 프론트 호출                                  |
| --- | ------ | ------------------------- | ---------- | ----- | --------------------------------------- |
| 25  | GET    | /orders                   | 전체 주문 조회   | ADMIN | 없음                                      |
| 26  | POST   | /orders                   | 주문 생성 (재고 차감)  | 인증요구  | order/page.tsx (브라우저)                   |
| 27  | GET    | /orders/me                | 내 주문 목록 조회 | 인증요구  | orders/page.tsx (서버 컴포넌트, Cookie 직접 전달) |
| 28  | POST   | /orders/toss/payment/auth | 토스 결제 승인   | 인증요구  | order/result/page.tsx (브라우저), toss-test/result (개발용) |
| 29  | GET    | /orders/{orderId}         | 내 주문 단건 조회 | 인증요구  | 없음                                      |
| 30  | PATCH  | /orders/{orderId}         | 내 주문 수량 수정 (PENDING만) | 인증요구  | 없음                                      |
| 31  | POST   | /orders/{orderId}/cancel  | 내 주문 취소·환불 | 인증요구  | CancelOrderButton.tsx (브라우저)            |
| 32  | DELETE | /orders/{orderId}         | 주문 삭제      | ADMIN | 없음                                      |

- 서버 내부 작업: OrderExpirationScheduler가 1분마다 30분(order.pending-expiration-minutes) 지난 PENDING 주문을 정리. 토스 조회 결과 DONE이면 PAID로 복구, 미결제면 EXPIRED + 재고 복구

### Inquiry (문의, 예정)

| #   | 메서드  | 경로                         | 설명                      | 권한        | 프론트 호출                                   |
| --- | ---- | -------------------------- | ----------------------- | --------- | ---------------------------------------- |
| 33  | GET  | /inquiries                 | 문의 목록 (제목, 가린 작성자, 날짜, 답변 상태) | x         | support/page.tsx (서버 컴포넌트)                |
| 34  | POST | /inquiries                 | 문의 작성                   | 인증요구      | support/inquiries/new/page.tsx (브라우저, authFetch) |
| 35  | GET  | /inquiries/{inquiryId}     | 문의 상세 + 답변              | 인증요구 (작성자·ADMIN) | support/inquiries/[inquiryId]/page.tsx (브라우저, authFetch) |
| 36  | POST | /inquiries/{inquiryId}/answer | 답변 등록                 | ADMIN     | 없음 (관리자 화면 예정)                          |

- 공개 범위 (20261105 사용자 결정): 목록은 누구나, 본문과 답변은 작성자와 관리자만
- 전부 백엔드 미구현. 지금은 기본 닫기 규칙(anyRequest ADMIN)에 걸려 목록 401 → 화면은 "문의 목록을 불러오지 못했습니다" 표시

## 2. 엔드포인트 상세

### Auth (인증)

#### POST /users/login

| 항목 | 내용 |
|---|---|
| 설명 | 로그인 |
| 컨트롤러 | AuthController.logIn |
| 권한 | x |
| 요청 바디 | LogInRequestDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = null, message "Success : Log In" |
| 에러 | 401 LOGIN_FAILED "Invalid email or password"<br>400 @Valid 실패 |
| 프론트 호출 | login/page.tsx (브라우저) |
| 비고 | 성공 시 Set-Cookie 2개: accessToken, refreshToken<br>이메일 없음·비밀번호 불일치를 같은 401 메시지로 통일하고, 이메일이 없어도 비밀번호 해시 비교를 해서 응답 시간 차이도 없앰 (PR 25) |

#### POST /auth/reissue

| 항목 | 내용 |
|---|---|
| 설명 | access token 재발급 + refresh token 교체 (rotation) |
| 컨트롤러 | AuthController.reissue |
| 권한 | x (access token이 만료돼도 호출해야 하므로 공개) |
| 요청 | 바디 없음. refreshToken 쿠키를 읽음 |
| 응답 200 | ApiResponse, data = null, message "Success : reissue token" + Set-Cookie 2개 |
| 에러 | 401 INVALID_REFRESH_TOKEN "Invalid or expired refresh token" (쿠키 없음, 서명·만료 오류, type이 refresh가 아님, Redis 저장값과 불일치) |
| 프론트 호출 | lib/api.ts authFetch (401 시 자동), auth/refresh/page.tsx (서버 컴포넌트용) |
| 비고 | refresh token은 사용자당 1개(Redis). 다른 기기에서 로그인하면 이전 기기는 다음 재발급에서 401 (멀티 디바이스 정책 결정 필요) |

#### DELETE /users/logout

| 항목 | 내용 |
|---|---|
| 설명 | 로그아웃 |
| 컨트롤러 | AuthController.logOut |
| 권한 | 인증요구 |
| 응답 200 | 빈 바디 + Set-Cookie 2개 (Max-Age=0으로 만료) |
| 에러 | 401 미인증 |
| 프론트 호출 | ProfileMenu.tsx (브라우저, authFetch) |
| 비고 | Redis의 refresh token 삭제, 현재 access token의 jti를 블랙리스트에 등록<br>access token이 만료된 상태면 authFetch가 먼저 재발급한 뒤 로그아웃 |

#### POST /auth/oauth/{provider} (예정, 백엔드 미구현)

| 항목 | 내용 |
|---|---|
| 설명 | 소셜 로그인. 프론트가 회사 로그인 화면에서 받은 authorization code를 넘기면, 백엔드가 회사 서버와 토큰을 교환해 사용자를 확인하고 우리 토큰 쿠키를 발급 |
| 컨트롤러 | 미정 (AuthController 권장) |
| 권한 | x (로그인 전 호출이므로 SecurityConfig permitAll에 추가 필요) |
| 경로 변수 | provider: kakao / naver / google (그 외 400) |
| 요청 바디 | SocialLoginRequestDTO (아래 스키마, 예정) |
| 응답 200 | ApiResponse, data = null + Set-Cookie 2개 (POST /users/login과 같은 accessToken·refreshToken) |
| 에러 (제안) | 400 지원하지 않는 provider, @Valid 실패<br>401 회사가 code를 거절 (만료, 재사용, redirectUri 불일치)<br>502 회사 서버 응답 없음 (토스와 같은 타임아웃 정책) |
| 프론트 호출 | auth/callback/[provider]/page.tsx (브라우저, credentials include). 응답이 4xx·5xx면 "OO 로그인에 실패했습니다" 표시 |
| 비고 | 프론트는 state를 이미 대조한 뒤 호출함 (CSRF 방지는 프론트 담당, 서버는 회사 요청에만 사용)<br>카카오: 토큰 교환에 REST API 키와 client secret 사용 (프론트의 JS 키 아님)<br>네이버: 토큰 교환 요청에 state 필수<br>구글: redirect_uri가 인가 요청과 정확히 같아야 함. 받은 id_token의 서명·aud 검증으로 사용자 확인 가능<br>회원 식별은 회사별 고유 ID(카카오 id, 네이버 id, 구글 sub)로 하고 이메일로 하지 않음<br>첫 로그인 시 가입 처리 가정. 전화번호 필수·이름 규칙 때문에 지금 UserCreateDTO로는 저장 불가 (결정 필요) |

### User (회원)

#### GET /users

| 항목 | 내용 |
|---|---|
| 설명 | 전체 유저 조회 |
| 컨트롤러 | UserController.getUsers |
| 권한 | ADMIN |
| 응답 200 | ApiResponse, data = List<UserResponseDTO> |
| 에러 | 401 미인증<br>403 권한 부족 |
| 프론트 호출 | 없음 |

#### GET /users/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 정보 조회 |
| 컨트롤러 | UserController.getUser |
| 권한 | 인증요구 |
| 응답 200 | ApiResponse, data = UserResponseDTO |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND |
| 프론트 호출 | profile/page.tsx (서버 컴포넌트) |

#### PATCH /users/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 정보 수정 (보낸 필드만 바꿈) |
| 컨트롤러 | UserController.patchUser |
| 권한 | 인증요구 |
| 요청 바디 | UserUpdateDTO (아래 스키마) |
| 검증 | 작동 (@Valid, 이름·이메일·전화번호 형식) |
| 응답 200 | ApiResponse, data = UserResponseDTO |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND<br>400 USER_ALREADY_EXIST (다른 회원이 쓰는 이메일로 변경)<br>400 @Valid 실패 |
| 프론트 호출 | ProfileEditor.tsx (브라우저, authFetch) |

#### DELETE /users/me

| 항목 | 내용 |
|---|---|
| 설명 | 회원 탈퇴 |
| 컨트롤러 | UserController.deleteUser |
| 권한 | 인증요구 |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | 찜을 먼저 지운 뒤 회원 삭제. 주문이 있는 회원은 orders.user_id FK 때문에 500 예상 (탈퇴 정책 결정 필요, 미확인) |

#### POST /users/signup

| 항목 | 내용 |
|---|---|
| 설명 | 회원가입 (장바구니 동시 생성) |
| 컨트롤러 | UserController.createUser |
| 권한 | x |
| 요청 바디 | UserCreateDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = UserCreateResponseDTO |
| 에러 | 400 @Valid 실패 (필드 메시지)<br>400 USER_ALREADY_EXIST (이메일 중복) |
| 프론트 호출 | signup/page.tsx (브라우저) |
| 비고 | role은 서버가 USER로 고정 (signUpRole 필드 삭제)<br>이름 규칙 ^[가-힣]{3,5}는 2글자·6글자 이상·외국인 이름 가입 불가 (검증 규칙 결정 필요) |

#### GET /users/find-id

| 항목 | 내용 |
|---|---|
| 설명 | 이름 + 전화번호로 가입 이메일 찾기 |
| 컨트롤러 | UserController.findId |
| 권한 | x |
| 쿼리 파라미터 | name, phoneNumber (FindIdRequestDTO, @ModelAttribute) |
| 검증 | 작동 (@Valid, 둘 다 필수) |
| 응답 200 | ApiResponse, data = String (마스킹 이메일, 여러 개면 ", "로 연결. 예: qw******@gmail.com) |
| 에러 | 404 USER_NOT_FOUND<br>400 @Valid 실패 |
| 프론트 호출 | find-id/page.tsx (브라우저) |
| 비고 | 로컬 파트 앞 2글자만 노출 (2글자 이하면 1글자), 별표는 최소 3개 |

### Cart (장바구니)

#### GET /carts

| 항목 | 내용 |
|---|---|
| 설명 | 전체 장바구니 조회 |
| 컨트롤러 | CartController.getCarts |
| 권한 | ADMIN |
| 응답 200 | ApiResponse, data = List<CartResponseDTO> |
| 에러 | 401 미인증<br>403 권한 부족 |
| 프론트 호출 | 없음 |

#### POST /carts

| 항목 | 내용 |
|---|---|
| 설명 | 장바구니에 상품 담기 |
| 컨트롤러 | CartController.addCartItemInCart |
| 권한 | 인증요구 |
| 요청 바디 | CartItemCreateDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = CartResponseDTO |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND<br>404 PRODUCT_NOT_FOUND<br>400 @Valid 실패 |
| 프론트 호출 | AddToCartForm.tsx (브라우저, authFetch) |
| 비고 | 이미 담긴 상품이면 행을 추가하지 않고 수량을 더함 |

#### DELETE /carts/items/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 장바구니에서 상품 하나 제거 |
| 컨트롤러 | CartController.deleteCartItemInCart |
| 권한 | 인증요구 |
| 경로 변수 | productId (Long) |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND |
| 프론트 호출 | cart/page.tsx (브라우저, authFetch) |

#### GET /carts/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 장바구니 조회 |
| 컨트롤러 | CartController.getCart |
| 권한 | 인증요구 |
| 응답 200 | ApiResponse, data = CartResponseDTO (항목마다 상품명·가격 포함) |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND |
| 프론트 호출 | cart/page.tsx (브라우저, authFetch) |

#### PATCH /carts/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 장바구니 수량 수정 |
| 컨트롤러 | CartController.patchCart |
| 권한 | 인증요구 |
| 요청 바디 | CartUpdateDTO (아래 스키마) |
| 검증 | 작동 (리스트 @Valid + @NotEmpty) |
| 응답 200 | ApiResponse, data = CartResponseDTO |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND<br>404 CART_ITEM_NOT_FOUND (장바구니에 없는 상품)<br>400 @Valid 실패 |
| 프론트 호출 | cart/page.tsx (브라우저, authFetch) |

#### DELETE /carts/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 장바구니 비우기 |
| 컨트롤러 | CartController.deleteCart |
| 권한 | 인증요구 |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | 쓰기 트랜잭션 누락으로 삭제가 반영되지 않던 문제 수정 (PR 23) |

### Product (상품)

#### GET /products

| 항목 | 내용 |
|---|---|
| 설명 | 상품 목록 조회 (서버 검색·정렬·페이지) |
| 컨트롤러 | ProductController.getProducts |
| 권한 | x |
| 쿼리 파라미터 | keyword (상품명 포함, 선택)<br>minPrice, maxPrice (선택)<br>sort: LATEST(기본) / NAME / PRICE_ASC / PRICE_DESC<br>page (0부터, 기본 0), size (기본 20) |
| 응답 200 | ApiResponse, data = ProductPageResponseDTO |
| 에러 | 400 잘못된 sort 값 |
| 프론트 호출 | products/page.tsx (브라우저) |
| 비고 | 상세 목록 N+1은 @BatchSize로 해결 (PR 25) |

#### POST /products

| 항목 | 내용 |
|---|---|
| 설명 | 상품 등록 |
| 컨트롤러 | ProductController.createProduct |
| 권한 | ADMIN |
| 요청 바디 | ProductCreateDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = ProductResponseDTO |
| 에러 | 401 미인증<br>403 권한 부족<br>400 @Valid 실패 |
| 프론트 호출 | 없음 |

#### GET /products/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 상품 단건 조회 |
| 컨트롤러 | ProductController.getProduct |
| 권한 | x |
| 경로 변수 | productId (Long) |
| 응답 200 | ApiResponse, data = ProductResponseDTO |
| 에러 | 404 PRODUCT_NOT_FOUND |
| 프론트 호출 | products/[productId]/page.tsx (서버), orders/page.tsx (서버, 주문 상품명 보조), order/page.tsx (브라우저) |

#### PATCH /products/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 상품 수정 (보낸 필드만 바꿈, 상세 목록은 통째로 교체) |
| 컨트롤러 | ProductController.patchProduct |
| 권한 | ADMIN |
| 경로 변수 | productId (Long) |
| 요청 바디 | ProductUpdateDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = ProductResponseDTO |
| 에러 | 401 미인증<br>403 권한 부족<br>404 PRODUCT_NOT_FOUND<br>400 @Valid 실패 |
| 프론트 호출 | 없음 |
| 비고 | 재고 지정도 이 API (stock). 이름 규칙이 등록과 다름 (5번 표) |

#### DELETE /products/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 상품 삭제 |
| 컨트롤러 | ProductController.deleteProduct |
| 권한 | ADMIN |
| 경로 변수 | productId (Long) |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>403 권한 부족<br>404 PRODUCT_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | 장바구니·주문·찜에 들어 있는 상품은 FK 때문에 500 예상 (soft delete 정책 결정 필요, 미확인) |

### Likes (찜)

#### POST /products/{productId}/likes

| 항목 | 내용 |
|---|---|
| 설명 | 찜하기 |
| 컨트롤러 | LikesController.like |
| 권한 | 인증요구 |
| 경로 변수 | productId (Long) |
| 응답 200 | ApiResponse, data = LikeStatusResponseDTO |
| 에러 | 401 미인증<br>404 PRODUCT_NOT_FOUND<br>404 USER_NOT_FOUND |
| 프론트 호출 | LikeButton.tsx (브라우저, authFetch) |
| 비고 | 이미 찜한 상품이면 그대로 성공 (멱등, (user_id, product_id) unique) |

#### DELETE /products/{productId}/likes

| 항목 | 내용 |
|---|---|
| 설명 | 찜 취소 |
| 컨트롤러 | LikesController.unlike |
| 권한 | 인증요구 |
| 경로 변수 | productId (Long) |
| 응답 200 | ApiResponse, data = LikeStatusResponseDTO |
| 에러 | 401 미인증<br>404 PRODUCT_NOT_FOUND |
| 프론트 호출 | LikeButton.tsx, likes/page.tsx (브라우저, authFetch) |
| 비고 | 찜하지 않은 상품이어도 성공 (멱등) |

#### GET /products/{productId}/likes/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 찜 여부와 상품의 찜 수 |
| 컨트롤러 | LikesController.getStatus |
| 권한 | 인증요구 |
| 응답 200 | ApiResponse, data = LikeStatusResponseDTO |
| 에러 | 401 미인증<br>404 PRODUCT_NOT_FOUND |
| 프론트 호출 | LikeButton.tsx (브라우저, authFetch) |

#### GET /users/me/likes

| 항목 | 내용 |
|---|---|
| 설명 | 내 찜 목록 (최근 찜한 순) |
| 컨트롤러 | LikesController.getMyLikes |
| 권한 | 인증요구 |
| 응답 200 | ApiResponse, data = List<LikedProductResponseDTO> |
| 에러 | 401 미인증 |
| 프론트 호출 | likes/page.tsx (브라우저, authFetch) |

### Order (주문·결제)

주문 상태(OrderStatus, 문자열 저장): PENDING(결제 대기) → PAID(결제 완료) / FAILED(결제 실패) / CANCELED(취소·환불) / EXPIRED(결제 시간 만료)

#### GET /orders

| 항목 | 내용 |
|---|---|
| 설명 | 전체 주문 조회 |
| 컨트롤러 | OrderController.getOrders |
| 권한 | ADMIN |
| 응답 200 | ApiResponse, data = List<OrderResponseDTO> |
| 에러 | 401 미인증<br>403 권한 부족 |
| 프론트 호출 | 없음 |

#### POST /orders

| 항목 | 내용 |
|---|---|
| 설명 | 주문 생성 (PENDING) |
| 컨트롤러 | OrderController.createOrder |
| 권한 | 인증요구 |
| 요청 바디 | OrderCreateDTO (아래 스키마) |
| 검증 | 작동 (@Valid, 리스트 @Valid + @NotEmpty) |
| 응답 200 | ApiResponse, data = OrderResponseDTO |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND<br>404 PRODUCT_NOT_FOUND<br>400 PRODUCT_OUT_OF_STOCK "Product is out of stock (id)"<br>400 @Valid 실패 |
| 프론트 호출 | order/page.tsx (브라우저, authFetch) |
| 비고 | 가격은 서버가 Product.price로 채움 (클라이언트 가격 필드 삭제)<br>재고는 조건부 UPDATE(stock >= 수량)로 차감, 상품 id 순서로 잠가 교착 방지<br>orderUid(토스 주문번호) 충돌 시 최대 5회 재생성 |

#### GET /orders/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 주문 목록 조회 |
| 컨트롤러 | OrderController.getOrdersWithUserId |
| 권한 | 인증요구 |
| 응답 200 | ApiResponse, data = List<OrderResponseDTO> |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND |
| 프론트 호출 | orders/page.tsx (서버 컴포넌트, Cookie 직접 전달) |
| 비고 | 고정 경로라 /orders/{orderId}보다 우선 매칭. 응답에 주문 날짜가 없어 화면에 표시하지 못함 |

#### POST /orders/toss/payment/auth

| 항목 | 내용 |
|---|---|
| 설명 | 토스 결제 승인 |
| 컨트롤러 | OrderController.authTossPaymentOrder |
| 권한 | 인증요구 |
| 요청 바디 | TossPaymentRequestDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = OrderResponseDTO |
| 에러 | 401 미인증<br>404 ORDER_NOT_FOUND<br>400 ORDER_PRICE_UNMATCHED "Unmatched Price Info"<br>400 ORDER_STATUS_INVALID (PENDING·PAID가 아닌 주문)<br>400 PAYMENT_FAILED (토스 거절, 주문 FAILED + 재고 복구)<br>502 TOSS_SERVER_ERROR (토스 응답 없음, 결제 조회로도 확정 불가 → PENDING 유지) |
| 프론트 호출 | order/result/page.tsx (브라우저, authFetch) |
| 비고 | 요청의 orderId는 주문 PK가 아니라 orderUid<br>주문 행 비관적 잠금 후 PAID면 토스를 다시 부르지 않고 현재 주문 반환 (새로고침·재클릭 멱등)<br>승인 성공 시 paymentKey 저장, 장바구니에서 결제한 상품만 제거<br>토스 타임아웃: 연결 5초, 응답 30초. 네트워크 오류 시 결제 조회 API로 상태 확정<br>주문 소유자 확인은 하지 않음 (20260826 결정으로 보류) |

#### GET /orders/{orderId}

| 항목 | 내용 |
|---|---|
| 설명 | 내 주문 단건 조회 |
| 컨트롤러 | OrderController.getOrderWithUserId |
| 권한 | 인증요구 |
| 경로 변수 | orderId (Long) |
| 응답 200 | ApiResponse, data = OrderResponseDTO |
| 에러 | 401 미인증<br>404 ORDER_NOT_FOUND (남의 주문도 404) |
| 프론트 호출 | 없음 |
| 비고 | orderId + userId 단건 쿼리로 변경 (PR 23) |

#### PATCH /orders/{orderId}

| 항목 | 내용 |
|---|---|
| 설명 | 내 주문 수량 수정 |
| 컨트롤러 | OrderController.patchOrder |
| 권한 | 인증요구 |
| 경로 변수 | orderId (Long) |
| 요청 바디 | OrderUpdateDTO (아래 스키마) |
| 검증 | 작동 (리스트 @Valid + @NotEmpty) |
| 응답 200 | ApiResponse, data = OrderResponseDTO |
| 에러 | 401 미인증<br>404 ORDER_NOT_FOUND (남의 주문, 주문에 없는 상품 포함)<br>400 ORDER_STATUS_INVALID (PENDING이 아님)<br>400 PRODUCT_OUT_OF_STOCK (늘린 수량만큼 재고 부족) |
| 프론트 호출 | 없음 |
| 비고 | 수량만 수정, 가격은 서버 값 유지. 늘면 재고 차감, 줄면 복구 |

#### POST /orders/{orderId}/cancel

| 항목 | 내용 |
|---|---|
| 설명 | 내 주문 취소 (PAID는 토스 환불까지) |
| 컨트롤러 | OrderController.cancelOrder |
| 권한 | 인증요구 |
| 경로 변수 | orderId (Long) |
| 요청 바디 | OrderCancelDTO (선택, 생략 가능) |
| 검증 | 작동 (cancelReason 200자 이하) |
| 응답 200 | ApiResponse, data = OrderResponseDTO (orderStatus CANCELED) |
| 에러 | 401 미인증<br>404 ORDER_NOT_FOUND (남의 주문도 404)<br>400 ORDER_STATUS_INVALID (FAILED·CANCELED·EXPIRED)<br>400 PAYMENT_CANCEL_FAILED (토스 취소 거절, paymentKey 없음)<br>502 TOSS_SERVER_ERROR |
| 프론트 호출 | CancelOrderButton.tsx (orders 페이지, authFetch) |
| 비고 | 주문 행 비관적 잠금. PENDING은 바로 취소, PAID는 토스 전액 취소(Idempotency-Key "cancel-{orderUid}"로 재시도 안전) 후 취소. 둘 다 재고 복구<br>cancelReason이 없으면 기본 사유로 요청<br>PR 25 이전 결제 주문은 paymentKey가 없어 API 환불 불가 → 토스 개발자센터에서 수동 환불 |

#### DELETE /orders/{orderId}

| 항목 | 내용 |
|---|---|
| 설명 | 주문 삭제 |
| 컨트롤러 | OrderController.deleteOrder |
| 권한 | ADMIN |
| 경로 변수 | orderId (Long) |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>403 권한 부족<br>404 ORDER_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | PENDING 주문이면 잡아 둔 재고를 복구한 뒤 삭제 |

### Inquiry (문의, 예정)

#### GET /inquiries (예정)

| 항목 | 내용 |
|---|---|
| 설명 | 문의 목록, 최신순 |
| 권한 | x (SecurityConfig permitAll 추가 필요) |
| 쿼리 파라미터 | page (0부터, 기본 0), size (기본 10) |
| 응답 200 | ApiResponse, data = InquiryPageResponseDTO (예정) |
| 프론트 호출 | support/page.tsx (서버 컴포넌트, cache no-store) |
| 비고 | 본문은 목록에 넣지 않음. 작성자 이름은 서버가 가려서 보냄 (예: 김*자, po***) |

#### POST /inquiries (예정)

| 항목 | 내용 |
|---|---|
| 설명 | 문의 작성 |
| 권한 | 인증요구 |
| 요청 바디 | InquiryCreateDTO (예정) |
| 응답 200 | ApiResponse, data = InquiryResponseDTO (예정, inquiryId 필수: 프론트가 작성 후 상세로 이동) |
| 에러 (제안) | 401 미인증 (프론트가 로그인 안내)<br>400 @Valid 실패 |
| 프론트 호출 | support/inquiries/new/page.tsx (브라우저, authFetch) |

#### GET /inquiries/{inquiryId} (예정)

| 항목 | 내용 |
|---|---|
| 설명 | 문의 상세와 답변 |
| 권한 | 인증요구. 작성자 본인 또는 ADMIN만 |
| 응답 200 | ApiResponse, data = InquiryResponseDTO (예정) |
| 에러 (제안) | 401 미인증<br>403 남의 문의 (프론트가 "작성자 본인만 볼 수 있는 문의입니다" 표시)<br>404 없는 문의 |
| 프론트 호출 | support/inquiries/[inquiryId]/page.tsx (브라우저, authFetch) |
| 비고 | 남의 문의를 404로 숨기는 방식(주문 단건 조회와 같은 방식)도 가능. 프론트는 둘 다 처리함 |

#### POST /inquiries/{inquiryId}/answer (예정)

| 항목 | 내용 |
|---|---|
| 설명 | 관리자 답변 등록 |
| 권한 | ADMIN |
| 요청 바디 | { content } |
| 프론트 호출 | 없음 (관리자 화면과 함께 예정) |

## 3. 스키마

제약은 DTO 어노테이션 기준. 현재 모든 요청 DTO에 @Valid가 붙어 있고 리스트 필드도 중첩 검증됨.

### 요청 DTO

#### UserCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| signUpName | String | 필수, 한글 3~5자 |
| signUpEmail | String | 필수, 이메일 형식 |
| signUpPassword | String | 필수 |
| signUpPhoneNumber | String | 필수, 010xxxxxxxx |
| signUpBirthday | LocalDate | 필수 |

#### LogInRequestDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| email | String | 필수 |
| logInPassword | String | 필수 |

#### FindIdRequestDTO (쿼리 파라미터)

| 필드 | 타입 | 제약 |
|---|---|---|
| name | String | 필수 |
| phoneNumber | String | 필수 |

#### UserUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| name | String | 빈 값 또는 한글 3~5자 |
| email | String | 이메일 형식 |
| phoneNumber | String | 빈 값 또는 010xxxxxxxx |
| birthday | LocalDate | - |

#### CartItemCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| quantity | Long | 필수, 최소 1 |

#### CartUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| cartItemUpdateDTOList | List<CartItemUpdateDTO> | 1개 이상, 원소 검증 |

#### CartItemUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| quantity | Long | 필수, 최소 1 |

#### ProductCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| name | String | 필수 (공백 불가) |
| price | Long | 필수, 최소 0 |
| productDetailCreateDTOList | List<ProductDetailCreateDTO> | 1개 이상, 원소 검증 |
| stock | Long | 필수, 최소 0 |

#### ProductDetailCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| detail | String | 필수 (공백 불가) |

#### ProductUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| name | String | 빈 값 또는 영소문자 3~20자 또는 한글 3~20자 |
| price | Long | 최소 0 |
| productDetailUpdateDTOList | List<ProductDetailUpdateDTO> | 원소 검증 (보내면 통째로 교체) |
| stock | Long | 최소 0 |

#### ProductDetailUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| detail | String | 필수 (공백 불가) |

#### OrderCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| orderItemCreateDTOList | List<OrderItemCreateDTO> | 1개 이상, 원소 검증 |

#### OrderItemCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| quantity | Long | 필수, 최소 1 |

#### OrderUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| orderItemResponseDTOList | List<OrderItemUpdateDTO> | 1개 이상, 원소 검증 (필드 이름이 Response인 것은 기존 명명 그대로) |

#### OrderItemUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| quantity | Long | 필수, 최소 1 |

#### OrderCancelDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| cancelReason | String | 선택, 200자 이하 |

#### SocialLoginRequestDTO (예정)

| 필드 | 타입 | 제약 |
|---|---|---|
| code | String | 필수 (회사가 발급한 authorization code, 1회용) |
| state | String | 필수 (네이버 토큰 교환에 사용) |
| redirectUri | String | 필수 ({사이트 주소}/auth/callback/{provider}, 회사 콘솔 등록값과 같아야 함) |

#### TossPaymentRequestDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| paymentKey | String | 필수 |
| orderId | Long | 필수 (주문의 orderUid) |
| amount | Long | 필수, 최소 0 |

#### InquiryCreateDTO (예정)

| 필드 | 타입 | 제약 |
|---|---|---|
| category | String | 필수, ORDER / DELIVERY / PRODUCT / ACCOUNT / ETC |
| title | String | 필수, 100자 이하 |
| content | String | 필수, 2000자 이하 |

### 응답 DTO

#### UserResponseDTO

| 필드 | 타입 |
|---|---|
| userId | Long |
| name | String |
| email | String |
| role | String |
| phoneNumber | String |
| birthday | LocalDate |

#### UserCreateResponseDTO

| 필드 | 타입 |
|---|---|
| userResponseDTO | UserResponseDTO |
| cartResponseDTO | CartResponseDTO |

#### CartResponseDTO

| 필드 | 타입 |
|---|---|
| userId | Long |
| cartItemList | List<CartItemResponseDTO> |
| totalCartPrice | Long |

#### CartItemResponseDTO

| 필드 | 타입 |
|---|---|
| cartItemId | Long |
| productItemId | Long (상품 id) |
| quantity | Long |
| productName | String |
| productPrice | Long |

#### ProductResponseDTO

| 필드 | 타입 |
|---|---|
| productId | Long |
| name | String |
| price | Long |
| productDetailResponseDTOList | List<ProductDetailResponseDTO> |
| stock | Long |

#### ProductDetailResponseDTO

| 필드 | 타입 |
|---|---|
| detail | String |

#### ProductPageResponseDTO

| 필드 | 타입 |
|---|---|
| content | List<ProductResponseDTO> |
| page | int (0부터) |
| size | int |
| totalElements | long |
| totalPages | int |
| hasNext | boolean |

#### LikeStatusResponseDTO

| 필드 | 타입 |
|---|---|
| productId | Long |
| liked | boolean |
| likeCount | long |

#### LikedProductResponseDTO

| 필드 | 타입 |
|---|---|
| productId | Long |
| name | String |
| price | Long |
| stock | Long |
| likedAt | LocalDateTime |

#### OrderResponseDTO

| 필드 | 타입 |
|---|---|
| orderId | Long |
| orderUid | Long (토스 주문번호) |
| orderItemResponseDTOList | List<OrderItemResponseDTO> |
| totalOrderPrice | Long |
| orderStatus | OrderStatus (PENDING, PAID, FAILED, CANCELED, EXPIRED) |

#### OrderItemResponseDTO

| 필드 | 타입 |
|---|---|
| productId | Long |
| curOrderItemPrice | Long (주문 시점 가격) |
| quantity | Long |
| totalOrderItemPrice | Long |
| productName | String |

#### InquirySummaryDTO (예정, 목록 항목)

| 필드 | 타입 |
|---|---|
| inquiryId | Long |
| category | String (ORDER, DELIVERY, PRODUCT, ACCOUNT, ETC) |
| title | String |
| writerName | String (서버에서 마스킹) |
| createdAt | LocalDateTime |
| answered | boolean |

#### InquiryPageResponseDTO (예정)

ProductPageResponseDTO와 같은 형식: content (List<InquirySummaryDTO>), page, size, totalElements, totalPages, hasNext

#### InquiryResponseDTO (예정, 상세)

| 필드 | 타입 |
|---|---|
| (InquirySummaryDTO 필드 전부) | |
| content | String |
| answer | { content: String, answeredAt: LocalDateTime } 또는 null |

## 4. 에러 코드

| ErrorCode | HTTP | 코드 | 기본 메시지 | 사용처 |
|---|---|---|---|---|
| INVALID_INPUT_VALUE | 400 | CM000 | Invalid input value | 미사용 |
| INTERNAL_SERVER_ERROR | 500 | CM001 | Server error | 미사용 (500은 catch-all이 "Internal Server Error"로 응답) |
| USER_NOT_FOUND | 404 | U001 | User not found | GET·PATCH·DELETE /users/me, GET /users/find-id, POST /orders, GET /orders/me, POST /products/{productId}/likes |
| USER_ALREADY_EXIST | 400 | U002 | User already exist | POST /users/signup, PATCH /users/me (이메일 중복) |
| USER_UPDATE_FAILED | 400 | U003 | User info cannot update | 미사용 |
| USER_PASSWORD_UNMATCHED | 400 | U004 | User password unmatched | 미사용 (로그인 실패는 U006으로 통일) |
| EMAIL_NOT_FOUND | 400 | U005 | Email not found | 미사용 (로그인 실패는 U006으로 통일) |
| LOGIN_FAILED | 401 | U006 | Invalid email or password | POST /users/login |
| PRODUCT_NOT_FOUND | 404 | P001 | Cannot found product | GET·PATCH·DELETE /products/{productId}, POST /carts, POST /orders, 찜 API 3개 |
| PRODUCT_ALREADY_EXIST | 400 | P002 | Product Already Exist | 미사용 |
| PRODUCT_OUT_OF_STOCK | 400 | P003 | Product is out of stock | POST /orders, PATCH /orders/{orderId} |
| CART_NOT_FOUND | 404 | C001 | Cannot found cart | POST /carts, GET·PATCH·DELETE /carts/me, DELETE /carts/items/{productId} |
| CART_ALREADY_EXIST | 400 | C002 | Cart Already Exist | 미사용 |
| CART_EMPTY | 400 | C003 | There are no CartItem in Cart | 미사용 |
| CART_ITEM_NOT_FOUND | 404 | CT001 | Cannot found cart item | PATCH /carts/me |
| ORDER_NOT_FOUND | 404 | O001 | Cannot found Order | GET·PATCH·DELETE /orders/{orderId}, POST /orders/{orderId}/cancel, POST /orders/toss/payment/auth |
| ORDER_PRICE_UNMATCHED | 400 | O002 | Unmatched Price Info | POST /orders/toss/payment/auth |
| ORDER_STATUS_INVALID | 400 | O003 | Order status does not allow this request | POST /orders/toss/payment/auth, PATCH /orders/{orderId}, POST /orders/{orderId}/cancel |
| INVALID_REFRESH_TOKEN | 401 | A001 | Invalid or expired refresh token | POST /auth/reissue |
| REFRESH_TOKEN_NOT_FOUND | 400 | RD001 | Cannot found refresh token | RefreshTokenRepository 조회용 (현재 API 응답 경로 없음) |
| PAYMENT_FAILED | 400 | PA001 | Payment Failed | POST /orders/toss/payment/auth |
| PAYMENT_CANCEL_FAILED | 400 | PA002 | Payment cancel failed | POST /orders/{orderId}/cancel |
| TOSS_SERVER_ERROR | 502 | TS001 | Cannot confirm payment status with Toss. Please try again | POST /orders/toss/payment/auth, POST /orders/{orderId}/cancel |

- 예외 생성 시 메시지를 따로 넘기면 기본 메시지 대신 그 메시지가 응답됨 (예: PRODUCT_OUT_OF_STOCK → "Product is out of stock (3)")
- 인증·인가 실패는 ErrorCode가 아니라 SecurityConfig에서 직접 응답: 401 "Invalid or missing access token", 403 "Access denied"

## 5. 명세 기준으로 드러난 문제

이전 표의 높음 항목(가입 role 지정, 인증 없는 상품 CUD, 클라이언트 가격, 전체 조회 공개, 승인 상태 미확인, @Valid 누락, 이메일 중복 500, 로그아웃 쿠키, 로그인 메시지)은 PR 20~25에서 모두 해결되어 삭제함.

| 심각도 | 대상 | 문제 | 계획 |
|---|---|---|---|
| 높음, 미확인 | DELETE /users/me, DELETE /products/{productId} | 주문·장바구니가 FK로 참조하면 500 예상 | soft delete 정책 결정 (TODO 2번) |
| 높음 | POST /auth/oauth/{provider} | 프론트(PR 30)는 호출하지만 백엔드 미구현 → 소셜 로그인 불가 | JWT 심화 단계에서 구현 |
| 중간 | POST /auth/oauth/{provider} | 소셜 사용자는 전화번호가 없고 이름이 영문·2글자일 수 있어 지금 회원 규칙으로 저장 불가 | 추가 정보 입력 또는 규칙 완화 결정 |
| 중간 | /inquiries 4개 | 프론트(PR 31)는 호출하지만 백엔드 미구현 → 고객센터 목록 실패 안내, 작성 불가 | Inquiry 엔티티·API 구현 |
| 중간 | POST /users/find-password | 프론트는 호출하지만 백엔드 미구현 (401) | 메일 인증 + Redis 재설정 토큰 방식 결정 (TODO 2번) |
| 중간 | POST /auth/reissue | refresh token이 사용자당 1개라 다른 기기 로그인 시 이전 기기 세션 종료 | 멀티 디바이스 정책 결정 (TODO 2번) |
| 중간 | POST /users/signup, PATCH /products/{productId} | 이름 규칙이 2글자·외국인 이름, 대문자·숫자·공백 상품명을 거부. 상품명 규칙이 등록·수정에서 다름 | 검증 규칙 결정 (TODO 2번) |
| 중간 | GET /orders/me | 응답에 주문 날짜가 없어 주문 내역 화면에 표시 불가 | OrderResponseDTO에 createdAt 추가 검토 |
| 중간 | GET /products, GET /products/{productId} | 상품 이미지 필드가 없음 (프론트 잡지 화면은 임시 그림 사용) | 이미지 업로드·저장소 결정 (TODO 7번) |
| 낮음 | POST /orders/toss/payment/auth | 주문 소유자 확인 없음 | 20260826 결정으로 보류 |
| 낮음 | 공통 | 에러 바디에 ErrorCode 코드 문자열 없음 (프론트가 메시지 문자열로 분기해야 함) | 미정 |
| 낮음 | ErrorCode | 미사용 코드 8개 (CM000, CM001, U003, U004, U005, P002, C002, C003) 정리 필요 | 정리 |
