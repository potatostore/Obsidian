---
tags:
  - seed
aliases: []
created: 2025-10-09
---
# Types
## Types

1. integer : 2진수의 자리수에 따른 크기 분류 (isize, usize는 컴퓨터 비트타입에 따른 크기, 32-bit window같은 경우 isize = 32bit)
2. char : unicode체제를 따르는 문자형, 4bytes size를 갖는다.
3. float : f32, f64 type을 갖는 소수

|         |         |          |         |     |
| ------- | :-----: | :------: | ------- | --- |
| Length  | Signed  | Unsigned | float   |     |
| 8-bit   |  `i8`   |   `u8`   |         |     |
| 16-bit  |  `i16`  |  `u16`   |         |     |
| 32-bit  | `i32`   |  `u32`   | `f32`   |     |
| 64-bit  |  `i64`  |  `u64`   | `f64` k |     |
| 128-bit | `i128`  |  `u128`  |         |     |
| arch    | `isize` | `usize`  |         |     |
```rust title='Types Ex'
fn main(){
	let a = 100; //i8 size integer
	let first_letter = 'A';
	let space = ' ';
	let cat_face = '😺'; // space, Emojis are also chars

	println!("{}{}{}{}", a, space, first_letter, cat_face);
}
```

```rust title='if you want show int to char [error]'
fn main(){

	let num = 100; // if you didn't write a type of
	               // integer, then they choose i32.

	println!("{}", num as char); // add 'as [Types]' if you 
	                             // want to change.

	//error : char's size is u8 but 'num' is i32 size. 
	//only 'u8' size can chage to char
}
```

- 따라서 위의 같은 경우는 char로 변환하여 출력할 때 크기도 u8로 바꿔줘야 한다.

```rust
fn main(){

	let num = 100; //i32 size integer

	println!("{}", num as u8 as char);
}
```

- unicode에서 100에 해당하는 문자는 'd'이므로 'd'가 정상적으로 출력되는 모습을 볼 수 있다.

## usize/isize

어느 메모리로든 유동적으로 변경이 가능하며 32-bit computer에서는 u32/i32가 최대이다. 만약 size가 usize인 127이 있으면 u8과 동일한 사이즈로 간주된다.

## usize를 indexing으로 사용하는 이유

1. index can't be negative(minus value)
2. it should be big, because sometimes you need to index many things.
3. 32-bit computers can't use u64 so usize unavitable.

- 보통 index는 container내에 특정 원소의 위치를 쉽게 파악하기 위해 지정한다.
	vector와 같은 container내에 다양한 원소,객체가 저장되어 있을텐데, 그 중 원하는 원소를 불러오는건 쉽지가 않다. 이를 위해 index라는 개념을 사용하는데 rust같은 경우 index를 usize로 설정하는 이유가 나온다. 예를 들어 회사원들의 정보(이름, 주민등록번호 등등)가 들어있는 container에서 과장급 이상의 모든 회사원에게 index를 설정하려고 한다. 과장급 이상의 회사원이 회사마다 다르며, 얼마나 클지 상상이 안되기 때문에 usize를 통해 설정을 하는 것이다.

## char

? : 왜 최대 4bytes를 갖을 수 있는 char에서 int를 casting하면 u8만 가능할 까?
    u32까지 가능해야 하는거 아님?

## Type inference

Type을 말해주지 않아도 자동으로 결정하는 것. 

```rust title=j'Type inference'
fn main(){

	let a = 100; //Type inference decide 'a' to i32
	let a: u8 = 100; // you decide type to u8
	let a = 100u8; // also decide type
	let a = 100_u8 // more readability
	let a = 100_100_100_i32 // more readability2
	let number = 0_________u8 // '_' didn't change the num
}
```

- type을 결정해줘야 하는 경우
	1. 매우 복잡한 것을 하거나, 컴파일러가 변수에 대한 type을 인식하지 못할 경우
	2. 다른 type으로 설정하고 싶은 경우

cjcidndkdk
