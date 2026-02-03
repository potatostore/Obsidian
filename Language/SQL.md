강의 : https://www.youtube.com/playlist?list=PLU7aNvsXRLZckCbpF_q88k7LpWjVTX43_
실습 예제 및 정보 :  https://www.w3schools.com/sql/default.asp

# SELECT & FROM

SELECT : 특정 컬럼을 가져오고 싶을 때 사용하는 명령어로 다음과 같이 사용할 수 있다.
FROM : Target Table를 적어 명령어를 실행할 위치를 지정한다.

```SQL
SELECT CustomerName
FROM Customers;
%% Customers라는 DB에서 CustomerName에 해당하는 테이블 내 레코드들을 가져온다. %%
```

# WHERE

필터링을 통해 사용자가 원하는 데이터를 뽑아올 때 사용한다. 

조건문을 통해 여러 레코드들 중 원하는 레코드에 해당되는 데이터를 뽑아낸다.

조건문처럼 사용하는 WHERE문은 AND, OR, !=(<>), >, <, >=, <= 등을 통해 다양한 조건은 만들어낼 수 있다.

```SQL
SELECT CountryName
FROM Countries
WHERE CountryName in ('한국', '일본', '중국', '미국') %% in 을 통해 여러 or문을 하나로 묶을 수 있다. %%

---

WHERE CountryName NOT in ('한국', '일본') %% 이런식으로 한국, 일본을 제외한 모든 나라를 조회하고 싶을 때, 즉 찾고 싶은 조건이 반대의 조건보다 많을 경우 NOT in을 통해 해당 조건을 제외한 나머지를 찾는 방법도 있다. %%
```

# BETWEEN

만약 정수형 데이터들로 이루어진 컬럼에서 특정 정수 범위에 해당되는 레코드들을 가져오고 싶으면 다음과 같은 SQL 코드를 짤 것이다.
```SQL
SELECT *
FROM Koreans
WHERE 30 <= 나이 AND 나이 <= 40
```

이는 '나이'라는 컬럼의 이름을 두 번 사용하여 약간의 번거로움이 존재한다.

이를 해결하기 위한 문법이 BETWEEN으로 위 코드를 BETWEEN을 통해 수정하면 다음과 같아진다.

```SQL
SELECT *
FROM Koreans
WHERE 나이 BETWEEN 30 AND 40
```

이때, BETWEEN에 사용된 두 숫자는 포함되어서 탐색을 한다

NOT BETWEEN을 통해서 해당 숫자 사이의 구간을 제외한 값들을 찾을 수도 있다.

```SQL
SELECT *
FROM Koreans
WHERE 나이 NOT BETWEEN 30 AND 40
%% 0~29, 41~세의 레코드들을 가져올 것이다. %%
```


# LIKE

LIKE는 조건을 포함하는 모든 레코드를 가져오는 조건문이다.

```SQL
SELECT *
FROM Koreans
WHERE 이름 LIKE '김%'
%% 모든 '이름'칼럼 중 '김'으로 시작되는 모든 레코드들을 출력한다. %%

---

WHERE 이름 LIKE '%이'
%% 이로 끝나는 %%

---

WHERE 이름 LIKE '%이%'
%% 등으로 다양하게 사용 가능 %%
```

# ORDER BY

위 조건문이나 SELECT문을 통해 출력할 레코드들이 존재한다고 가정해보자. 이때 이 레코드들을 사용자가 원하는 정렬형태로 출력하고 싶을 경우에 일일이 데이터들을 비교해가며 레코드들을 삭제/재삽입 과정을 거치는 행위는 매우매우 비효율 적이다.

ORDER BY는 원하는 정렬기준으로 내림차순/오름차순으로 정렬하여 레코드들을 출력해준다.

```SQL 
SELECT *
FROM Koreans
WHERE 이름 LIKE '김%' AND 나이 BETWEEN 30 AND 40
ORDER BY 나이 ASC
%% 30~40세 사이의 김씨를 오름차순으로 정렬하여 출력할 것이다. %%
```

ASC : 오름차순
DESC : 내림차순
생략 시 : ASC

# COUNT

집계함수 중 하나로, 레코드의 수를 출력해준다.

```SQL
SELECT COUNT(*)
FROM Koreans
WHERE 나이 BETWEEN 30 AND 40
```

이때 COUNT 뒤에 as를 붙여 새로운 행에 COUNT의 출력물을 저장해줄 수 있고, COUNT()안에 DISTINCT를 붙여 유니크한 값들을 count할 수 있다.

