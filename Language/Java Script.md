---
tags:
  - seed
aliases: []
created: 2026-02-10
---
강의 : https://www.youtube.com/watch?v=EerdGm-ehJQ&list=PL3r6NYvHcxgVTIxCxTKP4O_dWF4ZnSm1q&index=2
교재 : https://helloworldjavascript.net/

기존 노트(Type/function/Object)는 아래 "0. JS basic 정리"로 옮기고, ShoppingMall 웹서버 착수하면서 새로 필요해진
모듈/구조분해/async·await/React/Next.js까지 이어서 정리한다. (2026-08-21)

# 0. JS basic 정리 (기존 내용)

#### Template Literal
보통 문자 하나를 표현하고 싶은 경우, 작은따옴표(')로 표현하고, 문자열은 큰 따옴표(")을 통해 표현하게 된다.

```js
const name = "감자";
console.log(`${name}님, 주문이 완료됐어요.`);   // 백틱 + ${}로 변수를 문자열에 바로 끼워넣음
```

#### Type: number / string / undefined / NaN / null / typeof

#### function
많은 연산자들은 다른 언어들과 거의 동일하게 구현 가능하기에 건너뛰고, 함수부분을 설명한다.

사실 JS의 함수 또한 크게 다를 바 없다. 매개변수인 parameter 부분과 반환 모두 지원을 하는 편이지만, 변수에 대한
자료형이 강박적이지 않은 JS는 매개변수와 반환형의 타입을 명시하지 않는다.

```js
function exam(item1, item2){
	return item1 + item2
}
```

위 item1, 2가 string이라면 이어붙이기를 통해 하나의 문자열로 반환을 해줄 것이고, number에 해당되는 경우 연산을
통해 결과값을 반환해 줄 것이다. 또한 반환형이 없는 것도 가능하다.

#### Object
Object는 OOP의 class와 매우 유사하다.

```js
const product = {
	name: 'socks',
	price: 1000
};

console.log(product);

product.newProperty = true;

console.log(product);

delete product.newProperty;

console.log(product);
```

product Object는 마치 Map처럼 출력이 된다. Object.{anything you want to create new property}를 통해 원하는 속성을 새로 만들어 낼 수 있다(const로 선언된 Object는 새로운 속성을 부여할 때 반드시 값을 초기화해줘야 한다).

delete를 통해 속성값을 삭제 가능하다.

---

# 1. JS 갭 메우기 (모던 JS)

React/Next.js 코드에서 매 줄 마주치는데 위 기초 노트엔 없었던 문법들. `github.com/potatostore/html-css-js`의
Lesson 1~12(함수·배열·반복문·DOM 이벤트)는 이미 익혔다는 전제로, 그 이후만 정리.

#### 모듈: import / export
예전엔 `<script src="...">`를 여러 개 이어붙이고 전역 변수로 공유했다. 지금은 파일 하나하나가 독립된
**모듈**이고, 다른 파일이 쓸 걸 `export`로 내보내고 `import`로 가져온다.

```js
// utils.js
export function formatPrice(won) {
  return won.toLocaleString('ko-KR') + '원';
}
export default function Logo() { /* ... */ }

// page.tsx
import Logo from './Logo';               // default export → 이름 자유
import { formatPrice } from './utils';   // named export → 이름 그대로
```

`import React, { useEffect, useState } from "react";`가 바로 이거 — React가 내보낸 `useEffect`, `useState`를
이름 그대로 가져오는 것.

#### 구조분해 할당
객체나 배열에서 필요한 값만 바로 꺼내서 변수로 만드는 문법.

```js
const product = { name: "키보드", price: 30000 };
const { name, price } = product;

const pair = [0, "초기값"];
const [count, label] = pair;
```

> React의 `useState(0)`는 `[값, 값을_바꾸는_함수]` 형태의 배열을 돌려주는데, 거의 항상
> `const [count, setCount] = useState(0);`처럼 배열 구조분해로 바로 받아쓴다. 함수 매개변수 자리에서도 그대로
> 쓸 수 있고, React props를 받을 때 표준 패턴이다: `function ProductCard({ name, price }) {...}`

#### 전개 연산자(...) / 나머지 매개변수
배열·객체를 "펼칠" 때, 그리고 함수가 개수 정해지지 않은 인자를 받을 때 쓴다.

```js
// 객체 복사 + 일부만 덮어쓰기 (원본은 안 건드림)
const cartItem = { productId: 3, quantity: 1 };
const updated = { ...cartItem, quantity: 2 };   // { productId: 3, quantity: 2 }

// 배열에 새 항목 추가 (원본은 안 건드림)
const items = [1, 2, 3];
const withNew = [...items, 4];   // [1, 2, 3, 4]
```

> React state는 직접 수정하면 안 되고(`state.quantity = 2` 금지), 항상 "복사본을 만들어서 통째로 교체"해야
> 한다. `...`이 그 복사본을 만드는 표준 도구.

#### 화살표 함수와 this
Lesson 12에서 이미 `const multiply = (a, b) => a*b;` 형태로 써봤으니 문법은 익숙함. 화살표 함수는 자기 자신의
`this`를 안 만들고 바깥 스코프의 `this`를 그대로 물려받는다는 것만 추가로 기억. React 함수형 컴포넌트에서는
`this` 자체를 거의 안 써서 실전에서 부딪힐 일은 적다.

#### Promise와 async / await ⭐
`setTimeout`으로 "1초 뒤에 실행"은 이미 다룸. **Promise**는 그 아이디어를 "언젠가 끝나는 작업(주로 네트워크
요청)의 결과"로 일반화한 객체. `async`/`await`는 그 Promise를 마치 동기 코드처럼 순서대로 읽히게 해주는 문법.

