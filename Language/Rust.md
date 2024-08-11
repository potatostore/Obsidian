1. Types
	1. integer : 2진수의 자리수에 따른 크기 분류 (isize, usize는 컴퓨터 비트타입에 따른 크기, 32-bit window같은 경우 isize = 32bit)
	2. char : unicode체제를 따르는 문자형, 255번까지 존재하는 unicode특성상 u8의 size를 갖는다. 

| Length  | Signed  | Unsigned |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| arch    | `isize` | `usize`  |


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

- 따라서 위의 같은 경우는 char로 변환하여 출력할 때 크기도 바꿔주어야 한다.

```rust
fn main(){

	let num = 100; //i32 size integer

	println!("{}", num as u8 as char);
}
```

- unicode에서 100에 해당하는 문자는 'd'이므로 'd'가 정상적으로 출력되는 모습을 볼 수 있다.

[usize/isize] : 어느 메모리로든 유동적으로 변경이 가능하며 32-bit computer에서는 u32/i32가 최대이다. 만약 size가 usize인 127이 있으면 u8과 동일한 사이즈로 간주된다.

[usize를 indexing으로 사용하는 이유] 
1. index can't be negative(minus value)
2. it should be big, because sometimes you need to index many things.
3. 32-bit computers can't use u64 so usize unavitable.

