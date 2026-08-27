---
tags:
  - seed
aliases: []
created: 2026-08-22
---

Kubernetes(k8s)는 "여러 대의 서버에 걸쳐서 수많은 컨테이너를 어떻게 배치하고, 장애가 나면 어떻게 자동으로 복구하고, 트래픽이 몰리면 어떻게 자동으로 늘릴 것인가"를 대신 관리해주는 *컨테이너 오케스트레이션(orchestration)* 도구다. [[Docker]]가 "컨테이너 하나를 어떻게 잘 만들고 실행할 것인가"를 다룬다면, Kubernetes는 "그 컨테이너들을 대규모로, 안정적으로 운영하는 방법"을 다룬다.

# 0. Docker Compose로는 왜 부족한가 (필요성)
[[Docker]] 노트에서 다룬 Docker Compose는 *한 대의 컴퓨터(host)* 안에서 여러 컨테이너를 관리하는 도구다. 지금 이 프로젝트 규모(개인 프로젝트, 서버 한 대)에서는 사실 Docker Compose만으로도 충분하다 — 이 점을 먼저 솔직하게 짚고 가는 게 중요하다 (관련 내용은 맨 아래 9번 참고).

하지만 다음과 같은 상황이 되면 한 대의 컴퓨터로는 한계에 부딪힌다.

1. *서버 한 대가 감당 못 할 트래픽* — 서버(노드)를 여러 대로 늘려야 하는데, Docker Compose는 애초에 "여러 대의 서버에 컨테이너를 자동으로 나눠 배치"하는 기능이 없다 (한 대의 host를 벗어나지 못함).
2. *장애 자동 복구* — Docker Compose로 띄운 컨테이너가 죽으면 restart: always로 재시작 정도는 되지만, "이 컨테이너가 떠있던 서버 자체가 죽었을 때 다른 서버에서 대신 띄워준다"는 건 안 된다.
3. *무중단 배포(Rolling Update)* — 새 버전을 배포할 때 기존 컨테이너를 다 내리고 새로 올리면 그 사이 서비스가 끊긴다. 하나씩 순서대로 바꿔가면서 끊김 없이 배포하려면 이를 관리해주는 컨트롤러가 필요하다.
4. *오토스케일링* — 트래픽에 따라 컨테이너 개수를 자동으로 늘리고 줄이는 것.

Kubernetes는 이 네 가지를 *여러 대의 서버(클러스터)를 하나의 논리적인 컴퓨팅 자원 풀처럼 다루면서* 자동으로 해결해준다.

# 1. 핵심 원리 — 선언적(Declarative) 관리와 제어 루프
Kubernetes를 이해하는 데 가장 중요한 개념이 이것이다: *"어떻게 하라"가 아니라 "어떤 상태가 되어야 하는가"를 선언한다.*

- Docker Compose나 우리가 지금까지 하던 방식은 *명령형(imperative)* 이다 — "이 컨테이너를 띄워라", "저 컨테이너를 지워라"처럼 *행동*을 하나씩 지시한다.
- Kubernetes는 *선언형(declarative)* 이다 — "이 애플리케이션의 Pod가 항상 3개 떠있어야 한다"는 *원하는 최종 상태(desired state)* 만 YAML로 선언해두면, Kubernetes가 알아서 "지금 몇 개가 떠있는지 확인하고, 부족하면 띄우고, 넘치면 줄이는" 일을 계속 반복한다.

이 뒤에서 실제로 동작하는 원리가 *제어 루프(Control Loop / Reconciliation Loop)* 다. 이건 사실 순수 컴퓨터공학이라기보단 *제어공학(control theory)의 피드백 루프*와 정확히 같은 발상이다.

```
반복(무한 루프):
    현재 상태 관측 (Observe)   — 지금 Pod가 몇 개 떠있나?
    원하는 상태와 비교 (Diff)   — YAML에 선언된 개수(3개)와 다른가?
    차이를 좁히는 행동 (Act)    — 부족하면 Pod를 새로 만들고, 넘치면 지운다
```

이 루프를 담당하는 게 뒤에서 설명할 *Controller Manager*다. 사람이 "이렇게 해라"를 매번 지시하는 게 아니라, *시스템이 스스로 목표 상태로 수렴하도록* 만드는 것 — 이게 Kubernetes 전체를 관통하는 설계 철학이다. (온도조절기가 "목표 온도"만 설정해두면 알아서 히터를 켜고 끄는 것과 완전히 같은 구조라고 생각하면 이해가 빠르다.)

