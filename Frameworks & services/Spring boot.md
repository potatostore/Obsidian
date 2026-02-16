# 0. Spring boot

Spring boot를 자바를 통해 앱 백엔드를 구성하는 도구로 생각하는 것이 일반적이다.

Spring boot의 사전적인 의미를 찾아보게 되면

*Spring boot is a framework for build applications in the java programming language.*
즉, Spring boot는 자바 언어를 통해 앱을 구축하는 framework이다.

특히 Spring application API를 구축하는데 도움을 주는 도구들의 집합을 Spring boot라고 한다.

그럼 Spring application은 무엇일까?

---
#### Spring application

코드를 작성하고, 하나의 프로젝트(app)을 완성하게 되면, 90/10의 법칙에 의해 10%의 코드가 전체 실행 시간의 90%를 차지한다.

이는 일부 코드의 재사용율이 매우 높다는 뜻이고, 이러한 재사용율이 높으면서, 필수적으로 사용해야 하는 코드를 우리는 *보일러플레이트 코드*라고 한다.

즉 프로젝트 전반적으로 핵심적인 코드 일부를 뜻하며, 그렇기에 변경이 거의 없다.

그런데 만약에 이 핵심적인 코드들이 몇 줄만 실질적으로 사용되고, 나머지의 코드들이 버려진다면 어떻게 될까?

```java
Connection conn = null;
PreparedStatement ps = null;
ResultSet rs = null;

try {
    conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb", "user", "password");
    ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
    ps.setLong(1, userId);
    rs = ps.executeQuery();
    
    if (rs.next()) {
        // 데이터 처리 로직
        // User user = new User();
        // user.setId(rs.getLong("id"));
        // ...
    }
} catch (SQLException e) {
    // 예외 처리 로직
    e.printStackTrace();
} finally {
    // 자원 해제 (가장 중요한 보일러플레이트)
    if (rs != null) {
        try {
            rs.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    if (ps != null) {
        try {
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    if (conn != null) {
        try {
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

try-catch-finally문을 살펴보면, 아마 위 코드를 실행할 경우 try 내부문만 실질적으로 사용되고, 밑의 코드들은 사용이 거의 안될 것이다.

근데 catch,finally문을 제외할 수 있는가에 대해 생각해보면 불가능하다.

따라서 자주 사용되는 보일러플레이트 코드(try 문)을 변경하여 실행 시간을 줄이고자 하였고, Spring 어플리케이션은 이러한 보일러플레이트 코드를 줄이기 위해 만들어졌다.

위 기능에 더해, java app를 만드는데 편리한 기능, 도구들을 제공한다.

---

그렇다면 Spring app 어떤 도구를 통해 보일러플레이트 코드를 최소한으로 하여 목적을 달성하려고 할까?

App은 단일동작이 불가능하다. 즉, application을 구성하는 코드만으로는 동작이 불가능하고, 서버, DB등 다양한 요소가 상호소통을 해야 우리가 아는 App이 되는 것이다.

상호소통을 하는 경우, 소통을 위한 규칙인 API가 필요할 것이고, 이를 규정하고, 설정함으로서 App과 다양한 요소 간에 상호소통이 가능해질 것이다. (API가 없어도 가능은 할 수 있지만, 없을 경우 개발 효율성이 매우 떨어질 것이다. 따라서 API는 필수적이다.)

흔히 다양한 요소 간에 정보를 주고 받을 경우, 사용하는 요소가 바로 서버일 것이고, Spring App에서도 Tomcat이라는 서버가 존재한다.

즉 내장된, 독립된 웹서버가 spring boot 내부에 존재하고, 인프라를 구성한다는 뜻이다.

추가적으로 단일 주석을 통해 Spring application context를 수동으로 설정할 필요성을 대체한다.

??

이게 무슨 말일까?

먼저 Spring application context에 대해 알아야한다.

---
#### Spring application context

Spring API를 성공적으로 구축하고, App을 실행시키기 위해서는, Spring application context가 필요하다.

```java
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

// Spring 설정 클래스
@Configuration
@ComponentScan("com.example.app") // <-- 1. Bean을 찾을 패키지를 지정
public class AppConfig {
    // 필요한 경우, @Bean 메소드를 직접 작성하여 Bean을 등록
    // @Bean
    // public DataSource dataSource() { ... }
}

public class MySpringApp {
    public static void main(String[] args) {
        // <-- 2. 개발자가 직접 ApplicationContext를 생성
        ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);