콜백 → Promise → async/await 순서로 진화:

```js
// 옛날 방식: 콜백
setTimeout(() => { console.log("완료"); }, 1000);

// Promise 방식: .then()으로 이어붙임
fetch('/api/products')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// async/await 방식: 위와 완전히 같은 동작, 순서대로 읽힘
async function loadProducts() {
  try {
    const res = await fetch('/api/products');
    const data = await res.json();
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}
```

> `signin/page.tsx`의 `handleSignIn`이 정확히 이 패턴: `try { const response = await fetch(...); ... }
> catch(error) { ... }`.

#### fetch API
브라우저(또는 Node)에서 HTTP 요청을 보내는 내장 함수. 세 가지만 기억:
1. `fetch(url, options)`는 Promise를 돌려줌 → `await` 필요.
2. 응답이 와도 `response.ok`가 `false`일 수 있음(404, 401 등) — HTTP 에러가 나도 `catch`로 안 떨어지고
   정상적으로 다음 줄로 넘어가니 상태 코드를 직접 확인해야 함.
3. 본문은 `await response.json()`처럼 한 번 더 `await`해야 실제 데이터가 나옴.

```js
const response = await fetch('http://localhost:8080/api/v1/products', {
  method: 'GET',
  credentials: 'include',          // 쿠키(JWT)까지 같이 보낼지
  headers: { 'Content-Type': 'application/json' },
});

if (!response.ok) {                // 상태 코드는 여기서 직접 확인
  throw new Error('요청 실패: ' + response.status);
}
const products = await response.json();
```

#### map · filter · reduce
Lesson 11의 `forEach`와 형제 메서드지만 역할이 다르다.

| 메서드 | 하는 일 | 돌려주는 것 |
|---|---|---|
| `forEach` | 각 항목마다 뭔가 실행(로그 출력 등) | 없음 (undefined) |
| `map` | 각 항목을 다른 값으로 변환 | 변환된 새 배열 |
| `filter` | 조건에 맞는 항목만 골라냄 | 걸러진 새 배열 |
| `reduce` | 배열 전체를 값 하나로 누적 | 누적된 값 하나 |

```js
const cart = [
  { name: "키보드", price: 30000, quantity: 2 },
  { name: "마우스", price: 15000, quantity: 1 },
];

// map: 화면에 뿌릴 형태로 변환 (React 리스트 렌더링에서 매번 씀)
const lines = cart.map(item => `${item.name} x${item.quantity}`);

// filter: 수량 2개 이상인 것만
const bulky = cart.filter(item => item.quantity >= 2);

// reduce: 전체 합계
const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);   // 75000
```

