*Operating System Concepts라는 책과 OS학교 강의를 통해 배운 내용을 토대로 작성*

# OS
- User와 H/W의 상호작용을 위한 인터페이스
#### 기능 
1. UI : 컴퓨터의 H/W를 할당하거나, 관리하기 위한 상호작용을 제공하도록 만든 모든 인터페이스(CLI & GUI)
2. Program execution : 프로그램 실행
3. I/O operations : 입출력 필요시 I/O devices와의 소통을 제공
4. File-System manipulation : 파일시스템
5. Communication : 다른 컴퓨터와 network를 통해 
6. Error detection : 에러 감지
7. Resource allocation : 자원 할당
8. Logging : User의 어떤 프로그램이 어떤 resource를 사용했는지 확인
9. Protection and security : 보안 
-> 모든 기능들은 shell의 system call을 통해 OS에 명령할 수 있다.

- System call : OS의 기능들을 사용하기 위해 kernel에 접근하는데, 이때 kernel에 접근하기 위한 인터페이스

# Process
- 실행중인 프로그램, 메모리 내 프로그램들이 CPU에서 실행되기 위해 준비된 데이터들의 집합
#### Program을 구성하는 메모리 영역
1. Text section : program code
2. Stack section : program counter, 일시적인 데이터들, 즉 함수 내부 변수들이 저장된 영역
3. Data section : 전역변수
4. Heap section : 동적할당 변수
#### Process State(5 state)
- NEW : 방금 생성된 상태
- Running : cpu에 올라가 실행중인 Process
- Wating : I/O입출력 buffer을 기다리거나, 어떤 이벤트를 기다리는 상태
- Ready : Cpu에 올라가 실행될 준비가 끝난 상태로 OS의 scheduling을 통해 Running state로 변하며 실행됨
- Terminated : 실행이 끝난 상태
#### PCB
- Process Control Block : os가 process를 control하기 위해 필요한 모든 정보를 담고 있는 데이터 구조, process의 text section에 존재하는 명령어를 실행시킴, PC, RS와 같은 정보들도 담겨 이전 process context switching이 발생했을때 이전 process의 메모리 주소를 저장하거나, 다음 실행할 process의 정보를 담고있다.
#### Process Scheduling
- 많은 process를 관리하려는 목적
- Ready Queue : 실행 준비가 끝난 process들 저장
- Wait Queue : I/O event와 같은 이벤트들을 기다리는 process들 저장
#### Context Switching ++
- cpu core에서 다른 process를 실행하려고 할때, 이전 process를 저장하고, 새로운 process를 실행하는 작업
#### Process의 생성
1. fork() : 기존 process를 복제하여 자식 process를 생성.
2. exec() : 자식 process에게 생성하려는 Process에 대한 데이터를 덮어 씌움
exit()을 통해 process를 종료한다.

- cascading termination : 부모 process가 없을 시 자식 process 모두 종료
#### Process가 Memory를 사용하는 방식
- Personal allocated memory : 독립 시행 process는 각자 할당받은 메모리를 사용
- Shared Memory : 서로 협력하는 두 Process는 서로 접근 가능한 공유 메모리 사용

- InterProcess Communication(IPC) : cooperation process의 모델
	- Shared memory : moduler를 통해 in/out을 설정, in == out의 경우 buffer가 가득찬 로직과 빈 로직이 같은 문제 발생 -> in/out대신 count변수를 통해 해결 -> producer-consumer problem 발생
	- Message passing : send()와 receive()를 통해 중간 MailBox(buffer)에 데이터를 송수신 -> Mailbox에 동시 접근, producer-consumer problem 발생

각자 개인 메모리를 사용하는 경우, process별로 할당된 메모리를 사용하기에 동기화 문제가 발생하지 않지만, 공유 메모리를 사용하는 경우 문제가 발생할 수 있다. -> Producer-Consumer Problem

- Producer-Consumer Problem : 두 프로세스가 접근하는 동일 메모리에 발생하는 동기화 문제
	- 협력 동기화 문제: 버퍼가 가득 찼을때, 송신을 기다리고, 버퍼가 비었을때, 수신을 기다림 -> 정해진 스케줄을 보장하지 않는다. (Message Passing)
	- 경쟁 동기화 문제 : 데이터의 일관성이 깨지는 *Race Condition*발생

