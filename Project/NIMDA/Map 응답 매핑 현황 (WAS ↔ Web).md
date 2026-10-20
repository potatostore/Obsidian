---
created: 2026-10-19
branch: fix/all
tags: [nimda, refactoring, map-to-dto]
---

# Map 응답 매핑 현황 (WAS ↔ Web)

Controller에서 `Map<>`으로 응답을 내려주는 모든 지점과, 그걸 받는 프론트(`NimdaConFrontEnd/src/`) 호출부 정리.

- WAS 경로 기준: `NimdaConBackEnd/backend-spring/src/main/java/`
- Web 경로 기준: `NimdaConFrontEnd/src/`

## 핵심 구분

| 유형 | 형태 | JSON 모양 | DTO 전환 시 영향 |
|---|---|---|---|
| **A형** | `ApiResponse.ok(..., Map.of("key", v))` | `{ success, message, data: { key: v } }` | 키 이름 유지한 DTO로 바꾸면 **프론트 수정 불필요**. 래핑을 없애고 펼치면(`data.board` → `data`) 프론트 수정 필요 |
| **B형** | `ResponseEntity.ok(Map.of(...))` (ApiResponse 미사용) | 최상위에 필드 직접 | `ApiResponse`로 감싸면 필드가 `data` 아래로 내려가서 **최상위를 읽는 프론트가 깨짐** |

---

## A형 — `ApiResponse.ok(..., Map.of(...))`

| Endpoint | WAS 위치 | data 키 | Web 호출부 | Web에서 읽는 방식 |
|---|---|---|---|---|
| `POST /api/cite/board` | `BoardController.java:495` | `board` | `api/board.ts:177` `createBoardAPI` | `data.board \|\| result.board` |
| `GET /api/cite/board/{id}` (삭제글) | `BoardController.java:516` | `deleted` | `api/board.ts:126` `getBoardDetailAPI` | `data.deleted` |
| `GET /api/cite/board/{id}` | `BoardController.java:533` | `board` | 〃 | `data.board \|\| result.board` |
| `PUT /api/cite/board/{id}` | `BoardController.java:660` | `board` | `api/board.ts:257` `updateBoardAPI` | `data.board \|\| result.board` |
| `PATCH /api/cite/board/{id}/pin` | `BoardController.java:723` | `board` (**엔티티 직접 반환**) | `api/board.ts:690` `toggleBoardPinAPI` (**호출처 없음**) | `data.board` |
| `GET /api/cite/board/my/board-count` | `BoardController.java:746` | `postCount` | `api/board.ts:731` `getMyBoardCountAPI` | `result.data.postCount` |
| `POST /api/board/{boardId}/comments` | `CommentController.java:74` | `comment` | `api/comment.ts:73` `createCommentAPI` | `resData.comment ?? result.comment` |
| `GET /api/board/{boardId}/comments` | `CommentController.java:102` | `comments` | `api/comment.ts:125` `getCommentsAPI` | `resData.comments` |
| `GET /api/my-page/comments` | `CommentController.java:122` | `comments` | `api/comment.ts:299` `getMyCommentsAPI` | `result.data?.comments` |
| `PATCH /api/comments/{id}` | `CommentController.java:147` | `comment` | `api/comment.ts:166` `updateCommentAPI` | `resData.comment` |
| `PATCH /api/comments/{id}/status` | `CommentController.java:171` | `comment` | `api/comment.ts:213` `updateCommentStatusAPI` | `resData.comment` |
| `GET /api/comments/my/count` | `CommentController.java:220` | `commentCount` | `api/comment.ts:344` `getMyCommentCountAPI` | `result.data.commentCount` |
| `GET /api/comments/user/{nickname}` | `CommentController.java:261` | `comments` | `api/user.ts:143` `getUserCommentsByNickname` | `data.data?.comments` |
| `POST /api/cite/attachments/upload` | `AttachmentController.java:60` | `attachmentId` | `api/attachments.ts` `uploadBoardFileLocally` (~205) | `data.attachmentId` |
| `GET /api/cite/attachments/{id}` | `AttachmentController.java:71` | `attachment` | **프론트 미사용** (Bruno만) | – |
| `GET /api/cite/attachments/{id}/download-url` | `AttachmentController.java:139`, `:145` | `downloadUrl` | `api/attachments.ts:278` `getAttachmentPresignedUrl`, `:299` `openAttachmentDownloadInNewTab` | `data.downloadUrl` |
| `GET /api/cite/attachments/my` | `AttachmentController.java:159` | `attachments` | **프론트 미사용** (Bruno만) | – |
| `POST /api/cite/attachments/presigned` | `AttachmentController.java:200` | `uploadUrl`, `key` | `api/attachments.ts:100` `requestPresignedUpload` | `data.uploadUrl`, `data.key` |
| `POST /api/cite/attachments/register` | `AttachmentController.java:233` | `attachmentId` | `api/attachments.ts:170` `registerAttachmentAfterS3` | `data.attachmentId` |
| `GET /api/like/board/user/{nickname}/liked` | `BoardLikeController.java:50` | `boards` | `api/user.ts:69` `getUserLikedBoardsByNickname` | `data.data?.boards` |
| `GET /api/like/board/pushedLikes` | `BoardLikeController.java:109` | `boards` | `api/boardLike.ts:122` `getLikedBoardsAPI` | `result.data?.boards` |
| `GET /api/like/board/pushedLikes/count` | `BoardLikeController.java:126` | `likeCount` | `api/boardLike.ts:18` `getPushedBoardLikesCount` | `result.data?.likeCount` |
| `GET /api/cite/attendance` | `AttendanceController.java:112` | `visitCount` | `api/attendance.ts:175` `getMyTotalAttendanceCount` | `result.data.visitCount` |
| `POST /api/groups` | `GroupController.java:38` | `group` | **프론트 미사용** | – |
| `GET /api/groups` | `GroupController.java:56` | `groups` | **프론트 미사용** | – |
| `GET /api/groups/{id}` | `GroupController.java:68` | `group` (⚠ GET인데 `201 CREATED`) | **프론트 미사용** | – |
| `POST .../join-requests/apply`, `/invite` | `GroupJoinRequestController.java:33`, `:53` | `requestId` | **프론트 미사용** | – |
| `GET .../join-requests` | `GroupJoinRequestController.java:69` | `requests` | **프론트 미사용** | – |
| `GET .../members` | `GroupMemberController.java:30` | `members` | **프론트 미사용** | – |

