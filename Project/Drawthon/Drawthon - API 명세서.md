---
tags:
  - seed
  - type/project
aliases:
  - 드로톤 API 명세서
created: 2026-11-10
---
# Drawthon - API 명세서

drawthon_t1_backend main(4e958e6)에 아래 변경을 더한 상태(커밋 전)에서, 서버를 실제로 띄워 Swagger(/v3/api-docs)로 받은 API 17개를 도메인별로 정리했다. 권한 열은 관리자·일반 회원으로 직접 호출해 확인한 값이고, DTO 필드는 Swagger 스키마와 DTO 코드의 검증 조건을 합쳐 적었다.

- SecurityConfig merge 오류 수정
- 회원(Member)에 role 추가, 공고 API는 로그인 세션의 회원으로 권한 확인 (URL의 {userId} 제거)
- 사용자(User) 도메인 삭제, 공고 컬럼을 MVP 필수 항목으로 축소

## 공통

| 항목 | 내용 |
|---|---|
| 서버 | 로컬 http://localhost:8080 |
| Swagger UI | http://localhost:8080/swagger-ui/index.html |
| 인증 | 세션 쿠키(JSESSIONID). 로그인하면 발급되고, 마지막 요청부터 30분 유지 |
| CSRF | GET이 아닌 요청은 X-XSRF-TOKEN 헤더가 필요하다. 토큰은 GET /api/auth/csrf로 받는다. 없으면 403 |
| CORS 허용 | http://localhost:3000, http://localhost:5173 (쿠키 포함 허용) |
| 권한 표기 | 공개 = 비로그인 가능 / 로그인 = 세션 필요 / ADMIN·USER = 로그인한 회원의 role |
| 날짜 형식 | LocalDate는 yyyy-MM-dd 문자열 (예: 2026-11-10) |
| 미인증 응답 | 401 {"message":"로그인이 필요합니다."} |

### 회원 역할

| role | 할 수 있는 일 | 만드는 방법 |
|---|---|---|
| USER | 공고 조회, 신청, 철회 | 회원가입 (role을 보내도 항상 USER) |
| ADMIN | 공고 조회, 생성, 1365 등록, 수정, 삭제 | 서버 시작 시 환경변수 ADMIN_EMAIL, ADMIN_PASSWORD(8자 이상), ADMIN_NICKNAME(선택). 이미 가입한 이메일이면 ADMIN으로만 바꾼다 |

ADMIN은 공고를 신청할 수 없고, USER는 공고를 만들 수 없다 (403 권한이 없습니다.).

### 오류 응답 형식

컨트롤러에서 난 오류는 Problem Details 형식으로 온다.

{"title":"Not Found","status":404,"detail":"공고를 찾을 수 없습니다.","instance":"/api/v1/posting/999"}

- 400은 detail에 어느 필드가 틀렸는지 나오지 않는다 (Invalid request content. / Validation failure).
- 401(미인증)과 403(CSRF·접근 거부)은 Security 필터가 응답해서 {"message": ...} 형식이다.
- README는 모든 오류가 {"message": ...}라고 설명하지만, 실제로는 위처럼 두 형식이 섞여 있다.

## 한눈에 보기

| 도메인 | 컨트롤러 | 개수 |
|---|---|---|
| 인증 | SessionAuthApiController | 5 |
| 공고 | PostingController | 9 |
| 지도 | MapNoticeController, GeocodingController | 3 |
| 합계 | | 17 |

---

## 인증

컨트롤러: SessionAuthApiController

| Method | URL | 기능 | 권한 | 요청 | 응답 |
|---|---|---|---|---|---|
| GET | /api/auth/csrf | CSRF 토큰 발급. 변경 요청 전에 먼저 호출 | 공개 | 없음 | 200 CsrfTokenResponse |
| POST | /api/auth/signup | 회원가입 (항상 USER). 자동 로그인되지 않음. 이메일 중복 409 | 공개 | SignupRequest | 201 MemberResponse |
| POST | /api/auth/login | 로그인. 세션 쿠키 발급. 실패 401 | 공개 | LoginRequest | 200 MemberResponse |
| GET | /api/auth/me | 내 정보 조회. 프론트는 role로 관리자 화면 여부를 판단 | 로그인 | 없음 | 200 MemberResponse |
| POST | /api/auth/logout | 로그아웃 | 로그인 | 없음 | 204 본문 없음 |