- 동기화 문제 해결방안 : Blocking 동기화
	- Blocking : send(), receive()흐름을 막아 협력 동기화를 보장
		- Blocking send : send()후 receive() 전까지 send()를 block.
		- Blocking receive : 반대
	- Non-Blocking : send(), receive()를 막지 않지만, 프로그래머에게 동기화를 위임
		- Non-Blocking send : blocking x
		- Non-Blocking receive : blocking x

# Thread
- Process 내 독립적인 흐름 단위
- Process의 일부분을 cpu의 독립시행 단위로 쪼갠 명령어
- Thread들이 Process내에서 공유 메모리(RS, PC)를 가지고 할당받은 작업 수행

#### Benefit
- Responsiveness : Block을 통해 한 Thread가 막혀도 다른 Thread가 실행됨 -> 반응성이 좋다.
- Resource sharing : process내 모든 자원 공유
- Economy : Process 생성 비용보다 싸고, context switching을 통해 다른 process를 실행하는 것보다 쌈
- Scalability : 병렬성, process단위로 한 코어에서 실행되는 것보다 process를 thread단위로 쪼개 여러 코어에서 실행시킬 수 있다.

#### Parallelism vs Concurrency
- Parallelism : 병렬성, 여러 코어에서 작업 실행
	- Data parallelism : 데이터를 쪼개 병렬 시행
	- Task parallelsim : 실행 흐름을 쪼개 병렬 시행
- Concurrency : 동시성, 한 코어에서 여러 작업 실행
- Amdahl's Law : 직렬처리로직이 많을수록 처리시간 증가
	- speed up <= $$ \frac{1}{S+\frac{1-S}{N}}$$
#### ULT vs KLT
- ULT : User Level Thread, PCB를 통해 Context switching이 이루어지며, Thread단위가 아닌 Process단위로 mapping -> kernel층에서 확인이 불가능하지만, Blocking시에 OS에서 Process단위로 Blocking이 발생하기에 반응성이 떨어진다.
- KLT : Kernel Level Thread, KLT는 TCB를 통해 Context switching이 이루어지며, Thread단위로 cpu에 실행된다. 
- Mapping : CPU에서 실행되는 주체는 결국 KLT, 즉 운영체제가 직접 관리하는 Thread이므로, 프로그램에서 생성되는 ULT는 결국 KLT로 Mapping을 통해 CPU에 실행되어야 함.
	- one-to-many : 여러 ULT가 KLT 하나로 Mapping이 발생하는데, 큰 의미가 없다 -> Mapping과정에서 하나의 KLT가 여러 ULT를 Mapping되는 것은 거의 불가능하여 One-to-One처럼 작동하기 때문.
	- many-to-many : 여러 KLT - 여러 ULT
	- one-to-ont : 한 KLT - 한 ULT

# CPU scheduling

- cpu에 어떤 process를 실행시킬 것인지 결정하는 과정
#### CPU scheduling이 필요한 이유
- CPU burst : cpu 연산 처리 시간
- I/O burst : I/O 처리 시간
- 대부분의 process는 cpu burst, I/O burst를 통해 process 총 처리 시간을 갖게 됨.
- 이때 I/O burst 동안 CPU가 놀게 된다 -> 비효율성을 CPU scheduling으로 커버

#### CPU scheduling이 발생하는 경우
1. running state -> waiting state : I/O event와 같은 상황
2. running state -> ready state : time slice와 같은 주어진 시간을 전부 소진한 경우
3. waiting state -> ready state : event가 끝나고, scheduling 기다릴 때.
4. process terminated

#### preemptive vs nonpreemptive
- preemptive scheduling : 시분할 시스템을 통해 어떤 process가 정해진 시간 이상 사용한 경우, 해당 process대신 다른 process를 cpu에서 작업시키기 위해 interrupt를 발생하는 과정
	- Race Condition
		- 각 프로세스는 독립된 메모리를 갖지만, kernel level에서 실행되는 process들은 서로 공유하는 메모리를 보유하고 있다.
		- 두 프로세스의 공유메모리가 존재하는 경우, interrupt로 인한 race condition이 발생할 수 있다.
- nonpreemptive scheduling : I/O event, process exit과 같은 event가 발생했을 경우에 interrupt를 통해 다른 process를 cpu에서 작업시키는 과정 -> resposivity가 떨어짐

#### Dispatcher
- dispatcher는 cpu의 제어권을 통해 process를 선택하고, cpu에 scheduling을 한다. -> context switching
- Dispatch latency : dispatcher가 위 기능을 실행하고, 다른 process가 cpu에서 실행되기까지 걸리는 시간