---

## B형 — Map 자체가 응답 body (ApiResponse 전환 시 영향 큼)

| Endpoint | WAS 위치 | 응답 모양 | Web 호출부 | ApiResponse로 감싸면? |
|---|---|---|---|---|
| `POST /api/auth/register` | `AuthController.java:123`, `:128` (에러만 Map, 성공은 `User` 엔티티) | `{message}` | `api/auth.ts:159` `registerAPI` | `result.data ?? result`, `result.message` → OK |
| `GET /api/auth/me` | `AuthController.java:143`, `:175` (에러만 Map, 성공은 DTO 직접) | `{message}` | `api/auth.ts:262` `getMyPageInfo`, `:363` `validateSession` | `result.data ?? result` → OK |
| `PUT /api/auth/me` | `AuthController.java:188`, `:215`, `:222`, `:226` | `{success, message, data}` (이미 ApiResponse와 동일 모양) | `api/auth.ts:393` `updateProfileAPI` | `result.success`, `result.data` → OK |
| `PUT /api/auth/profile-image` | `AuthController.java:241`, `:247`, `:259`, `:268` | `{success, message, profileImageUrl, profileImageKey}` | `api/auth.ts:440` `updateProfileImageAPI` | ❌ 최상위 `result.profileImageUrl` → **깨짐** |
| `PUT /api/auth/profile-decoration` | `AuthController.java:282`~`303` | `{success, message, profileDecoration}` | `api/auth.ts:493` `updateProfileDecorationAPI` | ❌ 최상위 `result.profileDecoration` → **깨짐** |
| `POST /api/auth/email-hide` | `AuthController.java:314`, `:321`, `:328` | `{success, emailHide, message}` | `api/auth.ts:295` `toggleEmailHide` | ❌ 최상위 `result.emailHide` → **깨짐** |
| `GET /api/users/nickname/{nickname}` | `UsersController.java:48`, `:61`~`73`, `:76` | 프로필 Map 직접 | `api/user.ts:28` `getUserProfileByNickname` | ❌ `res.json()` 전체를 프로필로 사용 → **깨짐** |
| `GET /api/admin/boards/tag-stats` | `AdminBoardController.java:41`~`67` | `{success, categoryId, tagStats: List<Map>}` | **프론트 미사용** | – |
| `PUT /api/admin/boards/(de)activate-by-tag` | `AdminBoardController.java:80`~`119` | `{success, message, affectedCount}` | **프론트 미사용** | – |
| `POST /api/admin/users/tag-delete/{tag}` | `AdminUserController.java:163` (에러만) | `{success, message}` | **프론트 미사용** | – |

---

## 리팩터링 체크포인트

- [ ] **프론트 동시 수정 필요한 건 B형 4개뿐**: `toggleEmailHide`, `updateProfileImageAPI`, `updateProfileDecorationAPI`, `getUserProfileByNickname` → `result.data.xxx`로 경로 변경 필요
- [ ] **A형은 키 이름만 유지하면 프론트 무변경** (`Map.of("board", dto)` → `board` 필드를 가진 DTO). 래핑을 없애고 펼치면 위 표의 프론트 함수 전부 수정 필요
- [ ] `togglePin`(`BoardController.java:723`)은 `Board` **엔티티를 직렬화**해서 반환 중 → 프론트 호출처 없으니 DTO 전환 부담 적음
- [ ] 에러용 Map(`{message}`, `{success:false, message}`)은 `GlobalExceptionHandler`로 넘길 때 **`message` 키만 유지**하면 됨 (프론트는 대부분 `result.message`만 읽음)
- [ ] `bruno/` 컬렉션에 프론트 미사용 엔드포인트(`ToggleBoardPin`, `GetAttachmentDetail`, `GetMyFileList` 등) 요청이 있음 → 응답 모양 바꾸면 assertion 확인
- 기타
    - `mcp-server/index.js`는 `passwordChange` 계열만 써서 이번 작업과 무관
    - `BoardLikeController.java:125` 주석은 "count"라고 되어 있지만 실제 키/프론트 모두 `likeCount` (주석만 낡음)
    - `GroupController.java:68` GET인데 `201 CREATED` 반환

## 참고: 요청(@RequestBody)을 Map으로 받는 곳 (반환값 아님)

- `AuthController` — profile-image (`:237`), profile-decoration (`:278`)
- `AdminUserController` — grantRole (`:120`), revokeRole (`:133`)
- `ProfileDecorationController` — grant (`:105`), revoke (`:119`)
