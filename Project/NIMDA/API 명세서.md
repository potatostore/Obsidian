---
created: 2026-11-05
branch: fix/all
commit: 7fc2d80
tags: [nimda, api, swagger]
---

# API 명세서

fix/all(7fc2d80) 기준 cite·judgeServer 컨트롤러의 전체 API 135개를 Swagger UI처럼 도메인별로 정리했다. DTO·엔티티와 요청 파라미터는 뺐고, 요청 파라미터와 코드 점검 결과는 [[API 목록]]에 있다.

## 공통

| 항목 | 내용 |
|---|---|
| 서버 | 운영 api.nimda.kr, 로컬 localhost:8080 |
| 인증 | 로그인 시 발급되는 Authorization 쿠키(HttpOnly, 24시간)의 JWT |
| 권한 표기 | 공개 = 비로그인 가능 / 로그인 = 로그인 필요 / 관리자 = ROLE_ADMIN |
| 권한·기능 출처 | [[API 목록]]의 실측값(H2 + 일회용 Redis 환경) |
| 컨트롤러 밖 경로 | inst-{token}.{baseDomain} 서브도메인 요청은 SubdomainInstanceProxyFilter가 CTF 인스턴스로 프록시한다. URL이 아니라 호스트 기준이라 아래 표에는 없다 |

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
| [[#알림\|알림]] | AlarmController, NotificationController | 7 |
| [[#CTF\|CTF]] | ChallengeQueryController, ChallengeController, ChallengeDownloadController, InstanceController | 10 |
| [[#그룹\|그룹]] | GroupController, GroupJoinRequestController, GroupMemberController | 15 |
| 합계 | | 135 |

---

## 인증·계정

컨트롤러: AuthController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/auth/login | 로그인. JWT를 Authorization 쿠키(HttpOnly, 24시간)로 발급하고 user 정보 반환. 승인 대기·거부 계정은 403 | 공개 |
| POST | /api/auth/logout | 로그아웃. Authorization 쿠키 만료 | 로그인 |
| POST | /api/auth/register | 회원가입. 승인 대기(PENDING)로 생성되고 포인트 계좌도 함께 생성. 관리자 승인 후 로그인 가능 | 공개 |
| GET | /api/auth/me | 내 정보 조회 (마이페이지) | 로그인 |
| PUT | /api/auth/me | 프로필 부분 수정. 닉네임 중복 검사, 빈 값은 변경 안 함 | 로그인 |
| PUT | /api/auth/profile-image | 프로필 이미지 변경. S3 업로드 후 키를 저장하고 Presigned URL 반환 | 로그인 |
| PUT | /api/auth/profile-decoration | 프로필 장식 장착. 보유한 장식만 가능, 빈 값이면 해제 | 로그인 |
| POST | /api/auth/email-hide | 이메일 숨김 설정 토글 | 로그인 |

## 비밀번호 재설정

컨트롤러: UserRecoveryController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/cite/passwordChange/info-check | 아이디·학번·이메일 일치 확인. 모두 맞으면 password_change_token 쿠키(5분) 발급 | 공개 |
| POST | /api/cite/passwordChange/send-authMail | 인증 메일 발송. 항상 200 + 문자열 OK / UNAUTHORIZED / LIMIT_EXCEEDED | 공개 |
| POST | /api/cite/passwordChange/check-authcode | 인증 코드 확인 후 인증 완료 토큰 재발급. 문자열 응답 (실패 401/403) | 공개 |
| POST | /api/cite/passwordChange/change-password | 인증 완료 토큰으로 비밀번호 재설정. 문자열 응답 (실패 403) | 공개 |

## 사용자 공개 프로필

컨트롤러: UsersController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/users/nickname/{nickname} | 닉네임으로 공개 프로필 조회. 이메일 숨김이면 이메일 제외 | 로그인 |

## 관리자 — 사용자

컨트롤러: AdminUserController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/admin/users | 전체 사용자 목록 | 관리자 |
| GET | /api/admin/users/pending | 승인 대기 사용자 목록 + 인원 수 | 관리자 |
| GET | /api/admin/users/{id} | 사용자 상세 조회 (권한 목록 포함) | 관리자 |
| PUT | /api/admin/users/{id}/approve | 가입 승인. APPROVED로 변경하고 ROLE_USER 부여 | 관리자 |
| PUT | /api/admin/users/{id}/reject | 가입 거부. REJECTED로 변경 | 관리자 |
| GET | /api/admin/users/roles | 서버에 등록된 전체 권한 목록 | 관리자 |
| PUT | /api/admin/users/{id}/role | 사용자에게 권한 1개 추가 | 관리자 |
| PUT | /api/admin/users/{id}/role/remove | 사용자 권한 1개 제거 | 관리자 |
| GET | /api/admin/users/suggestions | 마일리지 지급용 학생 목록 (학번·이름) | 관리자 |
| POST | /api/admin/users/tag-delete/{tag} | 구현 없음. 받은 tag 문자열을 그대로 반환 | 관리자 |

## 게시판

### BoardController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/cite/board | 카테고리별 게시글 목록 (categoryId 또는 slug 필수). 검색·하위 카테고리 포함 지원. 카르텔은 ROLE_CARTEL·관리자만 | 로그인 |
| GET | /api/cite/board/pinned | 고정글 목록 (기본 4개, categoryId 또는 slug 필수) | 로그인 |
| GET | /api/cite/board/popular | 인기글 목록. 조회수순 최대 10개, 카테고리 지정 가능 | 로그인 |
| GET | /api/cite/board/recent-boards | 최신글 목록 | 로그인 |
| POST | /api/cite/board | 게시글 작성. 뉴스는 관리자·ROLE_DEV(패치 태그), 카르텔은 ROLE_CARTEL·관리자, 상점은 관리자만 | 로그인 |
| GET | /api/cite/board/{id} | 게시글 상세. 조회수 증가, 삭제된 글이면 data.deleted 반환 | 로그인 |
| PUT | /api/cite/board/{id} | 게시글 수정. 작성자·관리자만 | 로그인 |
| DELETE | /api/cite/board/{id} | 게시글 삭제. 작성자·관리자만 | 로그인 |
| PATCH | /api/cite/board/{id}/pin | 게시글 고정/해제 토글 | 관리자 |
| GET | /api/cite/board/my/board-count | 내 게시글 수 | 로그인 |
| GET | /api/cite/board/my/boards | 내가 쓴 게시글 목록 | 로그인 |
| DELETE | /api/cite/board/my/boards | 내가 쓴 게시글 여러 개 삭제 | 로그인 |
| GET | /api/cite/board/my/commented-boards | 내가 댓글 단 게시글 목록 | 로그인 |
| GET | /api/cite/board/user/{nickname} | 특정 유저가 쓴 게시글 목록 | 로그인 |

### PointUsageController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/cite/board/{id}/purchase | 마일리지로 상점 상품 구매 (배지 지급) | 로그인 |

## 관리자 — 게시판

컨트롤러: AdminBoardController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/admin/boards/tag-stats | 카테고리의 태그별 게시글 통계 (활성·숨김 수) | 관리자 |
| PUT | /api/admin/boards/deactivate-by-tag | 태그 기준 게시글 일괄 숨김 (ACTIVE → HIDDEN) | 관리자 |
| PUT | /api/admin/boards/activate-by-tag | 태그 기준 게시글 일괄 활성화 (HIDDEN → ACTIVE) | 관리자 |

## 카테고리

컨트롤러: CategoryController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/cite/category | 활성 카테고리 목록 | 공개 |
| GET | /api/cite/category/all | 전체 카테고리 목록 (비활성 포함) | 관리자 |
| GET | /api/cite/category/slug/{slug} | slug로 카테고리 조회 | 공개 |
| POST | /api/cite/category | 카테고리 생성 | 관리자 |
| PUT | /api/cite/category/{id} | 카테고리 수정 | 관리자 |
| DELETE | /api/cite/category/{id} | 카테고리 삭제 (소프트 삭제). 하위 카테고리나 게시글이 있으면 불가 | 관리자 |
| PUT | /api/cite/category/sort-order | 카테고리 순서 일괄 변경 | 관리자 |
| POST | /api/cite/category/enable-shop/{id} | 카테고리를 마일리지 상점으로 활성화 | 관리자 |

## 태그

컨트롤러: TagController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/cite/tag | 전체 태그 목록 | 공개 |
| GET | /api/cite/tag/{categoryId} | 카테고리의 태그 목록 | 공개 |
| POST | /api/cite/tag/add-tag | 태그 추가 | 관리자 |
| PATCH | /api/cite/tag/{tagId} | 태그 정보 수정 | 관리자 |
| DELETE | /api/cite/tag/{tagId} | 태그 삭제 | 관리자 |

## 댓글

컨트롤러: CommentController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/board/{boardId}/comments | 댓글·대댓글 작성 | 로그인 |
| GET | /api/board/{boardId}/comments | 게시글의 댓글 목록 | 로그인 |
| PATCH | /api/comments/{commentId} | 댓글 수정. 작성자만 | 로그인 |
| PATCH | /api/comments/{commentId}/status | 댓글 숨김 상태 변경 | 관리자 |
| DELETE | /api/comments/{commentId} | 댓글 삭제 (소프트 삭제) | 로그인 |
| GET | /api/comments/my/count | 내가 쓴 댓글 수 | 로그인 |
| GET | /api/comments/user/{nickname} | 특정 유저가 쓴 댓글 목록 | 로그인 |
| GET | /api/my-page/comments | 마이페이지 내 댓글 목록 | 로그인 |
| DELETE | /api/my-page/comments | 마이페이지에서 선택한 댓글 삭제 | 로그인 |

## 좋아요

### BoardLikeController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/like/board/{boardId} | 게시글 좋아요 토글 | 로그인 |
| GET | /api/like/board/{boardId}/likeCount | 게시글 좋아요 수 | 로그인 |
| GET | /api/like/board/{boardId}/likeStatus | 게시글 좋아요 수 + 내가 눌렀는지 | 로그인 |
| GET | /api/like/board/totalLikes | 내 글이 받은 좋아요 합계 | 로그인 |
| GET | /api/like/board/pushedLikes | 내가 좋아요한 게시글 목록 | 로그인 |
| GET | /api/like/board/pushedLikes/count | 내가 누른 좋아요 수 | 로그인 |
| GET | /api/like/board/user/{nickname}/liked | 특정 유저가 좋아요한 게시글 목록 | 로그인 |

### CommentLikeController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/like/comment/{commentId} | 댓글 좋아요 토글 | 로그인 |
| GET | /api/like/comment/{commentId}/likeCount | 댓글 좋아요 수 | 로그인 |

## 첨부파일

### AttachmentController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/cite/attachments/upload | 파일 업로드 (multipart) | 로그인 |
| POST | /api/cite/attachments/presigned | S3 업로드용 Presigned URL 발급 (type: profile, board, file 등) | 로그인 |
| POST | /api/cite/attachments/register | S3 업로드 완료 후 첨부 정보 등록 | 로그인 |
| GET | /api/cite/attachments/{id} | 첨부 메타정보 조회 | 로그인 |
| GET | /api/cite/attachments/{id}/download | 파일 다운로드·미리보기 (원본 파일명 반영) | 로그인 |
| GET | /api/cite/attachments/{id}/download-url | 다운로드 URL 반환. S3면 Presigned URL(10분), 로컬이면 다운로드 API 경로 | 공개 |
| GET | /api/cite/attachments/my | 내 첨부파일 목록 | 로그인 |
| DELETE | /api/cite/attachments | 선택한 첨부파일 삭제. 본인 파일만 | 로그인 |

### FileDownloadController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/download/{fileName} | 게시판 첨부 파일명으로 다운로드. 경로 조작(Path Traversal) 차단 | 로그인 |

## 출석

컨트롤러: AttendanceController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/cite/attendance/checkIn | 출석 체크. 하루 1회 | 로그인 |
| GET | /api/cite/attendance/today | 오늘 출석자 목록 (닉네임·프로필 이미지·장식) | 공개 |
| GET | /api/cite/attendance/rank/consecutive | 연속 출석 랭킹 TOP 5 | 로그인 |
| GET | /api/cite/attendance/rank/total | 누적 출석 랭킹 TOP 5 | 로그인 |
| GET | /api/cite/attendance/me | 내 출석 현황 | 로그인 |
| GET | /api/cite/attendance/me/logs | 내 출석 로그 | 로그인 |
| GET | /api/cite/attendance | 내 누적 방문 수 | 로그인 |

## 포인트(마일리지)

컨트롤러: PointController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/cite/point | 내 잔액 조회 | 로그인 |
| GET | /api/cite/point/pointDetails | 내 포인트 내역 | 로그인 |
| GET | /api/cite/point/user/{nickname} | 특정 유저 잔액 조회 | 로그인 |
| GET | /api/cite/point/user/{nickname}/details | 특정 유저 포인트 내역 | 로그인 |
| GET | /api/cite/point/allBalance | 전체 계좌 조회 | 관리자 |
| POST | /api/cite/point | 마일리지 수동 지급 | 관리자 |
| POST | /api/cite/point/bulk | 마일리지 일괄 지급 | 관리자 |

## 프로필 배지·장식

컨트롤러: ProfileDecorationController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/cite/profile-decorations | 활성 배지 목록 | 공개 |
| GET | /api/cite/profile-decorations/{key}/image | 배지 이미지로 리다이렉트 (302) | 공개 |
| GET | /api/cite/profile-decorations/me | 내가 보유한 배지 목록 | 로그인 |
| GET | /api/cite/admin/profile-decorations | 관리자용 배지 목록 | 관리자 |
| POST | /api/cite/admin/profile-decorations | 배지 등록 | 관리자 |
| POST | /api/cite/admin/profile-decorations/ownership/grant | 학번으로 배지 지급 | 관리자 |
| POST | /api/cite/admin/profile-decorations/ownership/revoke | 학번으로 배지 회수 | 관리자 |
| DELETE | /api/cite/admin/profile-decorations/{id} | 배지 삭제 | 관리자 |

## 알림

### AlarmController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/alarm/subscribe | 실시간 알림 구독 (SSE) | 로그인 |

### NotificationController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/notifications | 알림 목록 (최신순) | 로그인 |
| GET | /api/notifications/unRead | 읽지 않은 알림 목록 | 로그인 |
| GET | /api/notifications/hasUnread | 읽지 않은 알림 개수와 여부 | 로그인 |
| PATCH | /api/notifications/{notificationId}/read | 알림 읽음 처리 | 로그인 |
| PATCH | /api/notifications/readAll | 모든 알림 읽음 처리 | 로그인 |
| DELETE | /api/notifications/{notificationId} | 알림 삭제 | 로그인 |

## CTF

### ChallengeQueryController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/ctf/challenges | 문제 목록. 관리자는 비공개 초안까지 표시 | 로그인 |
| GET | /api/ctf/challenges/{code} | 문제 상세 | 로그인 |

### ChallengeController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/ctf/challenge | 문제 등록 (multipart, zip 파일 포함) | 관리자 |
| POST | /api/ctf/challenge/toggle-public/{id} | 문제 공개/비공개 전환 | 관리자 |
| DELETE | /api/ctf/challenge/{id} | 문제 삭제 | 관리자 |

### ChallengeDownloadController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/ctf/challenge/{code}/download | 문제 파일 다운로드 링크 요청 (비동기) | 로그인 |
| GET | /api/ctf/challenge/download/{requestId} | 다운로드 링크 발급 결과 조회. 아직이면 PENDING | 로그인 |

### InstanceController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/ctf/instance/{code} | 문제 인스턴스(컨테이너) 생성 요청. WEB·PWN 문제만 | 로그인 |
| GET | /api/ctf/instance/{code} | 이 문제에 내가 띄운 인스턴스 정보. 새로고침해도 이어서 조회 가능 | 로그인 |
| GET | /api/ctf/instance/status/{uuid} | 인스턴스 상태 조회 (생성 직후 폴링). 본인 인스턴스만 | 로그인 |

## 그룹

### GroupController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/groups | 그룹 생성 | 관리자 |
| GET | /api/groups | 그룹 목록 (keyword 검색) | 로그인 |
| GET | /api/groups/{groupId} | 그룹 상세 | 로그인 |
| PATCH | /api/groups/{groupId} | 그룹 수정. 그룹장만 | 로그인 |
| DELETE | /api/groups/{groupId} | 그룹 삭제. 그룹장만 | 로그인 |

### GroupJoinRequestController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| POST | /api/groups/{groupId}/join-requests/apply | 그룹 가입 신청 | 로그인 |
| POST | /api/groups/{groupId}/join-requests/invite | 사용자 초대 | 로그인 |
| GET | /api/groups/{groupId}/join-requests | 대기 중인 요청 목록. 그룹장만 | 로그인 |
| POST | /api/groups/{groupId}/join-requests/{requestId}/accept | 요청 수락 | 로그인 |
| POST | /api/groups/{groupId}/join-requests/{requestId}/reject | 요청 거절 | 로그인 |
| DELETE | /api/groups/{groupId}/join-requests/{requestId} | 요청 취소. 신청자 본인만 | 로그인 |

### GroupMemberController

| Method | URL | 기능 | 권한 |
|---|---|---|---|
| GET | /api/groups/{groupId}/members | 그룹 멤버 목록 | 로그인 |
| DELETE | /api/groups/{groupId}/members/me | 그룹 탈퇴 | 로그인 |
| DELETE | /api/groups/{groupId}/members/{targetUserId} | 멤버 강퇴 | 로그인 |
| PATCH | /api/groups/{groupId}/members/{targetUserId}/leader | 그룹장 위임 | 로그인 |
