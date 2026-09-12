## 안티패턴

코드들 살펴보니까 동일 안티패턴이 거의 모든 곳에서 동시 다발적으로 일어나고 있음. 따라서 “모든”이 포함된 토글들만 봐도 상관없을 것 같음.

- 들여쓰기를 정형화
    
- 파라미터가 3개 이상인 메서드는 dto로 정형화하기(컨트롤러의 경우 Map대신 dto입력 및 응답 필요)
    
- URI Name pattern : String으로 직접 주입 시 추후 api url 수정할 경우, 모든 코드들을 뜯어고쳐야 될 수 있음 → ApiURLNames와 같은 url 상수화 클래스 요구, 추가적으로 일부 getMapping같은 경우들은 url을 설정하지 않았는데, 빈 문자열로 상수화해서 용도별로 매핑해놓을 경우, 추후에 url을 설정하게 되었을때 편리함.
    
- ADMIN같은 role 또한 위처럼 상수화 요구(enum으로 관리)
    
- 전반적으로 NPE를 layer마다 걸어주는게 좋음
    
- HttpStatus.NOT_FOUND를 던지지말고 이렇게 해보는게 어떰?
    
    - GlobalNimdaException을 상속 받은 NotFoundException에 ErrorCode.CATEGORY_NOT_FOUND를 던지는데, ErrorCode에 enum으로 HttpStatus.NOT_FOUND + 통일된 Error Message를 넣고, 에러를 던지게 되는거임. 그러면 실질적으로 NotFoundException을 통해 던진 에러는 HttpStatus.NOT_FOUND(404) + 통일된 Error Message인데, 다음과 같은 이점을 건질 수 있음.
        - 테스트 코드 작성이 편함 : 메시지도 잘 전달되는지 테스트하는데, 이때 ErrorCode class하나만 보고도 모든 메시지를 확인 가능함.
        - 메시지가 부정확하거나, 변경하고 싶은 경우, Controller에서 일일이 찾아 고칠 필요가 없어짐.
    
    ```
    packagecom.shopping_mall_api.global.exception;
    
    importlombok.Getter;
    
    @Getterpublic classGlobalShoppingMallException extendsRuntimeException{
        private finalErrorCode errorCode;
    
        publicGlobalShoppingMallException(ErrorCode errorCode){
            super(errorCode.getMessage());
            this.errorCode= errorCode;
        }
    
        publicGlobalShoppingMallException(ErrorCode errorCode, String errorMessage){
            super(errorMessage);
            this.errorCode= errorCode;
        }
    }
    ```
    
    이렇게 모든 exception의 super class를 만들고,
    
    ```
    packagecom.shopping_mall_api.global.exception;
    
    public classNotFoundException extendsGlobalShoppingMallException {
        publicNotFoundException(ErrorCode errorCode) {
            super(errorCode);
        }
    
        publicNotFoundException(ErrorCode errorCode, String errorMessage){
            super(errorCode, errorMessage);
        }
    }
    
    ```
    
    상속만 해주셈. 그리고
    
    ```
    USER_NOT_FOUND(HttpStatus.NOT_FOUND, "U001", "User not found"),
    USER_ALREADY_EXIST(HttpStatus.BAD_REQUEST, "U002", "User already exist"),
    USER_UPDATE_FAILED(HttpStatus.BAD_REQUEST, "U003", "User info cannot update"),
    USER_PASSWORD_UNMATCHED(HttpStatus.BAD_REQUEST, "U004", "User password unmatched"),
    EMAIL_NOT_FOUND(HttpStatus.BAD_REQUEST, "U005", "Email not found"),
    ```
    
    이런식으로 Enum에 오류 코드들을 나열하면, error id를 통해 어디가 잘못된건지 파악하기도 쉽고, 메시지도 통일되어 있고, 오류코드 수정하는것도 쉬움.
    

### 모든 Controller