        // <-- 3. 컨텍스트에서 Bean을 직접 가져와 사용
        MyService myService = context.getBean(MyService.class);
        myService.doSomething();
    }
}
```

위 또한 반복적이고, 번거로운 보일러플레이트 코드이다.

*com.example.app*라는 패키지에서 Bean을 찾아 등록하고, 사용하는 것은 번거롭다.

따라서 Spring boot에서 이를
```java
@springbootapplication //single annotation
```
위 단 한 문장으로 줄여버렸다.

앞선 보일러플레이트 코드의 간결화를 달성한 것이다.

---

근데 위 설명을 읽다가 모르는 점이 존재하지 않았는가?

바로 *Bean*이다.

이는 Spring boot의 꽃인 *의존성 주입*과 관련된 내용이기에 추후에 의존성 얘기와 함께 설명하겠다.

---

Spring boot란 것은 통상적으로 다양한 application dev tools를 제공하기 위해 여러가지의 Spring이 존재한다. Spring web, Spring JDBC 등 이러한 도구들을 통틀어서 Spring이라고 부르고, 이러한 Spring을 더욱 쉽게 설정하고, 보일러플레이트 코드를 줄이기 위해 Spring boot가 나온 것이다.

# 1. Spring

Spring Application Project를 생성할 때, 수많은 설정을 수동적으로 설정하게 되면 프로젝트 생성부터 힘이 빠진다.

그렇기에 Spring initializr가 존재하는데, 이는 웹사이트에서 Project compiler, Language, model등을 설정하고, 의존성 설정이 이루어진다.

---
#### 의존성(종속성)

Spring boot를 입문할 때, 가장 많이 듣는 장점이 의존성 주입이 간편하다는 것이다.
그래서 포기를 많이 했던 것 같다.
의존성이 무엇인지 정확히 인지를 못하기에 Spring boot의 장점이 크게 와닿지 못했기 때문이다.

의존성을 상속과 비슷한 개념으로 출발한다.

상속은 쉽게 말하면 부모 클래스의 모든 속성을 자식 클래스가 이어 받는다.
이는 다른 말로 부모 클래스의 일부가 수정될 경우, 자식 클래스가 영향을 받아 수정된다.

의존성은 이와는 다른데, 다른 클래스의 속성을 가져와 사용할 수 있도록 만드는 것이다.

상속은 is-a방식으로 사용되지만, 의존성은 has-a방식으로 사용이 되는데, 상속은 클래스에 다른 클래스의 기능들을 메모리를 할당하여 부여하지만, 의존성은 다른 곳에 할당되어 있는 메모리의 주소를 참조하여 해당 메모리에 접근하여 기능을 구동시키는 개념이다.

즉 상속의 개념처럼 모든 속성을 물려 받는 것이 아니라, 해당 클래스의 속성을 가져와 사용을 한다. 이는 참조의 개념으로 해당 클래스의 인스턴스를 만들어 call by value형식으로 사용하는 것이 아니라 call by reference방식으로 사용하게 된다.

기능 구현에서 의존성을 주입할 경우 위와 같은 역할을 수행하지만, 빌더를 통한 의존성을 관리할 경우, 다음과 같은 역할도 수행 가능하다.
1. 개발 편의성 : 개발자가 일일이 라이브러리를 다운받거나, 배포시 탑재하지 않아도, 빌더를 통해 다운받을 수 있도록 만들어 준다.
2. 버전 충돌 방지 : 호환성의 문제로 인해 여러 라이브러리들이 충돌하는 문제가 발생할 수도 있지만, 수동적으로 다운로드를 하지 않고, 지정된 버전을 자동으로 다운 받기에 버전 충돌 문제가 발생하지 않는다. 
3. 필요한 기능을 쉽게 구현 : 미리 만들어진 기능(DB 연결, 웹 구현 등)을 의존성 주입 코드 한 줄로 가져와 사용할 수 있다.

즉 전반적인 내용으로 보면 의존성은 인터넷을 통해 가져와 사용하는 것이고, 이를 코드 관점에서 바라보았을 때, 주소 접근 방식으로 사용하는 점에서 매우 편리함을 제공한다고 볼 수 있다.
*싱글톤(Singleton) : 의존성 객체 하나만 생성하여 다른 클래스에서도 접근하여 사용할 수 있도록 만드는 방식*

---
#### URI / URL

앞선 개념 중에 *URI(Uniform Resource Idenfier)* 와 *URL(Uniform Resource Locator)* 의 차이가 분명하지 않아 매우 헷갈렸다.

Rest API의 핵심개념 중 하나인 모든 데이터를 하나의 자원으로 취급하는 것은 하나의 URI와 비슷하다. URI는 자원이 어떤 것이 존재하는지 확인하는 고유의 식별자로, 나타내는 방식은 종류별로 다르겠지만, 나타내는 방식을 통해 어떤 자원인지 확인하고, 가져올 수 있는 모든 식별자들을 의미한다.

URI는 크게 두 가지의 종류로 나뉘는데, *URL*과 *URN*이다.

*URN*은 urn:isbn:0451450523 과 같이 자원의 이름을 부여하고, 해당 자원의 식별 변호를 부여하게 된다. 앞선 예시는 책의 isbn 번호를 표현한 예시이다.

*URL*은 자원이 존재하고 있는 위치 주소를 의미하게 된다.
즉, URL을 통해 타고 들어가면 존재하는 자원을 어떤 프로토콜을 통해 접근이 가능한지 나타내는 식별자이다.

---
#### Endpoint

URL방식을 통해 자원에 접근을 할 때, 서버의 주소와 해당 자원의 경로를 특정하여 URL을 완성하고, 해당 URL을 통해 자원에 접근하여 HTTP Method를 통해 자원을 얻어 온다.

이때, 경로를 *Endpoint*라고 하며, https://github.com/potatostore/Obsidian.git 에서 서버의 주소를 제외한 뒤의 경로, 즉 potatostore/Obsidian.git이 *Endpoint*라고 설명할 수 있다.

---
#### IoC container

위 의존성을 이해하게 되면, 의존성을 구현하기 위해 하나의 객체가 무조건적으로 필요하고, 해당 객체의 주소를 반환하여 클래스 기능들을 사용할 수 있도록 만들어주는 로직 또한 필요하다는 것을 느낄 것이다. IoC container가 이에 해당되며, IoC container에 배열 형식처럼 선언된 객체들이 존재하고, API를 통해 일부 기능들을 호출할 경우 필요하지 않는 기능이나 변수들을 가져오는 것과는 다르게 IoC container은 필요한 일부분만을 가져와 사용할 수 있다. 

---
#### Bean

Bean은 IoC container에 생성된 객체들을 가르킨다. Bean을 생성하는 방식은 매우 간단한데, 바로 어노테이션이다. 한국말로 주석이란 뜻을 갖고 있는 어노테이션은 우리가 평상시에 사용하는 코드 내 주석과는 다르게 @를 통해 container에 객체를 만들거나, 가져와 사용하는 용도로 사용을 한다. 즉 의존성 주입 및 사용을 목적으로 @를 사용하고, IoC cotainer 내부에 존재하는 객체들을 spring boot에서는 *Bean*이라고 부른다.

---
#### 빌더

빌더들은 다음과 같은 역할을 수행한다.
1. 종속성 관리 : 앱을 만들어서 배포를 시행했을 때, 필요한 라이브러리 등을 수동적으로 설치해야하는 문제가 발생하고, 이를 maven과 같은 빌더들이 인터넷에서 필요한 JAR 파일을 직접 다운 받아 해결한다.
*JAR 파일 : Java Archive 파일로, 자바 클래스 파일, 파일에 대한 메타데이터, 리소스 등을 하나의 파일로 압축시켜 놓은 파일을 의미한다.*
2. 빌드 자동화 : Maven과 같은 빌더는 프로젝트 빌드 프로세스를 자동화하여 개발자가 소스 코드를 컴파일하고, 테스트를 실행하며, 배포 가능한 아티팩트를 생성하는 작업을 효율적으로 수행할 수 있도록 돕는다. 빌더는 다음과 같은 빌드 라이프사이클을 제공한다.
	 - validate(검증) : 프로젝트가 올바른지, 필요한 모든 정보가 사용 가능한지 확인한다.
	- compile(컴파일) : 소스 코드를 컴파일하여 `.class` 파일로 변환한다.
	- test(테스트) : 작성된 단위 테스트를 실행한다.
	- package(패키징) : 컴파일된 코드를 JAR 또는 WAR 파일과 같은 배포 가능한 형식으로 패키징한다.
	- verify(검증) : 통합 테스트와 같은 추가 검사를 실행하여 패키지의 품질을 확인한다.
	- install(설치) : 패키징된 아티팩트를 로컬 Maven 리포지토리(m2)에 설치하여 다른 로컬 프로젝트에서 종속성으로 사용할 수 있도록 한다.
	- deploy(배포) : 아티팩트를 원격 리포지토리에 배포하여 다른 개발자나 프로젝트가 사용할 수 있도록 한다.

spring boot 프로젝트를 생성할 때, 빌더를 선택하게 되는데, 이때 자동으로 해당 빌더 wrapper가 포함되도록 보장되어 있어서, 따로 설치를 진행하지 않더라도 사용할 수 있는 큰 장점도 존재한다.

spring boot builder는 크게 3가지가 있다. maven, gradle-groovy, gradle-kotlin.

maven은 쉬운 접근성과 낮은 난이도의 설정이 장점이지만, 느리고, 유연성이 낮다.

하지만 뒤에 두 빌더는 groovy, kotlin의 스크립트 언어를 통해 이루어지기 때문에 사용자의 의도에 맞게 코드를 작성하는 것이 매우 쉽다.

# 2. 구성 요소

spring initializr를 통해 spring boot project를 생성했을 경우, 폴더 내에 다양한 파일들이 존재하는 것을 확인할 수 있다.
#### .idea
.idea파일에는 spring boot에 사용되는 전반적인 파일들의 정보가 담겨 있으며, .gitignore과 같은 파일들도 존재한다.
#### .mvn
앞서 말했던 것처럼 spring boot는 builder를 통해 프로젝트를 관리하고, 유지하고, 자동화하는 시스템을 구축했다. 따라서 사용자는 목적과 편의성을 고려하여 빌더 중 하나를 고르게 되는데, 만약 maven을 선택했을 경우 위 .mvn파일과 같은 파일이 생성되어 있다.
#### src
src는 main폴더가 존재하고, main에는 java와 resource폴더가 존재한다. 아마 kotlin 언어를 선택할 경우 java 대신 kotlin이 존재할 것 같은데, 코드를 작성하는 main파일이다.
다른 resource파일은 static리소스를 관리한다. db나 web을 통해 저장한 변수 등을 모아 놓는 파일이다. 즉 앱의 구동을 목적으로 존재하는 코드들의 집합은 java에, 앱의 구동을 옆에서 지원하는 파일들을 넣는 폴더는 resource라고 보면 된다.
#### pom.xml
sprinb boot는 의존성 주입이 장점이라고 앞서 설명했었다. 의존성을 코드 측면에서 주입하는 경우가 존재할 것이고, builder측면에서 제공하는 경우도 존재할 것이다. pom.xml을 살펴볼 경우. 플러그인의 버전, 아티펙트ID, 설명 등 다양한 라이브러리 연동을 위해 설정해 놓은 코드들의 집합으로, 외부의 라이브러리를 사용하게 될 경우를 대비하여 maven이 어떤 플러그인, 라이브러리 등을 어디서, 무슨 버전을 설치할 것인지, 무엇인지 등을 설명하고 있는 일종의 코드를 적어놓은 파일이다.
#### etc
이외의 다른 파일들은 전부 maven compiler, guide, maven CLI등의 파일이기에, 나중에 무엇인지 확인하고 싶을 때, 한 번씩 보는 것을 추천한다.

# 3. REST API

거의 대부분의 웹/앱은 데이터를 상호작용을 통해 가져와 가공/처리 과정을 거쳐 원하는 목적을 달성하게 된다.

예를 들어 쇼핑물 웹 같은 경우, 회사의 DB내부에 존재하는 제품에 대한 데이터들을 웹으로 나타내고, 이를 사용자와 상호작용을 통해 어떤 이벤트가 발생된다. 예를 들어 제품이미지를 클릭할 경우, 확대가 되거나, 상세페이지로 넘어가 제품에 대한 자세한 설명을 볼 수 있는 것처럼.

이처럼 각 서비스별로 어플리케이션을 구현하고, 이들을 통합하여 하나의 인터페이스를 만드는 것을 마이크로서비스 어플리케이션이라고 한다.(반대 개념으로 모놀로식 어플리케이션이 존재한다.)

각 서비스별로 어플리케이션을 구현할 경우 다음과 같은 이점을 얻을 수 있다.
1. 어떤 서비스에 대해 트래픽이 발생했을 경우, 해당 서비스에 대한 조치만으로 원활한 서비스를 유지 가능
2. 추후 기능 구현을 통해 어플리케이션 재배포가 발생했을 때, 해당 서비스 어플리케이션만 재배포
3. 하나의 서비스를 통해 앱, 웹 등의 다양한 UI에서 공통된 기능을 사용

특히 3번과 같은 이점을 활용하기 위해서는 해당 서비스에 필요한 리소스, 혹은 기능이 담긴 데이터 코드들이 원활하게 동작을 하여야 한다.

결국 데이터를 가져오는 작업이 필요한데, 이를 우린 *통신*이라고 한다.

또한 상호 간에 통신에 대한 특별한 규칙이 없을 경우, 데이터가 난잡해지거나, 통신이 원활하지 않는 등 다양한 문제가 발생될 수 있고, 처리도 곤란할 것이다.

따라서 인터넷 상에서 정보를 주고받기 위한 규칙을 세운 것이 *통신 규약*이다.

이 중 REST API는 웹의 통신 규약(프로토콜)인 HTTP를 기반으로 API를 설정하는 것을 의미한다.

- API(App Programing Interface) : API는 APP을 구축할 때, 개발자가 세우는 가이드를 의미한다. 즉 APP을 어떻게 사용하고, 관리할 것인지 알려주는 것이 바로 API이다. 어떤 기능을 요청해서, 어떤 형식으로 만들어 보내야 하고, 어떤 형식의 응답을 받게 되는지 등을 상세하고 명확하게 설명한다.

<span style="color:rgb(146, 208, 80)">즉 REST API는 어플리케이션에 구축된 통신들이 어떤 규칙을 갖고 통신을 갖게 될 것인가에 대한 규칙이라고 볼 수 있다.</span>

REST API의 핵심 개념은 다음과 같다.
1. 자원 : 모든 데이터를 자원으로 취급한다. (자원은 고유한 URI로 식별)
2. HTTP Method를 통해 자원을 표현한다. (GET, POST, PUT/PATCH, DELETE)
3. 표현 : 모든 데이터를 통신할 때, 데이터의 형식을 통일한다.

위 3가지의 개념을 통해 다음과 같은 특징이 생성된다.
1. 클라이언트-서버 구조 (Client-Server Separation):
 클라이언트(사용자)와 서버(데이터 및 서비스 제공)가 서로 독립적이어야 한다. 각각 독립적으로 개발 및 개선될 수 있다.
2. 무상태성 (Stateless):
서버는 클라이언트의 이전 요청에 대한 정보를 저장하지 않다. 모든 요청은 그 요청을 처리하는 데 필요한 모든 정보를 담고 있어야 한다. 이를 통해 서버 부하를 줄이고 확장성을 높일 수 있다.
3. 캐싱 가능 (Cacheable):
응답을 캐시(저장)할 수 있도록 하여, 동일한 요청에 대한 응답 시간을 줄이고 서버 부하를 줄일 수 있다.
4. 균일한 인터페이스 (Uniform Interface):
자원에 대한 요청 방식이 일관되고 통일되어야 한다.
	- 자원 식별 (URI)
	- 메시지를 통한 자원 조작 (HTTP 메서드)
	- 자기-서술적 메시지 (Self-descriptive Message, 메시지 자체에 정보가 담겨있음)
	- 하이퍼미디어(HATEOAS, 선택 사항이지만 이상적임
5. 계층화 시스템 (Layered System):
클라이언트는 서버에 직접 연결되었는지, 중간 서버(로드 밸런서, 프록시 등)를 통해 연결되었는지 알 필요가 없다.

위 개념들과 특징들을 잘 지켜진 API를 RESTful한 API다라고 표현을 한다.

<span style="color:rgb(146, 208, 80)">특히 마이크로 서비스 어플리케이션에서 가장 중요한 개념은 무상태성이다.
</span>

상대방이 이전 상태를 저장하지 않는다는 의미는 "A가 B에게 어떤 자원을 요청할 때, 이전에 입력한 정보(상태)가 존재하지 않는다." 는 의미이다.


# 4. HTTPie

HTTPie를 통해 Spring boot에서 작성한 api method를 실행시켜 볼 수 있다.

앞선 REST API설명에서 Spring web에 의존성이 존재하는 Jackson 라이브버리를 통해 마샬링, 언마샬링을 진행할 수 있다고 설명하였다. 

Jackson의 작동방식은 기본생성자를 통해 객체를 만들고, 터미널에서 HTTP Method를 실행하였을 떄, 입력되는 값에 맞게 Getter/Setter을 실행하여 해당 객체를 마치 입력값으로 생성한 것처럼 초기화하게 된다. 즉 Jackson을 사용하여 마샬링/언마샬링을 하게 될 경우 기본생성자만 존재하고, Getter/Setter을 통해 필드변수에 접근하도록 만드는 것이 훨씬 유용하다.

```java
package com.potatostore.ShoppingApplication.Items;  
  
