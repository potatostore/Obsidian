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

App은 기본적으로 

