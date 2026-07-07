---
tags:
  - seed
aliases: []
created: 2026-05-08
---
# 1. swift

#### 언어적 특성
1. 안정성 : 프로그래머가 저지를 수 있는 실수를 엄격한 문법을 통해 사전에 컴파일러 차원에서 방지한다.
2. 신속성 : c언어 수준의 실행 속도의 최적화뿐만 아니라 지속적인 컴파일러 개량을 통해 더 빠른 컴파일 성능을 구현해 나가고 있다.
3. 더 나은 표현성 : 직관적인고, 현대적이며 세련된 문법을 통해 구사하려고 노력한다.

#### 패러다임
1. 객체지향
2. 함수형 프로그래밍 : 대규모 병렬처리를 통해 프로그램의 상태의 변화 없이 데이터 처리를 수학적 함수 계산으로 취급함
	- 일급 객체
		- 전달인자로 전달 가능
		- 동적 프로퍼티 할당 가능
		- 변수나 데이터 구조 안에 담을 수 있음
		- 반환 값으로 사용 가능
		- 할당할 때 사용된 이름과 관계없이 고유한 객체로 구별 가능
```Swift
func excute(tasks: [() -> void]){
	for task in tasks{
		task();
	}
}
```
위처럼 여러 객체들을 한 번에 함수인자로 전달하여 보낼 수 있음, 또한 함수 자체를 하나의 인자로 생각하는 람다형 함수를 매개변수로 하는 함수를 설정하는 등 다양한 표현식이 가능해진다.

#### REPL
- 인터프리터 언어에서 사용되는 하나의 구문이 끝날때마다 실행 결과를 출력해주는 작업을 통해 사용자는 어떤 부분에서 문제가 발생하는지 흐름대로 파악가능하고, SwiftUI를 사용하는 경우, 사용자가 변경한 코드가 즉각적으로 반영되어 UI를 통해 화면에 출력해주기 때문에 매우 유용함.

# 2. Start

#### 문자열 보간법
```swift
let name: String = 'university';
print("Place : \(name)");
```
위처럼 문자열을 "" + 변수 + "" 방식으로 중간에 추가해주는 것이 아닌 자연스럽게 녹도록 만듦.