### 인증 DTO

#### SignupRequest (회원가입 요청)

| 필드 | 타입 | 필수 | 제약 | 설명 |
|---|---|---|---|---|
| email | String | O | 이메일 형식, 120자 이하. 앞뒤 공백 제거 후 소문자로 저장 | 로그인 이메일 |
| password | String | O | 8~72자, UTF-8 72바이트 이하. BCrypt로 해싱 | 비밀번호 |
| nickname | String | O | 공백만 불가, 40자 이하 | 닉네임 |

{"email":"test@example.com","password":"password1234","nickname":"테스트"}

#### LoginRequest (로그인 요청)

| 필드 | 타입 | 필수 | 제약 | 설명 |
|---|---|---|---|---|
| email | String | O | 이메일 형식, 120자 이하 | 가입한 이메일 |
| password | String | O | 72자 이하 | 비밀번호 |

#### MemberResponse (회원 응답)

| 필드 | 타입 | 설명 |
|---|---|---|
| id | Long | 회원 ID |
| email | String | 이메일 |
| nickname | String | 닉네임 |
| role | enum | ADMIN 또는 USER |

#### CsrfTokenResponse (CSRF 토큰 응답)

Swagger에는 object로만 나온다. 실제 응답은 아래 두 필드다.

| 필드 | 타입 | 설명 |
|---|---|---|
| token | String | CSRF 토큰 값 |
| headerName | String | 토큰을 담을 헤더 이름. 항상 X-XSRF-TOKEN |

---

## 공고

컨트롤러: PostingController. 1365에서 가져온 공고와 ADMIN이 직접 만든 공고가 같은 post 테이블에 저장된다. 요청한 회원은 URL이 아니라 로그인 세션에서 가져온다.

| Method | URL | 기능 | 권한 | 요청 | 응답 |
|---|---|---|---|---|---|
| GET | /api/v1/posting | 공고 목록 (요약, 최신 등록순) | 로그인 | 없음 | 200 PostingInfoDTO 배열 (목록 항목만) |
| GET | /api/v1/posting/{postingId} | 공고 단건 (전체 항목). 없으면 404 | 로그인 | 없음 | 200 PostingInfoDTO (전체 항목) |
| GET | /api/v1/posting/external | 1365 공고 검색. 우리 DB가 아니라 1365를 한 페이지씩 조회 | 로그인 | 쿼리 파라미터 | 200 PostingExternalDTO 배열 |
| POST | /api/v1/posting | 공고 직접 생성 (1365와 무관) | ADMIN | PostingCreateDTO | 200 PostingResponseDTO |
| POST | /api/v1/posting/external | 1365 공고 등록. 등록번호로 상세를 가져와 저장. 중복 409, 1365에 없으면 404 | ADMIN | PostingImportDTO | 200 PostingResponseDTO |
| PUT | /api/v1/posting/{postingId} | 공고 수정 (우리 DB만, 1365 반영 안 됨) | ADMIN | PostingUpdateDTO | 200 PostingResponseDTO |
| DELETE | /api/v1/posting/{postingId} | 공고 삭제. 신청 내역도 함께 삭제 | ADMIN | 없음 | 200 PostingResponseDTO (삭제된 공고) |
| POST | /api/v1/posting/{postingId}/application | 공고 신청. 모집 기간·모집 인원·중복 신청 확인 (409) | USER | 없음 | 200 PostingResponseDTO |
| DELETE | /api/v1/posting/{postingId}/application | 신청 철회. 신청 내역 없으면 404 | USER | 없음 | 200 PostingResponseDTO |

- 권한이 맞지 않으면 403 권한이 없습니다.
- 로그인 후 회원이 삭제됐으면 401 회원 정보를 찾을 수 없습니다. 다시 로그인해 주세요.

### 1365 공고 검색 쿼리 파라미터

| 파라미터 | 타입 | 기본값 | 제한 | 설명 |
|---|---|---|---|---|
| keyword | String | 없음 | 선택 | 검색어. 비우면 조건 없이 목록 조회 |
| pageNo | int | 1 | 1 이상 | 페이지 번호 |
| numOfRows | int | 10 | 1~100 | 페이지당 건수 |