`reduce`의 두 번째 인자(`0`)는 누적을 시작할 초깃값, 콜백의 첫 번째 인자(`sum`)가 "지금까지 누적된 값".
백엔드 `Order.updateTotalOrderPrice()`가 `orderItemList.stream().mapToLong(...).sum()`으로 하는 것과 같은
개념(자바 스트림 reduce)이라 자바 쪽으로 유추하면 편함.

#### 옵셔널 체이닝(?.) / 널 병합(??)

```js
const price = product?.price;            // product가 null/undefined면 에러 대신 undefined
const safePrice = product?.price ?? 0;   // 그 undefined까지 기본값 0으로
```

`??`는 `||`와 비슷해 보이지만, `0`이나 `""`처럼 "값은 있지만 falsy한 것"은 그대로 살려주고 `null`/`undefined`일
때만 기본값으로 바꾼다. `price || '가격 미정'`로 잘못 쓰면 0원이 '가격 미정'으로 바뀌는 버그가 나는데 `??`는
이 문제가 없음.

#### JSON.stringify / JSON.parse
네트워크로는 문자열만 오갈 수 있어서, JS 객체를 보낼 땐 문자열로 바꾸고(`stringify`), 받은 문자열은 다시
객체로 바꿔야(`parse`) 한다. `fetch`의 `body: JSON.stringify({...})`, `await response.json()`이 각각 이 두
동작 — `response.json()`은 내부적으로 `JSON.parse`를 해주는 편의 메서드.

---

# 2. React 핵심 개념

React에서 가장 크게 바뀌는 건 문법이 아니라 사고방식. Lesson 12에서 `btn.innerHTML = 'Finished'`처럼
"요소를 직접 찾아서 고쳤다"면, React는 "지금 상태가 이거니까 화면은 이렇게 생겨야 한다"고 **선언**만 하고,
실제로 DOM을 고치는 건 React가 알아서 한다.

#### 컴포넌트와 JSX
컴포넌트는 그냥 **화면 조각을 돌려주는 함수**. 함수 안에서 HTML처럼 생긴 걸 쓸 수 있는데 이게 JSX —
사실은 `React.createElement(...)` 호출로 변환되는 문법 설탕일 뿐이다.

```js
function Greeting() {
  return <h1>안녕, 감자몰</h1>;
}
```

> JSX는 `<div>`처럼 소문자로 시작하면 진짜 HTML 태그로, `<Greeting />`처럼 대문자로 시작하면 컴포넌트 함수
> 호출로 해석한다. 재사용 컴포넌트를 뺄 때는 `ProductCard`처럼 대문자로 시작해야 함.

#### props: 부모 → 자식으로 데이터 전달

```js
function ProductCard({ name, price }) {
  return (
    <div>
      <p>{name}</p>
      <p>{price.toLocaleString()}원</p>
    </div>
  );
}

// 사용하는 쪽
<ProductCard name="키보드" price={30000} />
```

props는 자바 메서드의 매개변수랑 똑같음 — 부모가 값을 넘겨주고, 자식은 읽기만 함(자바에서 파라미터로 받은 걸
멋대로 재할당 안 하는 것과 비슷한 규율).

#### state: useState
컴포넌트가 "기억"해야 하고, 바뀌면 화면도 같이 바뀌어야 하는 값. 일반 변수로는 안 됨 — 변수를 바꿔도 React는
그걸 모르고 화면을 다시 그리지 않음.

```js
const [orderId, setOrderId] = useState('');
//     ^값        ^값을 바꾸는 함수    ^초깃값

<input value={orderId} onChange={(e) => setOrderId(e.target.value)} />
```

`setOrderId(...)`를 호출하면: 다음 렌더링부터 `orderId`가 새 값이 되고, 그 컴포넌트가 **다시 실행**됨(=
리렌더링). `toss-test/page.tsx`의 `orderId`, `amount` state가 전부 이 패턴.

> state는 직접 수정 금지. `orderId.value = 'x'`처럼 직접 건드리면 React가 변경을 감지 못 해서 화면이 안
> 바뀐다. 항상 `setOrderId('x')`처럼 setter 함수를 통해서만 바꿔야 함 — 위 `...` 전개 연산자가 여기서 쓰이는
> 이유(객체/배열 state를 통째로 새로 만들어서 교체).

