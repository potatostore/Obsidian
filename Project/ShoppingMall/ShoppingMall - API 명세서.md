# ShoppingMall - API 명세서

- 기준: origin/config/test 5ef71ff (main 병합 + /me 경로 변경 반영). config/test가 main에 머지되면 main 기준과 같아짐
- 생성: 2026-10-07, springdoc-openapi 2.6.0이 만든 /v3/api-docs를 변환 + 코드 확인으로 권한·에러·비고 보강
- Base URL: http://localhost:8080/api/v1
- Swagger UI (앱 실행 후): http://localhost:8080/api/v1/swagger-ui.html
- 코드가 바뀌면 이 노트는 자동으로 갱신되지 않음. 최신 명세는 Swagger UI 기준

## 0. 공통 규칙

### 인증
- 로그인 성공 시 서버가 accessToken, refreshToken 쿠키를 발급 (HttpOnly, Secure, SameSite=Lax)
- 요청 시 JwtAuthenticationFilter가 accessToken 쿠키를 먼저 읽고, 없으면 Authorization: Bearer 헤더를 읽음
- 브라우저 fetch는 credentials: "include" 필요, 서버 컴포넌트 fetch는 Cookie 헤더를 직접 전달
- userId는 경로가 아니라 토큰에서 꺼냄 (@AuthenticationPrincipal). /me 경로는 항상 본인 데이터

### 권한 등급
| 권한 | 의미 | 실패 시 |
|---|---|---|
| x | 누구나 (permitAll) | - |
| 인증요구 | 유효한 토큰 필요 (authenticated) | 401 "Invalid or missing access token" |
| ADMIN | ROLE_ADMIN 권한 필요 (hasRole) | 비로그인 401, 로그인했지만 권한 없음 403 (현재 Boot 기본 형식, ApiResponse 아님) |

권한은 의도한 정책 기준(Phase 1 SecurityConfig 수정 후). 현재 코드와 다른 곳은 5번 참고.

### 응답 형식 (ApiResponse)
| 필드 | 타입 | 설명 |
|---|---|---|
| status | String | "success" 또는 "error" |
| message | String | 처리 결과 메시지 |
| data | T | 응답 데이터 (에러·데이터 없음이면 null) |

- DELETE API는 반환 타입이 void라 200 + 빈 바디
- 에러 응답은 status "error" + message만 있음. ErrorCode의 코드 문자열(U001 등)은 바디에 포함되지 않음
- 에러 경로: 비즈니스 예외 → ErrorCode의 HTTP 상태, @Valid 실패 → 400 + 첫 번째 필드 메시지, 표준 예외(깨진 JSON 400, 미지원 메서드 405 등) → 해당 상태, 그 외 → 500 "Internal Server Error"

## 1. 엔드포인트 요약

### User (회원·인증)

| # | 메서드 | 경로 | 설명 | 권한 | 프론트 호출 |
|---|---|---|---|---|---|
| 1 | GET | /users | 전체 유저 조회 | ADMIN | 없음 |
| 2 | POST | /users/login | 로그인 | x | login/page.tsx (브라우저) |
| 3 | DELETE | /users/logout | 로그아웃 (refresh token 삭제) | 인증요구 | ProfileMenu.tsx (브라우저) |
| 4 | GET | /users/me | 내 정보 조회 | 인증요구 | profile/page.tsx (서버 컴포넌트) |
| 5 | PATCH | /users/me | 내 정보 수정 | 인증요구 | ProfileEditor.tsx (브라우저) |
| 6 | DELETE | /users/me | 회원 탈퇴 | 인증요구 | 없음 |
| 7 | POST | /users/signup | 회원가입 (장바구니 동시 생성) | x | signup/page.tsx (브라우저) |

미구현: 프론트가 호출하는 GET /users/find-id (find-id/page.tsx), POST /users/find-password (find-password/page.tsx)는 백엔드에 없음 → 현재 비로그인 401, 로그인 시 404.

### Cart (장바구니)

