강의 : https://www.youtube.com/watch?v=G3e-cpL7ofc&list=PL3r6NYvHcxgVTIxCxTKP4O_dWF4ZnSm1q&index=1
*vs code IDE와 "live server" market place를 사용하면 보다 편하게 구현가능함.*
# HTML(Hiper Text Markup Language)

html은 문자열을 웹페이지에 순차적으로 띄우는 도구이다.

- HTML Element : button과 문자열(paragraph)와 같이 HTML을 구성하는 요소들로, 자신이 웹페이지에 넣고 싶은 기능을
- Syntax : HTML에 설정된 규칙으로, 이를 통해 위 HTML Element를 나열하고, 배치할 수 있게 한다. <>, </>내부에 어떤 HTML Element인지 종류를 정하며, 사이에 문자열을 끼워 넣어 해당 Element를 명명하게 만들어준다.
	- Tag : 
		- Open Tag :
		- Close Tag:
- HTML Attribute : 
- Indent : 없으면 가독성이 떨어짐

## HTML Structure

```html
<!DOCTYPE html>
<html>
	<head></head>
	<body></body>
</html>
```
모든 HTML 코드는 위와 같은 구성으로 한 웹 페이지를 구성한다.

이때 head는 title과 같은 웹의 제목 등의 정보가 들어가고, 
body는 눈에 보이는 모든 HTML Element가 존재한다.

즉 head는 title 혹은 css code들을 묶고, body는 눈에 직접적으로 보여지는 HTML Element를 묶음.

## HTML Element

#### button
버튼을 만들어 주는 이벤트
#### p
Paragraph, 문단이란 뜻으로 문장을 나열해 주는 이벤트
#### a
Anckor Element, 클릭시 다른 웹사이트로 연결해주는 하이퍼링크와 같은 역할

#### input(type, placeholder)
text와 같이 키보드 입력이 가능한 영역이다.

type을 통해 어떤 종류에 대한 입력을 받을 것인지, placehorder을 통해 입력 칸에 글을 적어놓을 수도 있다. 