public class Coffee {  
    private String id;  
    private String name;  
  
    public Coffee(){  
        this.id = "-1";  
        this.name = "null";  
    }  
  
    public String getId() {  
        return id;  
    }  
  
    public void setId(String id) {  
        this.id = id;  
    }  
  
    public String getName() {  
        return name;  
    }  
  
    public void setName(String name) {  
        this.name = name;  
    }  
}
```

이후 테스트하고 싶은 HTTP Method가 존재하는 Controller/Service등을 설정해줘야 한다.
```java
package com.potatostore.ShoppingApplication.Controller;  
  
import com.potatostore.ShoppingApplication.Items.Coffee;  
import org.springframework.http.HttpStatus;  
import org.springframework.http.ResponseEntity;  
import org.springframework.web.bind.annotation.*;  
  
import java.util.ArrayList;  
import java.util.List;  
  
@RestController  
@RequestMapping("/coffees")  
public class CoffeeController {  
    private List<Coffee> coffees = new ArrayList<Coffee>();  
  
    @PostMapping  
    Coffee postCoffee(@RequestBody Coffee coffee){  
        coffees.add(coffee);  
        return coffee;  
    }  
  
    @GetMapping("/{id}")  
    Coffee getCoffee(@PathVariable String id){  
        for(Coffee c : coffees){  
            if(c.getId().equals(id)){  
                return c;  
            }  
        }  
  
        return null;  
    }  
  
