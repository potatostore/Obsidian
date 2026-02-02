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