#### 주석
- /* , // , 등도 지원하지만, 주석 내부에서는 markdown 기법을 통해 --- 처럼 한 줄을 표현하는 방식 등을 지원하게됨.
- 퀵헬프라는 기능을 통해 레퍼런스 문서의 요약된 내용으로 주석처리된 내용들을 보여줘 코드의 내용들을 한 눈에 파악하기 편함.

#### 변수 / 상수
- 변수 : var
- 상수 : let
- 타입추론을 통해 변수명 뒤에 타입을 자동선언 해주지만, 컴파일러 차원에서 지원해주기에 추후에 문제가 발생할 수도 있음.

# 3. Data Type

#### Int / UInt
- 8, 16, 32, 64 bit를 지원하는 정수 타입으로 Signed인가, Unsigned인가에 따라 위 두 가지 타입으로 나뉜다.

```swift
let 8bit: Int8 = 10;
let 16bit: Int16 = 20;

let 32bit: UInt32 = 30;
let 64bit: UInt64 = 40;

//기본적으로 2026년도 기준 시스템 아키텍처는 64bit체계를 따르기 때문에, 뒤에 비트 지정 없이 선언할 경우 64bit를 생성해준다.
let 64basicBit: UInt = 50;
```

#### Bool
- true / false

#### Float / Double
- 일반적인 언어처럼 32bit / 64bit의 부동소수점을 따르는 타입이다.

#### Character
- 영어나 한글 뿐만 아니라 이모티콘 한 글자도 사용 가능하다.
- 작은 따옴표가 아닌 큰 따옴표로 표시한다.
- 유니코드 9 문자를 사용하므로 2byte의 기본 타입 같지만, Grapheme Cluster을 통해 글자의 복잡함에 따라 메모리를 할당하는 방식이고, 이는 한 글자 단위로 적용되기 때문에, 항상 할당되는 메모리가 다를 수 있다.

#### String
- 문자열은 다양한 메서드 및 오퍼레이터를 지원한다.
- variable.hasPreffix(p: String) : p가 variable에 접두어로 존재하는지 확인 후, bool return
- variable.hasSuffix(p: String) : p가 variable에 접미어로 존재하는지 확인 후 , bool return
- 이외에도 uppercased(), lowercased(), isEmpty, count 등의 메서드와 +=, +, == 등 다양한 오퍼레이터도 지원한다.

#### Any, AnyObject, nil
- Any type은 c++ auto처럼 변수의 타입을 전적으로 컴파일러가 지정하는 것이 아닌 Any Type으로 값을 지정하는 것으로, 어떤 Type도 초기화 가능
- AnyObject는 클래스의 인스턴스(객체화할 때)에만 할당 가능하다.
- nil은 null과 동일하다.

# 4. Advanced Data Type

#### 타입 추론
- 앞선 상수 및 변수 부분에서 언급된 타입 추론은 swift언어의 안정성을 더해주는 문법으로 컴파일러가 자동으로 변수의 타입을 추론하여 정해주는 역할이다.
- auto와 차이점은 auto는 우항의 값을 복사하여 값에 해당하는 타입을 할당해주는 반면, 타입 추론은 문맥을 고려한다.
```
//cpp
pair<int, int> v = (10,10);
auto first = 10;
auto second = v;
cout << first == second; // IDE 차원에서 컴파일 에러 : Duck Typing

//swift
var name = "name";
var age = 10;
print(\(name == age)); // IDE가 없어도 컴파일러 차원에서 해당 타입 자체를 검열하고, 컴파일이 불가능하도록 만들어줌.
```
전자는 IDE가 사전 연산을 통해 검사를 해서 컴파일 오류를 발생시키지만, 후자는 사전 연산 없이도 타입 불일치로 인해 오류를 던진다.

#### TypeAlias
- typealias를 통해 dictionary, tuple와 같이 다양한 타입을 하나로 묶어서 자주 사용하게 될 경우, 사용될 수 있는 define과 비슷한 개념이다.
```swift
typealias studentInfo = (name: String, age: Int, height: Double) // for tuple
typealias school = [Int: studentInfo]; // Dictionary

var kongju: school = [0: ("kim", 20, 158.2)];
```

#### 튜플
```swift
var person: (name: String, age: int, height: Double) = ("name", 20, 182.5);
print(person.0, person.1, person.2);
print(person.name, person.age, person.height);
```
위처럼 다양한 타입을 하나의 튜플로 묶을 수 있고, 인덱싱을 통해 원하는 값을 가져올 수 있다.

#### 컬렉션
튜플 이외에도 많은 데이터를 묶어서 관리하는 방식들을 뜻함.
1. Array 
```swift
var names: Array<String> = ["kim", "Lee"];
var names: [String] = ["kim", "Lee];
var names: [String] = [String]();
var names: [String] = Array<Any>();

names.isempty
names.count
names.insert("park", at: 2);
names.append("choi");
names.firstIndex(of: "Lee");
names.first;
names.last;
names[1 ... 3] // python처럼 여러 배열을 for문 없이 조회 가능
```
위와 같이 빈 배열 및 배열 초기화를 다양한 방식으로 초기화 가능하고, isempty, count와 같은 기본 메서드도 지원한다.

2. Dictionary : key : value ([:]를 통해 빈 딕셔너리 생성 가능)
3. Set : 중복 없는 배열, 대괄호를 사용하기에 타입 추론을 사용할 경우 Array로 취급되기에 꼭 타입 지정을 해줘야 한다. (sorted함수 뿐만 아니라, intersection과 같은 집합연산도 가능함)

#### 열거형
- enum
``` swift
enum School{
	case primary 
	case elementary
	case middle = "중학교"
}

let highestEducationLevel: School = School.middle
let highestEducationLevel: School = School(rawValue: "중학교") // middle
highestEducationLevel.rawValue // "중학교"
```
원시값(rawValue) 프로퍼티 설정을 통해 원시값으로 설정가능함.

- 연관 값 설정을 통해 rawValue를 각 케이스에 초기화 하는 것이 아닌, 변수에 맞게 설정 가능하다.
```swift
enum PastaTaste{
	case cream, tomato
}

enum PizzaDough{
	case cheeseCrust, thin, original
}

enum PizzaTopping{
	case pepperoni, cheese, bacon
}

enum MainDish{
	case pasta(taste: PastaTaste)
	case pizza(dough: PizzaDough, topping: PizzaTopping)
	case chicken(withSauce: Bool)
	case rice
}

var dinner: MainDish = MainDish.pasta(taste: PastaTaste.tomato)
dinner = MainDish.pizza(dough: PizzaDough.cheeseCrust, topping:PizzaTopping.bacon)
```

#### 항목 순회
- 이처럼 열거형을 세분화해서 의존성을 주입하게 될 경우, 가장 큰 문제는 추후 열거형이 어떤 타입들로 구성되어 있는지 판단하기 어렵다는 것이다. 이때 CaseIterable Protocol을 통해 열거형에 타입 프로퍼티를 추가해준다.
```swift
//만약 열거형 내 모든 case에 원시값을 추가하고 싶으면 이처럼 {원시값}, {프로토콜}식으로 작성하면 된다.
enum School: String, CaseIterable {
	case primary = "유치원"
	case elementary = "초등학교"
	case middle = "중학교"
	case high = "고등학교"
}

let allCases: [School] = School.allCases
print(allCases) // 모든 열거형 내 case조회 가능
```

위 항목 순회 프로토콜을 제외하고도 순환 열거형(indirect), 비교 가능한 열거형(Comparable)을 통해 비교하거나, 이진 탐색을 위한 순환 알고리즘을 작성하는 등 다양한 열거형 형식을 추가가능하다.

# 5. Operator

- 기본적인 연산자들(<<, ++ ...)은 다른 언어와 동일하므로 서술하지 않는다.

#### Range Operator
- A...B : A~B
- A..<B: A~B-1
- A...: A~
- ...A: ~A
- ..<A: ~A-1

#### Overflow Operator
- 프로그래밍을 하다가 오버플로우가 발생할 수 있는데, 이때 오버플로우 연산자를 통해 오버플로우가 되는 것을 막는다.
```swift
let usignedInteger: Int = 0;
let underflowedValue: Uint8 = unsignedInteger &- 1; // 255
```

- 오버플로가 발생할 것 같아서 연산을 사용하는 목적이 아닌, 일부러 오버플로우를 발생시키고, 오류 없이 값을 순환시키는 알고리즘 등을 작성할 때, 이와 같은 연산자를 통해 훨씬 간편하게 진행 가능하다.

#### Customizing Operator
- 전위 / 중위 / 후위 연산자를 사용자의 원하는 기능대로 편집하는 방식으로, 새로운 연산자를 통해 연산처리를 간편하게 지원하는 방법

- 전위 연산자
```swift
prefix operator **

prefix func ** (value: int) -> int{
	return value * value;
}

let minusFive: UInt8 = -5;

print(**minusFive);
```

- 후위 연산자
```swift
postfix operator **

postfix func ** (value: int) -> int{
	return value * value;
}

let minusFive: UInt8 = -5;
print(minusFive**);
```

- 중위 연산자 
```swift
infix operator ** : MultiplicationPrecedence

func ** (value: Int, count: Int) -> Int {
	var result = 1;
	for i in 1...count:
		result *= value;
		
	return result;
}

let minusFive: UInt8 = -5;
print(minusFive**3);
```

# 6. 흐름 제어

## 조건문
#### if / if ~ else
- 조건문 괄호는 선택

#### Switch
- case를 통해 표현하는데, 이때 범위 연산자를 사용하여 표현 가능함.
- 문자열 경우, 여러 개의 문자열을 하나의 case에 묶어서 사용 가능.
- throughfall을 통해 밑에 case의 코드로 넘어가게 만들 수 있다.
- case 내부에 아무런 코드가 존재하지 않을 경우, 오류
```swift
switch(total){
	case 0 :
		~
		break;
	case 1...10:
		~
		break;
	default:
		break;
}


switch(str){
	case "kim", "park":
		~
		break;
		
	case "kim":
		fallthrough;
	case "park":
		~
		break;
}
//위 1개의 케이스와 아래 2개의 케이스는 같은 표현식
```


## 반복문

#### for-in
- for (임시 상수) in (범위 | 시퀀스 아이템)을 통해 실행코드를 반복하게 됨.
- 이때 범위에 범위 연산자 및 Collection등 다양한 자료구조를 반복할 수 있다.

#### while
- 다른 언어와 동일

#### repeat-while
- do-while문과 동일

#### 구문 이름표
- 반복문이 중첩되거나, 반복문 내부에서 특정 반복문으로 이동하는 등 복잡한 반복문을 구현할 때, 이름표를 통해 해당 반복문의 break / continue 작성 타이밍 및 가독성을 높일 수 있다.
```swift
numberLoop: for num in numbers{
	printLoop: while true{
		~
	}
	
	removeLoop: while true{
		~
	}
}
```

# 7. 함수

```swift 
//기본적으로 다음과 같은 형식을 유지
func "function name"(parameter ...) -> "return type"{
	codes...
	return "return value";
}
```

- 파라미터를 넣는 소괄호는 생략 불가(파라미터가 없는 것은 가능)

#### 전달인자 레이블
```swift
func "function name"(from myName: String, to name: String = "") -> "return type"{ // "전달인자" "파라미터":"파라미터명", default value설정 가능
	codes...
	return "return value";
}

function name(from: "kim", to: "park")
```

- 전달인자 레이블을 통해 함수의 파라미터를 정확하게 매핑하여 전달 가능
- 재정의 및 다중정의 시 전달인자 레이블만 다르게 해도 다중정의(오버로드)로 인식한다.

#### 가변 매개변수
swift에서 다음과 같은 방식으로 함수 호출이 이뤄진다.
1. 함수를 호출할 때, 전달인자의 값을 복사(깊은 복사)한다.
2. 복사한 변수를 함수 내부에서 변경한다.

따라서 매개변수의 값 수정이 이뤄지지 않는데, c++의 참조자처럼 값을 넘겨주면 값 변환이 가능해진다.
```swift
let number: Int = 1;
nonReferenceParapmeter(&number);//1+1
print(number);//2
```

진행 순서는 다음과 같다.
1. 함수를 호출할 때, 전달인자의 값을 깊은 복사한다.
2. 전달인자의 값 수정
3. 함수 반환 시점에서 매개변수에 수정된 값을 할당한다.

c++처럼 메모리에 접근하는 방식이 아닌, 메모리를 추가로 할당하고, 변경된 값을 매개변수에 초기화해주는 방식이다.

#### 반환이 없는 함수
- 반환타입을 정해주지 않거나, Void로 선언시 반환이 없는 함수로 간주.

#### 중첩 함수
- 열거형 내부에 열거형을 추가하거나, 클래스 내부에 클래스를 추가하는 등 다양한 중첩을 지원함.
- 이때 일급 객체의 특징을 살려 함수의 반환형으로 다른 함수를 반환해주는 것이 가능함.
```swift
typealias MoveFunc = (int) -> int;

func goRight(_ currentPosition: int) -> int{
	return currentPosition + 1;
}

func goleft(_ currentPosition: int) -> int{
	return currentPosition - 1;
}

func functionForMove(_ shouldGoLeft: Bool) -> MoveFunc{//반환으로 (int) -> int형을 지원하고, 이는 위 goRight/Left함수와 타입이 일치
	return shouldGoLeft ? goLeft : goRight; //함수명 자체를 반환 -> 함수를 함수 내부에서 실행하는 것이 아닌 반환형으로 하여 함수호출이 종료된 후 호출되어 사용
}

let moveToZero: MoveFunc = funtionForMove(position>0);

while position != 0{
	position = moveToZero(position);
}

//모듈화를 통해 각 함수가 단일 기능 모듈로 존재 가능
```


#### 종료되지 않는 함수
- 반환 타입을 Never로 지정하여 끝나지 않는 함수로 fetalError 등 에러 탐색 및 던지는 용도로 사용된다.

#### 반환 값을 무시할 수 있는 함수
- 함수 맨 앞에 @discardableResult를 통해 반환 값을 사용하지 않는다고 선언할 수 있다. (원래 반환값을 받는 변수가 존재하지 않을 경우 컴파일러가 오류를 던진다.)

# 8. 옵셔널
- 옵셔널이라는 문법은 스위프트의 안정성과 매우 연관된 문법이다.
- 스위프트 컴파일러는 안정성을 추구하기 위해 일반 변수에 null처럼 값이 지정되지 않는 값을 넣는 것을 컴파일 오류로 잡고, 파라미터를 통해 인자를 넘겨줄 때, null값이 존재하지 않는 것을 추구함.
- 그럼에도 switch-case처럼 case에 해당되지 않는 열거형을 null(undefined)값으로 넣어야 했고, 이때 옵셔널을 통해 넣게 됨

#### 옵셔널 생성
- 옵셔널은 다음과 같은 문법으로 생성 가능
```
var myName : String? = "name"
var myName : String? = nil 
//nil은 null과 동일
```

이때, 안정성 추구를 위해 nil값을 허용하지 않음에도, 옵셔널에는 예외적으로 허용, nil은 값이 없는 ""처럼 빈 문자열이 아닌, 정말 값이 없는 경우에만 해당.

- 열거형을 값으로 넣을 때는 다음과 같을 수 있음
```
let primary = School(rawValue: "유치원")
let graduate = School(rawValue: "석박사")
```

만약 위 값에서 "석박사"라는 case가 존재하지 않는 경우, nil값을 컴파일러가 할당하는데, 이때 graduate의 데이터 타입이 할당되어 있으면, nil값을 넣는 것이 컴파일 오류로 나올 수 있으므로, 타입 추론을 통해 컴파일러가 자동으로 School? 열거형 옵셔널로 매핑시킬 수 있도록 유도(열거형 내부에 실패 가능한 생성자를 default case에 대해 nil값 리턴)

-> 따라서 타입추론을 통해 변수를 선언하고, 열거형 값을 넣을때에는 꼭 조건문을 통해 nil값 확인이 필요, 추후에 api를 통해 변수를 열거형 case값으로 초기화를 할 경우, 내부 코드를 몰라 default case로 초기화하게 될 경우, 타입추론을 사용했기 때문에, 타입 지정을 통해 발생하는 컴파일 오류를 예방 가능함.

#### 옵셔널 추출
- 옵셔널이 아닌 변수에 옵셔널 값이 들어갈 수 없음
- 따라서 옵셔널 값을 추출하여 변수에 넣을 수 있는 값으로 치환 후 초기화가 필요한데, 이때 옵셔널 추출이 필요.

1. 강제 변환
```
var myName: String? = "yagom"
var yagom: String = myName!
```

<변수>!를 통해 옵셔널 값을 강제 변환 가능, 만약 이때 nil값을 강제 변환하여 초기화 할 경우, 런타임 오류가 발생 가능함. -> 강제추출(!)방식은 지양

2. 옵셔널 바인딩
```
var myName: String? = "yagom"

if var name = myName{
	/// name != nil
}
else{
	/// name == nil
}
```

if var(let)를 사용하게 될 경우, myName이라는 옵셔널 값을 자동으로 변환해서 변수에 할당해준다. 이때 변수가 free되는 시점은 if-else문이 끝나는 지점으로, 자동으로 옵셔널 값을 일반 타입으로 바꿔 사용가능하게 만들어주기 때문에, 위처럼 많이 사용한다.(옵셔널 값을 사용목적이 아닌 단순 nil확인 등의 목적으로 조건문을 사용하는 경우, 변수/상수 선언 없이 바로 nil비교만 하면 된다.)

3. 암시적 추출 옵셔널(IUO)
```
var myName: String! = "yagom" ///!를 강제추출용으로 사용하는 것이 아닌, 암시적 추출 옵셔널로 선언
myName = nil

if let name = myName{

} else{

}
```

위처럼 옵셔널 값을 추출 없이 사용하고 싶거나, myName이라는 변수가 nil값을 갖게 되어도, 런타임 오류가 발생하지 않을 것이라고 확신하는 경우, 암시적 추출 옵셔널을 통해 일반변수처럼 사용하면서 nil값을 할당할 수 있는 변수로 만들 수 있다.
-> 다만 매우 위험한 생각이며, 추후에 대입을 통해 자칫 nil값을 다른 변수에 넣는 시나리오가 발생할 경우, 런타임 오류가 발생하므로, 스위프트가 추구하는 안정성과는 살짝 먼 느낌이다.

# 9. 구조체 / 클래스
- 둘의 가장 큰 차이점은 구조체의 인스턴스는 값 타입이고, 클래스의 인스턴스는 주소 타입이다.
- 즉, 구조체는 스택메모리에 해당 데이터 타입만큼의 데이터를 할당받아 값을 저장하는 반면, 클래스는 힙에 할당하여 저장하고, head 주소를 stack에 저장하여 참조하게 된다.
- 자바처럼 하나의 소스파일에 클래스 하나만 선언하는 클래스 단위가 아닌, 소스파일에 여러 구조체 및 클래스를 저장해도 문제가 없음.
- 구조체 내부에 구조체, 클래스 내부에 클래스 등 중첩 선언이 가능

## 구조체

#### 구조체 정의
```
struct <struct name> {
	<properties>
	<methods>
}
```

- 상수로 선언된 구조체는 내부를 변경하지 못하지만, 변수는 가능하다.
``` 
var yagomInfo: BasicInfo = BasicInfo(name: "yagom", age: 99)
yagomInfo.name = "else"
yagomInfo.age = 100
///가능

let sebaInfo: BasicInfo = BasicInfo(name: "yagom", age: 100)
sebaInfo.name = "seba" ///불가능
```


## 클래스
- 기본적으로 자바에서는 모든 클래스에 java.lang.Object에 기본 클래스를 상속받아 toString(), equals()와 같은 메서드를 상속받음.
- 스위프트는 최상위 기본 클래스가 존재하지 않아 프로토콜을 부모 클래스로 상속 받아, 프로토콜 내 기능들을 상속하여 사용하게 된다.

#### 클래스 선언
```
class <className>{
	<properties>
	<methods>
}

class <className> : <parrentClass | protocols>{
	<properties>
	<methods>
	<any override methods>
}
```

- 이때 구조체와 달리 참조로 인스턴스가 생성되는 클래스는 주소는 상수이지만, 실제 값이 들어있는 메모리 자체는 변수이므로, 변경가능함.
```
class Person{
	var height: Float = 100.0
	var weight: Float = 1000.0
	
	init(height: Float, weight: Float){
		self.height = height
		self.weight = weight
	}
}

let human: Person = Person(height = 50.0, weight = 100.0)
human.height = 200.0 ///가능
```
- 프로퍼티가 초기화되어 있는 경우, 생성자에서 인자를 넘겨주지 않아도, 값이 초기화 되어 있다.
- 변수로 선언된 프로퍼티에 대해 인스턴스가 상수/변수에 상관없이 변경이 가능하다.(반대로 프로퍼티가 상수인경우, 어떠한 경우에서도 변경 불가)

#### 인스턴스 소멸
- 구조체는 stack에 선언되고, 블록 시스템을 통해 자동으로 스코프를 벗어나면 인스턴스가 해제됨(메모리 해제)
- 기본적으로 스위프트는 ARC라는 GC역할의 컴파일러가 자동으로 필요하지 않은 메모리에 대해 해제가 이뤄짐.
- 그럼에도 인스턴스의 소멸 전에 값을 따로 저장하는 등의 행위가 필요에 따라 발생하게 될 경우, deinit(소멸자)를 통해 특정 행동 실행 가능
- 위와 같은 이유로 싱글톤 패턴이 구조체에 적용되지 못하고, 클래스에만 적용가능해짐.
```
class Person{
	<properties>
	<methods>
	
	deinit{
		print("~~")
	}
}
```

위처럼 소멸자에 코드를 넣어 인스턴스 소멸 전 코드 실행 후 소멸.


#### 구조체와 클래스의 차이
- 구조체는 상속 불가
- 타입캐스팅은 클래스의 인스턴스에만 허용
- 소멸자는 클래스의 인스턴스에만 활용 가능
- 참조 횟수 계산은 클래스의 인스턴스에만 적용
- 클래스는 얕은 복사, 구조체는 깊은 복사가 이뤄짐

#### 식별 연산자
- 얕은 복사로 주소 값이 대입된 객체와 우항 객체는 같은 메모리를 가르키기에 참조가 같음. 
- 이때 같은지 확인하려면 단순 비교 연산자가 아닌 둘이 정말 같은 주소를 가지는지 식별하는 연산자 필요
```
var yagom: Person = Person()
let friend: Person = yagom /// shallow copy

if yagom===friend{ ///식별 연산자
	print("shallow copy")
}
```


#### 기본 데이터 값
- 스위프트의 모든 기본 데이터 값은 구조체이다. 
- 이는 주소가 아닌 값으로 전달이 이뤄진다.
- 따라서 매개변수와 같이 인자를 전달하는 경우, 상수로 전달이 이뤄지고, 매개변수의 값 수정 불가(이때 매개변수가 클래스 인스턴스일 경우, 앞선 개념을 대입하여 매개변수 내 프로퍼티의 값을 변경 가능함.)

-> 결론적으로 구조체 / 클래스를 선택하는 것은 개발자의 몫이며, 캡슐화나 값 복사를 위할 경우 구조체를 선택하고, 상속이나 위처럼 전달하는 매개변수가 경우에 따라 멤버의 값이 바뀌게 될 경우, 클래스를 선택하는 것이 합당하다.


# 10. 프로퍼티와 메서드

- 멤버 변수에 해당되는 프로퍼티는 세 종류로 나뉜다.

#### 저장 프로퍼티
- 값을 저장하는 가장 단순한 개념의 프로퍼티
- 일급 객체도 저장 프로퍼티로 간주된다.
- 이때 상수, 변수, 구조체 인스턴스 등 상관없이 옵셔널을 제외한 값들은 초기화되지 않는 경우 런타인 오류가 발생하기 때문에 기본값을 지정하거나, 생성자를 통해 초깃값 설정이 필요하다. (즉, 기본값이 없는 경우 생성자 필수)
- 초기값을 설정하여 이니셜라이저를 사용하지 않은 경우, 목적에 맞지 않는 인스턴스 사용이 되지 않고, 추후에 값을 일일이 변경해줘야 하는 불편함 존재 -> 따라서 프로퍼티를 옵셔널로 설정해주는 방식을 혼용할 수 있음

#### 지연 저장 프로퍼티 
- 만약 객체 호출이 발생하기 전까지 저장 프로퍼티에 값을 할당하지 않다가, 호출하는 시점에 메모리에 올리고 싶은 경우가 발생한다면 지연 저장 프로퍼티를 사용할 수 있다.
- 특히 추후에 값을 할당해줄 수도 있고, 안해줄 수도 있는 경우, lazy를 통해 초기값을 입력해놨다가, 추후에 값을 변경 가능함.(이는 var로 선언한 변수에 초기값을 넣었다가, 바꿔도 동일하게 작동하지만, lazy는 호출 시점에 메모리를 사용하기 때문에, 최적화 측면에서 매우 큰 이득임)
``` 
class Position{
	laxy var point: CoordinatePoint = CoordinatePoint()
	let name: String
	
	init(nmae: String){
		self.name = name
	}
}
```

즉 프로퍼티를 사용할 수도 있고, 안할 수도 있거나, 큰 메모리를 차지하여 추후에 호출 시점에서 올리고 싶은 경우 사용

#### 연산 프로퍼티
- 일반적으로 프로퍼티의 값을 변경하여 저장하고 싶은 경우, getter/setter을 통해 값을 가져와 연산하는 메서드를 외부에서 구현하게 되고, 이는 매우 비효율적임(모듈화가 되어 있지 않음)
- 따라서 멤버변수를 가져오거나, 값을 변경하는 메서드를 사용하기 위해 연산 프로퍼티를 사용
```
struct CoordinatePoint{
	var x: Int
	var y: Int
	
	// Self 대신 CoordinatePoint를 사용 가능
	func getOppositePoint() -> Self {
		return CoordinatePOint(x: -x, y: -y)
	}
	
	mutating func setOppositePoint(_ opposite: CoordinatePoint){
		self.x = -opposite.x
		self.y = -opposite.y
	}
}
```

위처럼 getter/setter을 변형하는 메서드를 내부에 생성하여 목적에 맞는 사용 유도

밑에처럼 더 간결하게 표현 가능
```
struct CoordinatePoint{
	var x: Int
	var y: Int
	
	func OppositePoint: Self{
		get{
			return CoordinatePoint(x: -x, y: -y)
		}
		set(opposite){
			self.x = -opposite.x
			self.y = -opposite.y
		}
	}
}

print(position.oppositePoint) //get
position.oppositePoint = position // set
```

#### 프로퍼티 감시자 
- 프로퍼티 값이 변경되었을때, 이에 따라 적절한 작업을 수행 가능함
```
class Acount{
	var credit: Int = 0{
		willSet {
			print("잔액이 \(credit)에서 \(newValue)로 변경 예정") // 자동으로 newValue라는 매개변수에 변경될 값 저장
		}
		
		didSet{
			print("잔액이 \(oldValue)에서 \(credit)으로 변경됨") //자동으로 oldValue라는 매개변수에 변경 전 값 저장
		}
	}
}
```


#### 타입 프로퍼티
- var, let, static등 프로퍼티의 타입을 정하는 값을 뜻함

#### 키 경로
- 일급 객체처럼 변수에 함수의 참조를 할당하여 사용 가능했음
```
class Person{
	var name: String
	
	init(name: String){
		self.name = name
	}
}

print(type(of: \Person.name)) // ReferenceWritableKeyPath<Person, String>
```

위처럼 키 경로가 KeyPath에 맵 형식으로 존재하고, 포인터처럼 키 경로를 통해 프로퍼티에 접근 가능하다.

``` 
let keyPath = \Person
let nameKeyPath = keyPath.appending(path: \.name) // 이처럼 키패스 뒤에 하위 경로를 덧붙이기 가능
```

#### 인스턴스 메서드
- 프로퍼티의 값이 변경될 때마다 호출되는 메서드를 설정 가능함
```
class LevelClass{
	var level: Int{
		didset{
			print("level : \(level)")
		}
	}
	
	func levelUp(){
		print("Level UP!")
		level+=1
	}
	
	func levelDown(){
		print("Level Down")
		level-=1
	}
	
	func reset(){
		print("Reset!")
		level = 0;
	}
}
```
클래스는 프로퍼티 값 수정시 별도의 키워드가 필요 없지만, 구조체/열거형은 mutating을 통해 인스턴스 내부 값을 변경함을 명시해야 한다.

```
struct LevelClass{
	var level: Int{
		didset{
			print("level : \(level)")
		}
	}
	
	mutating func levelUp(){
		print("Level UP!")
		level+=1
	}
	
	mutating func levelDown(){
		print("Level Down")
		level-=1
	}
	
	mutating func reset(){
		print("Reset!")
		level = 0;
	}
}
```

#### Self 프로퍼티
- this처럼 자기 자신(본인 인스턴스)를 가르키는 키워드

# 11. 인스턴스 생성 및 소멸
- 앞선 방식에 따라 이니셜라이저/디이니셜라이저를 통해 인스턴스의 생성 및 소멸을 관리함
- 본격적으로 이니셜라이저/디이니셜라이저를 통해 인스턴스의 생성과 소멸을 관리하는 방식을 배움

#### 생성
```
class SomeClass{
	init() {
		//~
	}
}
```

init()을 통해 앞에 func 키워드 없이 생성자임을 선언, 이때 프로퍼티에 적절한 초깃값을 설정해야 옵셔널을 제외한 데이터 타입에 초깃값 할당 및 런타임 에러 방지가 가능함

``` 
class SomeClass{
	var squareMeter: Double = 0.0 //바로 할당
	
	init(squareMeter: Double){
		self.squareMeter = squareMeter // 초깃값 설정, 상수도 이니셜라이저에서 초기화 가능
	}
}
```

```
class SomeClass{
	var length: Double
	
	init(fromPy py: Double){
		self.length = py * 3.141592
	}
	
	init(_ squareMeter: Double){
		self.length = squareMeter
	}
}

let circle = someClass(fromPy: 5.0)
let square = someClass(10.0)
```

위처럼 다중 이니셜라이저에 _ (와일드카드)를 통해 지정을 자유롭게 할 수 있음.

```
class SomeClass{
	let length: Int? // nil
	let height: Double
	
	init(fromHeight height: Double){
		self.height = height
	}
}
```
위처럼 옵셔널 저장 프로퍼티에 대해 초기화가 없을 경우 자동으로 nil값 할당.

#### 기본 이니셜라이저 / 멤버와이즈 이니셜라이저
- 기본적으로 구조체는 멤버와이즈 이니셜라이저라는 기본 이니셜라이저 존재
```
struct Shape{
	let width: Int
	let height: Int
}

let rectangle: Shape = Shape(width: 10, height: 10) // 멤버와이즈 이니셜라이저
```
-> 저장 프로퍼티에 대한 기본 생성자를 생성(AllArgsConstructor)

하지만, 클래스는 불가능함 -> 상속에 대한 문제 때문
```
class Parent {
    var name: String
    init(name: String) {
        self.name = name
        // ⚡️ 부모 생성자 도중에 함수 호출!
        self.printInfo() 
    }
    func printInfo() { print("부모: \(name)") }
}

class Child: Parent {
    var age: Int // ⚠️ 아직 메모리 공간(방)이 안 만들어진 상태!

    override func printInfo() {
        // ❌ 여기서 대폭발 발생!
        // 함수 자체는 메모리에 존재하지만, 이 함수가 접근하려는 'age'라는 
        // 실제 메모리 방은 아직 세상에 존재하지 않습니다! (할당 전)
        print("자식: \(name), 나이: \(age)") 
    }
}
// parent.init()에서 printInfo를 실행하는데, 다형성에 의해 child printInfo실행, age는 초기화 이전이기 때문에 런타임 오류 발생
```
따라서 구조체는 멤버와이저 이니셜라이저를 지원하지만, 클래스는 불가능함 -> 직접 프로퍼티에 맞는 init생성 필요

#### 초기화 위임
- 위와 같은 이유로 클래스는 사용불가능, 열거형/구조체에서 위임을 통해 추가적인 args에 대해 다른 init을 호출 가능함
```
enum Student{
	case elementary, middle, high
	case none
	
	// 다른 이니셜라이저 존재시, 기본 이니셜라이저를 직접 설정해야 사용 가능
	init(){
		self = .none
	}
	
	init(koreanAge: Int){
		switch koreanAge{
			case 8...13:
				self = .elementary
			case 13...16:
				self = .middle
			case 16...19:
				self = .high
			default:
				selt = .none
		}
	}
	
	init(bornAt: Int, currentYear: Int){
		self.init(koreanAge: currentYear - bornAt + 1) // 초기화 위임
	}
}
```

#### 실패 가능한 이니셜라이저
- 이니셜라이저를 통해 인스턴스가 실패하는 경우를 대비
- 실질적으로 nil값을 리턴하는 것이 아니지만, 컴파일러에게 nil을 알리고, 인스턴스 메모리 자체를 폐기하여 nil값을 넣어줌
```
enum Student: String{
	case elementary = "초등학생", middle = "중학생", high = "고등학생"
	
	//실패 가능한 이니셜라이저
	init?(koreanAge: Int){
		switch koreanAge{
			case 8...13:
				self = .elementary
			case 13...16:
				self = .middle
			case 16...19:
				self = .high
			default:
				return nil //실패 시
		}
	}
}

var younger: Student? = Student(koreanAge : 50) // nil을 넣어주기에 반드시 옵셔널
```

#### 함수를 통해 프로퍼티 기본값 설정
- 모든 변수/상수가 일급객체임을 이용하여 함수를 통해 값을 초기화해줌
- 이때, 다른 프로퍼티는 초기화되지 않은 상태이므로, 연산에 사용할 수 없고, self도 사용 불가능(아직 메모리가 할당되는 시점이기 때문)
```
struct Student{
	var anme: String?
	var age: Int
}

class SchoolClass{
	//반환값은 프로퍼티와 같은 타입으로 이뤄지도록 클로저를 설정
	var students: [Student] = {
		var arr: [Student] = [Student]()
		
		for i in 1...15{
			var student: Student = Student(name: nil, age: i)
			arr.append(student)
		}
		
		return arr
	}()
}
```

#### 디이니셜라이저
- 인스턴스가 필요 없어진 시점에 자동으로 기본 디이니셜라이저 사용
- 이때 클래스 프로퍼티를 파일에 저장하는 등의 기능이 필요하는 경우 유용
```
class Person{
	deinit{
		//~
		//소괄호 필요 x
		//인스턴스에서 강제 호출 불가
	}
}
```


# 12. 접근제어
- OOP의 은닉화 / 캡슐화에서 유용
- open, public, internal(기본 접근수준), fileprivate, private 순

| **접근 제어자 (Level)** | **다른 모듈 (외부 라이브러리)** | **같은 모듈 (앱 프로젝트 내부)** | **같은 파일 (.swift)** | **같은 중괄호 블록 ({ })** | **주요 용도 & 특징**                       |
| ------------------ | -------------------- | --------------------- | ------------------ | ------------------- | ------------------------------------ |
| open               | **상속 / 접근 모두 가능**    | ⭕️                    | ⭕️                 | ⭕️                  | 외부 모듈에서 **상속/오버라이드** 허용 (클래스 전용)     |
| public             | **접근만 가능** (상속 ❌)    | ⭕️                    | ⭕️                 | ⭕️                  | 외부 모듈에서 **가져다 쓰기만** 허용 (상속 방지)       |
| internal           | ❌                    | **모든 곳에서 가능**         | ⭕️                 | ⭕️                  | **기본값 (Default).** 우리 앱 프로젝트 안에서 공유  |
| fileprivate        | ❌                    | ❌                     | **하나의 파일 안에서만**    | ⭕️                  | 같은 파일에 있는 다른 클래스/확장(`extension`)과 공유 |
| private            | ❌                    | ❌                     | ❌                  | **선언된 블록 내에서만**     | 가장 강력한 보안. 해당 객체 내부의 비밀 데이터          |
- 하위 모듈은 상위 모듈의 접근 제어 이상의 권한을 가질 수 없음

# 13. 클로저

https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/

스위프트에서 c언어의 포인터처럼 악명이 높은 문법으로, 자바의 람다형 함수처럼 스트림을 간편하게 넘겨주고, 기능하는 함수를 일급 객체에 저장하는 등의 행위를 하기 위해 만든 문법이다.

- 일정 기능을 하는 코드를 하나의 블록으로 모아놓은 것을 의미하며, 

**
# 14. 옵셔널 체이닝과 빠른 종료
- 구조체나 클래스의 프로퍼티에 옵셔널 값을 넣고, 이를 인스턴스로 갖는 프로퍼티를 멤버로 갖는 클래스/구조체를 다중으로 설계하게 될 경우, 최상위 인스턴스의 옵셔널 값에 따라 프로퍼티가 갖는 값이 nil이 될 수도 있고, 아닐 수도 있기에, 모든 값을 옵셔널로 갖게 하는 구조를 옵셔널 체이닝이라고 한다.
```
class Room{
	var number: Int
	
	init(number: Int){
		self.number = number
	}
}

class Building{
	var name: String
	var room: Room?
	
	init(name: String){
		self.name = name
	}
}

struct Address{
	var province: String
	var city: String
	var street: String
	var building: Building?
	var detailAddress: String
}

clss Person{
	var name: String
	var address: Address?
	
	init(name: String){
		self.name = name
	}
}

let yagomRoomViaOptionalChaining: Int? = yagom.address?.building?.room?.number // !와 같은 강제추출이 이때 매우 위험
```

이때 옵셔널 체이닝에서 강제추출시 하나의 옵셔널이 nil값을 갖는 경우, 이후의 하위 인스턴스에 대해 nil값을 리턴하기에 강제추출이 매우 위험

#### 빠른 종료
- throw-catch문처럼 특정 조건 하에 예외처리를 하거나, 코드 블럭을 종료시켜야 하는 구문에서 guard-else문을 통해 간단하게 표현 가능함
```
for i in 0...3{
	if i == 2{
		print(i)
	} else{
		continue
	}
}

->

for i in 0...3{
	guard i == 2 else{
		continue
	}
	print(i)
}
```

특히 위 옵셔널 체이닝과 관련되어 다음과 같이 표현 가능하다.

```
let person: [String: String] = {
	"name" : "minjun"
	"location" : "library"
}

guard let location: String = person["location"] else{
	print("nil")
	return
} // person에 location에 해당되는 내용이 없을 경우 return
```

가장 큰 특징은 return, break, continue, throw등의 제어문 전환 명령어가 없으면 사용이 불가능하다는 점이다.

# 15. 맵, 필터, 리듀스
- 일반적으로 함수를 입급 객체 취급하는 스위프트에서는 다른 함수의 파라미터로 함수를 보낼 수 있고, 이러한 함수를 고차 함수라고 지칭함.

#### 맵
- 맵은 두가지의 관점에서 바라볼 수 있다.
	1. 자료에서의 맵 : 자료에서의 맵은 일대일 대응이 되는 key-value형식의 자료형이다.
	2. 기능에서의 맵 : 위 일대일 대응에서 결론적으로 집합 A의 원소를 집합 B의 원소로 일대일 대응시키는 방식으로 이때 해시함수처럼 함수라는 과정을 거쳐 집합 B에 매핑을 시키게 된다.

- 스위프트에서 맵은 컨테이너(집합 A)와 클로저(함수)를 통해 집합 B를 얻어내는 고차 함수를 의미함
```
// container.map(f(x)) -> return의 형식을 띔

let numbers: [Int] = [0,1,2,3]

doubledNumbers = numbers.map{$0 * 2} // (numbers: [Int]) -> ([Int]){}처럼 사용해도 됨
```

#### 필터
- 컨테이너 내부의 값을 걸러서 추출하는 고차함수
- Bool return 형식의 클로저를 사용
```
let evenNumbers: [Int] = numbers.filter {(number: Int) -> Bool in
	return number % 2 = 0
}


// 맵과 이어서 사용가능함
let oddNumbers: [Int] = numbers.map{$0 + 3}.filter{$0 % 2 == 1}
```

#### 리듀스
- 컨테이너 값들을 클로저 함수를 통해 하나의 값으로 결합하는 경우 사용
```
let sumFromThree: Int = numbers.reduce(3){//초기값 3
	return $0 + $1
}
```

초기값이 포함된 컨테이너를 클로저의 인자로 넘겨주기에 초기값 설정 필요

# 16. 모나드