#### 선언형 렌더링 — DOM을 직접 안 만지는 이유
Lesson 12의 습관이 `btn.innerHTML = 'Loading...'`처럼 "요소를 찾아서 직접 바꾸기"였다면, React 컴포넌트
안에서는 이 방식을 쓰지 않는다. 대신 "로딩 중이라는 state가 있고, 그 state가 true면 이 문구가 보인다"고
조건부로 그린다.

| | 방식 |
|---|---|
| 바닐라 JS(명령형) | `btn.innerHTML = 'Loading...'` — "이렇게 해라"고 순서대로 지시 |
| React(선언형) | `{isLoading ? 'Loading...' : '전송'}` — "이 상태면 이 모습"이라고 결과만 정의 |

```js
const [isLoading, setIsLoading] = useState(false);

async function handleClick() {
  setIsLoading(true);
  await requestPayment();
  setIsLoading(false);
}

return <button onClick={handleClick}>{isLoading ? '처리 중...' : '결제하기'}</button>;
```

#### useEffect: 렌더링 바깥의 일
컴포넌트가 화면에 나타난 뒤에 한 번, 또는 특정 값이 바뀔 때마다 실행하고 싶은 코드(데이터 fetch, SDK 스크립트
로드 등)를 넣는 곳. 두 번째 인자인 의존성 배열이 실행 시점을 결정.

```js
useEffect(() => {
  // 컴포넌트가 처음 화면에 나타났을 때 딱 한 번만 실행
  const script = document.createElement('script');
  script.src = 'https://js.tosspayments.com/v1/payment';
  script.onload = () => setSdkReady(true);
  document.head.appendChild(script);
}, []);   // ← 빈 배열 = "처음 한 번만"
```

| 의존성 배열 | 실행 시점 |
|---|---|
| 없음 | 렌더링될 때마다 매번 (거의 안 씀, 무한루프 주의) |
| `[]` | 처음 화면에 나타났을 때 딱 한 번 |
| `[orderId]` | 처음 한 번 + `orderId`가 바뀔 때마다 |

`toss-test/page.tsx`의 Toss SDK 스크립트 로딩이 정확히 `[]` 패턴 — "이 페이지가 열렸을 때 딱 한 번, 결제
SDK를 불러와라."

#### 이벤트 핸들링
바닐라 JS의 `addEventListener('click', fn)`이 JSX 안에서는 `onClick={fn}` 속성으로 바뀐다. 소문자
`onclick="..."`(문자열)이 아니라 카멜케이스 `onClick`에 함수 자체(참조)를 넘긴다는 게 포인트.

```js
// 바닐라 JS
btn.addEventListener('click', () => { ... });

// React
<button onClick={() => { ... }}>클릭</button>
```

#### 리스트 렌더링과 key

```js
{cart.map(item => (
  <li key={item.cartItemId}>{item.name} x{item.quantity}</li>
))}
```

배열을 화면에 그릴 땐 거의 항상 `.map()`. `key`는 React가 "이전 목록과 지금 목록에서 어떤 항목이 같은
항목인지" 구분하는 이름표 — 배열 인덱스가 아니라 `cartItemId`, `productId`처럼 그 항목 고유의 값을 넣어야
순서가 바뀌거나 항목이 삭제될 때 엉뚱한 요소가 재사용되는 버그를 피할 수 있다.

#### 훅의 규칙
`useState`, `useEffect` 같은 "use"로 시작하는 함수를 **훅(Hook)** 이라 부른다. 규칙 두 개: 컴포넌트 함수의
**최상위**에서만 호출(if문/반복문/중첩 함수 안에서 호출 금지), **일반 함수가 아니라 컴포넌트 안에서만** 호출.
React가 훅을 호출된 "순서"로 추적하기 때문.

---

# 3. Next.js 동작 원리

React는 "컴포넌트를 어떻게 그리는가"만 다루고, 페이지 이동·서버 렌더링·빌드는 다루지 않는다. Next.js는 그
나머지 전부를 채워주는 프레임워크.

