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