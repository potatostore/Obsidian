---
created: 2026-11-02
branch: fix/all → dev
commit: 7fc2d80
tags: [nimda, pr, refactoring, exception, error-code]
---

# fix/all → dev : ErrorCode 기반 전역 예외 처리 & 컨트롤러 리팩토링

cite 도메인 컨트롤러의 try/catch + Map 응답을 걷어내고, 예외를 ErrorCode 기반으로 통일한 PR.

- 범위: backend-spring/src/main/java/com/nimda/cite/ (judgeServer, redis 변경 없음)
- 규모: 143 files, +3,932 / −2,846
- 응답 모양: 기존 dev와 동일하게 유지 → **프론트 수정 불필요**
- 관련 노트: [[Map 응답 매핑 현황 (WAS ↔ Web)]]

## 한눈에 보기

| 구분 | 핵심 변경 |
|---|---|
| [[#1. 전역 예외 처리 — GlobalExceptionHandler\|전역 예외 처리]] | ResponseEntityExceptionHandler 상속, 모든 에러를 {success:false, message}로 통일 |
| [[#2. 커스텀 예외 — GlobalNimdaException 계층\|커스텀 예외]] | GlobalNimdaException 상속 예외 9종 |
| [[#3. 에러 코드 — ErrorCode\|에러 코드]] | ErrorCode 인터페이스 + 도메인별 enum 14개, 코드 106개 |
| [[#4. 응답 형식 & DTO\|응답 DTO]] | Map 응답 → DTO 전환 (JSON 키는 그대로) |
| [[#5. 컨트롤러 → 서비스 계층 이동\|서비스 계층 이동]] | 권한·검증·변환 로직을 서비스로 이동, 컨트롤러는 호출 + 응답만 |
| [[#6. 엔티티\|엔티티]] | User/Authority setter 제거, 도메인 메서드 도입 |
| [[#7. 상수 · 유틸\|상수·유틸]] | TableNames, UrlNames, CheckConfig, CustomUserDetails.getLoginUser |
| [[#8. 의존성 주입 · 패키지 정리\|DI · 패키지]] | 컨트롤러 전부 private final + @RequiredArgsConstructor, 패키지명 정리 |

---

## 1. 전역 예외 처리 — GlobalExceptionHandler

common/exception/GlobalExceptionHandler.java · @RestControllerAdvice + extends ResponseEntityExceptionHandler

| 처리 대상 | HTTP 상태 | 응답 message | 비고 |
|---|---|---|---|
| GlobalNimdaException (커스텀 예외 전체) | ErrorCode.httpStatus | 예외 메시지 (기본값 ErrorCode.message) | 비즈니스 예외의 기본 경로 |
| MethodArgumentNotValidException (@Valid) | 400 | 첫 번째 필드 에러의 message | handleMethodArgumentNotValid 오버라이드 |
| Spring MVC 내부 예외 (405, 415, 파라미터 누락 등) | 원래 상태 유지 | 4xx → CO001, 5xx → CO003 메시지 | handleExceptionInternal 오버라이드 |
| AccessDeniedException (@PreAuthorize) | 403 | CO002 | Exception 핸들러에 먹혀 500이 되지 않도록 분리 |
| AuthenticationException | 401 | AE001 | |
| IllegalArgumentException (CheckConfig 등) | 400 | CO001 | 내부 메시지 비노출 |
| ResponseStatusException (judgeServer) | 던진 상태 유지 | reason | 기존 핸들러 유지 |
| Exception (그 외 전부) | 500 | CO003 | 내부 메시지 비노출, log.error로 스택 기록 |

- 로그: 예상한 예외는 warn (errorNum - message), 예상하지 못한 예외는 error
- 컨트롤러의 try/catch 및 ApiResponse.fail(...) 직접 반환은 전부 제거 → 예외를 던지면 핸들러가 응답


---

## 2. 커스텀 예외 — GlobalNimdaException 계층

- 위치: common/exception/
- 모든 예외는 GlobalNimdaException(ErrorCode) / (ErrorCode, String message) 생성자 2개를 가진다.
- **HTTP 상태는 예외 클래스가 아니라 ErrorCode가 결정**

| 예외 | 의미 | 대표 상태 | 사용 수 | 주요 사용처 |
|---|---|---|---|---|
| GlobalNimdaException | 최상위 (RuntimeException, ErrorCode 보유) | – | – | 전역 핸들러에서 일괄 처리 |
| NotFoundException | 리소스 없음 | 404 | 75 | 거의 모든 서비스 |
| NotAllowFormException | 입력 형식·값 오류 | 400 | 34 | Attachment, Board, Category, PointUsage, ProfileDecoration, S3Service |
| NotIncludeRoleException | 권한 없음 | 403 | 18 | Board, Category, Comment, Attachment, Auth, FileDownload |
| InvalidStateException | 현재 상태 때문에 처리 불가 (중복 출석, 삭제된 댓글 수정, 잔액 부족 등) | 400 | 14 | Comment, Attendance, Attachment, Category, PointUsage |
| UnauthorizedException | 인증 실패·로그인 필요 | 401 / 403 | 8 | CustomUserDetails.getLoginUser, Auth, UserRecovery, Category |
| AlreadyExistException | 중복 (회원, 닉네임, slug, 배지 키, 보유 배지) | 400 | 5 | User, Auth, Category, ProfileDecoration, PointUsage |
| UserNotApprovedException | 승인 대기·거부 계정 로그인 | 403 | 3 | AuthService.validateUser |
| ExternalServiceException | S3 등 외부 서비스 실패 | 503 / 500 | 3 | Attachment, ProfileDecoration |
| VersionMismatchException | 앱 버전 불일치 | 426 | 1 | VersionCheckInterceptor |

---

## 3. 에러 코드 — ErrorCode

- ErrorCode 인터페이스: getHttpStatus(), getErrorNum(), getMessage()
- 도메인별 enum이 구현 → 위치 common/exception/errorcode/{common, user, domain}/ (enum 14개, 코드 106개)
- 배정 기준: 코드 하나를 실제로 발생하는 컨트롤러 하나에 배정. 여러 컨트롤러에서 발생하면 도메인 컨트롤러에 배정

### 공통 (5)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| AE001 | CANNOT_AUTHORIZED | 401 | 인증이 필요합니다. |
| CO001 | INVALID_INPUT | 400 | 잘못된 요청입니다. |
| CO002 | ACCESS_DENIED | 403 | 접근 권한이 없습니다. |
| CO003 | INTERNAL_SERVER_ERROR | 500 | 서버 오류가 발생했습니다. |
| CO004 | VERSION_MISMATCH | 426 | 앱 버전이 일치하지 않습니다. 최신 버전으로 업데이트 해주세요. |

> CO 코드는 전역 핸들러·버전 인터셉터에서, AE001은 로그인이 필요한 모든 API(CustomUserDetails.getLoginUser)에서 발생

### AuthController (10)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| AE002 | USER_NOT_FOUND | 404 | 해당 유저 정보를 찾을 수 없습니다. |
| AE003 | STATUS_PENDING | 403 | 승인 대기 중인 계정입니다. 관리자 승인 후 로그인할 수 있습니다. |
| AE004 | STATUS_REJECTED | 403 | 승인이 거부된 계정입니다. |
| AE005 | STATUS_NOT_APPROVED | 403 | 승인되지 않은 계정입니다. |
| AE006 | INVALID_CREDENTIALS | 401 | Invalid user ID or password |
| PD003 | DECORATION_NOT_USABLE | 400 | 사용할 수 없는 프로필 장식입니다. |
| PD005 | DECORATION_NOT_OWNED | 403 | 보유한 프로필 장식만 사용할 수 있습니다. |
| UE001 | USER_ALREADY_EXIST | 400 | 해당 정보를 가진 유저가 이미 존재합니다. |
| UE003 | NICKNAME_ALREADY_EXIST | 400 | 이미 사용 중인 닉네임입니다. |
| UE004 | PROFILE_IMAGE_KEY_REQUIRED | 400 | 프로필 이미지 키가 필요합니다. |

> PD003·PD005는 프로필 장식 변경(PUT /api/auth/profile-decoration)에서 발생

### UsersController (1)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| UE002 | USER_NOT_FOUND | 404 | 사용자를 찾을 수 없습니다. |

> UE002는 닉네임으로 사용자를 찾는 다른 API(게시글·댓글·좋아요·포인트 조회 등)에서도 발생

### AdminUserController (8)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| US001 | USER_NOT_FOUND | 404 | User not found |
| US002 | USER_PENDING_FAILED (미사용) | 400 | User pending failed |
| US003 | USER_CONVERT_ROLE_FAILED (미사용) | 400 | User role convert failed |
| US004 | USER_CONVERT_STATUS_FAILED (미사용) | 400 | User status convert failed |
| US005 | USER_ROLE_NOT_FOUND | 500 | User role not found |
| US006 | USER_GRANT_ROLE_FAILED (미사용) | 400 | User role grant failed |
| US007 | USER_REVOKE_ROLE_FAILED (미사용) | 400 | User role revoke failed |
| US008 | AUTHORITY_NOT_EXIST | 400 | Authority not found |

> 미사용 5개(US002~US004, US006, US007)는 정리 대상. 메시지가 영어라 관리자 화면 alert에 그대로 노출

### UserRecoveryController (3)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| UR001 | RECOVERY_SESSION_EXPIRED | 403 | 인증 세션이 만료되었습니다. |
| UR002 | AUTH_CODE_MISMATCH | 401 | 인증에 실패했습니다. |
| UR003 | EMAIL_NOT_VERIFIED | 403 | 이메일 인증이 완료되지 않은 요청입니다. |

### BoardController (23)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| BO001 | BOARD_NOT_FOUND | 404 | 게시글을 찾을 수 없습니다. |
| BO002 | BOARD_ACCESS_DENIED | 403 | 접근 권한이 없습니다. |
| BO003 | BOARD_UPDATE_FORBIDDEN | 403 | 게시글을 수정할 권한이 없습니다. |
| BO004 | BOARD_DELETE_FORBIDDEN | 403 | 게시글을 삭제할 권한이 없습니다. |
| BO005 | BOARD_PIN_FORBIDDEN | 403 | 게시글을 고정/해제할 권한이 없습니다. 관리자만 가능합니다. |
| BO006 | NEWS_UPDATE_FORBIDDEN | 403 | 새 소식 게시판은 관리자만 수정할 수 있습니다. |
| BO007 | SHOP_WRITE_FORBIDDEN | 403 | 상품 등록은 관리자만 가능합니다. |
| BO008 | SHOP_UPDATE_FORBIDDEN | 403 | 상품 수정은 관리자만 가능합니다. |
| BO009 | INVALID_ITEM_PRICE | 400 | 상품 가격을 1 NC 이상으로 입력해주세요. |
| BO010 | INVALID_ITEM_TYPE | 400 | 지원하지 않는 상품 종류입니다. |
| BO011 | SHOP_BADGE_REQUIRED | 400 | 배지 상품은 배지를 선택해야 합니다. |
| BO012 | SHOP_BADGE_NOT_FOUND | 404 | 존재하지 않는 배지입니다. |
| BO013 | SHOP_BADGE_INACTIVE | 400 | 비활성화된 배지는 상품으로 등록할 수 없습니다. |
| BO014 | SHOP_THUMBNAIL_REQUIRED | 400 | 마일리지 상점 상품은 썸네일 이미지가 필요합니다. |
| BO015 | DELETE_TARGET_REQUIRED | 400 | 삭제할 게시글을 선택해주세요. |
| CT002 | INVALID_SLUG | 400 | 유효하지 않은 카테고리 slug입니다. |
| CT003 | CATEGORY_PARAM_REQUIRED | 400 | categoryId 또는 slug 파라미터가 필요합니다. |
| TG002 | TAG_NOT_IN_CATEGORY | 400 | 이 태그는 해당 카테고리에 속하지 않습니다. |
| UF009 | ATTACHMENT_LINK_FORBIDDEN | 403 | 첨부 소유자만 게시글에 연결할 수 있습니다. |
| UF010 | ATTACHMENT_ALREADY_LINKED | 400 | 이미 다른 게시글에 연결된 첨부입니다. |
| UF011 | ATTACHMENT_CATEGORY_MISMATCH | 400 | 첨부 카테고리가 게시글 카테고리와 일치하지 않습니다. |
| UF012 | ATTACHMENT_REMOVE_FORBIDDEN | 403 | 다른 사용자가 올린 첨부는 제거할 수 없습니다. |
| UF013 | INVALID_THUMBNAIL | 400 | 썸네일은 첨부된 이미지 중에서 선택해야 합니다. |

> CT002·CT003(카테고리 조회 파라미터), UF009~UF013(첨부 연결), TG002(태그 소속)는 게시글 작성·수정·목록 API에서 발생

### CategoryController (10)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| CT001 | CATEGORY_NOT_FOUND | 404 | 카테고리를 찾을 수 없습니다. |
| CT004 | ADMIN_REQUIRED | 403 | 관리자 권한이 필요합니다. |
| CT005 | SELF_PARENT_NOT_ALLOWED | 400 | 자기 자신을 부모로 설정할 수 없습니다. |
| CT006 | CIRCULAR_REFERENCE | 400 | 순환 참조가 발생합니다. 해당 카테고리를 부모로 설정할 수 없습니다. |
| CT007 | HAS_CHILD_CATEGORY | 400 | 하위 카테고리가 존재하여 삭제할 수 없습니다. 먼저 하위 카테고리를 삭제하거나 비활성화하세요. |
| CT008 | HAS_POSTS | 400 | 해당 카테고리에 게시글이 존재하여 삭제할 수 없습니다. |
| CT009 | SLUG_ALREADY_EXIST | 400 | 이미 사용 중인 슬러그입니다. |
| CT010 | PARENT_NOT_FOUND | 404 | 부모 카테고리를 찾을 수 없습니다. |
| CT011 | INACTIVE_PARENT | 400 | 비활성화된 카테고리는 부모로 설정할 수 없습니다. |
| CT012 | MAX_DEPTH_EXCEEDED | 400 | 카테고리는 최대 2단계까지만 설정 가능합니다. |

### TagController (1)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| TG001 | TAG_NOT_FOUND | 404 | 태그가 존재하지 않습니다. |

### CommentController (9)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| CM001 | COMMENT_NOT_FOUND | 404 | 댓글을 찾을 수 없습니다. |
| CM002 | PARENT_COMMENT_NOT_FOUND | 404 | 부모 댓글을 찾을 수 없습니다. |
| CM003 | REPLY_DEPTH_EXCEEDED | 400 | 대댓글에는 답글을 달 수 없습니다. |
| CM004 | PARENT_COMMENT_DELETED | 400 | 삭제된 댓글에는 답글을 달 수 없습니다. |
| CM005 | DELETED_COMMENT_STATUS_CHANGE | 400 | 삭제된 댓글은 상태를 변경할 수 없습니다. |
| CM006 | COMMENT_UPDATE_FORBIDDEN | 403 | 댓글 수정 권한이 없습니다. |
| CM007 | DELETED_COMMENT_UPDATE | 400 | 삭제된 댓글은 수정할 수 없습니다. |
| CM008 | COMMENT_DELETE_FORBIDDEN | 403 | 댓글 삭제 권한이 없습니다. |
| CM009 | COMMENT_ALREADY_DELETED | 400 | 이미 삭제된 댓글입니다. |

### AttachmentController (9)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| UF001 | UPLOAD_FILE_NOT_FOUND | 404 | 업로드할 파일이 없습니다. |
| UF002 | FILE_FORM_NOT_ALLOW | 400 | 허용되지 않는 파일 형식입니다 |
| UF003 | FILE_ROLE_NOT_EXIST | 403 | 삭제 권한이 없는 파일이 포함되어 있습니다 |
| UF004 | S3_KEY_INNEED | 400 | S3 key가 필요합니다. |
| UF005 | ATTACHMENT_NOT_FOUND | 404 | 파일이 존재하지 않습니다. |
| UF006 | FILE_IDS_REQUIRED | 400 | fileIds가 필요합니다. |
| UF007 | FILE_STORAGE_UNAVAILABLE | 503 | 파일 업로드 서비스를 사용할 수 없습니다. |
| UF008 | IMAGE_PROCESSING_FAILED | 500 | 이미지 처리에 실패했습니다. |
| UF016 | FILE_NOT_FOUND | 404 | 파일을 찾을 수 없습니다. |

### FileDownloadController (3)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| UF014 | INVALID_FILE_NAME | 400 | 잘못된 파일명입니다. |
| UF015 | INVALID_FILE_PATH | 403 | 잘못된 파일 경로입니다. |
| UF017 | FILE_READ_FORBIDDEN | 403 | 파일에 접근할 권한이 없습니다. |

### AttendanceController (2)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| AT001 | ALREADY_CHECKED_IN | 400 | 이미 오늘 출석을 완료했습니다. |
| AT002 | ATTENDANCE_NOT_FOUND | 404 | 출석 정보가 없습니다. |

### NotificationController (1)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| NT001 | NOTIFICATION_NOT_FOUND | 404 | 알림이 존재하지 않습니다. |

### PointController (2)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| PT001 | BALANCE_NOT_FOUND | 404 | 포인트 계좌가 존재하지 않습니다. |
| PT002 | BALANCE_NOT_FOUND_PENDING | 404 | 포인트 계좌가 존재하지 않습니다! 승인 대기 중일 수 있습니다. |

### PointUsageController (7)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| PT003 | ITEM_NOT_PURCHASABLE | 400 | 구매할 수 없는 상품입니다. |
| PT004 | NOT_SHOP_ITEM | 400 | 마일리지 구매 상품이 아닙니다. |
| PT005 | ITEM_PRICE_NOT_SET | 400 | 상품 가격이 설정되지 않았습니다. |
| PT006 | ITEM_BADGE_NOT_LINKED | 400 | 상품에 연결된 배지가 없습니다. |
| PT007 | BADGE_ALREADY_OWNED | 400 | 이미 보유한 배지입니다. |
| PT008 | INVALID_SPEND_AMOUNT | 400 | 차감할 마일리지가 올바르지 않습니다. |
| PT009 | INSUFFICIENT_BALANCE | 400 | 보유 마일리지가 부족합니다. |

### ProfileDecorationController (12)

| 코드 | 상수 | HTTP | 메시지 |
|---|---|---|---|
| PD001 | DECORATION_NOT_FOUND | 404 | 존재하지 않는 프로필 장식입니다. |
| PD002 | BADGE_NOT_FOUND | 404 | 존재하지 않는 프로필 배지입니다. |
| PD004 | BADGE_NOT_USABLE | 400 | 사용할 수 없는 프로필 배지입니다. |
| PD006 | BADGE_KEY_REQUIRED | 400 | 배지 키를 입력해주세요. |
| PD007 | BADGE_KEY_INVALID | 400 | 배지 키는 영문 소문자, 숫자, 하이픈만 사용할 수 있습니다. |
| PD008 | BADGE_LABEL_REQUIRED | 400 | 배지 이름을 입력해주세요. |
| PD009 | BADGE_IMAGE_REQUIRED | 400 | 배지 이미지 경로가 필요합니다. |
| PD010 | BADGE_KEY_ALREADY_EXIST | 400 | 이미 존재하는 배지 키입니다. |
| PD011 | STUDENT_NUM_REQUIRED | 400 | studentNum 값이 필요합니다. |
| PD012 | DECORATION_ID_REQUIRED | 400 | decorationId 값이 필요합니다. |
| PD013 | STUDENT_NUM_NOT_FOUND | 404 | 존재하지 않는 학번입니다. |
| PD014 | IMAGE_SERVICE_UNAVAILABLE | 503 | 배지 이미지 서비스를 사용할 수 없습니다. |

---

## 4. 응답 형식 & DTO

Map 응답을 DTO로 바꾸되, **JSON 키는 dev와 동일하게 유지**했다. (ApiResponse로 새로 감싸면 값이 data 아래로 내려가 프론트의 result.x가 undefined가 되므로, 원래 최상위로 내려가던 응답은 최상위 그대로 둠)

| 유형 | 형태 | JSON | 적용 |
|---|---|---|---|
| A형 | ApiResponse.ok(msg, XxxResponseDTO) | {success, message, data: {...}} | 게시판, 댓글, 첨부, 좋아요, 출석, 포인트, 카테고리, 태그, 알림, 프로필 배지, PUT /api/auth/me |
| B형 | ResponseEntity.ok(XxxResponseDTO) (DTO가 success/message 포함) | {success, message?, ...} | 로그인, 관리자 사용자, 프로필 이미지·장식, 이메일 숨김, 관리자 태그 통계 |
| DTO 그대로 | ResponseEntity.ok(XxxResponseDTO) | {...} | 내 정보, 공개 프로필, 회원가입 |
| 문자열 | ResponseEntity\<String\> | text/plain | send-authMail, check-authcode, change-password |
| 에러 | ApiResponse.fail(message) | {success:false, message} | 전역 핸들러 |

→ 만약 모든 컨트롤러 반환을 ApiResponse로 통일시키고 싶으면, 프론트 내 dto받는 형식도 통일 시켜주기

### 응답 DTO

| DTO | 필드 | 엔드포인트 | 유형 |
|---|---|---|---|
| AttachmentUploadResponseDTO | attachmentId | POST /api/cite/attachments/upload, /register | A |
| AttachmentDetailResponseDTO | attachment | GET /api/cite/attachments/{id} | A |
| AttachmentDownloadUrlResponseDTO | downloadUrl | GET /api/cite/attachments/{id}/download-url | A |
| AttachmentListResponseDTO | attachments | GET /api/cite/attachments/my | A |
| AttachmentPresignedUploadResponseDTO | uploadUrl, key | POST /api/cite/attachments/presigned | A |
| AttendanceVisitCountResponseDTO | visitCount | GET /api/cite/attendance | A |
| BoardDetailResponseDTO | board | POST /api/cite/board, GET·PUT /{id}, PATCH /{id}/pin | A |
| BoardDeletedResponseDTO | deleted | GET /api/cite/board/{id} (삭제된 글) | A |
| BoardPostCountResponseDTO | postCount | GET /api/cite/board/my/board-count | A |
| CommentDetailResponseDTO | comment | POST /api/board/{boardId}/comments, PATCH /api/comments/{id}, /status | A |
| CommentListResponseDTO | comments | GET /api/board/{boardId}/comments | A |
| MyCommentListResponseDTO | comments | GET /api/my-page/comments, GET /api/comments/user/{nickname} | A |
| CommentCountResponseDTO | commentCount | GET /api/comments/my/count | A |
| BoardLikeListResponseDTO | boards | GET /api/like/board/pushedLikes, /user/{nickname}/liked | A |
| BoardLikeCountResponseDTO | likeCount | GET /api/like/board/pushedLikes/count | A |
| LoginSuccessResponseDTO | success, message, user (토큰은 쿠키로만) | POST /api/auth/login | B |
| AdminUsersResponseDTO\<T\> | success, users, count(대기 목록만) | GET /api/admin/users, /pending, /suggestions | B |
| AdminUserResponseDTO | success, message(승인·거부만), user | GET /api/admin/users/{id}, PUT /{id}/approve, /reject | B |
| AdminUserRolesResponseDTO | success, message(부여·제거만), roles | GET /api/admin/users/roles, PUT /{id}/role, /role/remove | B |
| ProfileImageUpdateResponseDTO | success, message, profileImageUrl, profileImageKey | PUT /api/auth/profile-image | B |
| ProfileDecorationUpdateResponseDTO | success, message, profileDecoration | PUT /api/auth/profile-decoration | B |
| EmailHideUpdateResponseDTO | success, emailHide, message | POST /api/auth/email-hide | B |
| BoardTagStatsResponseDTO | success, categoryId, tagStats[] (tagId, tagName, activeCount, hiddenCount) | GET /api/admin/boards/tag-stats | B |
| BoardTagStatusUpdateResponseDTO | success, message, affectedCount | PUT /api/admin/boards/deactivate-by-tag, /activate-by-tag | B |
| UserPublicProfileResponseDTO | nickname, profileImage, profileDecoration, bojId, major, createdAt, email(숨김 시 제외) | GET /api/users/nickname/{nickname} | 그대로 |
| RegisterResponseDTO | id, userId, name, nickname, studentNum, email, major, birth, bojId | POST /api/auth/register | 그대로 |
| AdminUserListResponseDTO | id, userId, nickname, email, createdAt | 관리자 목록의 users[] 원소 | – |
| AdminUserDetailResponseDTO | id, userId, name, nickname, email, studentNum, major, birth, status, createdAt, updatedAt, roles, profileImage, profileDecoration | 관리자 user 원소 | – |

### 요청 DTO

| DTO | 필드 | 엔드포인트 | 비고 |
|---|---|---|---|
| LoginRequestDTO | userId, password | POST /api/auth/login | LoginDTO에서 이름 변경 |
| RegisterRequestDTO | userId, name, nickname, password, studentNum, email, major, birth, bojId | POST /api/auth/register | RegisterDTO에서 이름 변경 |
| BoardWriteRequestDTO | categoryId, title, content, tagId, attachmentIds, pinned, itemPrice, itemType, profileDecorationId, thumbnailAttachmentId | POST /api/cite/board, PUT /{id} | 신규, 요청 body 아님 — 컨트롤러가 @RequestParam 값으로 만들어 서비스에 전달 |
| AdminUserRoleUpdateRequestDTO | role | PUT /api/admin/users/{id}/role, /role/remove | Map\<String,String\> 대체 |
| ProfileImageUpdateRequestDTO | profileImageKey | PUT /api/auth/profile-image | Map\<String,String\> 대체 |
| ProfileDecorationUpdateRequestDTO | profileDecorationKey | PUT /api/auth/profile-decoration | Map\<String,String\> 대체 |
| ProfileDecorationGrantRequestDTO | studentNum, decorationId | POST /api/cite/admin/profile-decorations/ownership/grant, /revoke | 신규 |

---

## 5. 컨트롤러 → 서비스 계층 이동

컨트롤러는 "로그인 사용자 꺼내기 → 서비스 호출 → 응답"만 하고, 권한·검증·변환은 서비스가 담당한다. 로그인 필수 API는 CustomUserDetails.getLoginUser() (없으면 401).

| 도메인               | 옮긴 로직                                                                                                                      | 서비스 메서드                                                                                              |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Board             | 작성·수정 권한 (뉴스·상점·작성자·관리자, ROLE_DEV 패치 태그), 카르텔 접근 체크, 태그 소속 검증, 상점 상품 검증 (가격·종류·배지·썸네일), 조회 + 접근 체크, 카테고리 ID/slug 해석, 태그 통계 | writeBoard, updateBoard, viewBoard, deleteBoard, checkCategoryReadable, resolveCategory, getTagStats |
| Auth · User       | 로그인 검증 (Optional 반환 → 예외), 회원가입 + 포인트 계좌(UserBalance) 생성, 프로필 이미지 키 검증, 닉네임 조회                                             | AuthService.validateUser, register, UserService.createUser, getUserByNickname                        |
| AdminUser         | 엔티티 → DTO 변환 (컨트롤러에서 하던 것)                                                                                                 | findAll, findByStatus, findById, approveUser, rejectUser, grantRole, revokeRole, findUserSuggestions |
| UserRecovery      | 메일 발송 전 토큰 검증, 인증 코드 확인 + 토큰 재발급, 비밀번호 변경 토큰 검증                                                                            | sendAuthMail, verifyAuthCode, validatePasswordChangeToken                                            |
| Attachment        | 업로드 결과 DTO 변환, presigned 다운로드 URL 생성                                                                                       | uploadFile, getAttachment, createPresignedDownloadUrl                                                |
| FileDownload      | 파일명·경로 검증 (Path Traversal), 존재·읽기 권한 확인 → **신규 서비스**                                                                       | FileDownloadService.getDownloadFile                                                                  |
| Comment           | 닉네임으로 댓글 조회                                                                                                                | getCommentsByNickname                                                                                |
| ProfileDecoration | 배지 이미지 URL 생성                                                                                                              | getDecorationImageUrl                                                                                |
| Category          | 예외 메시지 문자열 매칭 ("권한" 포함 시 403) 제거 → ErrorCode로 상태 결정                                                                        | –                                                                                                    |

---

## 6. 엔티티

| 대상 | 변경 | 비고 |
|---|---|---|
| User | @Setter, @AllArgsConstructor, public 기본 생성자 제거 → @NoArgsConstructor(PROTECTED) + @Builder 생성자 | 외부에서 임의 수정 불가 |
| User 도메인 메서드 | changeStatus, toggleEmailHide, changeProfileImage, changeProfileDecoration, changePassword, updateProfile, addAuthority, removeAuthority | addAuthority는 이름으로 중복 검사 (Authority가 equals 미구현이라 Set.contains 대신) |
| Authority | @Setter → @Builder | |
| cite 엔티티 전체 | @Table(name = TableNames.X) | 테이블명·컬럼 변경 없음 (ddl-auto: none) |
| Attendance, Notification | @Table 신규 추가 | 기본 네이밍 전략과 같은 이름 (attendance, notification) |

---

## 7. 상수 · 유틸

| 클래스                                                 | 위치                 | 역할                                                                |
| --------------------------------------------------- | ------------------ | ----------------------------------------------------------------- |
| TableNames                                          | common/util        | 테이블명 상수 (judgeServer 테이블 상수도 정의만 되어 있음, 적용은 cite만)                |
| UrlNames                                            | common/util        | 컨트롤러 매핑 경로 상수 (클래스 base + 메서드 path) — dev 대비 135개 경로 동일           |
| CheckConfig                                         | config             | npeCheck, npeAndBlankCheck, npeAndNegativeCheck, npeAndEmptyCheck |
| CustomUserDetails.getLoginUser / getLoginUserOrNull | user/security      | 로그인 필수 (없으면 401) / 비로그인 허용                                        |
| MailSendResult                                      | user/enums         | OK, UNAUTHORIZED, LIMIT_EXCEEDED (인증 메일 발송 결과)                    |
| VersionCheckInterceptor                             | common/interceptor | VersionMismatchException(CO004) 사용                                |
| S3Service                                           | common/s3          | 허용되지 않은 확장자 → NotAllowFormException(UF002)                        |

---

## 8. 의존성 주입 · 패키지 정리

### 의존성 주입 — cite 컨트롤러 20개 전부 private final + @RequiredArgsConstructor

| 변경 전 | 대상 |
|---|---|
| @Autowired 필드 주입 | Auth, AdminUser, UserRecovery, Users, Board, Category, Comment, AdminBoard, Attachment 등 |
| @RequiredArgsConstructor + S3Service만 @Autowired(required = false) | Attendance, Notification |
| 명시적 생성자 | FileDownload, ProfileDecoration |
