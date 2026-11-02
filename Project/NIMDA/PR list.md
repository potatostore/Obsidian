# PR 내용
- [ ] url & table name 상수화
- [ ] 전역 예외 처리
- [ ] 컨트롤러 내부 예외 던지기 부분 삭제

# 하지 못한 내용
1. attachment - controller : download 메서드에서 호출 서비스가 get, createPresignedDownloadUrl 이 두 개인데, 차라리 service내부에 download 메서드를 만들어서 호출만 하는 방식이 좋아보임. 지금 시점에서 손대지는 않았음. 
2. board - controller : 위와 동일 내용이고, 이처럼 controller 내부에서 response dto를 만들거나, 예외를 직접 처리하는 문제들이 꽤 보임. → 일단 예외는 전역예외처리를 하면서 기존에 존재하는 서비스에 이관시키거나 했는데, 하지 못한 부분들은 대응되는 서비스 내 메서드가 없어서 이관을 못함.
3. filedownload service : 이게 위 2개의 문제 controller내부 구현을 claude 통해서 service로 이관시키는 코드를 작성해봤는데, 확인 요구.
4. DTO 네이밍 컨벤션
5. DTO 사용되지 않은 부분들에 DTO 사용(대부분 컨트롤러에 와일드카드를 사용하는 경우가 dto가 없는 경우임)
6. apiResponse : 이거 바꾸려고 했는데, front쪽에서 값을 X.[field]이런 식으로 한 코드들을 X.data.[field]이런식으로 다 바꿔야 되서, 일단은 건드린거 되돌린 상태
7. controller 내부 예외 던지는 문제 