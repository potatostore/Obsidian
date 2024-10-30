# [[1. 전처리기]]

.c와 .h, 즉 소스코드와 헤더파일은 정의를 하냐, 선언을 하냐에 따라 차이를 나눌 수 있다.

# [[2. 자료형]]

- 상수 : ASCII, UNI 등의 부호체제가 존재함
	- 리터럴 : 숫자
	- 심볼릭 : 문자
	- #부호체계 : 일정 수의 나열을 문자로 인식하는 약속 (ASCII, UNI etc...), 0x3c를 해당하는 문자로 바꾸어 입출력함.
- 변수 : 우리가 아는 변수들 (char, int, long, long long int, float, double ...)

*변수사용시 주의점*
- 메모리 관리 주의 : 각 자료형의 사용되는 메모리를 정확하게 이해하고, 특히 문자열같은 경우 마지막에 '\n'을 위해 한자리가 소모된다는 점을 망각하면 memory overflow가 발생.

# [[3.I/O]]

- 입출력을 정확하게 이해하기 위해 컴퓨터용어 및 구성을 이해해야함.
	- Computer
		- H/W : 다양한 컴퓨터 장치들이 구성을 이룸
		- S/W : 크게 두 개의 층이 존재하는데, User, Kernel층이 존재함
			- User : 개인이 컨트롤할 수 있는 영역으로 process, debugger, file등이 존재함.
				- Debbuger : 다른 process에 접근할 수 있는 유일한 process로 이를 통해 해킹과 같은 
				- Process : 특정 기능을 수행하기 위해 메모리 등의 컴퓨터 자원을 할당 받아 독립적으로 실행되는 단위
				- Thread : Process내에서 특정 기능을 수행하기 위한 실행 단위
			- kernel : S/W 조작을 위해 장치에 신호를 주거나 받는 영역.
		- 1개의 os가 여러 process를 조작함 -> multi-tasking
		- 1개의 process가 여러 thread를 조작함 -> multi-thread

<span style="color:rgb(0, 176, 80)">High level</span>  <span style="color:rgb(255, 0, 0)">User</span>   Process, Thread, Debugger

--- 
		   <span style="color:rgb(255, 0, 0)">Kernel</span>    Driver, Os, 

--- 
<span style="color:rgb(0, 176, 80)">Low level </span>  <span style="color:rgb(255, 0, 0)">H/W</span>   Device, monitor etc...


I/O는 기본적으로 장치로부터 입력을 받거나, 장치에 전기신호를 통해 출력을 하는 형태이다. 따라서 H/W에 직접적으로 간여할 수 있는 Kernel S/W에 I/O가 해당된다고 볼 수 있다. 

또한 H/W에 신호를 주고 받을 수 있는 Kernel과는 달리 User는 Kernel에 직접적으로 신호를 줄 수 없다. 따라서 file을 통해 kernel에 접근하게 되는데, 이때 우리가 User층에서 출력문을 실행하면, file이 변경되어 모니터로 확인이 되기에 I/O가 마치 User층에서 실행되는 것처럼 보이기에 혼동된다고 볼 수 있다. 

file을 작성하기 위해 정보나 규칙을 정해놓는데, 이를 Protocol이라고 한다.

그리고 이 Protocol에 맞추어 일일이 작성하는 것을 지양하고자 getchar(), putchar()와 같은 I/O함수들이 탄생했다고 볼 수 있다.

- 궁금증
	1. thread는 유저층이고, core는 하드웨어층인데, core를 어떻게 thread가 간접적으로 밑에서 도와줄까?


1. 