#### 왜 Next.js인가
React만으로 웹사이트를 만들려면 직접 짜야 하는 것들: URL과 화면을 연결하는 라우터, 검색엔진이 읽을 수 있게
서버에서 미리 HTML을 만드는 로직, 여러 파일을 브라우저가 이해할 하나의 번들로 합치는 빌드 도구, 이미지
최적화... Next.js는 이걸 전부 "규칙"으로 대신 처리해줌 — 특히 **폴더 구조 자체가 라우팅**이 되는 게 제일
큰 차이.

#### 파일 기반 라우팅 (App Router)
`src/app/` 아래의 폴더 구조가 그대로 URL이 된다.

| 파일 경로 | 실제 URL |
|---|---|
| `app/page.tsx` | `/` |
| `app/main/page.tsx` | `/main` |
| `app/signin/page.tsx` | `/signin` |
| `app/toss-test/page.tsx` | `/toss-test` |
| `app/toss-test/result/page.tsx` | `/toss-test/result` |

핵심 파일 세 가지 규칙:
- `page.tsx` — 그 경로의 실제 화면. 폴더에 이 파일이 있어야 그 경로가 접속 가능해짐.
- `layout.tsx` — 여러 페이지가 공유하는 뼈대(공통 헤더, 네비게이션 등). 하위 페이지들을 감싸는 틀이고,
  페이지를 옮겨다녀도 다시 렌더링되지 않아서 상태(예: 로그인 헤더)가 유지됨.
- `route.ts` — 화면이 아니라 API 엔드포인트.

동적인 값이 들어가는 경로는 대괄호로 표현: `app/products/[productId]/page.tsx`는 `/products/12`,
`/products/57` 같은 요청을 전부 받아주고, 페이지 컴포넌트가 `params.productId`로 값을 꺼내 씀.

#### Server Component vs Client Component ⭐ (가장 중요)
App Router의 가장 큰 패러다임. **기본값은 Server Component** — 아무 표시도 없으면 그 컴포넌트는 브라우저가
아니라 **서버(Node.js)에서 실행**된다.

| | Server Component (기본값) | Client Component (`'use client'`) |
|---|---|---|
| 실행 위치 | 서버에서만 | 브라우저에서 (첫 HTML은 서버가 만듦) |
| JS 번들 크기 | 브라우저로 코드가 안 나감 → 0 | 브라우저로 전송되는 JS에 포함됨 |
| useState/useEffect | 사용 불가 | 사용 가능 |
| onClick 등 이벤트 | 사용 불가 | 사용 가능 |
| 백엔드 직접 호출 | 컴포넌트를 async function으로 만들고 바로 await fetch(...) | useEffect나 이벤트 핸들러 안에서 fetch |

```js
// Server Component (기본값 — 'use client' 없음)
// 상품 목록처럼 "보여주기만" 하는 페이지에 적합
export default async function ProductListPage() {
  const res = await fetch('http://backend:8080/api/v1/products');
  const products = await res.json();

  return (
    <ul>
      {products.map(p => <li key={p.productId}>{p.name}</li>)}
    </ul>
  );
}
```

> 지금까지 만든 페이지는 전부 Client Component였다. `signin/page.tsx`, `main/page.tsx`,
> `toss-test/page.tsx` 모두 맨 윗줄이 `'use client';`. 이유는 명확함 — 입력 폼(useState), 클릭 이벤트, 결제
> SDK 로딩(useEffect)까지 전부 브라우저에서 상호작용이 필요한 페이지들이라 어쩔 수 없이 Client여야 했음.
> 근데 CORS 문제들(`allowCredentials`, `SecurityConfig`의 `.cors()` 누락)은 전부 **"브라우저에서 직접
> 백엔드를 호출"** 했기 때문에 생긴 것. 상품 목록처럼 순수하게 보여주기만 하는 페이지를 Server Component로
> 만들면, 서버끼리(Next.js 서버 ↔ Spring 서버) 통신이라 브라우저의 CORS 정책 자체가 적용 안 됨 — 이 문제군이
> 통째로 사라짐.