    @PutMapping("/{id}")  
    ResponseEntity<Coffee> putCoffee(@PathVariable String id, @RequestBody Coffee coffee){  
        int putIdx = -1;  
  
        for(Coffee c : coffees){  
            if(c.getId().equals(id)){  
                putIdx = coffees.indexOf(c);  
                break;  
            }  
        }  
  
        return (putIdx == -1) ?  
                new ResponseEntity<Coffee>(postCoffee(coffee), HttpStatus.CREATED) :  
                new ResponseEntity<Coffee>(coffee, HttpStatus.OK);  
    }  
  
    @DeleteMapping("/{id}")  
    Coffee deleteCoffee(@PathVariable String id){  
        Coffee result = null;  
  
        for(Coffee c : coffees){  
            if(c.getId().equals(id)){  
                result = c;  
                coffees.remove(c);  
                break;  
            }  
        }  
  
        return result;  
    }  
}
```

이후 가장 중요한 점은 @SpringBootApplication이 붙은 main method와 같은 패키지에 Controller가 존재하거나, 보다 하위 패키지에 존재해야 한다.

#### Step 1 : HTTPie install
```
pip install --upgrade pip
pip install httpie
```

#### Step 2 : Start SpringBoot
#### Step 3 : HTTP Method 확인
intellij에서 spring boot를 실행했다면, 터미널을 하나 더 열어서 다음과 같은 명령어를 통해 확인을 해본다.

1. POST 
```
http POST :8080/coffees/{id} id="{id}" name="Americano"
```
POST작업시 위 {id}란에 id를 입력하거나, id를 입력하지 않으면 자동적으로 -1이라는 id가 부여되도록 설정하였다.

2. GET
```
http GET :8080/coffees/{id}
```

3. PUT
```
http PUT :8080/coffees/{id} name="Latte"
```
이후 GET을 통해 이름이 바꼈는지 확인해보기

4. DELETE
```
http DELETE :8080/coffees/{id}
```
GET을 통해 삭제되었는지 확인해보기

# 5. DB Access

Spring boot는 Tomcat이라는 내장 서버가 존재하고, 이는 독립적으로 작동하는 서버이다.

그렇다면 spring boot로 만들어진 app들은 데이터들을 어떻게 저장할 것인가?

DB를 사용할 것이고, 여러 종류의 DB가 있지만, 아직 SQL을 배우지 않았으므로, NoSQL 중 하나인 MongoDB를 통해 Springboot에 DB를 연결하고 핸들링하는 방식을 배울 것이다.

#### JPA(Java Persistence API)
[[ORM(Oriented Relational Mapping)]]을 Java에서 지원할 수 있도록 만든 라이브러리가 바로 JPA이다. 이는 관계형 데이터베이스와 같이 정형화된 스키마에 객체를 mapping할 수 있을 경우에 사용되는 방식으로, 관계형 데이터베이스에 비해 상대적으로 스키마가 적고, 유연한 비관계형 데이터베이스는 JPA를 통해 mapping하는 방식이 불가능하다.

따라서 Spring boot에서는 다음과 같은 방식으로 MongoDB와 mapping을 한다.

#### Repository
DB의 의존성을 추가하고, 이를 연결하여 JPA를 통해 해당 데이터를 가져오는 작업을 하기 위해 PersistenceUnit, EntityManagerFactory, EntityManager API와 관련된 추가 단계를 수행하고, 이를 반복하는 작업이 발생한다. 이를 해결하기 위해 DB를 추상화한 *Repository*라는 개념을 도입하게 되었으며, 이는 VFS가 여러 OS마다 다른 FS를 추상화해놓은 개념처럼 추상화된 인터페이스이다.

#### Loader
Repository를 생성할 때, 생성자 내부에 초기화할 값들을 넣어 초기화를 시키는 방식은 원칙상 좋지 않다. 단일 책임 원칙에 따라 Controller은 REST API를 처리하는 용도로 사용이 되어야 하지만, 생성자에서 DB값을 가져오는 기능도 추가가 되어 원칙에 어긋나게 된다. 따라서 Loader라는 class를 따로 빼주어 

#### Mapping Springboot-MongoDB
1. MongoDB에 종속성(의존성)을 부여한다. (pom.xml에 dependency주석을 통해 maven으로 주입)
	1. 라이브러리/모듈과 같은 MongoDB에 필요한 드라이버들을 추가한다.
	2. MongoDB에 접근하는 객체를 생성하여 IoC Container에 bean으로 등록한다.
	으로 이해할 수 있으며, MongoDB에 접근하여 쿼리문을 수행할 수 있는 객체를 만드는 모든 과정을 의존성 부여로 설명할 수 있다.

#### DSL(Domain-Specific Language)
- query method DSL
- Criteria API 

# 6. Application Setting

어플리케이션은 홀로 기능하지 못할 가능성이 매우 높다. 다른 서비스/어플리케이션과 상호작용을 통해 어플리케이션의 온전한 기능을 다할 것이다.

이때 어플리케이션은 오류가 발생하거나, 일부 기능/설정 등을 재설정하여 원하는 기능을 실행할 수 있다. 이는 동적으로 어플리케이션이 실행되는 도중에 수행되어야하며, 이와 비슷한 기능들은 다음과 같다.
- 어플리케이션의 동적 설정과 재설정
- 현재 설정과 출처의 확인과 결정
- 어플리케이션 환경과 헬스 지표의 검사와 모니터링
- 실행 중인 어플리케이션의 로깅 수준을 일시적으로 조정해 오류 원인 식별

위 기능들을 동적으로 처리하기 위해 Spring boot에서는 내장된 설정 기능, 자동 설정 리포트와 함께 Spring boot actuator을 통해 환경설정을 동적으로 설정할 수 있도록 하였다.

동적으로 어플리케이션의 설정을 변경한다는 것은 어플리케이션이 실행되는 도중 세팅값을 원하는대로 재설정할 수 있음을 뜻한다. Spring boot에서 이와 같은 기능을 Spring Environment를 활용하여 관리하게 되는데 이는 https://docs.spring.io/spring-boot/reference/features/external-config.html (Spring boot 공식 문서 - PropertySources)를 통해 확인 가능하다.

특히 다음과 같은 설정이 매우 유용하다.
- 명령 줄 인수
- OS 환경 변수
- 패키징된 어플리케이션 jar 안에 있는 어플리케이션 속성

# 6. Annotation

Spring initializr를 통해 만든 project를 intellij와 같은 IDE에서 열었다면, src폴더 내부의 main폴더가 존재할 것이다. main폴더 내부에 쓰여진 java코드들을 통해 API를 구성하는 것이며, 이외의 폴더는 spring boot 환경 설정이라고 봐도 무방하다.

우선 initializr를 통해 만든 프로젝트를 수정 없이 열었을 경우 다음과 같다.

```java
package com.example.potatostoreapplication;  
  