| # | 메서드 | 경로 | 설명 | 권한 | 프론트 호출 |
|---|---|---|---|---|---|
| 8 | GET | /carts | 전체 장바구니 조회 | ADMIN | 없음 |
| 9 | POST | /carts | 장바구니에 상품 담기 | 인증요구 | AddToCartForm.tsx (브라우저) |
| 10 | DELETE | /carts/items/{productId} | 장바구니에서 상품 하나 제거 | 인증요구 | cart/page.tsx (브라우저) |
| 11 | GET | /carts/me | 내 장바구니 조회 | 인증요구 | cart/page.tsx (브라우저) |
| 12 | PATCH | /carts/me | 내 장바구니 수정 | 인증요구 | cart/page.tsx (브라우저) |
| 13 | DELETE | /carts/me | 내 장바구니 삭제 | 인증요구 | 없음 |

### Product (상품)

| # | 메서드 | 경로 | 설명 | 권한 | 프론트 호출 |
|---|---|---|---|---|---|
| 14 | GET | /products | 상품 목록 조회 | x | page.tsx·orders/page.tsx (서버), products·cart·order 페이지 (브라우저) |
| 15 | POST | /products | 상품 등록 | ADMIN | 없음 |
| 16 | GET | /products/{productId} | 상품 단건 조회 | x | products/[productId]/page.tsx (서버) |
| 17 | PATCH | /products/{productId} | 상품 수정 | ADMIN | 없음 |
| 18 | DELETE | /products/{productId} | 상품 삭제 | ADMIN | 없음 |

### Order (주문·결제)

| # | 메서드 | 경로 | 설명 | 권한 | 프론트 호출 |
|---|---|---|---|---|---|
| 19 | GET | /orders | 전체 주문 조회 | ADMIN | 없음 |
| 20 | POST | /orders | 주문 생성 | 인증요구 | order/page.tsx (브라우저) |
| 21 | GET | /orders/me | 내 주문 목록 조회 | 인증요구 | orders/page.tsx (서버 컴포넌트, Cookie 직접 전달) |
| 22 | POST | /orders/toss/payment/auth | 토스 결제 승인 | x | order/result/page.tsx (브라우저) |
| 23 | GET | /orders/{orderId} | 내 주문 단건 조회 | 인증요구 | 없음 |
| 24 | PATCH | /orders/{orderId} | 내 주문 수정 | 인증요구 | 없음 |
| 25 | DELETE | /orders/{orderId} | 주문 삭제 | ADMIN | 없음 |

## 2. 엔드포인트 상세

### User (회원·인증)

#### GET /users

| 항목 | 내용 |
|---|---|
| 설명 | 전체 유저 조회 |
| 컨트롤러 | UserController.getUsers |
| 권한 | ADMIN |
| 응답 200 | ApiResponse, data = List<UserResponseDTO> |
| 에러 | 401 미인증 |
| 프론트 호출 | 없음 |
| 비고 | 현재 로그인만 하면 누구나 조회 가능 |

#### POST /users/login

| 항목 | 내용 |
|---|---|
| 설명 | 로그인 |
| 컨트롤러 | AuthController.logIn |
| 권한 | x |
| 요청 바디 | LogInRequestDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = Object |
| 에러 | 400 EMAIL_NOT_FOUND "Email not found"<br>400 USER_PASSWORD_UNMATCHED "User password unmatched"<br>400 @Valid 실패 |
| 프론트 호출 | login/page.tsx (브라우저) |
| 비고 | 성공 시 Set-Cookie 2개: accessToken, refreshToken (HttpOnly, Secure, SameSite=Lax, Path=/)<br>access token 만료 현재 7일 (application.yml TODO: 30분으로 원복)<br>실패 메시지가 이메일 없음/비밀번호 불일치로 구분되어 가입 여부 노출 (Phase 5) |

#### DELETE /users/logout

| 항목 | 내용 |
|---|---|
| 설명 | 로그아웃 (refresh token 삭제) |
| 컨트롤러 | AuthController.logOut |
| 권한 | 인증요구 |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>400 REFRESH_TOKEN_NOT_FOUND "Cannot found refresh token" |
| 프론트 호출 | ProfileMenu.tsx (브라우저) |
| 비고 | 응답 바디 없음, 쿠키 만료 처리 없음<br>access token 만료 시 401로 로그아웃 불가 (Phase 5) |

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
| 설명 | 내 정보 수정 |
| 컨트롤러 | UserController.patchUser |
| 권한 | 인증요구 |
| 요청 바디 | UserUpdateDTO (아래 스키마) |
| 검증 | 무효 (@Valid 있으나 DTO 제약 0개) |
| 응답 200 | ApiResponse, data = UserResponseDTO |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND |
| 프론트 호출 | ProfileEditor.tsx (브라우저) |

