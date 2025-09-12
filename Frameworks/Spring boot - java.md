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

Spring API를 성공적으로 구축하고, APP을 실행시키기 위해서는, SPring application context가 필요하다.

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