import org.springframework.boot.SpringApplication;  
import org.springframework.boot.autoconfigure.SpringBootApplication;  
  
@SpringBootApplication  
public class PotatostoreapplicationApplication {  
    public static void main(String[] args) {  
        SpringApplication.run(PotatostoreapplicationApplication.class, args);  
    }  
}
```

중간에 @SpringBootApplication과 같이 주석처럼 처리된 명령어를 볼 수 있는데, 이거 java문법에서 @Override와 유사하다.

java에서 @Override를 통해 컴파일러에게 오버라이딩을 한다는 것을 알려준다.

비슷하게 spring boot에서는 주석처리를 통해 컴파일러에게 다음에 나올 명령문에 대해 *의존성을 주입한다(DI, Dependency injection)* 고 알려주는 것이다.

---

앞서 말한 바와 같이 spring boot는 기존의 tomcat서버에서 내장된 독립 서버로 바뀌였는데, 실제로 위 코드를 실행할 경우, PID(Process ID)와 tomcat server port등 다양한 정보들이 CLI를 통해 출력되는 것을 확인할 수 있다.

즉 spring boot코드를 실행을 통해 나는 서버를 직접적으로 구성하고, 실행하고, 연결하지 않아도, 연결이 된다는 것을 알 수 있는데, 눈으로 확인하고 싶으면 직접 웹페이지를 통해 서버에 접속하면 된다.

localhost:8080(tomcat server port에 따라 변동하면 된다.)에 접속하면 whitelabelerror page, 즉 서버는 살아있는데, 작동은 하지 않는 식물서버를 볼 수 있다.

여기에 직접 API endpoint를 설정해서 웹페이지를 살려보자.

아무 클래스 하나를 만들어서
```java
package com.example.potatostoreapplication;  
  
import org.springframework.web.bind.annotation.GetMapping;  
import org.springframework.web.bind.annotation.RestController;  
  
