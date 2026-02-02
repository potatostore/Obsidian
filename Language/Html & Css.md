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
## HTML Element

#### button
버튼을 만들어 주는 이벤트
#### p
Paragraph, 문단이란 뜻으로 문장을 나열해 주는 이벤트
#### a
Anckor Element, 클릭시 다른 웹사이트로 연결해주는 하이퍼링크와 같은 역할

#### input(type, placeholder)
text와 같이 키보드 입력이 가능한 영역이다.

type을 통해 박스, 
placehorder을 통해 입력 칸에 글을 적어놓을 수도 있다. 

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