#### DELETE /users/me

| 항목 | 내용 |
|---|---|
| 설명 | 회원 탈퇴 |
| 컨트롤러 | UserController.deleteUser |
| 권한 | 인증요구 |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | 응답 바디 없음 |

#### POST /users/signup

| 항목 | 내용 |
|---|---|
| 설명 | 회원가입 (장바구니 동시 생성) |
| 컨트롤러 | UserController.createUser |
| 권한 | x |
| 요청 바디 | UserCreateDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = UserCreateResponseDTO |
| 에러 | 400 @Valid 실패 (필드 메시지)<br>500 이메일 중복 (unique 제약 위반이 catch-all로 처리됨) |
| 프론트 호출 | signup/page.tsx (브라우저) |
| 비고 | signUpRole을 클라이언트가 지정 → ADMIN 가입 가능 (Phase 1에서 서버 고정 예정) |

### Cart (장바구니)

#### GET /carts

| 항목 | 내용 |
|---|---|
| 설명 | 전체 장바구니 조회 |
| 컨트롤러 | CartController.getCarts |
| 권한 | ADMIN |
| 응답 200 | ApiResponse, data = List<CartResponseDTO> |
| 에러 | 401 미인증 |
| 프론트 호출 | 없음 |
| 비고 | 현재 로그인만 하면 누구나 조회 가능 |

#### POST /carts

| 항목 | 내용 |
|---|---|
| 설명 | 장바구니에 상품 담기 |
| 컨트롤러 | CartController.addCartItemInCart |
| 권한 | 인증요구 |
| 요청 바디 | CartItemCreateDTO (아래 스키마) |
| 검증 | 무효 (@Valid 없음 → 제약 무시) |
| 응답 200 | ApiResponse, data = CartResponseDTO |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND<br>404 PRODUCT_NOT_FOUND |
| 프론트 호출 | AddToCartForm.tsx (브라우저) |
| 비고 | Phase 1: 파라미터에 @Valid 추가 예정 |

#### DELETE /carts/items/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 장바구니에서 상품 하나 제거 |
| 컨트롤러 | CartController.deleteCartItemInCart |
| 권한 | 인증요구 |
| 경로 변수 | productId (Long) |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND<br>404 CART_ITEM_NOT_FOUND |
| 프론트 호출 | cart/page.tsx (브라우저) |
| 비고 | 응답 바디 없음 |

#### GET /carts/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 장바구니 조회 |
| 컨트롤러 | CartController.getCart |
| 권한 | 인증요구 |
| 응답 200 | ApiResponse, data = CartResponseDTO |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND |
| 프론트 호출 | cart/page.tsx (브라우저) |

#### PATCH /carts/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 장바구니 수정 |
| 컨트롤러 | CartController.patchCart |
| 권한 | 인증요구 |
| 요청 바디 | CartUpdateDTO (아래 스키마) |
| 검증 | 무효 (리스트 필드에 @Valid 없음 → 원소 제약 무시) |
| 응답 200 | ApiResponse, data = CartResponseDTO |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND |
| 프론트 호출 | cart/page.tsx (브라우저) |

#### DELETE /carts/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 장바구니 삭제 |
| 컨트롤러 | CartController.deleteCart |
| 권한 | 인증요구 |
| 응답 200 | 빈 바디 |
| 에러 | 401 미인증<br>404 CART_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | 응답 바디 없음 |

### Product (상품)

#### GET /products

| 항목 | 내용 |
|---|---|
| 설명 | 상품 목록 조회 |
| 컨트롤러 | ProductController.getProducts |
| 권한 | x |
| 응답 200 | ApiResponse, data = List<ProductResponseDTO> |
| 에러 | - |
| 프론트 호출 | page.tsx·orders/page.tsx (서버), products·cart·order 페이지 (브라우저) |
| 비고 | 페이지네이션 없음 (Phase 6) |

#### POST /products

| 항목 | 내용 |
|---|---|
| 설명 | 상품 등록 |
| 컨트롤러 | ProductController.createProduct |
| 권한 | ADMIN |
| 요청 바디 | ProductCreateDTO (아래 스키마) |
| 검증 | 무효 (@Valid 없음 → 제약 무시) |
| 응답 200 | ApiResponse, data = ProductResponseDTO |
| 에러 | (현재 인증 없음) |
| 프론트 호출 | 없음 |
| 비고 | 현재 누구나 등록 가능<br>Phase 1: @Valid 추가 + ADMIN 제한 예정 |