# 2. 아키텍처 — Control Plane과 Node
Kubernetes 클러스터는 크게 두 종류의 서버로 구성된다.

## 2-1. Control Plane (관제탑 — 클러스터를 관리하는 두뇌)
- *API Server*: 모든 요청(내가 kubectl로 보내는 명령, 다른 컴포넌트들끼리의 통신)이 반드시 거쳐가는 유일한 창구. "이 클러스터의 상태를 바꾸고 싶으면 무조건 API Server를 통해야 한다."
- *etcd*: 클러스터의 모든 상태(어떤 Pod가 몇 개 있어야 하는지, 지금 어디에 떠있는지 등)를 저장하는 *분산 key-value 저장소*. Kubernetes의 "기억"에 해당하는 부분이다.
- *Scheduler*: 새로 만들어야 할 Pod를 *어느 노드에 배치할지* 결정한다 (그 노드의 남은 CPU/메모리, 배치 제약조건 등을 고려).
- *Controller Manager*: 위 1번에서 설명한 제어 루프를 실제로 계속 돌리는 주체. "Deployment가 Pod 3개를 요구하는데 지금 2개면 하나 더 만들어라" 같은 판단을 여기서 한다.

## 2-2. Node (실제로 컨테이너가 돌아가는 서버들, Worker Node)
- *kubelet*: 각 노드에서 돌아가는 에이전트. Control Plane(API Server)의 지시를 받아 "이 노드에 이 Pod를 실제로 띄워라"를 수행하고, 컨테이너 런타임(Docker/containerd)에게 실제 실행을 맡긴다.
- *kube-proxy*: 노드의 네트워크 규칙을 관리해서, 뒤에서 설명할 Service로 들어온 트래픽이 올바른 Pod로 전달되도록 라우팅해준다.
- *Container Runtime*: 실제로 컨테이너를 실행하는 소프트웨어. Docker 엔진 자체이거나, 요즘은 더 가벼운 containerd를 직접 쓰는 경우가 많다 (Docker Desktop 안에도 사실 containerd가 들어있다).

```
[Control Plane]                         [Node 1]           [Node 2]
 API Server ── etcd                      kubelet             kubelet
     │                                   kube-proxy          kube-proxy
 Scheduler                               containerd          containerd
 Controller Manager                      Pod, Pod, ...       Pod, Pod, ...
```

# 3. Pod — 컨테이너가 아니라 왜 "Pod"인가
Kubernetes가 다루는 가장 작은 배포 단위는 컨테이너가 아니라 *Pod*다. Pod는 *하나 이상의 컨테이너를 묶은 것*인데, 그 안의 컨테이너들은 다음을 공유한다.

- *같은 네트워크 네임스페이스* — 같은 Pod 안의 컨테이너들은 localhost로 서로 통신 가능하고, IP 주소도 하나만 갖는다.
- *같은 Volume* — 파일을 공유할 수 있다.

왜 컨테이너 하나로 안 끝내고 굳이 이런 묶음을 만드냐면, *사이드카 패턴(sidecar pattern)* 때문이다 — 예를 들어 메인 애플리케이션 컨테이너 옆에 로그를 수집해서 외부로 전송하는 컨테이너를 하나 더 붙이고 싶을 때, 이 둘을 "논리적으로 하나의 배포 단위"로 묶어서 항상 같이 뜨고 같이 죽게 만드는 게 Pod다. (지금 이 프로젝트처럼 백엔드 하나만 있는 단순한 경우는 Pod 안에 컨테이너 하나만 있는 게 보통이다.)

*Pod는 휘발성이다* — Pod가 재시작되면 새로운 IP를 받는다. 그래서 "이 Pod의 IP로 직접 접속"하는 방식은 안 쓰고, 다음에 설명할 Service를 거친다.

# 4. Deployment / ReplicaSet — 원하는 개수 유지 + 무중단 배포
- *ReplicaSet*: "이 Pod가 항상 N개 떠있어야 한다"만 담당하는 컨트롤러. 1번에서 설명한 제어 루프의 가장 단순한 예시 — Pod가 죽으면(N개 미만이 되면) 즉시 새 Pod를 만들어서 다시 N개를 채운다.
- *Deployment*: ReplicaSet을 한 단계 더 감싸서, *버전 업데이트(롤링 업데이트)* 를 관리한다. 새 버전을 배포하면:
  1. 새 버전의 Pod를 하나씩 추가로 띄우고
  2. 그게 정상 동작(readiness) 확인되면 구버전 Pod를 하나씩 내린다
  3. 이 과정을 전체 Pod가 교체될 때까지 반복

