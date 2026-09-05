# 1주차 질문

1. 현재 ApiResponse라는 공통 응답을 설정하고, userController부분에서 사용하지 않음 : 공통된 응답 방식이 존재하지 않아 controller내부에서 일일이 success, message, data부분들을 map으로 반환하는 모습이 보임 (예를 들어 adminuserservice에서 findall은 list전체를 apiresponse가 아니라 그냥 리스트로 반환해줌)
2. Builder을 일부분에 사용하는 모습을 보여줌 : setter나 allargsconstructor을 사용하는 것보다 일관된 방식으로 생성할 수 있고, setter은 보안에 취약한 모습을 보이기에 수정하는 것이 좋아보임
3. 예기치 않은 오류가 발생했을 때, RuntimeException과 Exception으로만 예외를 처리하는데, 이보다 errorcode + exception handler을 통해 상황에 맞는 예외를 던지는게 추후 오류 발생 시 로깅하기 편리해보임. (user정보를 찾지 못했을때, NotFoundException + ErrorCode.USER_NOT_FOUND이런식으로 리턴하는 것이 좋아 보임, 이러면 user정보를 찾지 못해서 에러가 던져졌는지, 권한이 일치하지 않아서 에러를 던졌는지 등을 알 수 있을듯)
4. Id를 왜 pathvariable로 받는지 모르겠음. jwt가 구현된 현재, 쿠키에서 accessToken을 필터를 거치게 되면 userId의 주입 없이 token에서 userId를 AuthenticationPrincipal을 통해 받을 수 있는데, 이렇게 구현한 이유를 모르겠음
5. request를 dto로 매핑하는 것이 아닌 map으로 받는 이유를 모르겠음. dto는 data transfer object, 즉 request response의 형식을 front와 통일하게 되는데, 이 방식으로 일관된 request, response를 받는게 더 좋아보임.
6. url : api url을 상수로 빼내어 추후에 url이 다소 엉키더라도 하나의 파일에서 모든 의존성을 리펙토링할 수 있도록 하는 것이 편해보임
7. 와일드카드(?)사용보다 명시해주는게 추후에 testcode작성에 훨씬 편함
8. autowired보다 requiredargsconstructor을 통해 서비스 의존성을 주입받는게 좋아 보임 : 최근 것들은 다 그렇게 해놨던데, user처럼 과거에 만든 파일에 대해 리펙토링이 아직 안된 것으로 판별
9. UserRecoveryService의 존재 
	1. npe check : 기본적으로 controller 레이어에서 @Valid를 통해 입력값을 검증하고, 들어오는데 이때 각 레이어의 책임분산에 따라 각각 npe check가 필요하다면 npe를 전적으로 체크해주는 config를 통해 체크해주는 것이 바람직해 보임(Objects.requireNonNull)
	2. column -> dto : dto로 각 컬럼들을 매핑해주는 것은 생성자(빌더)를 통해 해주는 것이 바람직해 보임
	따라서 userservice에 userid를 확인하는 코드를 넣고, npecheck config를 global하게 만들게 되면, 사용처가 전혀 존재하지 않은 service로 리펙토링 가능함.
10. usernotapprovedexception : 이것도 baseEntity처럼 공통된 exception 틀을 만들어둔 뒤에 상속받아서 사용하는 것이 좋아보임.
11. 가끔 service내부에서 다른 service의 의존성을 볼 수 있는데, 이거 잘못하면 무한 순환 참조로 런타임 에러 남 (최대한 respotiory로 의존성을 갖게 하고, 만약에 추가적인 기능이 필요할 경우에는 해당 service에서만 단방향 의존성을 갖는 service를 생성하는게 좋음, 현재는 문제 없음)
12. authservice에서 validateuser에서는 findbyuserid해서 optional을 그대로 사용하는데, login에서는 왜 optional에서 orelsethrow를 던짐? optional은 기본적으로 service에서 repository를 통해 가져오게 되면 null을 긁어오진 않았는지 확인을 강제하려고 만들었는데, optional을 반환하는게 좀 이해 안됨.
13. 종종 url 맨 앞에 / 가 없음 : 이것도 url 상수화 하면 다 해결될듯?