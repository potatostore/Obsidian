강의 : https://www.youtube.com/watch?v=EerdGm-ehJQ&list=PL3r6NYvHcxgVTIxCxTKP4O_dWF4ZnSm1q&index=2
교재 : https://helloworldjavascript.net/


# 0. JS basic



# 1. Type

#### number

#### string

#### undefined

#### NaN(Not a Number)

#### null

# 2. function

많은 연산자들은 다른 언어들과 거의 동일하게 구현가능하기에 건너뛰고, 함수부분을 설명한다.

사실 JS의 함수또한 크게 다를바 없다. 

매개변수인 parameter부분과 반환 모두 지원을 하는 편이지만, 앞선 type에서 알 수 있듯이 변수에 대한 자료형이 강박적이지 않은 JS는 매개변수와 반환형의 타입을 명시하지 않는다. 

```js
function exam(item1, item2){
	return item1 + item2
}
```

만약 위 item1, 2가 string이라면 이어붙이기를 통해 하나의 문자열로 반환을 해줄 것이고, number에 해당되는 경우 연산을 통해 결과값을 반환해 줄 것이다. 또한 반환형이 없는 것도 가능하다.

# 3. Object

Object는 c언어의 구조체와 매우 유사하다. 

Union처럼 