```SQL
SELECT COUNT(*) as count_res %% count_res 컬럼을 만들고 값을 넣음 %%
SELECT COUNT(DISTINCT 나이) as count_age_variation %% 나이 컬럼에 해당되는 레코드의 수 중 중복되는 수를 제외하고 count_age_variation 컬럼을 만들어서 넣음 %%
```

# SUM

집계함수로 합계를 도출.

```SQL
SELECT SUM(Height)
FROM Students
WHERE grade BETWEEN 3 AND 6
```

# AVG

집계함수로 평균을 도출

```SQL
SELECT AVG(Height)
FROM Students
WHERE grade BETWEEN 1 AND 4
```

이때 Null값이 들어있는 record는 집계에 포함되지 않는다. 
즉, AVG(hegith)와 SUM(height)/COUNT(* )의 값이 다를 수도 있다.

# MIN, MAX

집계함수로 최소, 최대 도출

# HAVING

앞선 WHERE와 사용법이 동일하지만, 집계 결과에 대한 조건문을 작성한다는 차이점이 존재한다.

즉 WHERE는 조건문에 적합한 레코드들을 전체 레코드들에서 찾는다면, HAVING은 집계 결과가 필터링을 통해 걸려져 나온 상태에서 한 번 더 걸러주는 역할을 한다.

```SQL
SELECT city_name
FROM Korea
WHERE city_people >= 300,000
ORDER BY city_people
HAVING city_area >= 1000000
```

위와 같은 예제로 사용하게 될 경우 city_people 30만 명이 넘는 도시들 중 지역의 크기가 1,000,000 이상의 레코드들의 city_name이 출력된다.

# AS

ALias, 별칭이라는 뜻으로 집계결과를 SELECT할 때, 해당 컬럼을 다른 이름으로 명명해야 할 경우 AS를 통해 다른 별칭을 붙여줄 수 있다.

# CASE WHEN

SWTICH CASE와 비슷한 맥락으로 CASE로 시작하고, WHEN으로 조건을 설정하여 새로운 열에 THEN으로 저장한다. 이때 맨 마지막은 ELSE와 같이 default로 사용할 수 있지만, 필수는 아니다.

```SQL
SELECT drink, snack, milk, shin-ramen AS ramen
FROM Market_price
ORDER BY price
CASE
	WHEN drink >= 4000 then 'Expensive'
	WHEN snack >= 5000 then 'more Expensive'
	ELSE 'normal'
```

위 예제처럼 특정 조건에 의해 레코드들을 구분하여 새로운 열에 저장하려고 할 때 유용하게 사용할 수 있다.

# INNER JOIN

테이블이 한 개라면 위 조건문과 집계함수로 복잡하지만 원하는 데이터를 뽑아낼 수 있다. 

하지만 테이블이 2개가 된다면 불가능해질 것이다. 원하는 조건에 해당되는 컬럼이 어디 테이블에 존재하는지 식별할 수 없을 것이고, 식별한다고 해도 두 테이블 간 테이터의 불일치 문제도 발생할 것이다. 이를 해결하기 위한 문법이 JOIN이고, INNER JOIN은 그 중에서도 공통 합을 다루는 JOIN이다.

![[Pasted image 20260203113615.png]]

벤다이어그램의 두 집합이 교차하는 부분을 합집합이라고 한다. 합집합을 나타내는 INNER JOIN은 두 테이블에 공통적으로 존재하는 column을 일치하는 레코드들끼리 합쳐 하나의 테이블을 사용하는 것과 동일한 효과를 준다.

```SQL
SELECT F.name, S.ID
FROM First-DB AS F
INNER JOIN Second-DB AS S ON F.ID = S.ID
WHERE F.price >= 300 AND S.count >= 500
```

위와 같이 class에 멤버 변수, 함수를 사용하는 것처럼 두 테이블의 명칭을 AS로 바꿔 사용하는 것이 일방적이다. 

# LEFT JOIN

![[Pasted image 20260203114002.png]]
INNER JOIN을 제외한 JOIN 방식을 OUTER JOIN이라고 하는데, 이때 LEFT JOIN은 A, B의 합잡합을 포함하여 A 테이블 기준으로 데이터를 나타내게 된다. 이때 A테이블에 존재하는 데이터가 B테이블에 존재하지 않을 가능성이 있는데, 위 INNER JOIN에서는 그런 서로 존재하지 않은, 매칭되지 않은 데이터들은 전부 삭제를 하고 집계하는 반면, LEFT JOIN은 A 테이블에 존재하는 모든 레코드들을 집계하고, 이때 B 컬럼에 존재하지 않은 데이터들은 NULL로 표시되게 된다.


# RIGHT JOIN


# FULL JOIN


# UNION


# SUBQUERY