@RestController  
public class EX01 {  
    @GetMapping("ABC")  
    public String sayHello(){  
        return "Hello";  
    }  
}
```

위 코드를 넣고,

@GetMapping에 넣은 문자열을 localhost:8080/(이곳)에 넣는다.

그리고 찾아보면 @RestController를 설정한 public String sayHello method가 실행되서 page에 Hello가 찍히는 것을 확인할 수 있다.

이처럼 spring boot에는 DI를 위한 다양한 어노테이션 뿐만 아니라, http method(GET, POST, PET/PATCH, DELETE)를 지원, Bean생성 등 다양한 작업을 위해 어노테이션이 붙을 수 있다.
#### @SpringbootApplication
무조건 main method가 포함된 class 앞에 붙여줘야 한다.

그 이유는 다음과 같다.
1. IoC container 초기화
2. 내장 웹서버(Tomcat) 구동
3. Component scan 로직 포함

위 이유는 각각 @Configuration, @EnableAutoConfiguration, @ComponentScan과 관련되어 있다.
#### @Configuration
Spring boot api를 설정하는 기능이며, Bean을 수동으로 등록할 수 있게 알려주는 역할을 한다. 즉, @Bean이나 @Component, @RestControler등을 사용하기 위해 @Configuration을 통해 작동해야 한다.
#### @EnableAutoCOnfiguration
위 @Configuration을 Spring boot application 실행 시 자동으로 실행하게 만들어주는 기능이다.

#### @ComponentScan
앞서 배운 내용인 IoC container에 Bean이라는 객체를 생성하고, 보관할 경우에 필수적으로 진행해야 하는 작업이 존재한다. 이를 componentScan이라고 부르며, 이는 구성요소 살펴보기 정도의 기능으로 생각하면 된다. 즉 Bean으로 만들고자 하는 클래스를 살펴 해당 component가 이미 IoC container에 존재하는지, 적합한지 등을 따지고, Bean객체로 만들어 IoC container에 보관까지 하는 작업을 진행한다.

component scan의 가장 중요한 점은 위 SpringbootApplication annotation이 붙은 main method와 동일 패키지에 존재해야만 해당 IoC container에 종속될 수 있다.

즉, A,B 두 패키지가 존재하고, 각각 @SpringbootApplication을 통해 IoC container을 할당한 상태에서 B 패키지의 @Bean을 통해 생성된 객체를 A의 IoC container에 속하게 하는 방법은 없다.

따라서 Bean객체를 생성했는데, 해당 객체가 IoC container에 존재하지 않다면, Component Scan이 정상적으로 실행된건지, Bean객체가 다른 IoC container에 존재하지 않는지 확인을 통해 오류를 해결할 수 있다. 

---
## REST API

#### @RestController
우선 기존 서버가 데이터를 가져와 화면에 출력하는 과정을 이해하여야 한다. 

*MVC pattern*은 Model, View, Controller을 뜻하며, 순수 데이터(객체)를 뜻하는 Model, 해당 데이터를 시각적인 요소로 보여주는 View, 데이터를 입력받거나 DB에서 가져와 Model로 만들어주는 Controller의 삼요소를 통해 서버를 구성하는 대표적인 디자인 패턴이다.

<span style="color:rgb(146, 208, 80)">기존 MVC pattern같은 경우 Controller -> Model -> View를 통해 객체들을 html에 담아 시각화 하였지만, MVC spring같은 경우 View에서 html대신 json형식으로 전송하게 된다. 추후 웹/앱(react)에서 json파일을 html형식으로 개발자가 원하는 디자인에 맞춰 시각화한다.</span>

이때 위 M, V, C를 각각 만들고 연결을 도와주는 어노테이션이 바로 *@Controller*이다.
##### @Controller
기존 MVC pattern처럼 Model을 controller을 통해 받고, spring에 존재하는 ViewResolver와 함께 작동하여 앱이 뷰 기술에 의해 렌더링도니 특정 뷰를 표시(html형식으로 model을 변환하여 시각화)

##### @ResponseBody
class, method에 추가하여 json, xml과 같은 파일 형식으로 보내도록 @Controller 클래스에 지시 <span style="color:rgb(146, 208, 80)">(Controller 어노테이션 클래스과 같은 응답을 하는 방식에서 사용을 하지만, 이때 json, xml과 같은 파일 형식으로 보내는 방식이 필요한 클래스는 Controller어노테이션이 붙은 클래스가 99%이고, 예외처리 응답 클래스에서도 아주 드물게 사용된다.)</span>

위 두 개의 어노테이션을 합쳐 현대의 MVC spring(REST API에 맞춰 설계된 클래스)에 맞춰지게 만드는 어노테이션이 바로 *@RestController*이다.

#### @RequestMapping
당신이 Get method를 Controller을 통해 DB에서 가져와 하나의 Model을 만들고 있을 때, 해당 Model을 저장하는 객체가 존재할 것이다. 이때 보통 DB에서 데이터를 긁어오면 Iterable, List형태의 결과값을 받게 되는데, 이는 곧 Model을 저장할 때, 최상위 레벨 타입의 선택을 권장하게 된다(List, Iterable등). 

```java
@RestController
class apidemo{
	private List<Coffes> coffees = new ArrayList<coffee>;
	
	public apidemo(){
		coffees.addAll(List.of(
						new Coffee("starbucks"),
						new Coffee("mega coffee"),
						new Coffee("compose coffee")
		))
	}
	