- 실행 단계
	1. scheduling이 발생하는 경우 1~4의 상황 발생
	2. 프로세스 끝에 다음과 같은 코드를 삽입
		1. Timer interrupt
		2. process yield
		3. I/O Block
		4. System call exit()
	3. scheduler 호출, context를 PCB에 저장
	4. 다음 Process 결정
	5. 해당 Process context 복원 -> 실행

#### scheduling 평가 척도
- CPU utilization : 단위시간당 많은 일을 했는가
- Throughtput : 처리량
- turnaround time : process 한 개 처리 후 돌아와 다음 process Run할 때까지 시간
- Waiting time : ready queue에서 기다린 시간
- Response time : 만들고 첫 실행까지 시간

## Scheduling Example

- Gantt Chart : Process를 동시성 처리하는 것처럼 막대바에 Process의 CPU brust time만큼 표시하여 1열로 세운 차트
#### Fist-Come, First-Served(FCFS) Scheduling
- P1 = 24,
- p2 = 3
- p3 = 3
만큼의 burst time이 발생할 때, 위 scheduling을 통해 
- P1 waiting time : 0
- P2 waiting time : 24
- P3 waiting time : 27
- AVG waiting time : 17

- Convoy Effect : burst time이 긴 process를 먼저 배치하고, 짧은 process 배치하면 AVG waiting time이 길어짐

#### Shortest-Job-Fisrt(SJF) Scheduling
- Convoy-Effect 해결 목적
- non-preemptive schedluing입장에서는 최적의 scheduling
- cpu burst를 예측할 수 없기에 정확하지 않음

#### Shortes-Job-Next(SJN) Scheduling
- CPU burst를 CPU에서 Process를 실제로 실행하기 전까지는 알 수 없다. -> 예측치를 통해 CPU burst를 정함
- EMA(Exponential Moving Average) : 최근 데이터에 가중치를 부여함으로서 cpu burst를 예측한다.
$$ τ_{n+1}=αtn​+(1−α)τn​ $$
#### Shortest-Job-Time-First(SJT) Scheduling
- 위 SJN을 preemptive scheduling에 적용한 방식
- I/O event, exit()으로만 scheduling을 하던 non-preemptive와는 달리 timer와 같은 시분할 시스템으로도 프로세스간의 scheduling이 발생하므로, preemptive에 맞는 scheduling이 필요함.
- 중간에 cpu burst가 더 짧은 process가 대기할 경우, scheduling.
- 즉 (예상 cpu burst time-cpu에서 작업한 시간)이 다음 process의 예측 cpu burst보다 클 경우, scheduling 발생.

#### Round-Robin(RR)
- quantum이라는 시간을 설정하여, 각 process별로 실행하는 시간을 정함.
- quantum만큼 시간이 지나면 다음 process로 context switching -> time slice
- Responsiveness를 높여주지만, 너무 작은 값을 quantum으로 설정할 경우, context switching 비용이 증가, scheduling overhead

#### Priority Scheduling
- 각 process별로 우선순위를 설정하고 우선순위 queue에 inqueue, 상위 우선순위의 process를 먼저, 동일 우선순위일경우 Round-Robin을 통해 scheduling
- 특정 process만 실행되고, 하위 우선순위 process는 실행이 안되는 starvation 발생 -> Aging을 통해 오래 기다린 process는 우선순위를 높여버려 문제 해결
---
#### Multilevel Queue
- 우선순위별로 queue를 분류하고, 각 우선순위에 맞는 queue에 ready state process를 inqueue -> 여러 개의 priority queue에 inqueue.

#### Multilevel Feedback Queue
- Multilevel Queue를 구현하는데, 시간에 따라 우선순위가 증가하거나 감소하면서 다른 priority queue로 이동할 수 있음 -> starvation해결
- quantum을 다르게 설정한 RR queue 여러 개를 병렬로 연결하고, 마지막에 FCFS queue를 등록하여 starvation문제와 Synchronization문제를 해결하는 등 다양한 방식으로 사용될 수 있음

# Synchronization Tools
- Synchronization Problem : Race condition, Producer-Consumer Problem
- Process creation할 때, fork()와 exec()를 통해 발생하는데, fork()하면서 자식 process에게 PID를 부여하게 됨. -> 이때 PID는 kernel level에서 모든 process가 공용으로 사용하는 메모리에 할당되어 있기에 두개 이상의 프로세스가 동시에 fork()시에 Race condition 발생할 수 있음. -> PID를 critical section으로 분류

