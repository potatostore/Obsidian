1. Types
	1. integer : 2진수의 자리수에 따른 크기 분류 (isize, usize는 컴퓨터 비트타입에 따른 크기, 32-bit window같은 경우 isize = 32bit)

		
	2. char : 기본 unicode에 따른 문자형

```rust
fn main(){
	let a = 100; //i8 size integer
}
```

|Length|Signed|Unsigned|
|---|---|---|
|8-bit|`i8`|`u8`|
|16-bit|`i16`|`u16`|
|32-bit|`i32`|`u32`|
|64-bit|`i64`|`u64`|
|128-bit|`i128`|`u128`|
|arch|`isize`|`usize`|