	@RequestMapping(value = "/coffees", method = RequestMethod.GET)
	Iterable<Coffee> getCoffees(){
		return coffees;
	}
}
```

RequestMapping을 통해 Model을 응답해줄때 API URL, HTTP Method type을 매개변수로 넣어준다.

스프링부트를 처음 생성할때, 어떤 스프링의 의존성을 추가할 것인지 선택하는 부분이 있는데, 이때 spring web의존성을 추가하게 될 경우 spring web에 존재하는 *Jackson*이라는 라이브러리를 사용할 수 있다. 이는 Model을 JSON파일 형식으로, 혹은 반대로 변환해주는 라이브러리다.

*Jackson*을 통해 객체를 JSON, XML파일 형식으로 바꿔주는 작업을 *마샬링*이라고 하고, 반대 작업을 *언마샬링*이라고 한다.

<span style="color:rgb(146, 208, 80)">즉 Spring boot는 Jackson을 통해 MVC pattern에서 Model을 View로 전환하는 작업을 실행한다.</span>

#### @GetMapping(HTTP method : Get)
@RestController을 통해 class를 REST API에 맞춰 작성할 때, 기본적으로 HTTP method를 구현하는 것이 매우 중요하다. 위 @RequestMapping을 통해 응답을 요구하는 URL을 Mapping하여 HTTP method에 맞춰 응답해주는 방식도 존재하지만, 이는 HTTP method, 총 5가지의 requestmapping이 필요하며, 보일러플레이트 코드를 증가하게 만들고, 가독성이 떨어지는 결과로 이어질 것이다. 따라서 직관적으로 Get 기능을 넣는 어노테이션이 바로 GetMapping이다.

```java
@GetMapping("/coffees")
Iterable<Coffee> getCoffees(){
	return coffees;
}
```

앞선 RequestMapping은 URL, HTTP Method type의 매개변수를 요구하지만, 위 GetMapping은 두 번째 매개변수를 고정하므로, URL만 확인하면 된다. 또한 매개변수간 충돌 가능성이 존재하지 않아, 등호(=)를 통한 값 지정 방식도 불필요해진다.

##### @PathVariable
만약 특정 커피에 대해 HTTP Method를 실행하고 싶으면 PathVariable annotation을 사용하면 된다.
```java
@GetMappint("/coffees/{id}")
Optional<Coffee> getCoffeeById(@PathVariable String id){
	for(Coffee c : coffees){
		if(c.getId().equals(id)){
			return Optional.of(c);
		}
	}
}
```

URL내 URI형태의 변수가 입력되면 @PathVariable을 통해 해당 URI를 인식하고, 이를 id 매개변수로 넘겨주게 된다. 이후 id를 List에서 확인하여 일치하는 Option을 넘겨주게 된다.
#### @PostMapping(HTTP Method : Post)
post method annotation으로 리소스, 객체를 생성하는 기능을 수행하게 된다. 이때 객체를 JSON파일 형식으로 받아와 해당 객체로 만들고, 매개변수로 넘겨주어야 한다. 이를 수행해주는 어노테이션이 바로 @RequestBody이다.

##### @RequestBody
언마샬링을 하는 어노테이션으로 JSON 파일 형식의 리소스를 객체화하여 매개변수로 넘겨준다.

```java
@PostMapping("/coffees")
Coffee postCoffee(@RequestBody Coffee coffee){
	coffees.add(coffee);
	return coffee;
}
```

#### @PutMapping(HTTP Method : Put)
알다시피 Put과 Patch의 가장 큰 차이점은 일부 업데이트인가 전체 업데이트인가 이다.
```java
@PutMapping("/coffees/{id}")
Coffee putCoffee(@PathVariable String id, @RequestBody Coffee coffee){
	int coffeeIndex = -1;
	
	for(Coffee c : coffees){
		if(c.getId().equals(id)){
			coffeeIndex = coffees.indexof(c);
			coffees.set(coffeeIndex, coffee);
		}
	}
	
	return (coffeeIndex == -1) ? postCoffee(coffee) : coffee;
}
```

1. @PathVariable을 통해 업데이트 작업을 할 id를 찾기
2. @RequestBody를 통해 업데이트할 내용을 받아
3. id에 해당하는 내용을 update! (없으면 Post)
#### @PatchMapping(HTTP Method : Patch)
PatchMapping은 PUT과 달리 받은 데이터 일부를 수정하게 된다. 이때 @RequestBody로 받은 업데이트 될 매개변수의 수정될 부분이 아닌 경우 NULL값이 들어 있어, 위 PUT과 같은 방식으로 교체작업이 이뤄지면 안된다. 
```java
@PatchMapping("/coffees/{id}")
Coffee patchCoffee(@PathVariable String id, @RequestBody Coffee coffee){
	int patchIdx = -1;
	
	for(Coffee c : coffees){
		if(c.getID().equals(id)){
			if(coffee.getID() != null){
				coffees[patchIdx].setID(coffee.getID());
			}
			if(coffee.getName() != null){
				coffees[patchIdx].setName(coffee.getName());
			}
			...
		}
	}
	
	return (patchIdx == -1) ? postCoffee(coffee) : coffee;
}
```
coffee class내 모든 필드변수와 대조해가며 null값이 존재하는지 확인하는 작업을 통해 일부 교체만 이뤄져야 한다.
#### @DeleteMapping(HTTP Method : Delete)
Delete Method 또한 작동방식을 떠올리기만 하면 구현하는 것은 쉽다.
```java
@DeleteMapping("/coffees/{id}")
void deleteCoffee(@PathVariable String id){
	coffees.removeIf(c -> c.getID().equals(id));
}
```

Collection의 removeIf와 람다를 통해 깔끔한 구현이 가능하다.

#### HTTP Method Mapping 최적화하기
1. 앞선 5가지의 method들 전부 "/coffees" 매핑 URI를 통해 쿼리를 보내오는 것을 확인할 수 있다. 이는 coffees라는 URI를 공통으로 묶는 것이 중요한데 이를 위해 다음과 같이 사용할 수 있다.
```java
@RestController
@RequestMapping("/coffees/")
class apidomo{
	@GetMapping
	...
	
	@GetMapping("/{id}")
	...
	
	@PostMapping
	...
	
	@PutMapping("/{id}")
	...
	
	@DeleteMapping("/{id}")
	...
}
```
class 맨 앞에 @RequestMapping을 넣음으로서 자동으로 HTTP method mapping에 URI를 반복적으로 넣는 작업을 제거해줄 수 있다.

2. POST, DELETE는 상태 코드를 권장하고, PUT은 상태 코드를 필수적으로 반환해주어야 한다. HTTP Method가 정상적으로 작동하였는지 확인할 수 있는 코드를 상태 코드라고 하며, GET은 정상적으로 작동시 원하는 데이터를 가져올 수 있기에 상태 코드가 자동적으로 반환되지만, 다른 Method들은 상태 코드를 반환해 주는 것이 쿼리를 요청하는 쪽에서 식별하기 쉬워진다.
```java
@PutMapping
ResponseEntity<Coffee> putCoffee(@PathVariable String id, 
	@RequestBody Coffee coffee){
	int coffeeIdx = -1;
	
	for(Coffee c : coffees){
		if(c.getID().equals(coffee)){
			coffeeIdx = coffees.indexof(c);
			coffees.set(coffeeIdx, coffee);
		}
	}	
	
	return (coffeeIdx == -1) ? 
			new ResponseEntity<>(postCoffee(coffee), HttpStatus.CREATEd):
			new ResponseEntity<>(coffee, HttpStatus.OK);
}
```
위 예제 코드처럼 ResponseEntity에 HttpStatus라는 HTTP Method 상태 코드를 생성하여 보내주는 것이 일반적이다.

---
## DB Access

#### @Entity
JPA(Java Persistent API)를 통해 객체에 영속성을 부여하여 DB에 저장하게 만들기 위해서 DB의 테이블과 객체의 Mapping이 되어야 한다. 이때 JPA를 통해 Mapping을 하고, 하기 위해 지원하는 어노테이션이 바로 Entity이다. 
```java
@Entity
public class Coffee {  
    @Id  
    private String id;  
    private String name;  
  
    public Coffee(){  
        this.id = "-1";  
        this.name = "null";  
    }  
  
    public Coffee(String name){  
        this.id = "-1";  
        this.name = name;  
    }  
  
    public Coffee(String id, String name){  
        this.id = id;  
        this.name = name;  
    }  
  
    public String getId() {  
        return id;  
    }  
  
    public void setId(String id) {  
        this.id = id;  
    }  
  
    public String getName() {  
        return name;  
    }  
  
    public void setName(String name) {  
        this.name = name;  
    }  
}
```

1. 기본 키(primary key)가 존재해야 한다 -> 각 row별로 구분을 위해
2. 기본생성자가 존재해야 한다. -> JPA가 데이터를 읽고, 

---
## Application Setting

#### @Value
application.properties(설정 파일)나 환경 변수에 저장된 값을 자바 변수에 넣어주는 작업을 진행한다. 위 어노테이션은 단순히 파일에 해당 변수 값을 읽어와 자바 변수에 넣어주는 기능만 작동을 하고, 환경 변수를 수정하는 작업 제공하지 않는다. 
```java hl=19
#application.properties
spring.application.name=ShoppingApplication  
greeting-name=Dakota  
greeting-coffee=${greeting-name} is drinking ice americano

---

#GreetingController.java
package com.potatostore.ShoppingApplication.Controller;  
  
import org.springframework.beans.factory.annotation.Value;  
import org.springframework.web.bind.annotation.GetMapping;  
import org.springframework.web.bind.annotation.RequestMapping;  
import org.springframework.web.bind.annotation.RestController;  
  