- 모든 컨트롤러에서 jwt관련된 문제 발견, 다음과 같은 방식으로 통일 요구
    - jwt세팅을 user detail이 아닌 userId로 세팅하는 것이 좋아보임 : 필요한 곳에서 requestbody를 통해 비용을 발생시키는 구조여야 하는데, user detail을 통채로 jwt로 만들어 놓으면, 사용하지 않는 곳에서도 정보가 노출됨.
    - pathvariable이 아닌 authenticationPrincipal을 통해 서블릿 필터를 거쳐 뽑힌 userId를 context에서 꺼내 사용하는 방식이 훨씬 스프링스럽고, jwt세팅에서 맞는 것 같음(일부 미적용)
- 모든 컨트롤러의 반환값을 ResponseEntity< ? >가 아닌 ResponseEntity<ApiResponse<”Entity에 맞는 responseDTO”>>형식으로 반환하는 것이 깔끔함
- URL 상수화
- try-catch를 통해 예외를 컨트롤러에서 발생시키는 것이 아닌, ExceptionHandler에게 넘기는 것이 좋음.
- npe / data validation check를 깔끔하게 (자세한 예는 밑에 적어놓음)
- 반환 객체 통일 및 와일드 카드 사용 지양
- controller에는 절대 service에서 실행되어야 할 코드들을 넣지 말것(getAllusers같은 경우, stream을 실행하는 것이 아닌, service에서 완성된 반환 객체를 가져와서 사용)
- builder을 통한 생성자
- 현재 try-catch문을 통해 유저정보를 찾지 못하는 경우에 예외를 발생(에러문 생성)을 하도록 코드가 구현되어 있는데, 외부에서 공격하였을때, 정보가 제대로 뽑히는지 확인할 수 있는 척도가 될 수 있음 → 따라서 개인적으로 추천하는 방식은 공통 ApiResponse 객체에 성공만을 넣고, http status를 200이나, 400, 404등을 넣어서 반환해주는 방식을 추천함(이때 상태코드도 다양하게 넣으면 척도가 될 가능성이 높으므로 단순하게 통일하고, 메시지를 통해 확인할 수 있도록 함
- requestbody dto로 매핑하기(내부 맵을 사용하게 될 경우, webserver와 field가 일치하지 않을 수 있습니다.)
- 전반적으로 예외를 컨트롤러 내부에서 발생하는 것이 아닌 restcontrolleradvice를 통해 예외의 주체를 넘기는 것이 좋습니다.
- 역할전환 메서드 같은 것들은 sql쿼리를 다이렉트로 보내는 것이 안전할 것입니다.
- delete작업에 대해 컨벤션이 두 가지로 나뉩니다. 통일 요구
    - void return : 반환값이 존재하지 않아 외부에서 해당 내용이 실존해서 삭제되었는지 파악하지 못하도록 합니다.
    - dto return : 삭제된 dto를 반환하여 삭제가 되었는지 파악할 수 있습니다.
- Id : 서블릿 필터를 통해 @AuthenticationPrinciple으로 context에서 userId를 뽑아 사용하도록 변경(jwt / cookie 세팅이 되어있는 것을 판단)
- ResponseEntity반환을 ResponseEntity.ok이런식으로 반환하면 좋음. 이때 에러가 발생하면 200이 아니라 500 이런식으로 반환하기 때문에 하나로 뭉치는 것도 추천.
- Map, List로 만드는 것을 제발 controller에서 멈춰주세요
- optinal을 service 리턴값으로 반환받으면 안됨. optional을 repository에서 반환해주는 이유는, service layer에서 예외를 던져 데이터를 확인하라는 차원에서 넣었는데, 컨트롤러에서 예외를 확인하는 흐름을 발생해서는 안됨. (컨트롤러에서 발생하는 예외는 공통에서 언급한대로 restcontrolleradvice를 통해 넘겨줘야함.
- controller에서 respository를 의존하는 코드가 간간히 보이는데, service에서 처리할 수 있도록 기능을 옮기는 것을 추천

### 모든 DTO

- Setter 빼기 : 현재 spring boot에서는 setter을 통해 인자 넘기기를 지양하는 중임. 남용 및 일관성을 해칠 수 있음. 따라서 setter보다는 특정 필드를 고치는 메서드를 컨벤션에 맞춰 네이밍하는게 좋음.
- Builder 통일 요구. 이때 dto → entity로 매핑하는 과정이나, Entity → dto로 매핑하는 과정은 builder을 사용한 생성자를 호출하는 생성자 형식으로 하는게 좋음.

### 모든 Entity

- BaseEntity 상속되지 않은 Entity존재
- 컬럼명을 일일이 지정해주었는데, 이런식으로 계속 지정을 할거면 상수화가 맞고, auto snakecase to camelcase(gradle에는 있었는데 maven은 잘 모르겠음)같은 기능이 존재할 수도 있으니까 확인하고 정하길 바람.(이때 like같은 sql쿼리문이 가능한 것들은 에러 발생가능하니까 주의)
- tableName을 상수화 해서 테이블로서 관리하는 것도 좋아보임
- 마샬링 / 언마샬링 : getter + NoArgsConstructor를 필요 + 생성자는 Builder로, 엔티티로 변환은 Builder를 활용하여
- 궁금한게 있는데, orphanremoval같은 고아객체 삭제는 안걸어 두는게 규칙임? 아니면 고아객체 삭제도 걸어두는게 좋아보임.

### 모든 Service

- Authwired를 통한 의존성 주입 → requiredArgsConstructor로 변경
- transactional을 클래스 위로 readonly로 빼고, write가 필요한 create/update에만 transactional을 사용
- 반환형식을 responseDTO로 반환
- 파라미터가 많으면 dto로 매핑해서 requestDTO만들기(한 개여도 통일하는게 좋아 보임)
- repository에서 꺼내올 때, optional일 경우 orElseThrow를 통해 항상 해당 데이터가 존재하는지 확인 후 사용할 것(이때 예외 따로 생성해서 관리하는 것을 추천)
- service에서 service를 의존성으로 추가하였는데, 왜 이렇게 되었는지 잘 모르겠음. service를 서로 참조하게 되면, 무한 순환참조로 인해 런타임 오류가 발생함 → 최대한 repository를 의존성으로 갖도록 해야 함.
- transactional(readOnly = true)로 class밖에 걸어놓고, cud가 발생하는 메서드에 transactional붙이기 : 권한을 필요한 만큼만 줄 수 있고, 중복코드 줄일 수 있음.
- NPE문제를 하나의 클래스에서 전체관리할 수 있도록 할 수 있음.

```
packagecom.shopping_mall_api.global.config;

importjava.util.List;
importjava.util.Objects;

public class CheckConfig<T>{
    public static<T> void npeCheck(Tdata, String fieldName){
        Objects.requireNonNull(data, () -> fieldName+ " : must not be null");
    }

    public static void npeAndBlankCheck(String data, String fieldName){
        npeCheck(data, fieldName);
        if(data.isBlank()){
            throw newIllegalArgumentException(fieldName + " : must not be blank");
        }
    }

    public static void npeAndNegativeCheck(Long data, String fieldName){
        npeCheck(data, fieldName);
        if(data < 0){
            throw newIllegalArgumentException(fieldName + " : must not be negative");
        }
    }

    public static<T> void npeAndEmptyCheck(List<T> data, String fieldName){
        npeCheck(data, fieldName);
        if(data.isEmpty()){
            throw newIllegalArgumentException(fieldName + " : must not be empty");
        }
    }
}
```

이렇게 npeCheck, 각 데이터 타입별로 필요한 메서드를 설정해두고, 값의 정당성을 체크하는 방식이 있음. 보통은 @Valid 어노테이션으로 데이터 유효성을 검사하지만, 이는 컨트롤러 레이어에서 책임지는 타입 검증이지만, service레이어에서는 Valid를 사용하지 않으므로, 이처럼 공통 npe 체크가 가능함. (현재 attachment의 입력값에서 file이 비어있을 경우, RuntimeException을 발생하게 되는데, 이를 묶어서 추상화가 가능하다는 뜻)

### User

### 공통

- @Autowired를 통한 DI보다 @RequiredArgsConstructor을 통해 주입 받는 방식이 현재 스프링 부트에서 권고하는 사항임

### Controller

- cookie : 쿠키를 왜 controller에서 만드는 것이 아닌 service레이어에서 accessToken / refreshToken을 생성하고 반환해주면 곧바로 헤더에 설정하는 것이 좋음
- register을 controller에서 구현하는게 맞을까? 그리고 반환 받는 객체도 user로 받게 될 경우, password도 노출될 수 있으니 userResponseDTO를 만드는 것이 좋아 보임.
- 개인적으로 DTO 네이밍 컨벤션이 조금 불편한데, 현재 기능 + 도메인 + DTO이런식으로 되어있는데, 도메인 + 기능 + DTO로 바꾸는게 좀 더 좋아보임.(근데 이건 진짜 관점차이라서 크게 상관 x)
- jwt provider / jwt util을 나눈 이유를 모르겠음.

### UserRecoveryController

- requestbody의 dto 네이밍 불일치
- cookievalue를 사용할 것인지 authenticationPrincipal을 사용할 것인지 판단해야 하는데, 후자를 추천함. 이유는 cookie에 userInfo를 전부 담으면 안된다고 생각하기 때문

### DTO

- userInfo처럼 추가적인 detail이 필요한 클래스들은 record로 정하는 것도 좋아보임.
- DTO 네이밍 패턴이 한눈에 알아보기 힘듬

### Entity

- Authrotiy는 BaseEntity를 상속받지 않음.

### Security

- CustomUserDetail에 사용하지 않은 메서드들이 상태들을 반환해주는 메서드들로 추후 구현 예정처럼 보이는데, 상태에 대한 메서드들은 엔티티에서 반환해주는게 좋아보임.

### Service

- 디버깅용 로그 출력문 삭제
- login에서 테스트 까지 진행하는 것은 말이 안됨. 그리고 authentication을 통해 context에 유저 정보를 직접 주입했는데, 이건 좋지 않은 패턴인 것 같음. 주입을 필터를 통해 유도하는 것이 깔끔해 보임.

### EventListener

### LoginEventListener

- log는 찍지 말고, 테스트 코드로 남기는 것이 좋아 보임.
- 이벤트 리스너의 경우 로그를 찍지 않은 이상 상태의 변화 감지를 파악하는게 어려워 보임. 따라서 test code를 통해 변화를 한번씩 감지해보는 것도 좋아보임

### RegisterEventListener

- 구현체가 없어서 패스

### Domain

### attachment

- dto에 마샬링 / 언마샬링 언급이 있는데, 필요한 NoArgsConstructor가 없음. 추후에 문제가 될 수도 있음
- 여기서 delete가 원래 컨벤션이 삭제한 데이터를 반환값으로 돌려주는 것으로 보이는데, attachService에서는 적용되지 않았음.
- LocalFileStore에서 uploadProblemFile 미구현

### attendence

- url에 대문자 넣는 패턴 발견 : “checkIn”말고 check-in과 같은 방식으로 패턴 통일
- userId로 orElseThrow를 던지는데 예외가 없는 경우도 존재 (getUserAttendence())

### Board

- controller에서 repository를 의존하는 끔찍한 패턴 발견 : MVC패턴을 완전히 무시하는 코드이므로, repository에서 찾는 기능을 전부 service레이어로 내릴 것을 추천
- requestParam을 사용하는 HTTP Method Request 방식을 보았는데, requestparam은 web server - was사이에서의 네이밍 패턴이 서로 다르거나, 예약어 충돌 등의 이유로 reqeust의 필드명과 parameter명이 서로 다를 경우 매핑시켜주기 위함이지, 지금처럼 서로 통일되지 않은 네이밍을 억지로 끼워맞추기용도가 아님. 따라서 통일 요구

### Comment

- BaseTime이 있는데, 이걸 responseDTO에 상속해서 사용
- STATUS도 commentStatus로 네이밍 변경
- service 예외도 “부모 댓글을 찾을 수 없습니다” 같은 경우 NotFoundException으로 통일. (다른 것들도 예외상황에 맞는 예외처리 + 에러코드로 바꾸기)

### Notification

- Entity에 baseEntity 상속 + createAt삭제
- repository이름 잘못됨 (NotificationRepositroy → NotificationRepository)
- delete할때, notificationId가 null일 경우, npe가 터질 수 있음

### Point

- DTO 언마샬링 불가 : 기본생성자가 없음