#### GET /products/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 상품 단건 조회 |
| 컨트롤러 | ProductController.getProduct |
| 권한 | x |
| 경로 변수 | productId (Long) |
| 응답 200 | ApiResponse, data = ProductResponseDTO |
| 에러 | 404 PRODUCT_NOT_FOUND |
| 프론트 호출 | products/[productId]/page.tsx (서버) |

#### PATCH /products/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 상품 수정 |
| 컨트롤러 | ProductController.patchProduct |
| 권한 | ADMIN |
| 경로 변수 | productId (Long) |
| 요청 바디 | ProductUpdateDTO (아래 스키마) |
| 검증 | 무효 (@Valid 있으나 DTO 제약 0개) |
| 응답 200 | ApiResponse, data = ProductResponseDTO |
| 에러 | 404 PRODUCT_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | 상세 목록 교체 버그 (Phase 1) |

#### DELETE /products/{productId}

| 항목 | 내용 |
|---|---|
| 설명 | 상품 삭제 |
| 컨트롤러 | ProductController.deleteProduct |
| 권한 | ADMIN |
| 경로 변수 | productId (Long) |
| 응답 200 | 빈 바디 |
| 에러 | 404 PRODUCT_NOT_FOUND |
| 프론트 호출 | 없음 |
| 비고 | 응답 바디 없음 |

### Order (주문·결제)

#### GET /orders

| 항목 | 내용 |
|---|---|
| 설명 | 전체 주문 조회 |
| 컨트롤러 | OrderController.getOrders |
| 권한 | ADMIN |
| 응답 200 | ApiResponse, data = List<OrderResponseDTO> |
| 에러 | 401 미인증 |
| 프론트 호출 | 없음 |
| 비고 | 현재 로그인만 하면 누구나 조회 가능 |

#### POST /orders

| 항목 | 내용 |
|---|---|
| 설명 | 주문 생성 |
| 컨트롤러 | OrderController.createOrder |
| 권한 | 인증요구 |
| 요청 바디 | OrderCreateDTO (아래 스키마) |
| 검증 | 작동 (@Valid, 리스트에도 @Valid) |
| 응답 200 | ApiResponse, data = OrderResponseDTO |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND<br>400 @Valid 실패 |
| 프론트 호출 | order/page.tsx (브라우저) |
| 비고 | 상품 가격(curOrderItemPrice)을 클라이언트가 보냄 → 서버 재조회 없음 (가격 조작 가능)<br>재고 차감·장바구니 비우기 미구현 (서비스 TODO) |

#### GET /orders/me

| 항목 | 내용 |
|---|---|
| 설명 | 내 주문 목록 조회 |
| 컨트롤러 | OrderController.getOrdersWithUserId |
| 권한 | 인증요구 |
| 응답 200 | ApiResponse, data = List<OrderResponseDTO> |
| 에러 | 401 미인증<br>404 USER_NOT_FOUND |
| 프론트 호출 | orders/page.tsx (서버 컴포넌트, Cookie 직접 전달) |
| 비고 | 고정 경로라 /orders/{orderId}보다 우선 매칭 |

#### POST /orders/toss/payment/auth

| 항목 | 내용 |
|---|---|
| 설명 | 토스 결제 승인 |
| 컨트롤러 | OrderController.authTossPaymentOrder |
| 권한 | x |
| 요청 바디 | TossPaymentRequestDTO (아래 스키마) |
| 검증 | 작동 (@Valid) |
| 응답 200 | ApiResponse, data = OrderResponseDTO |
| 에러 | 404 ORDER_NOT_FOUND<br>400 ORDER_PRICE_UNMATCHED "Unmatched Price Info"<br>400 PAYMENT_FAILED "Payment Failed" |
| 프론트 호출 | order/result/page.tsx (브라우저) |
| 비고 | 요청의 orderId는 주문 PK가 아니라 orderUid<br>결제 금액을 주문 totalOrderPrice와 대조하지만, 그 가격 자체가 클라이언트 입력값<br>8/26 결정(공개)이 SecurityConfig에 미반영 |

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
| 비고 | 본인 주문 전체를 조회한 뒤 메모리에서 거름 (경미한 비효율) |

#### PATCH /orders/{orderId}

