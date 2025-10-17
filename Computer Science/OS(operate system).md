*Operating System Concepts라는 책과 OS학교 강의를 통해 배운 내용을 토대로 작성*

# OS
- User와 H/W의 상호작용을 위한 인터페이스
- 기능 
	1. UI : 컴퓨터의 H/W를 할당하거나, 관리하기 위한 상호작용을 제공하도록 만든 모든 인터페이스(CLI)
	2. Program execution : 프로그램 실행
	3. I/O operations : 입출력 필요시 I/O devices와의 소통을 제공
	4. File-System manipulation : 파일시스템
	5. Communication : 다른 컴퓨터와 network를 통해 
	6. Error detection : 에러 감지
	7. Resource allocation : 자원 할당
	8. Logging : User의 어떤 프로그램이 어떤 resource를 사용했는지 확인
	9. Protection and security : 보안 
	-> 모든 기능들은 shell의 system call을 통해 OS에 명령할 수 있다.