#### Section
- Critical Section : kernel층의 공유메모리처럼 다수가 동시에 접근가능한 영역
- Entry Section : Critical Section에 진입하기 위해 순서를 정하는 영역
- Exit Section : Critiacal Section을 탈출하는 영역
- Remainder Section : 위 3개를 제외한 나머지 영역

#### Critical Section Problem
- 결국 다수의 Process가 Critical Section에 접근하는 동기화 문제가 발생 가능함.
- 따라서 다음과 같은 조건으로 해결을 하려 시도
	1. Mutual Exclusion : 한쪽 접근시 다른 한쪽 막기
	2. Progress : process의 진행흐름 보장
	3. Bounded Waiting : 무한히 Wait(starvation) 방지하기 위해 Bounded time 설정
-> 위 3개의 조건 충족시 Critical Section Problem 해결

#### Interrupt-based Solution 
- Critical section problem의 해결방안으로 entry section에서 critical section에 들어갈 process가 정해질 경우, 모든 process의 interrupt를 막음 -> 이후 들어간 process가 exit section으로 나올 때 다시 interrupt를 푼다.
- 위 3개의 조건 중 1번은 만족하지만, 2,3번은 만족하지 않음 -> Timer interrupt와 같이 time slice를 통해 progress를 보장해주는 시스템을 막았고, exit section으로 나온 process가 다시 entry section에 들어가 계속 critical section에 진입할 경우, starvation도 해결하지 못하기 때문이다.
#### Peterson's Solution
- turn, flag변수를 통해 critical section에 진입할 process를 선택
	- turn : 어떤 process가 critical section에 들어갈지 알려주는 변수
	- flag : process가 critical section에 들어갈 준비가 되었는지 알려주는 변수
- single-thread 상황에서는 괜찮지만, multi-thread 상황에서 reorderring(cpu가 효율성을 위해 코드를 순서를 바꿔서 실행)으로 인하여 원하는 결과가 나오지 않을 가능성이 존재한다.

#### Memory Barrier
- Peterson's Solution이 Multi thread환경에서 정상적으로 작동하지 않을 가능성 때문에 Memory Barrier 개념 등장
- Reorderring을 막는 용도로 사용
- Cache에 쓴 데이터를 Reorderring하지 않고 순서대로 진입할 수 있도록 대기 -> cpu avg wait time증가

## Synchronization H/W
- 앞선 critical section condition 3개를 충족시키기 위해 소프트웨어적인 동기화를 제공하였지만, cpu avg wait time이 증가하는 등 다양한 추가적인 문제가 발생함 -> 이를 하드웨어 차원에서 막고자 시도

### Hardware Instructions
- 하드웨어적 차원에서 동기화 문제의 해결책을 제시, 함수와 같은 형태
#### Test-and-Set instruction
- critical section에 들어갈 수 있는지 판단하는 공유 변수 lock을 설정하고, test_and_set(&lock) == false인 경우, 해당 process가 critical section에 접근할 수 있도록 한다.
- 위 설명대로라면 공유변수 lock에 멀티 프로세서로 인해 동시에 접근하게 될 경우, race condition이 무조건 발생할 것으로 보이는데, 이를 H/W차원에서 막는 Atomicity(원자성)을 제공 -> 즉 하드웨어적인 중재로 둘 중 하나의 process만 lock에 접근할 수 있는 권한을 부여하고, 나머지는 대기. -> Race condition 해결.
- 하지만 3번 조건, Bounded Waiting을 막지는 못함 -> time slice가 따로 없어 한 process만 접근할 수 있다.(Starvation)
#### Compare-and-Swap instruction
- lock과 예측값을 비교하고, 같으면 새 값으로 덮어 씌우고, 참 반환, 다르면 거짓 반환하고 종료.
- 예측값이 bool로 반환되는 것이 아닌, int로 반환되므로 상대적으로 매우 유연하다.
- 그럼에도 bound wait을 해결하지 못하였다.
->waiting queue를 도입하여 lock에 해당하는 process가 waiting queue에 존재할 경우, 실행해주도록 만들었다

### Atomic Variables
- 통상적으로 앞서 설명한 H/W instructions는 다른 코드 블럭과 함께 동기화 도구로 사용됨. -> 단일로 동기화를 이룰 수 없음

# Synchronization Problem and Solution

#### Bounded-Buffer Problem

#### Readers and Writers Problem

#### Dining-Philosoper Probelm
