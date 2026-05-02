# 1.  swift

# 2. Start

# 3. Data Type

#### Int / UInt
- 8, 16, 32, 64 bit를 지원하는 정수 타입으로 Signed인가, Unsigned인가에 따라 위 두 가지 타입으로 나뉜다.
```Swift
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
- 유니코드 9 문자를 사용하므로 2byte의 기본 타입 같지만, 영어를 사용할 때에는 1byte를 사용하다가, 이모지와 같이 2byte가 필요한 경우, 동적으로 할당해준다.

# 4. Advanced Data Type
