# 1. swift

## 
# 2. Start


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