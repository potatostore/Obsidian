
Mapping한다 라는 개념은 데이터를 서로 짝지어주는 기능을 의미한다.

보통 Mapping이 많이 필요한 경우는 class의 상속일 수도 있지만, API를 통해 DB와 같은 저장소와 앱/웹과의 통신이 발생할 때, Mapping이 많이 발생한다고 볼 수 있다.

class간의 상속은 컴파일러나 IDE에 내장된 시스템에 따라 언더프로모션과 같은 기능이 자연스럽게 발생하며 Mapping에 큰 신경을 안써도 된다. 물론 문제가 발생해도 디버깅시에 터미널에서 다 알려주기 때문에 큰 문제가 발생하지 않을 수도 있다.(물론 신경을 아예 안쓰면 큰 문제가 발생한다.)

하지만 DB와 앱/웹의 Mapping을 생각해 보면 겉으로 보기엔 데이터를 DB의 짜여진 스키마에 따라 저장만 하면 되는 간단한 구조처럼 보일 것이다.

근데 이런 경우가 발생할 수도 있을 것이다. 
Field에 5개의 column이 존재하는데, 내가 저장하려는 객체의 멤버 변수가 총 3개이다. 그렇다면 나머지 2개의 column에는 무엇을 채워 넣어야 할까? 아니면 빈 칸으로 남겨서 메모리가 낭비되더라도 일관성을 유지할 것인가?

바로 이러한 문제를 해결하기 위한 Mapping 방식인 *ORM*이 탄생하게 되었다.

---
ORM은 객체와 관계형 DB의 스키마를 연결하여 저장할 수 있는 Mapping 방식을 의미한다.

여기서 관계형 DB를 강조하게 되는 이유는 정확하고, 일관된 스키마가 존재해야 객체들을 저장할 때 문제가 발생하지 않게 된다.

즉 다음과 같은 예시가 정상적인 ORM의 예시가 될 수 있다.
```java
@Document
class ID{
	private String id;
	private String password;
	private String name;
}

---
DB schema : json
<MemberInformation>
	{
		"id",
		"password",
		"Name"
	}
</MemberInformation>

```

이렇게 되면 DB의 idcolumn과 class의 id멤버변수가 1대1로 Mapping되어 데이터의 저장이 정상적으로 이루어진다.

만약 멤버 변수에 해당되는 column이 존재하지 않을 경우 어떻게 될까?

```java
@Document
class ID{
	private String id;
	private String password;
	private String Name;
	private String age;
}

---
DB schema : json
<MemberInformation>
	{
		"id",
		"password",
		"Name"
	}
</MemberInformation>
```

이렇게 될 경우 ORM의 규칙에 따라 다음과 같은 경우의 수가 발생할 수 있다.

1. 매핑 무시 처리
	age 멤버 변수에 대해 DB에 저장이 되는 것을 무시(영속화 x), 일시적인 데이터로 간주한다.
2. 복합 객체 매핑
	column을 하나 더 만들어서 저장한다.
3. 매핑 오류 발생 
	일반 컴파일러처럼 mapping에 오류가 존재한다고 알린다, 예외처리 혹은 위 2개의 방식으로 유도.

객체 지향 프로그래밍이 점점 많아지고, 사용되는 추세에 ORM은 필수 개념이다. class의 객체와 DB가 어떤 방식으로 Mapping되어 저장되는지 확인하면, 추후에 DB를 연결하여 사용할 때, 발생하는 Mapping오류들을 보다 쉽게 처리할 수 있다.