실전 판단 기준: 이 화면이 사용자 입력을 받거나(폼, 버튼), 클라이언트 상태를 들고 있거나(장바구니 담긴 개수
실시간 표시), 브라우저 전용 API(로컬스토리지, Toss SDK)가 필요하면 Client, 그냥 데이터를 불러와서 보여주기만
하면 Server. 한 페이지 안에서도 섞어 쓸 수 있음 — Server Component인 레이아웃 안에 Client Component인
"장바구니 담기 버튼"만 부분적으로 넣는 식으로.

#### 렌더링 전략: SSR · SSG · ISR · CSR
같은 질문 하나에 대한 네 가지 답 — "이 페이지의 HTML을 언제 만드는가?"

| 전략 | HTML을 만드는 시점 | 적합한 예 |
|---|---|---|
| SSG | 빌드할 때 미리 한 번 | 자주 안 바뀌는 상품 상세, 약관 페이지 |
| ISR | SSG처럼 미리 만들되, 일정 주기로 재생성 | 재고/가격이 가끔 바뀌는 상품 목록 |
| SSR | 요청이 올 때마다 서버에서 | 로그인한 사용자별로 다른 "내 주문 내역" |
| CSR | 브라우저에서 JS로 | 지금까지 만든 `'use client'` 페이지 대부분 |

Next.js가 이걸 대부분 **자동으로** 결정한다 — Server Component에서 `fetch`를 쓰면 Next.js가 그 페이지를
기본적으로 정적(SSG)으로 만들려 시도하고, 로그인 정보처럼 요청마다 달라지는 값을 쓰면 자동으로 SSR로 전환.
지금 단계에서는 "네 가지가 있고 선택은 대부분 자동"이라는 것만 알아두면 충분.

#### 데이터 페칭 패턴

| | Server Component | Client Component |
|---|---|---|
| 방법 | 컴포넌트를 async function으로 선언하고 바로 await | useEffect 안에서, 또는 이벤트 핸들러 안에서 |
| 로딩 상태 | Next.js의 `loading.tsx` 파일이 대신 처리 | 직접 `isLoading` state로 관리 |
| 지금 프로젝트 예 | 상품 목록/상세 페이지에 적용하면 좋음(아직 미작성) | `toss-test/result/page.tsx`의 "백엔드 결제 승인 호출" 버튼 |

#### 라우트 핸들러 (API Routes)
`app/api/hello/route.ts` 안에 `GET`, `POST` 같은 이름의 함수를 내보내면, 그 자체로 `/api/hello` API
엔드포인트가 된다. Next.js 서버가 Spring 백엔드와 브라우저 사이의 중간 서버 역할을 해야 할 때(예: 시크릿
키를 브라우저에 노출하지 않고 서버에서만 쓰고 싶을 때) 여기에 로직을 넣는다.

```js
// app/api/products/route.ts
export async function GET() {
  const res = await fetch('http://backend:8080/api/v1/products');
  const data = await res.json();
  return Response.json(data);
}
```

#### 미들웨어
프로젝트 루트의 `middleware.ts`에 정의하면, 지정한 경로로 오는 모든 요청이 실제 페이지에 도달하기 전에
먼저 실행된다. 로그인 안 한 사용자가 `/main`에 접근하면 `/signin`으로 돌려보내는 것 같은 전역 인증 체크에
주로 씀 — JWT 쿠키 유무를 여기서 검사할 수 있음.

#### 환경변수와 NEXT_PUBLIC_
`.env.local`에 넣은 값은 기본적으로 **서버에서만** 읽힌다(브라우저로 안 나감). 브라우저(Client Component)
에서도 써야 하는 값은 이름 앞에 `NEXT_PUBLIC_`을 붙여야 노출됨 — 반대로 말하면 이 접두사가 없는 값은
실수로라도 브라우저에 새 나가지 않는다는 뜻.

> `toss-test/page.tsx`에 `TOSS_CLIENT_KEY`를 파일에 그냥 문자열로 박아뒀는데, 테스트 클라이언트 키는 원래
> 공개돼도 되는 값이라 당장 문제는 없음. 정석대로 하면 `.env.local`에
> `NEXT_PUBLIC_TOSS_CLIENT_KEY=test_ck_...`로 넣고 코드에서는
> `process.env.NEXT_PUBLIC_TOSS_CLIENT_KEY`로 읽는 게 맞음 — 나중에 운영 키로 바꿀 때 코드를 안 건드리고
> 값만 교체할 수 있게.