전체 건수(totalCount)는 응답에 없다. 빈 목록이나 요청 건수보다 적은 결과가 오면 마지막 페이지다.

### 공고 DTO

#### PostingCreateDTO (공고 직접 생성 요청)

| 필드 | 타입 | 필수 | 제약 | 설명 |
|---|---|---|---|---|
| programTitle | String | O | 공백만 불가, 500자 이하 | 봉사 제목 |
| programContent | String | | | 내용 |
| programStartDate | LocalDate | O | | 봉사 시작일 |
| programEndDate | LocalDate | O | 봉사 시작일보다 빠를 수 없음 | 봉사 종료일 |
| activityStartTime | String | | 255자 이하 | 봉사 시작 시간 (형식 자유, 예: 09:00) |
| activityEndTime | String | | 255자 이하 | 봉사 종료 시간 |
| recruitmentStartDate | LocalDate | O | | 모집 시작일 |
| recruitmentEndDate | LocalDate | O | 모집 시작일보다 빠를 수 없음 | 모집 종료일 |
| recruitmentCapacity | Integer | O | 1 이상 | 모집 인원 |
| activityPlace | String | | 500자 이하 | 봉사 장소 |

Swagger 스키마에 programPeriodValid, recruitmentPeriodValid가 보이지만, 날짜 검증용 메서드가 노출된 것이라 보내지 않아도 된다.

{"programTitle":"환경 정화 봉사","programContent":"내용","programStartDate":"2026-12-01","programEndDate":"2026-12-02","activityStartTime":"09:00","activityEndTime":"18:00","recruitmentStartDate":"2026-11-10","recruitmentEndDate":"2026-11-30","recruitmentCapacity":3,"activityPlace":"서울"}

#### PostingUpdateDTO (공고 수정 요청)

PostingCreateDTO와 필드·제약이 같다. PUT이므로 수정하지 않는 항목도 모두 보내야 한다. 등록번호와 등록 기관은 수정할 수 없다.

#### PostingImportDTO (1365 공고 등록 요청)

| 필드 | 타입 | 필수 | 제약 | 설명 |
|---|---|---|---|---|
| programRegistrationNumber | String | O | 공백만 불가, 이미 등록된 번호 불가 | 1365 프로그램등록번호. 1365 공고 검색 결과에서 고른다 |

#### PostingResponseDTO (공고 생성·수정·삭제·신청·철회 응답)

값이 없는 항목도 null로 모두 내려온다.

| 필드 | 타입 | 설명 |
|---|---|---|
| id | Long | 공고 ID |
| programRegistrationNumber | String | 1365 프로그램등록번호. 직접 만든 공고는 null |
| programTitle | String | 봉사 제목 |
| programContent | String | 내용 |
| programStartDate | LocalDate | 봉사 시작일 |
| programEndDate | LocalDate | 봉사 종료일 |
| activityStartTime | String | 봉사 시작 시간 |
| activityEndTime | String | 봉사 종료 시간 |
| recruitmentStartDate | LocalDate | 모집 시작일 (신청 가능 기간의 시작) |
| recruitmentEndDate | LocalDate | 모집 종료일 (이날까지 신청 가능) |
| recruitmentCapacity | Integer | 모집 인원. 없거나 0이면 인원 제한 없음 |
| applicantCount | Long | 이 서비스에서 신청한 인원 |
| registeringOrganizationName | String | 등록 기관 (1365 나눔주체명). 직접 만든 공고는 null |
| activityPlace | String | 봉사 장소 |

#### PostingInfoDTO (공고 목록·단건 조회 응답)

필드의 뜻은 PostingResponseDTO와 같다. 목록 조회는 "목록" 열이 O인 항목만 담고, 단건 조회는 전부 담는다. 값이 없는 항목은 응답에서 아예 빠진다 (null로 오지 않음).