| type                                                                       | 설명                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| [button](http://www.tcpschool.com/html-input-types/intro)                  | 클릭할 수 있는 버튼을 정의함.                                             |
| [checkbox](http://www.tcpschool.com/html-input-types/checkbox)             | 체크박스(checkbox)를 정의함.                                          |
| [color](http://www.tcpschool.com/html-input-types/color)                   | 색을 선택할 수 있는 입력 필드(color picker)를 정의함.                         |
| [date](http://www.tcpschool.com/html-input-types/date)                     | 날짜를 선택할 수 있는 입력 필드를 정의함. (year, month, day)                   |
| [datetime-local](http://www.tcpschool.com/html-input-types/datetime-local) | 날짜와 시간을 선택할 수 있는 입력 필드를 정의함. (year, month, day, hour, minute) |
| [email](http://www.tcpschool.com/html-input-types/email)                   | 이메일 주소를 입력할 수 있는 입력 필드를 정의함.                                  |
| [file](http://www.tcpschool.com/html-input-types/file)                     | 업로드할 파일을 선택할 수 있는 입력 필드와 “파일 선택” 버튼을 정의함.                     |
| [hidden](http://www.tcpschool.com/html-input-types/hidden)                 | 사용자에게는 보이지 않는 숨겨진 입력 필드를 정의함.                                 |
| [image](http://www.tcpschool.com/html-input-types/image)                   | 제출 버튼(submit button)으로 사용될 이미지를 정의함.                          |
| [month](http://www.tcpschool.com/html-input-types/month)                   | 날짜를 선택할 수 있는 입력 필드를 정의함. (year, month)                        |
| [number](http://www.tcpschool.com/html-input-types/number)                 | 숫자를 입력할 수 있는 입력 필드를 정의함.                                      |
| [password](http://www.tcpschool.com/html-input-types/password)             | 비밀번호를 입력할 수 있는 입력 필드를 정의함.                                    |
| [radio](http://www.tcpschool.com/html-input-types/radio)                   | 라디오 버튼(radio button)을 정의함.                                    |
| [range](http://www.tcpschool.com/html-input-types/range)                   | 슬라이드 바를 조정하여 범위 내의 숫자를 선택할 수 있는 입력 필드를 정의함.                   |
| [reset](http://www.tcpschool.com/html-input-types/reset)                   | 리셋 버튼(reset button)을 정의함.                                     |
| [search](http://www.tcpschool.com/html-input-types/search)                 | 검색어를 입력할 수 있는 텍스트 필드를 정의함.                                    |
| [submit](http://www.tcpschool.com/html-input-types/submit)                 | 제출 버튼(submit button)을 정의함.                                    |
| [tel](http://www.tcpschool.com/html-input-types/tel)                       | 전화번호를 입력할 수 있는 입력 필드를 정의함.                                    |
| [text](http://www.tcpschool.com/html-input-types/text)                     | type 속성의 기본값으로, 한 줄로 된 텍스트 필드를 정의함.                           |
| [time](http://www.tcpschool.com/html-input-types/time)                     | 시간을 선택할 수 있는 입력 필드를 정의함. (hour, minute)                       |
| [url](http://www.tcpschool.com/html-input-types/url)                       | URL 주소를 입력할 수 있는 입력 필드를 정의함.                                  |
| [week](http://www.tcpschool.com/html-input-types/week)                     | 날짜를 선택할 수 있는 입력 필드를 정의함. (year, week)                         |

#### Img
img는 이미지를 정해진 프레임 안에 넣어 화면에 출력해주는 Element으로, src를 통해 target image의 파일 경로를 정해준다.

#### link
앞선 방식에 따르면 html코드 내부에 style tag를 통해 css코드를 html내 파일에 구현했다. 이는 가독성을 해치므로, 따로 css파일에 빼줄 것인데, 이때 필요한 tag가 link tag이다. 이는 void tag로 close tag가 필요 없는 tag이다. 또한 html파일 내부에서 css파일을 연결하여 사용가능 하도록 만들어 준다.

- void tag : close tag가 필요 없는 tag

link tag는 두 가지 속성이 존재하는데 *rel*과 *href*이다.

- rel같은 경우 다음과 같은 속성값들이 들어갈 수 있다.

| 속성값          | 설명                                                                    |
| ------------ | --------------------------------------------------------------------- |
| alternate    | 프린트 페이지나 번역된 페이지와 같이 해당 문서의 대체 버전에 대한 링크를 제공함.                        |
| author       | 해당 문서의 저자에 대한 링크를 제공함.                                                |
| dns-prefetch | 브라우저가 대상 리소스의 원본에 대해 DNS 확인(DNS resolution) 작업을 미리 수행하도록 명시함.         |
| help         | 도움말 문서에 대한 링크를 제공함.                                                   |
| icon         | 사용자 인터페이스에서 해당 문서를 나타낼 리소스(일반적으로 아이콘)를 불러옴.                           |
| license      | 해당 문서의 저작권 정보에 대한 링크를 제공함.                                            |
| next         | 연관된 문서들의 모음 중 다음 문서에 대한 링크를 제공함.                                      |
| pingback     | 현재 문서에 대한 핑백(pingback)을 처리하는 핑백 서버의 주소를 제공함.                          |
| preconnect   | 브라우저가 대상 리소스의 원본에 미리 연결하도록 명시함.                                       |
| prefetch     | 사용자가 요청할 가능성이 있으므로, 브라우저가 대상 리소스를 미리 가져와 캐시(cache)하도록 명시함.            |
| preload      | 브라우저가 as 속성과 해당 대상과 관련된 우선순위에 따라 현재 탐색에 사용할 대상 리소스를 미리 가져와 캐시하도록 명시함. |
| prev         | 연관된 문서들의 모음 중 이전 문서에 대한 링크를 제공함.                                      |
| search       | 현재 문서 및 관련 페이지를 검색하는데 사용할 수 있는 리소스에 대한 링크를 제공함.                       |
| stylesheet   | 스타일 시트(stylesheet)로 사용할 외부 리소스를 불러옴.                                  |
- href는 연결할 파일을 넣어준다.

#### Div
Div는 틀을 짜는 Element이다. 가장 중요한 점은 Div내부에 어떤 HTML Element를 추가할 수 있다.

이에 가장 큰 장점은 Nested Layout을 만들 수 있다는 것이다.

예를 들어서 유튜브 동영상 목록이 3열로 같은 margin을 두고 나열 되어 있는 것을 확인할 수 있다. 그렇다면 div를 생성해서 하나의 동영상에 대한 정보(썸네일, 제목, 시간, 프로필, 기제 시간, 동영상 시간 등)을 한꺼번에 관리 및 복제 가능해진다.

일일이 설정해주는 것이 아니라 

# CSS(Cascading Style Sheets)

HTML Element의 외형을 바꾸게 됨

- CSS Selector : target HTML Element를 설정
- CSS Property : HTML Element의 어떤 부분을 수정할 것인지 지정
- CSS Value : 위 지정된 부분을 설정하는 값

*HTML Element의 요소는 매우 많으므로, 필요한 부분을 검색을 통해 찾는 것을 권장*

- Background-color
- color
- width
- height
등 다양한 HTML Element 내 요소를 수정가능.

이처럼 다양한 HTML Element 내 요소를 수정할 때, 어떤 부분을 수정해야 내가 원하는 방향으로 수정되는지 확인하기 힘든데, 이때 사용하면 좋은 도구가 *chrome devtools*이다.

#### Chrome Devtools
F11을 누르게 되면, 현재 화면에 출력된 페이지의 HTML, CSS 코드를 보여줄 것이다. 이때 마우스 포인팅 버튼을 누르게 되면 해당 HTML Element가 어떤 CSS코드로 이루어져 있는지 확인가능하다. 추가적으로 *CSS Box Model*또한 확인 가능하다.
- CSS Box Model : HTML Element가 화면에 출력될 때, 몇 픽셀만큼 어떤 요소로 갖고 있는지 확인가능하도록 만든 모델로, margin, border, padding등을 통해 화면 내 특정 구간을 차지하는 픽셀단위를 확인 가능

#### Hover, Active
HTML Element - Button에 클릭 동작을 넣고 싶다면 Hover을 통해 넣을 수 있다.

- pseudo class :
	- Hover : cursor을 HTML Element에 포인팅 했을 때, HTML Element의 요소를 바꿈
	- Active : cursor로 click했을 때, "

위 Hover, Active 동작은 내가 의도한 바처럼 매우 자연스럽게 동작하지 않을 것이다. 커서를 가져다 댔을 때, Button의 투명도(opacity)를 자연스럽게, 천천히 낮춰지도록 설정하고 싶으면 Transition을 사용해야 한다.

#### Transition
IDLE -> Hover -> Active 상태로 넘어갈 때 Transition을 설정하므로 내가 원하는 동작을 프레임별로 끊어 자연스럽게 넘어갈 수 있도록 만들어준다. 앞선 opacity 뿐만 아니라 Background-color, color등 다양한 변화에도 자연스럽게 동작 가능

#### Inline CSS
앞선 방식에 따르면 css를 통해 HTML Element의 속성을 변경하기 위해 style tag 속에서 pseudo class를 부여하여 해당 속성을 변경하는 방식을 사용해 왔다. 

하지만 HTML Element의 color만 변경할 때, 한 개의 속성만 변경하기 위해 따로 클래스를 빼는 방식은 매우 불편하다. 따라서 cpp inline function처럼 inline css를 통해 psuedo class를 통하지 않고 수정을 하도록 만들었다.
```html
<div sytle="
	background-color: blue;
	color: white;
"></div>
```

위 예제처럼 두 개 이상을 넣어도 무방하지만, 두 개 이상을 넣게 되면 가독성이 떨어지므로 상황에 맞게 사용하는 것을 권장한다.


## Display

#### block

#### inline

#### inline-block
#### Grid
위에서 Element의 대부분의 요소들은 구글링을 통해 찾아 변경하는 방식이 좋다고 언급하였는데, grid는 nested layout에서 중요한 포인트인 것 같아 언급이 필요하다.

Grid는 격자모양을 뜻하는 단어로 DB의 테이블처럼 열과 행이 나눠져 있다. display: grid를 통해 해당 Element를 grid로 만들기로 한다면, grid-template-column을 통해 열의 수를 정하고, block, inline-block처럼 딱딱한 방식으로 조정을 하는 것이 아닌, 열의 수만큼 해당 Element를 쪼개어 사용하게 만든다.

#### Flex