#### dev · build · start, 그리고 Turbopack

| 명령어 | 역할 |
|---|---|
| `npm run dev` | 개발 서버. 코드 저장하면 브라우저가 바로 갱신(Hot Reload)됨. |
| `npm run build` | 배포용으로 최적화된 정적 파일·서버 번들을 생성. 타입 에러도 이때 걸러짐. |
| `npm run start` | `build`로 만든 결과물을 실제로 서빙 — 운영 환경에서 쓰는 명령. |

"Turbopack"은 Next.js의 새 번들러(여러 파일을 하나로 합치고 변환하는 도구) 이름 — 기존 Webpack보다 훨씬
빨라서 `npm run dev`의 기본값이 됨. 지금은 "빌드 속도를 담당하는 내부 도구" 정도로만 알아둬도 충분.

---

# 4. 내 코드에 적용해보기

#### 지금까지 짠 코드 다시 읽기
- **`signin/page.tsx`** — `'use client'` + 여러 개의 `useState`로 폼 입력을 관리하는 전형적인 Client
  Component. `handleSignIn`의 `async/await + try/catch`는 위에서 다룬 표준 fetch 패턴 그대로.
- **`main/page.tsx`** — 지금은 빈 뼈대. 상호작용이 필요 없는 부분(상품 목록 등)이 채워진다면 Server
  Component로 바꾸는 것도 고려해볼 만하지만, 로그인 버튼 같은 상호작용이 들어갈 걸 감안하면 Client로 유지하는
  게 자연스러움.
- **`toss-test/page.tsx`** — 결제 SDK를 `useEffect(() => {...}, [])`로 한 번만 로드하고, `orderId`/`amount`
  state를 폼으로 관리하는 Client Component. 브라우저 전용 SDK를 쓰는 만큼 Server Component로 바꿀 수 없는
  페이지의 좋은 예시.
- **`toss-test/result/page.tsx`** — `useSearchParams`로 URL 쿼리를 읽고(Toss가 돌려준 `paymentKey` 등),
  버튼 클릭 시 백엔드로 `fetch`. 이벤트 핸들러 안에서 데이터를 가져오는 Client Component 데이터 페칭의 예시.

#### 웹서버 구조 설계할 때 고려할 것
백엔드에 이미 있는 기능(회원가입/로그인, 상품, 장바구니, 주문, 결제)을 화면으로 옮길 때 각 페이지가
Server/Client 중 뭐가 자연스러운지 미리 가늠해두면 나중에 구조를 다시 짜는 일이 줄어든다.

| 페이지 | 자연스러운 선택 | 이유 |
|---|---|---|
| 상품 목록 / 상세 | Server Component | 보여주기만 함, 로그인 없이도 접근 가능, 서버-투-서버라 CORS 이슈 없음 |
| 로그인 / 회원가입 | Client Component | 폼 입력·검증·제출이 필요(이미 이렇게 돼 있음) |
| 장바구니 | Client Component | 수량 조절, 체크박스 선택 등 즉각적인 상호작용 필요 |
| 주문/결제 | Client Component | Toss SDK, 폼, 결제 상태 관리가 전부 브라우저 쪽 일 |
| 주문 내역 조회 | Server Component + 인증 | 로그인한 사용자만 보는 데이터라 SSR 성격이지만, 상호작용 없이 목록만 보여준다면 Server Component + 쿠키 전달로 구현 가능 |

공통 헤더(로그인 상태 표시, 장바구니 아이콘)는 `app/layout.tsx`에 두면 페이지를 옮겨다녀도 다시 그려지지
않아 상태가 자연스럽게 유지된다. 다음 단계로 실제 폴더 구조(`app/products`, `app/cart`, `app/orders`)와
백엔드 API를 감싸는 공용 fetch 함수부터 설계.

---
기준: 백엔드 `shopping-mall-api`와 `frontend/shopping-mall-web` 코드(2026-08-21 기준). 이후 실제로 페이지를
짜면서 막히는 부분이 생기면 그때그때 이어서 채운다.