이 방식 덕분에 *배포 도중에도 항상 일정 개수 이상의 Pod가 요청을 처리할 수 있는 상태를 유지* — 이게 "무중단 배포"의 실제 구현 원리다. (지금 이 프로젝트에서는 IntelliJ로 서버를 내렸다가 다시 켜는 동안 서비스가 완전히 끊기는데, Deployment는 이 끊김을 없앤다.)

문제가 생기면 이전 버전으로 *롤백*하는 것도 (kubectl rollout undo) 이전 ReplicaSet을 다시 늘리고 현재 것을 줄이는 것뿐이라 원리는 동일하다.

# 5. Service — Pod의 휘발성 IP 문제 해결
Pod는 재시작될 때마다 IP가 바뀐다. 그런데 프론트엔드가 백엔드 API를 호출할 때마다 "지금 IP가 뭐지?"를 매번 확인할 수는 없다. *Service*는 여러 개의(그리고 계속 바뀌는) Pod들 앞에 놓이는 *안정적인 가상 IP/DNS 이름*을 제공하는 추상화 계층이다.

- Service는 label selector로 "이 라벨을 가진 Pod들"을 대상으로 지정하고, 그 Pod들에게 트래픽을 *로드밸런싱*해서 분산한다.
- Pod가 죽고 새로 뜨든, 개수가 늘든 줄든 Service의 이름/IP는 그대로 유지된다 — 이게 Service의 핵심 가치.

Service의 종류:

| 타입 | 설명 |
|---|---|
| ClusterIP (기본값) | 클러스터 *내부에서만* 접근 가능한 가상 IP. 백엔드↔DB처럼 내부 통신용. |
| NodePort | 각 노드의 특정 포트를 열어서 클러스터 *외부*에서도 접근 가능하게 함. |
| LoadBalancer | 클라우드(AWS/GCP 등)의 실제 로드밸런서를 자동으로 프로비저닝해서 외부 트래픽을 받음. 실무에서 외부 노출용으로 가장 많이 씀. |

# 6. ConfigMap / Secret — 설정과 코드의 분리
[[Docker]]에서 environment:로 환경변수를 주입했던 것과 같은 문제의식이다 — 설정값(DB 주소, 포트 등)과 민감정보(비밀번호, API 키)를 이미지 안에 하드코딩하지 않고 외부에서 주입한다.

- *ConfigMap*: 민감하지 않은 설정값(예: SPRING_PROFILES_ACTIVE=prod)을 담는다.
- *Secret*: 민감한 값(DB 비밀번호, JWT 시크릿 키 등)을 담는다. 기본적으로 base64로 인코딩되어 저장되는데, *이건 암호화가 아니라 인코딩이라 그 자체로는 안전하지 않다* — 실무에서는 etcd 저장 시 암호화(encryption at rest) 옵션을 켜거나, Vault 같은 외부 시크릿 관리 도구와 연동한다.

이 둘 다 YAML로 정의해두고, Pod의 env 또는 파일로 마운트해서 컨테이너에 주입한다. 원리적으로 CI/CD 노트의 GitHub Secrets와 정확히 같은 목적(설정과 코드의 분리, 민감정보의 안전한 주입)을 클러스터 레벨에서 하는 것이다.

# 7. YAML 매니페스트 작성법
Kubernetes의 모든 리소스는 아래 4가지 최상위 필드를 공통으로 갖는다.

```yaml
apiVersion: apps/v1     # 어떤 버전의 API를 쓸지 (리소스 종류마다 다름)
kind: Deployment         # 무슨 종류의 리소스인지 (Pod, Deployment, Service, ConfigMap...)
metadata:                # 이름, 라벨 등 식별 정보
  name: shopping-mall-api
spec:                    # 이 리소스가 "원하는 상태"를 선언하는 부분 (핵심)
  ...
```

실전 예시 — 백엔드 Deployment + Service:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shopping-mall-api
spec:
  replicas: 3                       # 항상 Pod 3개 유지
  selector:
    matchLabels:
      app: shopping-mall-api        # 이 라벨을 가진 Pod를 관리 대상으로 인식
  template:                         # 새로 만들 Pod의 스펙 (템플릿)
    metadata:
      labels:
        app: shopping-mall-api
    spec:
      containers:
        - name: api
          image: myrepo/shopping-mall-api:latest
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_DATASOURCE_URL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: db-url
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: app-secret
                  key: jwt-secret
---
apiVersion: v1
kind: Service
metadata:
  name: shopping-mall-api-service
