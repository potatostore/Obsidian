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
5. 

#### Process State(5 state)
- NEW : 방금 생성된 상태
- Running : cpu에 올라가 실행중인 Process
- Wating : I/O입출력 buffer을 기다리거나, 어떤 이벤트를 기다리는 상태
- Ready : Cpu에 올라가 실행될 준비가 끝난 상태로 OS의 scheduling을 통해 Running state로 변하며 실행됨
- Terminated : 실행이 끝난 상태