| 항목 | 내용 |
|---|---|
| 설명 | 내 주문 수정 |
| 컨트롤러 | OrderController.patchOrder |
| 권한 | 인증요구 |
| 경로 변수 | orderId (Long) |
| 요청 바디 | OrderUpdateDTO (아래 스키마) |
| 검증 | 무효 (리스트 필드에 @Valid 없음 → 원소 제약 무시) |
| 응답 200 | ApiResponse, data = OrderResponseDTO |
| 에러 | 401 미인증<br>404 ORDER_NOT_FOUND (남의 주문, 주문에 없는 상품 포함) |
| 프론트 호출 | 없음 |
| 비고 | 수량뿐 아니라 curOrderItemPrice도 클라이언트 값으로 덮어씀 (가격 조작 가능) |

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
| 비고 | 응답 바디 없음 |

## 3. 스키마

제약은 DTO 어노테이션 기준. 컨트롤러에 @Valid가 없거나 리스트 필드에 @Valid가 없으면 실제로는 검증되지 않음 (2번 상세의 "검증" 항목 참고).

### 요청 DTO

#### UserCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| signUpName | String | 필수 |
| signUpEmail | String | 필수 |
| signUpPassword | String | 필수 |
| signUpRole | String | 필수 |
| signUpPhoneNumber | String | 필수 |
| signUpBirthday | LocalDate | 필수 |

#### LogInRequestDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| email | String | 필수 |
| logInPassword | String | 필수 |

#### ProductCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| name | String | 필수 |
| price | Long | 필수, 최소 0 |
| productDetailCreateDTOList | List<ProductDetailCreateDTO> | - |

#### ProductDetailCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| detail | String | - |

#### OrderCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| orderItemCreateDTOList | List<OrderItemCreateDTO> | 필수 |

#### OrderItemCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| curOrderItemPrice | Long | 필수, 최소 0 |
| quantity | Long | 필수, 최소 0 |

#### TossPaymentRequestDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| paymentKey | String | 필수 |
| orderId | Long | 필수 |
| amount | Long | 필수, 최소 0 |

#### CartItemCreateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| quantity | Long | 필수, 최소 1 |

#### UserUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| name | String | - |
| email | String | - |
| phoneNumber | String | - |
| birthday | LocalDate | - |

#### ProductDetailUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| detail | String | - |

#### ProductUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| name | String | - |
| price | Long | - |
| productDetailUpdateDTOList | List<ProductDetailUpdateDTO> | - |

#### OrderItemUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| curOrderItemPrice | Long | 필수, 최소 0 |
| quantity | Long | 필수, 최소 1 |

#### OrderUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| orderItemResponseDTOList | List<OrderItemUpdateDTO> | - |

#### CartItemUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | 필수 |
| quantity | Long | 필수, 최소 1 |

#### CartUpdateDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| cartItemUpdateDTOList | List<CartItemUpdateDTO> | - |

### 응답 DTO

#### CartItemResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| cartItemId | Long | - |
| productItemId | Long | - |
| quantity | Long | - |

#### CartResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| userId | Long | - |
| cartItemList | List<CartItemResponseDTO> | - |
| totalCartPrice | Long | - |

#### UserCreateResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| userResponseDTO | UserResponseDTO | - |
| cartResponseDTO | CartResponseDTO | - |

#### UserResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| userId | Long | - |
| name | String | - |
| email | String | - |
| role | String | - |
| phoneNumber | String | - |
| birthday | LocalDate | - |

#### ProductDetailResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| detail | String | - |

#### ProductResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | - |
| name | String | - |
| price | Long | - |
| productDetailResponseDTOList | List<ProductDetailResponseDTO> | - |

#### OrderItemResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| productId | Long | - |
| curOrderItemPrice | Long | - |
| quantity | Long | - |
| totalOrderItemPrice | Long | - |

#### OrderResponseDTO

| 필드 | 타입 | 제약 |
|---|---|---|
| orderId | Long | - |
| orderUid | Long | - |
| orderItemResponseDTOList | List<OrderItemResponseDTO> | - |
| totalOrderPrice | Long | - |

## 4. 에러 코드