spec:
  selector:
    app: shopping-mall-api          # Deployment가 만든 Pod들과 같은 라벨로 매칭
  ports:
    - port: 80              # Service가 노출하는 포트
      targetPort: 8080       # 실제 Pod(컨테이너)의 포트
  type: ClusterIP
```

---로 구분해서 파일 하나에 여러 리소스를 같이 정의할 수 있다. selector/labels로 Deployment와 Service가 서로 연결되는 방식 — *이름이 아니라 라벨(key-value 태그)로 매칭*한다는 게 Kubernetes 전반에 걸친 원칙이다.

# 8. Ingress — 여러 Service로의 라우팅
Service(특히 LoadBalancer 타입)를 서비스마다 하나씩 만들면 외부 로드밸런서도 그만큼 늘어나서 비용/관리 부담이 커진다. *Ingress*는 하나의 진입점에서 *경로(URL path)나 도메인*을 기준으로 여러 내부 Service에 트래픽을 나눠주는 역할을 한다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: shopping-mall-ingress
spec:
  rules:
    - host: api.shoppingmall.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: shopping-mall-api-service
                port:
                  number: 80
```

이건 하나의 도메인/IP로 들어온 요청을 내부적으로 어느 Service로 보낼지 정하는 *리버스 프록시*와 개념적으로 동일하다 (Nginx가 여러 백엔드로 라우팅하는 것과 같은 발상).

# 9. Docker Compose vs Kubernetes — 언제 넘어가야 하는가 (솔직한 현실 조언)
| | Docker Compose | Kubernetes |
|---|---|---|
| 범위 | 한 대의 서버 | 여러 대의 서버(클러스터) |
| 장애 복구 | 컨테이너 재시작 정도 | 노드 장애까지 감안한 자동 재배치 |
| 무중단 배포 | 직접 스크립트로 구현해야 함 | Deployment가 기본 제공 |
| 오토스케일링 | 없음 | 있음 (HPA, Horizontal Pod Autoscaler) |
| 러닝커브/운영 복잡도 | 낮음 | 높음 (etcd, 네트워크 정책, RBAC 등 배울 게 많음) |
| 적합한 규모 | 개인/소규모 프로젝트, 서버 1대로 충분한 트래픽 | 여러 서버에 걸친 트래픽, 높은 가용성이 요구되는 서비스 |

솔직하게 말하면, *지금 이 프로젝트 규모(개인 프로젝트, 서버 1대)에서 Kubernetes는 과한 선택(오버엔지니어링)일 가능성이 높다.* 이건 지금까지 이 프로젝트에서 계속 지켜온 야그니 원칙과 같은 맥락이다 — Kubernetes가 해결하는 문제(여러 서버, 자동 스케일링, 무중단 배포)가 실제로 필요해지는 시점(트래픽이 늘어서 서버를 여러 대로 늘려야 할 때)에 도입하는 게 맞고, 그 전까지는 Docker Compose로 충분하다.

다만 *학습 목적*으로는 지금 미리 익혀두는 게 합리적이다 — 실무에서 매우 널리 쓰이는 표준 기술이고, 개념(선언적 관리, 제어 루프, Pod/Service 분리)을 이해해두면 나중에 실제로 필요해졌을 때 훨씬 빠르게 적용할 수 있다.

# 10. 로컬에서 연습하는 법
실제 클라우드에 클러스터를 만들지 않고도 로컬 컴퓨터에서 연습할 수 있다.

- *minikube*: 로컬에 가상머신(또는 컨테이너) 하나를 띄워서 그 안에 단일 노드짜리 미니 Kubernetes 클러스터를 만들어준다.
- *kind (Kubernetes IN Docker)*: Docker 컨테이너를 "노드"처럼 취급해서 그 안에 Kubernetes 클러스터를 만든다 — 별도 VM 없이 Docker만 있으면 됨.

```bash
minikube start                      # 로컬 클러스터 시작
kubectl apply -f deployment.yaml    # 위에서 작성한 YAML을 클러스터에 적용(원하는 상태 선언)
kubectl get pods                    # 현재 떠있는 Pod 목록 확인
kubectl get deployments             # Deployment 상태 확인
kubectl logs <pod-이름>              # 특정 Pod의 로그 확인
kubectl port-forward svc/shopping-mall-api-service 8080:80   # 로컬 포트로 Service를 연결해서 접속 테스트
```

kubectl apply -f가 1번에서 설명한 "원하는 상태를 선언"하는 행위 그 자체다 — "이 YAML대로 되게 해줘"라고 선언하면, Control Plane의 Controller Manager가 알아서 현재 상태와 비교하고 차이를 좁혀나간다.
