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

# 1. Spring initializr

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
#### REST API

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


# 3. 어노테이션

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
#### @RestController

RestController은 REST API 개발을 위해 사용되는 핵심 어노테이션으로, 다음 두 가지의 어노테이션의 기능을 합쳐놓은 것이다.
- @Controller
- @ResponseBody 
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



# 4. MongoDB

Spring boot는 Tomcat이라는 내장 서버가 존재하고, 이는 독립적으로 작동하는 서버이다.

그렇다면 spring boot로 만들어진 app들은 데이터들을 어떻게 저장할 것인가?

DB를 사용할 것이고, 여러 종류의 DB가 있지만, 아직 SQL을 배우지 않았으므로, NoSQL 중 하나인 MongoDB를 통해 Springboot에 DB를 연결하고 핸들링하는 방식을 배울 것이다.

#### JPA(Java Persistence API)
[[ORM(Oriented Relational Mapping)]]을 Java에서 지원할 수 있도록 만든 라이브러리가 바로 JPA이다. 이는 관계형 데이터베이스와 같이 정형화된 스키마에 객체를 mapping할 수 있을 경우에 사용되는 방식으로, 관계형 데이터베이스에 비해 상대적으로 스키마가 적고, 유연한 비관계형 데이터베이스는 JPA를 통해 mapping하는 방식이 불가능하다.

따라서 Spring boot에서는 다음과 같은 방식으로 MongoDB와 mapping을 한다.

#### Mapping Springboot-MongoDB

1. MongoDB에 종속성(의존성)을 부여한다. (pom.xml에 dependency주석을 통해 maven으로 주입)
	1. 라이브러리/모듈과 같은 MongoDB에 필요한 드라이버들을 추가한다.
	2. MongoDB에 접근하는 객체를 생성하여 IoC Container에 bean으로 등록한다.
	으로 이해할 수 있으며, MongoDB에 접근하여 쿼리문을 수행할 수 있는 객체를 만드는 모든 과정을 의존성 부여로 설명할 수 있다.

#### DSL(Domain-Specific Language)
- query method DSL
- Criteria API 