| ErrorCode | HTTP | 코드 | 기본 메시지 | 사용처 |
|---|---|---|---|---|
| INVALID_INPUT_VALUE | 400 | CM000 | Invalid input value | 미사용 |
| INTERNAL_SERVER_ERROR | 500 | CM001 | Server error | 미사용 (500은 catch-all이 "Internal Server Error"로 응답) |
| USER_NOT_FOUND | 404 | U001 | User not found | GET·PATCH·DELETE /users/me, POST /orders, GET /orders/me |
| USER_ALREADY_EXIST | 400 | U002 | User already exist | 미사용 (이메일 중복은 500) |
| USER_UPDATE_FAILED | 400 | U003 | User info cannot update | 미사용 |
| USER_PASSWORD_UNMATCHED | 400 | U004 | User password unmatched | POST /users/login |
| EMAIL_NOT_FOUND | 400 | U005 | Email not found | POST /users/login |
| PRODUCT_NOT_FOUND | 404 | P001 | Cannot found product | GET·PATCH·DELETE /products/{productId}, POST /carts |
| PRODUCT_ALREADY_EXIST | 400 | P002 | Product Already Exist | 미사용 |
| PRODUCT_OUT_OF_STOCK | 400 | P003 | Product quantity is less than 1 | 미사용 (재고 로직 미구현) |
| CART_NOT_FOUND | 404 | C001 | Cannot found cart | POST /carts, GET·PATCH·DELETE /carts/me, DELETE /carts/items/{productId} |
| CART_ALREADY_EXIST | 400 | C002 | Cart Already Exist | 미사용 |
| CART_EMPTY | 400 | C003 | There are no CartItem in Cart | 미사용 |
| CART_ITEM_NOT_FOUND | 404 | CT001 | Cannot found cart item | DELETE /carts/items/{productId} |
| ORDER_NOT_FOUND | 404 | O001 | Cannot found Order | GET·PATCH·DELETE /orders/{orderId}, POST /orders/toss/payment/auth |
| ORDER_PRICE_UNMATCHED | 400 | O002 | Unmatched Price Info | POST /orders/toss/payment/auth |
| REFRESH_TOKEN_NOT_FOUND | 400 | RD001 | Cannot found refresh token | DELETE /users/logout |
| PAYMENT_FAILED | 400 | PA001 | Payment Failed | POST /orders/toss/payment/auth |
| TOSS_SERVER_ERROR | 400 | TS001 | Toss Server Error | 미사용 |

예외 생성 시 메시지를 따로 넘기면 기본 메시지 대신 그 메시지가 응답됨 (예: USER_NOT_FOUND → "Cannot Found User (3)").

## 5. 명세 기준으로 드러난 문제

| 심각도 | 대상 | 문제 | 계획 |
|---|---|---|---|
| 높음 | POST /users/signup | signUpRole을 클라이언트가 지정 → ADMIN 가입 가능 | Phase 1 |
| 높음 | POST /products, PATCH·DELETE /products/{productId} | 인증 없이 상품 등록·수정·삭제 가능 | Phase 1 |
| 높음 | POST /orders, PATCH /orders/{orderId} | 상품 가격을 클라이언트 값으로 저장·수정 → 토스 승인은 이 가격과 대조하므로 낮은 금액으로 결제 가능 | Phase 6 (주문 가격 서버 재조회) |
| 중간 | GET /users, GET /carts, GET /orders | 로그인만 하면 전체 데이터 조회 가능 | Phase 1 |
| 중간 | POST /orders/toss/payment/auth | 공개 결정이 SecurityConfig에 미반영 → 비로그인 결제 승인 401 | Phase 1 |
| 중간 | POST /carts, POST /products | @Valid 없음 → 음수 수량·빈 상품명 등이 그대로 저장 | Phase 1 |
| 중간 | PATCH /carts/me, PATCH /orders/{orderId} | 리스트 필드에 @Valid 없음 → 원소 제약 무시 | Phase 1~2 |
| 중간 | POST /users/signup | 이메일 중복 시 400이 아니라 500 | 미정 |
| 중간 | GET /users/find-id, POST /users/find-password | 프론트는 호출하지만 백엔드 미구현 | 결정 필요 |
| 낮음 | DELETE /users/logout | 쿠키 만료 없음, access token 만료 시 로그아웃 불가 | Phase 5 |
| 낮음 | POST /users/login | 실패 메시지로 가입 여부 노출 | Phase 5 |
| 낮음 | 공통 | 에러 바디에 ErrorCode 코드 문자열 없음 (프론트가 메시지 문자열로 분기해야 함) | 미정 |
