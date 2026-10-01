# ShoppingMall PR Description Form

## 사용법
1. PR을 만들 때 아래 "양식" 코드 블록을 복사해 GitHub PR Description에 붙여넣고 채운다.
2. `<!-- -->` 주석은 GitHub 화면에 표시되지 않으므로 지우지 않아도 된다.
3. 해당 없는 섹션은 지우지 말고 "없음"으로 적는다. 검토했는데 없는 것과 빠뜨린 것을 구분하기 위함이다.
4. 변경 사항은 파일 단위가 아니라 동작(기능) 단위로 적는다. 파일 목록은 GitHub Files changed 탭에서 이미 보인다.
5. 변경 이유에는 "문제 → 해결 → 택하지 않은 대안"을 적는다. 나중에 같은 고민을 반복하지 않기 위한 기록이다.

## PR 제목 규칙
- 형식: `<type>: <요약>` (소문자 type, 콜론 뒤 한 칸, 요약은 명령형)
- type: `feat`(기능 추가) / `fix`(버그 수정) / `refactor`(동작 변화 없는 구조 변경) / `test`(테스트) / `chore`(설정·빌드·의존성) / `docs`(문서) / `ci`(CI/CD)
- 예: `fix: unify standard exception response format`

---

## 양식

```markdown
## 개요
<!-- 이 PR이 무엇을 하는지 1~2줄 -->


## 변경 사항
<!-- 동작(기능) 단위로. 해당 없는 줄은 삭제 -->
- [추가]
- [수정]
- [삭제]

## 변경 이유
<!-- 변경 사항마다 1개씩. 문제에는 증상과 근거(에러 메시지, 재현 방법)를 적는다 -->
1.
   - 문제:
   - 해결:
   - 택하지 않은 대안:

## 검증
<!-- 실행한 명령, 추가/수정한 테스트, 수동 확인 결과(요청 → 응답) -->
- [ ] `./gradlew test` 통과
- [ ] 추가/수정한 테스트:
- [ ] 수동 확인:

```

---

## 작성 예시 (dev/globalconfig 예외 처리 PR 기준)

```markdown
## 개요
Spring MVC 표준 예외가 500으로 바뀌던 문제를 고치고, 모든 에러 응답 바디를 ApiResponse 형식으로 통일한다.

## 관련 기록
- copilot-addendum.md [20260930 ~ 20261006] 구현 기능 관련 문제점 7번

## 변경 사항
- [수정] GlobalExceptionHandler가 ResponseEntityExceptionHandler를 상속
- [수정] handleExceptionInternal 오버라이드: 표준 예외 응답 바디를 ApiResponse로 변환, 4xx warn / 5xx error 로그
- [수정] @Valid 실패 처리를 @ExceptionHandler(MethodArgumentNotValidException)에서 handleMethodArgumentNotValid 오버라이드로 이동

## 변경 이유
1. 표준 예외 상태코드
   - 문제: @ExceptionHandler(Exception.class)가 모든 예외에 매칭되어 깨진 JSON(400), 미지원 메서드(405)까지 500으로 응답
   - 해결: ResponseEntityExceptionHandler 상속으로 표준 예외 20종을 올바른 4xx/5xx로 매핑
   - 택하지 않은 대안: catch-all 삭제(응답 형식이 Spring Boot 기본 /error 형식과 ApiResponse로 갈라짐), 표준 예외 개별 핸들러 추가(20종 누락 위험)
2. 응답 바디 통일
   - 문제: 상속만 하면 표준 예외가 ProblemDetail 형식으로 나가 ApiResponse와 형식이 둘로 갈라짐
   - 해결: handleExceptionInternal에서 ProblemDetail/ErrorResponse의 detail을 꺼내 ApiResponse로 감쌈
   - 택하지 않은 대안: ex.getMessage() 사용(내부 메서드 시그니처, 입력값, JSON 파서 메시지 노출)
3. @Valid 처리 이동
   - 문제: 상속 후에도 같은 예외에 @ExceptionHandler를 두면 Ambiguous @ExceptionHandler로 기동 실패
   - 해결: handleMethodArgumentNotValid 오버라이드로 이동, 첫 필드 에러 메시지 유지

## 검증
- [ ] `./gradlew test` 통과
- [ ] 추가/수정한 테스트: 깨진 JSON 400, @Valid 400, 미지원 메서드 405
- [x] 수동 확인: MockMvc로 위 3건 + 타입 불일치 400, PathVariable 누락 500 응답이 ApiResponse 형식인지 확인

## 영향 범위
- API 계약: 표준 예외 상태코드가 500에서 실제 코드(400/405 등)로 변경, 바디 형식은 기존 ApiResponse 유지
- DB 스키마(Flyway): 없음
- 환경변수/설정: 없음
- 프론트엔드 수정 필요: 없음(에러 시 message 필드 사용 방식 동일)

## 남은 작업
- @Valid 실패 응답에 field/reason 목록 추가
- 컨트롤러 예외 매핑 테스트(Phase 2)
```
