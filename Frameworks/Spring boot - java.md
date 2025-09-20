# 0. Spring boot

Spring boot를 자바를 통해 앱 백엔드를 구성하는 도구로 생각하는 것이 일반적이다.

Spring boot의 사전적인 의미를 찾아보게 되면

*Spring boot is a framework for build applications in the java programming language.*
즉, Spring boot는 자바 언어를 통해 앱을 구축하는 framework이다.

특히 Spring application API를 구축하는데 도움을 주는 도구들의 집합을 Spring boot라고 한다.

그럼 Spring application은 무엇일까?

---
#### Spring applcation

코드를 작성하고, 하나의 프로젝트(app)을 완성하게 되면, 90/10의 법칙에 의해 10%의 코드가 전체 실행 시간의 90%를 차지한다.

이는 일부 코드의 재사용율이 매우 높다는 뜻이고, 이러한 재사용율이 높으면서, 필수적으로 사용해야 하는 코드를 우리는 보일러플레이트 코드라고 한다.

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

따라서 Spring 어플리케이션은 이러한 보일러플레이트 코드를 줄이기 위해 만들어졌다.

위 기능에 더해, java app를 만드는데 편리한 기능, 도구들을 제공한다.

---

그렇다면 Spring app 또한 기본적인 java app에서 많은 개선을 통해 나왔는데, 무엇을 더 편리하게 해주는 도구를 제공할까?

App은 단일동작이 불가능하다.

본인 스스로가 API없이 사용하는 경우는 가능하지만, 그렇지 않는 경우, 서버를 통해 API를 구축해야 한다.

Spring은 Tomcat이라는 서버를 사용하였지만, Spring boot를 통해 더 이상 웹서버가 불필요해졌다.

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

*com.example.app*에서 Bean을 찾아 등록하고, 사용하는 것은 번거롭다.

따라서 Spring boot에서 이를
```java
@springbootapplication //single annotation
```
위 단 한 문장으로 줄여버렸다.

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


# 3. 시작

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