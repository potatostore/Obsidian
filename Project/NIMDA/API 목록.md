---
created: 2026-11-02
branch: fix/all
commit: 7fc2d80
tags: [nimda, api, swagger]
---

# API 목록

fix/all(7fc2d80) 기준 cite·judgeServer 컨트롤러의 전체 API 135개.

- URL·메서드·요청 파라미터: springdoc이 코드에서 생성한 OpenAPI 문서에서 추출
- 권한: 비로그인과 일반 유저(ROLE_USER)로 전 API를 실제 호출해 측정 + @PreAuthorize 확인
- 응답 형식: [[PR 컨벤션#4. 응답 형식 & DTO]] / 에러 코드: [[PR 컨벤션#3. 에러 코드 — ErrorCode]]

## 공통

| 항목 | 내용 |
|---|---|
| 서버 | 운영 api.nimda.kr (nginx → backend), 로컬 localhost:8080 |
| 인증 | 로그인 시 발급되는 Authorization 쿠키(HttpOnly, 24시간)의 JWT. Authorization 헤더는 읽지 않음 |
| 권한 표기 | 공개 = 비로그인 가능 / 로그인 = 로그인 필요 / 관리자 = ROLE_ADMIN |
| 비로그인 차단 응답 | 보안 필터에서 막히면 401이 아니라 **403** + Spring 기본 에러 JSON. 컨트롤러까지 간 경우만 401 + {success:false, message} |
| 에러 응답 | {success:false, message} (비밀번호 재설정만 문자열) |
| 요청 칸 표기 | param = 쿼리/폼 파라미터, body = JSON, form = multipart, ? = 선택. URL의 경로 변수는 생략. body의 ?는 DTO에 필수 검증이 있을 때만 구분됨 |
| 앱 버전 검사 | VersionCheckInterceptor가 어디에도 등록되어 있지 않아 동작하지 않음 |

## 한눈에 보기

| 도메인 | 컨트롤러 | 개수 |
|---|---|---|
| [[#인증·계정\|인증·계정]] | AuthController | 8 |
| [[#비밀번호 재설정\|비밀번호 재설정]] | UserRecoveryController | 4 |
| [[#사용자 공개 프로필\|사용자 공개 프로필]] | UsersController | 1 |
| [[#관리자 — 사용자\|관리자 — 사용자]] | AdminUserController | 10 |
| [[#게시판\|게시판]] | BoardController, PointUsageController | 15 |
| [[#관리자 — 게시판\|관리자 — 게시판]] | AdminBoardController | 3 |
| [[#카테고리\|카테고리]] | CategoryController | 8 |
| [[#태그\|태그]] | TagController | 5 |
| [[#댓글\|댓글]] | CommentController | 9 |
| [[#좋아요\|좋아요]] | BoardLikeController, CommentLikeController | 9 |
| [[#첨부파일\|첨부파일]] | AttachmentController, FileDownloadController | 9 |
| [[#출석\|출석]] | AttendanceController | 7 |
| [[#포인트(마일리지)\|포인트(마일리지)]] | PointController | 7 |
| [[#프로필 배지·장식\|프로필 배지·장식]] | ProfileDecorationController | 8 |
| [[#알림\|알림]] | NotificationController, AlarmController | 7 |
| [[#CTF\|CTF]] | ChallengeController, ChallengeQueryController, ChallengeDownloadController, InstanceController | 10 |
| [[#그룹\|그룹]] | GroupController, GroupJoinRequestController, GroupMemberController | 15 |
| 합계 | | 135 |

---

## 인증·계정

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| POST | /api/auth/login | 로그인. JWT를 Authorization 쿠키(HttpOnly, 24시간)로 발급하고 user 정보 반환. 승인 대기·거부 계정은 403 | 공개 | body: userId, password |
| POST | /api/auth/logout | 로그아웃. Authorization 쿠키 만료 | 로그인 | – |
| POST | /api/auth/register | 회원가입. 승인 대기(PENDING)로 생성되고 포인트 계좌도 함께 생성. 관리자 승인 후 로그인 가능 | 공개 | body: userId, name, nickname, password, studentNum, email, major, birth, bojId? |
| GET | /api/auth/me | 내 정보 조회 (마이페이지) | 로그인 | – |
| PUT | /api/auth/me | 프로필 부분 수정. 닉네임 중복 검사, 빈 값은 변경 안 함 | 로그인 | body: nickname, bojId, birth, major, studentNum |
| PUT | /api/auth/profile-image | 프로필 이미지 변경. S3 업로드 후 키를 저장하고 Presigned URL 반환 | 로그인 | body: profileImageKey |
| PUT | /api/auth/profile-decoration | 프로필 장식 장착. 보유한 장식만 가능, 빈 값이면 해제 | 로그인 | body: profileDecorationKey |
| POST | /api/auth/email-hide | 이메일 숨김 설정 토글 | 로그인 | – |

## 비밀번호 재설정

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| POST | /api/cite/passwordChange/info-check | 아이디·학번·이메일 일치 확인. 모두 맞으면 password_change_token 쿠키(5분) 발급 | 공개 | body: userId, studentNum, email |
| POST | /api/cite/passwordChange/send-authMail | 인증 메일 발송. 항상 200 + 문자열 OK / UNAUTHORIZED / LIMIT_EXCEEDED | 공개 | body: userId, studentNum, email; 쿠키: password_change_token |
| POST | /api/cite/passwordChange/check-authcode | 인증 코드 확인 후 인증 완료 토큰 재발급. 문자열 응답 (실패 401/403) | 공개 | body: authCode; 쿠키: password_change_token |
| POST | /api/cite/passwordChange/change-password | 인증 완료 토큰으로 비밀번호 재설정. 문자열 응답 (실패 403) | 공개 | body: password; 쿠키: password_change_token |

## 사용자 공개 프로필

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/users/nickname/{nickname} | 닉네임으로 공개 프로필 조회. 이메일 숨김이면 이메일 제외 | 로그인 | – |

## 관리자 — 사용자

| Method | URL                               | 기능                                 | 권한  | 요청         |
| ------ | --------------------------------- | ---------------------------------- | --- | ---------- |
| GET    | /api/admin/users                  | 전체 사용자 목록                          | 관리자 | –          |
| GET    | /api/admin/users/pending          | 승인 대기 사용자 목록 + 인원 수                | 관리자 | –          |
| GET    | /api/admin/users/{id}             | 사용자 상세 조회 (권한 목록 포함)               | 관리자 | –          |
| PUT    | /api/admin/users/{id}/approve     | 가입 승인. APPROVED로 변경하고 ROLE_USER 부여 | 관리자 | –          |
| PUT    | /api/admin/users/{id}/reject      | 가입 거부. REJECTED로 변경                | 관리자 | –          |
| GET    | /api/admin/users/roles            | 서버에 등록된 전체 권한 목록                   | 관리자 | –          |
| PUT    | /api/admin/users/{id}/role        | 사용자에게 권한 1개 추가                     | 관리자 | body: role |
| PUT    | /api/admin/users/{id}/role/remove | 사용자 권한 1개 제거                       | 관리자 | body: role |
| GET    | /api/admin/users/suggestions      | 마일리지 지급용 학생 목록 (학번·이름)             | 관리자 | –          |
| POST   | /api/admin/users/tag-delete/{tag} | 구현 없음. 받은 tag 문자열을 그대로 반환          | 관리자 | –          |

## 게시판

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/cite/board | 카테고리별 게시글 목록 (categoryId 또는 slug 필수). 검색·하위 카테고리 포함 지원. 카르텔은 ROLE_CARTEL·관리자만 | 로그인 | param: categoryId?, slug?, searchKeyword?, includeChildren?, page?, size?, sort? |
| GET | /api/cite/board/pinned | 고정글 목록 (기본 4개, categoryId 또는 slug 필수) | 로그인 | param: categoryId?, slug?, page?, size?, sort? |
| GET | /api/cite/board/popular | 인기글 목록. 조회수순 최대 10개, 카테고리 지정 가능 | 로그인 | param: categoryId?, slug?, page?, size?, sort? |
| GET | /api/cite/board/recent-boards | 최신글 목록 | 로그인 | param: page?, size?, sort? |
| POST | /api/cite/board | 게시글 작성. 뉴스는 관리자·ROLE_DEV(패치 태그), 카르텔은 ROLE_CARTEL·관리자, 상점은 관리자만 | 로그인 | param: categoryId, title, content, tagId?, attachmentIds?, pinned?, itemPrice?, itemType?, profileDecorationId?, thumbnailAttachmentId? |
| GET | /api/cite/board/{id} | 게시글 상세. 조회수 증가, 삭제된 글이면 data.deleted 반환 | 로그인 | – |
| PUT | /api/cite/board/{id} | 게시글 수정. 작성자·관리자만 | 로그인 | param: categoryId, title, content, tagId?, attachmentIds?, pinned?, itemPrice?, itemType?, profileDecorationId?, thumbnailAttachmentId? |
| DELETE | /api/cite/board/{id} | 게시글 삭제. 작성자·관리자만 | 로그인 | – |
| PATCH | /api/cite/board/{id}/pin | 게시글 고정/해제 토글 | 관리자 | – |
| POST | /api/cite/board/{id}/purchase | 마일리지로 상점 상품 구매 (배지 지급) | 로그인 | – |
| GET | /api/cite/board/my/board-count | 내 게시글 수 | 로그인 | – |
| GET | /api/cite/board/my/boards | 내가 쓴 게시글 목록 | 로그인 | – |
| DELETE | /api/cite/board/my/boards | 내가 쓴 게시글 여러 개 삭제 | 로그인 | body: boardIds |
| GET | /api/cite/board/my/commented-boards | 내가 댓글 단 게시글 목록 | 로그인 | – |
| GET | /api/cite/board/user/{nickname} | 특정 유저가 쓴 게시글 목록 | 로그인 | – |

## 관리자 — 게시판

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/admin/boards/tag-stats | 카테고리의 태그별 게시글 통계 (활성·숨김 수) | 관리자 | param: categoryId |
| PUT | /api/admin/boards/deactivate-by-tag | 태그 기준 게시글 일괄 숨김 (ACTIVE → HIDDEN) | 관리자 | param: categoryId, tagId |
| PUT | /api/admin/boards/activate-by-tag | 태그 기준 게시글 일괄 활성화 (HIDDEN → ACTIVE) | 관리자 | param: categoryId, tagId |

## 카테고리

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/cite/category | 활성 카테고리 목록 | 공개 | – |
| GET | /api/cite/category/all | 전체 카테고리 목록 (비활성 포함) | 관리자 | – |
| GET | /api/cite/category/slug/{slug} | slug로 카테고리 조회 | 공개 | – |
| POST | /api/cite/category | 카테고리 생성 | 관리자 | body: name, slug, parentId?, sortOrder?, isActive?, availableTags?, redirectUrl?, shopEnabled? |
| PUT | /api/cite/category/{id} | 카테고리 수정 | 관리자 | body: name, slug, parentId, sortOrder, isActive, availableTags, redirectUrl, shopEnabled |
| DELETE | /api/cite/category/{id} | 카테고리 삭제 (소프트 삭제). 하위 카테고리나 게시글이 있으면 불가 | 관리자 | – |
| PUT | /api/cite/category/sort-order | 카테고리 순서 일괄 변경 | 관리자 | body 배열: id, sortOrder |
| POST | /api/cite/category/enable-shop/{id} | 카테고리를 마일리지 상점으로 활성화 | 관리자 | – |

## 태그

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/cite/tag | 전체 태그 목록 | 공개 | – |
| GET | /api/cite/tag/{categoryId} | 카테고리의 태그 목록 | 공개 | – |
| POST | /api/cite/tag/add-tag | 태그 추가 | 관리자 | body: name, categoryId, sortValue |
| PATCH | /api/cite/tag/{tagId} | 태그 정보 수정 | 관리자 | body: name, categoryId, sortValue |
| DELETE | /api/cite/tag/{tagId} | 태그 삭제 | 관리자 | – |

## 댓글

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| POST | /api/board/{boardId}/comments | 댓글·대댓글 작성 | 로그인 | body: parentId?, context |
| GET | /api/board/{boardId}/comments | 게시글의 댓글 목록 | 로그인 | – |
| PATCH | /api/comments/{commentId} | 댓글 수정. 작성자만 | 로그인 | body: context |
| PATCH | /api/comments/{commentId}/status | 댓글 숨김 상태 변경 | 관리자 | body: status |
| DELETE | /api/comments/{commentId} | 댓글 삭제 (소프트 삭제) | 로그인 | – |
| GET | /api/comments/my/count | 내가 쓴 댓글 수 | 로그인 | – |
| GET | /api/comments/user/{nickname} | 특정 유저가 쓴 댓글 목록 | 로그인 | – |
| GET | /api/my-page/comments | 마이페이지 내 댓글 목록 | 로그인 | – |
| DELETE | /api/my-page/comments | 마이페이지에서 선택한 댓글 삭제 | 로그인 | body: commentIds |

## 좋아요

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| POST | /api/like/board/{boardId} | 게시글 좋아요 토글 | 로그인 | – |
| GET | /api/like/board/{boardId}/likeCount | 게시글 좋아요 수 | 로그인 | – |
| GET | /api/like/board/{boardId}/likeStatus | 게시글 좋아요 수 + 내가 눌렀는지 | 로그인 | – |
| GET | /api/like/board/totalLikes | 내 글이 받은 좋아요 합계 | 로그인 | – |
| GET | /api/like/board/pushedLikes | 내가 좋아요한 게시글 목록 | 로그인 | – |
| GET | /api/like/board/pushedLikes/count | 내가 누른 좋아요 수 | 로그인 | – |
| GET | /api/like/board/user/{nickname}/liked | 특정 유저가 좋아요한 게시글 목록 | 로그인 | – |
| POST | /api/like/comment/{commentId} | 댓글 좋아요 토글 | 로그인 | – |
| GET | /api/like/comment/{commentId}/likeCount | 댓글 좋아요 수 | 로그인 | – |

## 첨부파일

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| POST | /api/cite/attachments/upload | 파일 업로드 (multipart) | 로그인 | form: file, boardId?, categoryId |
| POST | /api/cite/attachments/presigned | S3 업로드용 Presigned URL 발급 (type: profile, board, file 등) | 로그인 | param: type, fileName |
| POST | /api/cite/attachments/register | S3 업로드 완료 후 첨부 정보 등록 | 로그인 | body: key, originFilename, fileSize, boardId, categoryId |
| GET | /api/cite/attachments/{id} | 첨부 메타정보 조회 | 로그인 | – |
| GET | /api/cite/attachments/{id}/download | 파일 다운로드·미리보기 (원본 파일명 반영) | 로그인 | param: disposition? |
| GET | /api/cite/attachments/{id}/download-url | 다운로드 URL 반환. S3면 Presigned URL(10분), 로컬이면 다운로드 API 경로 | 공개 | – |
| GET | /api/cite/attachments/my | 내 첨부파일 목록 | 로그인 | – |
| DELETE | /api/cite/attachments | 선택한 첨부파일 삭제. 본인 파일만 | 로그인 | body: fileIds |
| GET | /api/download/{fileName} | 게시판 첨부 파일명으로 다운로드. 경로 조작(Path Traversal) 차단 | 로그인 | – |

## 출석

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| POST | /api/cite/attendance/checkIn | 출석 체크. 하루 1회 | 로그인 | – |
| GET | /api/cite/attendance/today | 오늘 출석자 목록 (닉네임·프로필 이미지·장식) | 공개 | – |
| GET | /api/cite/attendance/rank/consecutive | 연속 출석 랭킹 TOP 5 | 로그인 | – |
| GET | /api/cite/attendance/rank/total | 누적 출석 랭킹 TOP 5 | 로그인 | – |
| GET | /api/cite/attendance/me | 내 출석 현황 | 로그인 | – |
| GET | /api/cite/attendance/me/logs | 내 출석 로그 | 로그인 | – |
| GET | /api/cite/attendance | 내 누적 방문 수 | 로그인 | – |

## 포인트(마일리지)

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/cite/point | 내 잔액 조회 | 로그인 | – |
| GET | /api/cite/point/pointDetails | 내 포인트 내역 | 로그인 | – |
| GET | /api/cite/point/user/{nickname} | 특정 유저 잔액 조회 | 로그인 | – |
| GET | /api/cite/point/user/{nickname}/details | 특정 유저 포인트 내역 | 로그인 | – |
| GET | /api/cite/point/allBalance | 전체 계좌 조회 | 관리자 | – |
| POST | /api/cite/point | 마일리지 수동 지급 | 관리자 | body: studentNum, description, amount |
| POST | /api/cite/point/bulk | 마일리지 일괄 지급 | 관리자 | body 배열: studentNum, description, amount |

## 프로필 배지·장식

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/cite/profile-decorations | 활성 배지 목록 | 공개 | – |
| GET | /api/cite/profile-decorations/{key}/image | 배지 이미지로 리다이렉트 (302) | 공개 | – |
| GET | /api/cite/profile-decorations/me | 내가 보유한 배지 목록 | 로그인 | – |
| GET | /api/cite/admin/profile-decorations | 관리자용 배지 목록 | 관리자 | – |
| POST | /api/cite/admin/profile-decorations | 배지 등록 | 관리자 | body: key, label, filePath, requiredRole, purchaseRequired |
| POST | /api/cite/admin/profile-decorations/ownership/grant | 학번으로 배지 지급 | 관리자 | body: studentNum, decorationId |
| POST | /api/cite/admin/profile-decorations/ownership/revoke | 학번으로 배지 회수 | 관리자 | body: studentNum, decorationId |
| DELETE | /api/cite/admin/profile-decorations/{id} | 배지 삭제 | 관리자 | – |

## 알림

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/alarm/subscribe | 실시간 알림 구독 (SSE) | 로그인 | – |
| GET | /api/notifications | 알림 목록 (최신순) | 로그인 | – |
| GET | /api/notifications/unRead | 읽지 않은 알림 목록 | 로그인 | – |
| GET | /api/notifications/hasUnread | 읽지 않은 알림 개수와 여부 | 로그인 | – |
| PATCH | /api/notifications/{notificationId}/read | 알림 읽음 처리 | 로그인 | – |
| PATCH | /api/notifications/readAll | 모든 알림 읽음 처리 | 로그인 | – |
| DELETE | /api/notifications/{notificationId} | 알림 삭제 | 로그인 | – |

## CTF

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| GET | /api/ctf/challenges | 문제 목록. 관리자는 비공개 초안까지 표시 | 로그인 | – |
| GET | /api/ctf/challenges/{code} | 문제 상세 | 로그인 | – |
| POST | /api/ctf/challenge | 문제 등록 (multipart, zip 파일 포함) | 관리자 | form: code, title, description, category, points?, flagType?, flag?, isolationType?, zipFile?, isPublic |
| POST | /api/ctf/challenge/toggle-public/{id} | 문제 공개/비공개 전환 | 관리자 | – |
| DELETE | /api/ctf/challenge/{id} | 문제 삭제 | 관리자 | – |
| POST | /api/ctf/challenge/{code}/download | 문제 파일 다운로드 링크 요청 (비동기) | 로그인 | – |
| GET | /api/ctf/challenge/download/{requestId} | 다운로드 링크 발급 결과 조회. 아직이면 PENDING | 로그인 | – |
| POST | /api/ctf/instance/{code} | 문제 인스턴스(컨테이너) 생성 요청. WEB·PWN 문제만 | 로그인 | – |
| GET | /api/ctf/instance/{code} | 이 문제에 내가 띄운 인스턴스 정보. 새로고침해도 이어서 조회 가능 | 로그인 | – |
| GET | /api/ctf/instance/status/{uuid} | 인스턴스 상태 조회 (생성 직후 폴링). 본인 인스턴스만 | 로그인 | – |

## 그룹

| Method | URL | 기능 | 권한 | 요청 |
|---|---|---|---|---|
| POST | /api/groups | 그룹 생성 | 관리자 | body: name, capacity, description? |
| GET | /api/groups | 그룹 목록 (keyword 검색) | 로그인 | param: keyword? |
| GET | /api/groups/{groupId} | 그룹 상세 | 로그인 | – |
| PATCH | /api/groups/{groupId} | 그룹 수정. 그룹장만 | 로그인 | body: name, capacity, description? |
| DELETE | /api/groups/{groupId} | 그룹 삭제. 그룹장만 | 로그인 | – |
| POST | /api/groups/{groupId}/join-requests/apply | 그룹 가입 신청 | 로그인 | – |
| POST | /api/groups/{groupId}/join-requests/invite | 사용자 초대 | 로그인 | param: inviteeId |
| GET | /api/groups/{groupId}/join-requests | 대기 중인 요청 목록. 그룹장만 | 로그인 | – |
| POST | /api/groups/{groupId}/join-requests/{requestId}/accept | 요청 수락 | 로그인 | – |
| POST | /api/groups/{groupId}/join-requests/{requestId}/reject | 요청 거절 | 로그인 | – |
| DELETE | /api/groups/{groupId}/join-requests/{requestId} | 요청 취소. 신청자 본인만 | 로그인 | – |
| GET | /api/groups/{groupId}/members | 그룹 멤버 목록 | 로그인 | – |
| DELETE | /api/groups/{groupId}/members/me | 그룹 탈퇴 | 로그인 | – |
| DELETE | /api/groups/{groupId}/members/{targetUserId} | 멤버 강퇴 | 로그인 | – |
| PATCH | /api/groups/{groupId}/members/{targetUserId}/leader | 그룹장 위임 | 로그인 | – |

---

## Swagger 연결

**연결 가능.** 현재는 미적용이고, 아래 설정은 커밋 복사본에서 실제로 띄워 확인한 결과다. (repo에는 아직 반영 안 함)

| 확인 항목 | 결과 |
|---|---|
| 현재 상태 | pom.xml과 코드에 springdoc·swagger 설정 없음 |
| 버전 호환 | Spring Boot 3.2.0 + Java 17 + springdoc 2.5.0으로 정상 기동 |
| 보안 설정 그대로일 때 | /v3/api-docs, /swagger-ui 모두 403 (anyRequest().authenticated()에 막힘) |
| 허용 규칙 추가 후 | /v3/api-docs 200, /swagger-ui/index.html 200, /swagger-ui.html은 302로 이동 |
| 문서 범위 | API 135개 전부 잡힘 (UrlNames 상수, 슬래시 없는 api/cite/passwordChange 경로도 정상) |
| 전역 예외 핸들러 | 문서 생성 방해 없음 |
| 운영에서 끄기 | springdoc.api-docs.enabled=false, springdoc.swagger-ui.enabled=false면 세 경로 모두 404 |
| nginx | location / 가 backend로 전달하므로 설정 변경 없이 도달함 (설정 파일 기준, 운영에서 시험은 안 함) |
| 브라우저 Try it out | 아직 안 해봄 |

### 적용 방법

| 위치 | 내용 |
|---|---|
| pom.xml | org.springdoc : springdoc-openapi-starter-webmvc-ui : 2.5.0 추가 |
| SecurityConfig | /v3/api-docs/\*\*, /swagger-ui/\*\*, /swagger-ui.html 을 permitAll (anyRequest 규칙보다 앞에) |
| application.yml | springdoc.api-docs.enabled, springdoc.swagger-ui.enabled를 환경변수로 받고 기본값 false 권장. API 전체 구조가 공개되므로 운영에서는 끄거나 접근을 제한 |
| Boot 업그레이드 시 | springdoc 버전도 함께 올려야 함 (Boot 3.2는 springdoc 2.3~2.5 대응) |

### 로그인이 필요한 API 시험

JWT가 HttpOnly 쿠키라 Swagger의 Authorize 버튼으로는 넣을 수 없다. Swagger에서 POST /api/auth/login을 먼저 실행하면 같은 출처의 쿠키가 이후 요청에 자동으로 붙는 구조다. 쿠키에 Secure가 기본으로 붙으므로, http로 띄우는 로컬에서 쿠키가 저장되지 않으면 AUTH_COOKIE_SECURE=false로 실행한다.

### 그대로 띄웠을 때의 한계

| 항목 | 현상 | 개선 방법 |
|---|---|---|
| 응답 스키마 | 135개 중 84개는 응답이 object로만 표시 (ResponseEntity\<?\> 반환) | 반환 타입을 구체적으로 쓰거나 @ApiResponse 추가 |
| 에러 응답 | 400·403 등이 문서에 나오지 않음 | @ApiResponse 추가 |
| 페이징 | GET board 목록 등 4개에서 pageable이 객체 파라미터 하나로 표시 | 파라미터에 @ParameterObject |
| 문제 등록 | POST /api/ctf/challenge가 쿼리 파라미터 하나로 표시되어 파일 업로드 시험 불가 | @ParameterObject 또는 스키마 직접 지정 |
| 설명 | 기능 설명 없음, 태그가 컨트롤러 이름 그대로, 제목이 OpenAPI definition | @Operation, @Tag, OpenAPI 설정 빈 |

---

## 정리하다 발견한 것

| 구분 | API | 내용 |
|---|---|---|
| 버그 | GET /api/cite/attendance/rank/consecutive, rank/total, me, me/logs | 데이터가 있으면 500. Attendance·AttendanceLog 엔티티를 그대로 응답해서 lazy user 프록시 직렬화 실패 (ByteBuddyInterceptor). 공개 프론트(api/attendance.ts)가 rank 2개를 호출함. dev와 코드 구조가 같아 이번 PR에서 생긴 문제는 아님(코드 비교 기준). 직렬화만 풀면 User의 이름·학번·이메일·생년월일이 함께 나가므로 DTO 변환으로 고칠 것 |
| 권한 확인 필요 | GET /api/cite/attachments/{id}/download-url | 비로그인으로 첨부 ID만 있으면 다운로드 URL 발급 (소유자·카테고리 확인 없음). 카르텔처럼 접근 제한된 게시판의 첨부도 해당 |
| 에러 코드 | POST /api/cite/passwordChange/info-check | 필드가 빠지면 400이 아니라 500 (@Valid 없음 + CheckConfig의 NullPointerException) |
| 에러 코드 | POST /api/cite/attachments/upload | multipart가 아닌 요청이 400이 아니라 500 |
| 에러 코드 | GET·DELETE /api/groups/{groupId}, join-requests/apply, invite, members/me 등 | 없는 그룹이면 404가 아니라 500 (catch Exception). judgeServer 코드 |
| 주석 불일치 | GET /api/comments/user/{nickname}, /api/like/board/user/{nickname}/liked, /api/cite/point/user/{nickname}, /details | 주석은 인증 불필요인데 실제로는 로그인 필요 |
| 죽은 보안 규칙 | /api/actuator/\*\*, /api/cite/mail/\*\*, DELETE /api/users/\*\*, PUT /api/users/\*/role | SecurityConfig에 있지만 해당 API가 없음 (actuator 의존성도 없음) |
| 죽은 보안 규칙 | GET /api/cite/category/all | 관리자 규칙이 앞의 공개 규칙에 가려 동작 안 함. 대신 서비스에서 막음 (비로그인 401, 일반 유저 403) |
| 미사용 상수 | UrlNames의 problem·submission 경로 | 해당 컨트롤러가 없음 |

> 측정 환경은 H2 + 일회용 Redis. 일반 유저 호출에서 나온 500 중 좋아요·인기글(GET /api/like/board/totalLikes, pushedLikes, pushedLikes/count, GET /api/cite/board/popular)은 H2에서 board_like 테이블이 안 만들어져 생긴 테스트 환경 문제라 위 목록에서 제외.
