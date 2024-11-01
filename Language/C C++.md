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
		- 1개의 process가 여러 thread를 조작함 -> multi-threading

<span style="color:rgb(0, 176, 80)">High level</span>  <span style="color:rgb(255, 0, 0)">User</span>   Process, Thread, Debugger

--- 
		   <span style="color:rgb(255, 0, 0)">Kernel</span>    Driver, Os, 

--- 
<span style="color:rgb(0, 176, 80)">Low level </span>  <span style="color:rgb(255, 0, 0)">H/W</span>   Device, monitor etc...


I/O는 기본적으로 장치로부터 입력을 받거나, 장치에 전기신호를 통해 출력을 하는 형태이다. 따라서 H/W에 직접적으로 간여할 수 있는 Kernel S/W에 I/O가 해당된다고 볼 수 있다. 

또한 H/W에 신호를 주고 받을 수 있는 Kernel과는 달리 User는 Kernel에 직접적으로 신호를 줄 수 없다. 따라서 file을 통해 kernel에 접근하게 되는데, 이때 우리가 User층에서 출력문을 실행하면, file이 변경되어 모니터로 확인이 되기에 I/O가 마치 User층에서 실행되는 것처럼 보이기에 혼동된다고 볼 수 있다. 

file을 작성하기 위해 정보나 규칙을 정해놓는데, 이를 Protocol이라고 한다.

그리고 이 Protocol에 맞추어 일일이 작성하는 것을 지양하고자 getchar(), putchar()와 같은 I/O함수들이 탄생했다고 볼 수 있다.

- Buffer : Memory의 일종으로 데이터를 일시적으로 저장하는 공간으로 생각하면 쉽다. buffer은 user층, kernel층 모두에 해당하는데 이는 프로세스, file, os등 모든 user, kernel층이 일시적으로 갖을 수 있다. 각각의 역할에 따라 buffer의 쓰임새가 다른데, 만약 데이터 송수신이 발생했을 때, 수신속도보다 송신속도가 빠를경우, 송신이 일시적으로 매끄럽게 이루어지지 않아 데이터가 마치 끊기는 듯한 현상이 발생하는데, 이를 ==Buffering==이라고 한다.

Buffer의 개념에 대해 짚고 넘어간 이유는 c언어의 getchar(), scanf(), gets()등의 input fucntion들은 키보드를 통한 하드웨어 인터럽트가 발생을 하면, 이 데이터들이 file의 read buffer에 일시적으로 쌓이게 되는데, 이때문에 c언어의 I/O을 ==Buffered I/O==라고 한다.

- Read Buffer가 쌓이는 과정
	1. H/W에 하드웨어 인터럽트 발생
	2. kernel층의 console이 이벤트 신호를 받아 console을 추상화한 file에 신호를 넘김
	3. file은 이를 read buffer에 쌓음

- 궁금증
	1. thread는 유저층이고, core는 하드웨어층인데, core를 어떻게 thread가 간접적으로 밑에서 도와줄까?


1. 이것은 우리가 직관적으로 봤을 때 코어 바로 밑에 쓰레드가 존재하여 도와주는 것처럼 보이지만, 실상은 다음과 같다.
	1. 입력, 출력 등 컴퓨터가 연산해야하는 행위가 발생한다.
	2. 하드웨어층에서 ==하드웨어 인터럽트==를 통해 커널로 신호를 보낸다.
	3. 커널층에서 이를 받고, 인터럽트를 처리하여 유저층에 있는 프로세스에 전달을 해야하는데 이 과정을 ==커널의 인터럽트 처리 루틴== 이라고 한다.
	4. 인터럽트 처리 루틴 이후 프로세스에 이벤트를 넘겨주면, 프로세스가 이에 대해 판단을 하여 자원 및 연산 요청을 커널층으로 보낸다. 이를 ==시스템 호출 (System Call)==이라고 한다.
	5. 커널에 존재하는 ==스케줄러(scheduler)==가 이를 받아 해당 프로세스의 스레드가 어떤 코어에서 실행할지 결정한다. 
	- 결론적으로 위 과정을 통해 프로세스 내에 존재하는 스레드가 코어에 할당받아 연산을 실행하는 것이므로 코어 밑에 스레드가 작동을 한다고 볼 수 있는 것이다.

어느정도의 기본적인 컴퓨터과학 지식을 이해했으니 I/O에 대해 배워보자

- Input : 