@RestController  
@RequestMapping("/greeting")  
public class GreetingController {  
    @Value("${greeting-name: Mirage}")  
    private String name;  
  
	@Value("${greeting-coffee: ${greeting-name} is drinking ice americano}")  
    private String coffee;  
  
    @GetMapping  
    String getGreeting(){  
        return name;  
    }  
  
    @GetMapping("/coffee")  
    String getGreetingCoffee(){  
        return coffee;  
    }  
}
```

위 코드에서 19번째 코드를 확인해보면 application.properties에 존재하는 환경 변수를 읽어오는 것 뿐만 아니라 초기화를 진행하는 듯한 코드를 보여준다. 이는 초기화를 진행하는 코드가 아닌 greeting-name이라는 값이 존재하지 않는 경우 우항의 값으로 변수를 초기화한다 라는 뜻이다.

위와 같은 코드에서 가장 중요한 점은 22번째 줄이다.
22번째 줄을 보게 되면 greeting-name이라는 환경변수에 영향을 받아 greeting-coffee를 정의하게 된다. 이는 곧 greeting-name이라는 환경변수가 존재하지 않을 경우 greeting-coffee또한 compile error(BeanCreationException)가 발생할 수 있다.

물론 다음과 같이 해결 가능하다.
```java
@Value("${greeting-coffee: ${greeting-name: Makao} is drinking ice americano}")
```

@Value에 입력값이 모두 문자열로 되어있는 것 또한 단점으로 작용한다. 이는 IDE 내부 컴파일러가 환경 변수를 어플리케이션이 사용한다고 인식하지 못한다. 

이러한 단점으로 인하여 @ConfigurationProperties라는 어노테이션을 추가적으로 만들게 되었다.

#### @ConfigurationProperties
1. 가독성과 유지보수의 지옥 (Readability)
방금 작성하신 중첩 문법은 값이 2~3개만 넘어가도 코드를 읽기가 매우 힘들어진다.
- @Value: 문자열 안에 복잡한 로직이 섞여 있어 오타가 나기 쉽고, 나중에 설정을 바꿀 때 모든 컨트롤러를 뒤져야 한다.
- @ConfigurationProperties : 자바 객체(POJO) 구조로 관리하므로,  greeting.getName() 처럼 메서드로 깔끔하게 가져올 수 있다.

2. 느슨한 바인딩 (Relaxed Binding)
@Value는 이름이 정확히 일치해야 하지만, @ConfigurationProperties는 훨씬 유연하다.
- 예: 설정 파일에  greeting_name ,  GREETINGNAME ,  greeting-name  중 무엇으로 적어도 자바의  greetingName 필드에 똑똑하게 연결해 준다.

문자열과 변수명을 컴파일러는 다르게 받아들이는데, 이때 변수명을 심볼(symbol)이라고 한다.
```java
String name = "name";
name : symbol
"name" : String
```
이 때문에 문자열이 아닌 값을 사용하게 될 경우, 심볼을 컴파일러나 IDE가 자동완성을 지원하여 오류가 더 적어진다.

3. 타입 안정성 (Type Safety)
- @Value: 기본적으로 모든 것을 문자열로 처리하거나 간단한 타입 변환만 지원한다.
- @ConfigurationProperties: 숫자, 리스트, Map, 심지어 중첩된 객체 구조까지 자바 타입에 맞춰서 자동으로 넣어주고 검증(Validation)까지 할 수 있다.

앞선 @Value의 단점을 보완하기 위해 만들어진 어노테이션으로 IDE가 환경변수 관련 속성을 파악하고, 연결하는 것을 확인하기 위해 다음과 같은 작업들로 행할 수 있다.
1. main class(@SpringBootApplication이 붙은 class)에 @ConfigurationPropertiesScan 추가
2. pom.xml에 의존성 추가


---
#### @Component
가장 기본적으로 component scan을 통해 bean 객체를 만들고, 이를 IoC container에 저장하려고 할 때, 사용되는 어노테이션 @component가 있다.

```java
@Component
public class MyComponent{
	// Class is automatically registered as a Spring bean
}
```

앞서 설명한 것처럼 IoC의 bean은 객체를 IoC에 할당하고, 이를 의존성 주입이 이루어지는 구간에 mapping하여 사용하도록 기능을 한다.

그렇다면 IoC container에 bean이 존재해야 가능하다는 뜻이고, 이처럼 동작하는 어노테이션이 바로 @Component이다. 

즉 @Component는 해당 클래스를 객체로 인스턴스화 시켜서 IoC container에 보관하는 기능을 구현한다.

#### @Autowired

DI(Dependency Injection)을 위한 어노테이션으로 앞선 방식으로 IoC container에 bean이 보관되어 있다면, 해당 bean을 가져와 사용하는 기능이다.

```java
@Component
public class Dog{
	public String fun(){
		return "dog";
	}
}

@RestControler
public class Car{
	@Autowired
	private Dog dog = new Dog(); // field DI
	
	@GetMapping("\ok")
	public String ok(){
		return dog.fun();
	}
}
```

#### @Bean

앞서 IoC container에 저장된 객체를 스프링에서는 Bean이라고 설명하였다. @Bean 또한 해당 클래스를 IoC container에 객체로 등록하는 기능을 수행한다.
#### @Controller

어노테이션이 붙은 클래스가 HTTP Method(GET, POST, PUT/PATCH, DELETE), 즉 클라이언트의 요청을 처리하는 스프링에게 알려주고, 클래스를 bean 객체로 등록하여 IoC container에 저장하게 된다.

그렇다면 @Bean의 기능에 포괄적으로 포함된 개념일까?

결론적으로는 아니다.

두 어노테이션 모두 IoC container에 bean을 등록하는 기능은 동일하지만, @Controller은 등록 시 HTTP Method를 처리하는 역할임을 스프링에 알려주고, @Bean은 객체 등록만 하는 행위이다.
그렇기에 HTTP Method를 수행하는 클래스를 @Bean을 통해 등록하게 될 경우, HTTP Method를 기능하기에 다른 개념이라고 볼 수 있다.
#### @ResponseBody

메소드의 반환값을 HTTP 응답 본문으로 직접 전송하는 어노테이션으로, 서버-클라이언트의 구조를 갖는 REST API에서 클라이언트의 HTTP Method와 같은 요청이 들어올 때, 서버에서 처리 후 반환하는 값을 반환해주는 메서드를 따로 만들어서 수행하는 것이 아닌 어노테이션을 통해 직접적으로 전송해줄 수 있는 것이 큰 장점이다.

#### @GetMapping

HTTP Method의 GET 요청을 지정한 EndPoint에 연결해준다. 즉, 클라이언트가 URL에 경로를 붙여 특정 자원에 접근하거나, 이벤트를 요구할 경우, @GetMapping("PATH")를 통해 해당 Endpoint에 mapping해줄 수 있다.
#### @Document

#### @id
