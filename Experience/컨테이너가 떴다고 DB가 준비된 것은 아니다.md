---
tags:
  - seed
  - type/experience
aliases: []
created: 2026-09-25
---
# 컨테이너가 떴다고 DB가 준비된 것은 아니다

## 상황
- docker-compose로 MySQL과 서버를 띄웠는데, MySQL이 초기화를 하지 못해 응답을 받지 못하는 상태가 이어져서 고생했다 — [[ShoppingMall - 트러블 슈팅 기록]] 2026-08-19 주차 "docker"
- GitHub Actions를 설정할 때도, DB를 docker에서 빌드하더라도 아직 실행되지 않은 시점에 백엔드가 먼저 돌아갈 수 있다는 점을 고려해야 했다 — [[ShoppingMall - 트러블 슈팅 기록]] 2026-08-26 주차

## 한 일
- DB → 백엔드 순서로 실행되게 하고, 명령어로 DB 상태를 계속 확인해서 실행 중일 때만 다음 단계로 넘어가게 했다 — [[ShoppingMall - 트러블 슈팅 기록]] 2026-08-26 주차

## 배운 점
- 실행 순서만 정해서는 부족하다. "시작됨"과 "요청을 받을 준비가 됨"은 다른 상태다

## 참고
- (보충) Docker Compose에서는 DB 서비스에 `healthcheck`를 두고, 의존하는 서비스에 `depends_on: condition: service_healthy`를 걸면 같은 효과를 설정만으로 낼 수 있다

> [!info]- 🔗 위키 연결
> - 상위: [[경험]]
> - 개념: [[Docker]] · [[CI-CD(GitHub Actions)]]
> - 프로젝트: [[ShoppingMall - 트러블 슈팅 기록]]
