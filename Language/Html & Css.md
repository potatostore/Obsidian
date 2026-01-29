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

# CSS(Cascading Style Sheets)

HTML Element의 외형을 바꾸게 됨

- CSS Selector : target HTML Element를 설정
- CSS Property : HTML Element의 어떤 부분을 수정할 것인지 지정
- CSS Value : 위 지정된 부분을 설정하는 값

*HTML Element의 요소는 매우 많으므로, 필요한 부분을 검색을 통해 찾는 것을 권장*

#### Hover, Active
HTML Element - Button에 클릭 동작을 넣고 싶다면 Hover을 통해 넣을 수 있다.

- pseudo class :
	- Hover : cursor을 HTML Element에 포인팅 했을 때, HTML Element의 요소를 바꿈
	- Active : cursor로 click했을 때, "

위 Hover, Active 동작은 내가 의도한 바처럼 매우 자연스럽게 동작하지 않을 것이다. 커서를 가져다 댔을 때, Button의 투명도(opacity)를 자연스럽게, 천천히 낮춰지도록 설정하고 싶으면 Transition을 사용해야 한다.

#### Transition
IDLE -> Hover -> Active 상태로 넘어갈 때 Transition을 설정하므로 내가 원하는 동작을 프레임별로 끊어 자연스럽게 넘어갈 수 있도록 만들어준다. 앞선 opacity 뿐만 아니라 Background-color, color등 다양한 변화에도 자연스럽게 동작 가능