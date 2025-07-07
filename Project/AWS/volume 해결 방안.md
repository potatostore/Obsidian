가장 먼저 인스턴스를 생성하였을때 시스템 디스크, 즉 root volume이 생성된다.

이는 인스턴스에 필요한 AMI의 정보를 저장하므로, 최소 한 개 이상의 volume이 인스턴스에 연결되어야 한다.

이를 인지하고 

1. 인스턴스 생성 : 루트 volume 또한 default로 생성된다.
2. volume에서 우리가 mount할 volume을 추가 (위 방식에서 volume에 이름을 붙여 구분하는 것을 추천)
3. 수업시간에 mount한 방식대로 mount 진행 -> /data내에 txt파일 생성
4. volume으로 가서 root volume이 아닌 mount volume으로 스냅샷 생성
5. 해당 스냅샷으로 volume 생성
6. volume을 두 번째 instance에 연결(이후 instance에 volume연결이 잘 되었는지 인스턴스-스토리지 가서 확인, root volume, copy volume 총 2개 존재)
7. 두 번째 instance에 가서 mount 진행(mount를 하지 않으면 volume이 붙어도 해당 volume 내 파일이 안열립니다.)
8. mount진행 후 /data가서 ls로 확인하면 기존에 만든 txt파일이 보이는 것을 확인할 수 있습니다.

-> 실시간 attach가 필요한 작업에는 부적합한 방식으로 EFS를 사용하거나, EBS Multi-Attach기능을 통해 volume하나에 최대 16개의 인스턴스를 붙일 수 있는데, 동기화 문제로 후자보단 전자를 택한다고 합니다.