| 필드 | 타입 | 목록 | 단건 |
|---|---|---|---|
| id | Long | O | O |
| programRegistrationNumber | String | O | O |
| programTitle | String | O | O |
| registeringOrganizationName | String | O | O |
| activityPlace | String | O | O |
| programStartDate | LocalDate | O | O |
| programEndDate | LocalDate | O | O |
| recruitmentStartDate | LocalDate | O | O |
| recruitmentEndDate | LocalDate | O | O |
| recruitmentCapacity | Integer | O | O |
| programContent | String | | O |
| activityStartTime | String | | O |
| activityEndTime | String | | O |
| applicantCount | Long | | O |

#### PostingExternalDTO (1365 공고 검색 응답)

1365 응답 값을 그대로 전달한다. 날짜도 형식을 바꾸지 않은 문자열이다.

| 필드 | 타입 | 설명 |
|---|---|---|
| programRegistrationNumber | String | 1365 프로그램등록번호. 1365 공고 등록에 쓰는 값 |
| programTitle | String | 봉사 제목 |
| registeringOrganizationName | String | 등록 기관 (나눔주체명) |
| programStartDate | String | 봉사 시작일 (1365 원본) |
| programEndDate | String | 봉사 종료일 (1365 원본) |
| recruitmentStatus | String | 모집 상태 (1365 값, 저장하지 않음) |
| recruitmentStartDate | String | 모집 시작일 (1365 원본) |
| recruitmentEndDate | String | 모집 종료일 (1365 원본) |
| activityPlace | String | 봉사 장소 |
| programDetailUrl | String | 1365 상세 페이지 URL |

---

## 지도

컨트롤러: MapNoticeController, GeocodingController

| Method | URL | 기능 | 권한 | 요청 | 응답 |
|---|---|---|---|---|---|
| GET | /api/map/notices | 지도 마커 목록 | 공개 | 없음 | 200 MapMarkerResponse 배열 |
| GET | /api/map/notices/{noticeId} | 마커를 눌렀을 때의 공고 요약 | 공개 | 없음 | 200 MapNoticeSummaryResponse |
| GET | /api/map/geocode | 주소를 위도·경도로 변환 (카카오 API). KAKAO_REST_API_KEY가 없으면 503 | 로그인 | 쿼리 address(필수, 공백만 불가) | 200 GeocodingResponse |

- 지도 공고(map_notice)는 서버 시작 시 넣는 더미 3건이며, 공고 도메인의 post 테이블과는 별개다.
- 주소 변환은 카카오 API 사용량을 소모해서 로그인한 사용자만 쓸 수 있게 했다.

### 지도 DTO

#### MapMarkerResponse (지도 마커 응답)

| 필드 | 타입 | 설명 |
|---|---|---|
| noticeId | Long | 지도 공고 ID |
| title | String | 공고 제목 |
| latitude | Double | 위도 |
| longitude | Double | 경도 |
| status | enum | 모집 상태. RECRUITING(모집 중) 또는 CLOSED(마감) |

#### MapNoticeSummaryResponse (지도 공고 요약 응답)

| 필드 | 타입 | 설명 |
|---|---|---|
| noticeId | Long | 지도 공고 ID |
| title | String | 공고 제목 |
| organization | String | 주관 기관 |
| address | String | 활동 주소 |
| recruitStartDate | LocalDate | 모집 시작일 |
| recruitEndDate | LocalDate | 모집 종료일 |
| status | enum | RECRUITING 또는 CLOSED |

#### GeocodingResponse (주소 변환 응답)

| 필드 | 타입 | 설명 |
|---|---|---|
| address | String | 카카오에서 검색된 주소 |
| latitude | Double | 위도 |
| longitude | Double | 경도 |

---

## 테이블

MVP 필수 기능에 필요한 컬럼만 둔다.

| 테이블 | 컬럼 |
|---|---|
| member | id, email(unique), pw_hash, nickname, role, created_at, updated_at |
| post | id, program_registration_number(unique, 1365 공고만), program_title, program_content, program_start_date, program_end_date, activity_start_time, activity_end_time, recruitment_start_date, recruitment_end_date, recruitment_capacity, registering_organization_name, activity_place |
| post_application | id, post_id, member_id (post_id + member_id unique) |
| map_notice | 지도 담당 도메인 (이번 정리 범위 밖) |

> [!info]- 🔗 위키 연결
> - 상위: [[프로젝트]]
> - 개념: [[API(Application Programming Interface)]]
