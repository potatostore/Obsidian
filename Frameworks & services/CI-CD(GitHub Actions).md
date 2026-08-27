---
tags:
  - seed
aliases: []
created: 2026-08-22
---

CI/CD는 "코드 변경 → 빌드/테스트 → 배포"라는 반복 작업을 사람이 손으로 하지 않고 자동화된 파이프라인이 대신 하도록 만드는 방법론이다. GitHub Actions는 이 파이프라인을 GitHub 저장소 안에 YAML 파일로 정의하고, GitHub이 제공(또는 내가 등록)하는 실행 환경(runner)에서 그 파이프라인을 실제로 돌려주는 서비스다.

# 0. CI/CD가 왜 필요한가 (원리/문제의식)
지금까지 이 프로젝트에서 해온 방식을 그대로 떠올려보면 이해가 빠르다: 코드를 고치고 → IntelliJ에서 직접 재시작하고 → 브라우저로 직접 눌러보며 확인한다. 이 방식의 문제는 다음과 같다.

1. *사람이 하는 일은 반드시 실수가 생긴다* — 테스트를 깜빡하고 배포하거나, 로컬에서는 되는데 다른 환경(포트/OS/의존성 버전)에서는 안 되는 경우를 뒤늦게 발견한다.
2. *반복 작업에 시간이 든다* — 빌드, 테스트, 배포를 매번 손으로 하면 그 시간만큼 실제 개발에 쓸 시간이 줄어든다.
3. *"내 컴퓨터에서는 되는데요" 문제* — 로컬 환경과 실제 서버 환경이 다르면, 로컬 테스트를 통과해도 서버에서 깨질 수 있다.

CI/CD는 이 세 가지를 다음과 같이 해결한다.

- *CI (Continuous Integration, 지속적 통합)*: 코드를 저장소에 push/PR 할 때마다 자동으로 빌드하고 테스트를 돌려서, "이 변경이 기존 기능을 깨뜨리지 않았는가"를 즉시 검증한다. 즉 문제를 최대한 빨리, 작은 단위로 발견하자는 원칙이다 (늦게 발견할수록 원인 추적 비용이 커진다는 건 이미 디버깅하면서 여러 번 경험했을 것이다).
- *CD (Continuous Delivery/Deployment, 지속적 배포)*: CI를 통과한 결과물을 실제 서버(스테이징/프로덕션)에 자동으로 배포한다. Delivery는 배포 직전 단계(승인 후 배포 가능한 상태)까지, Deployment는 승인 없이 자동으로 실제 배포까지 가는 것을 말한다.

핵심 원리는 하나다: *"검증되지 않은 변경은 절대 배포 단계까지 가면 안 된다"*를 사람의 의지가 아니라 파이프라인이라는 강제 장치로 보장하는 것.

# 1. GitHub Actions의 핵심 개념 (Workflow / Job / Step / Runner)
GitHub Actions는 저장소의 .github/workflows/ 디렉터리 안에 있는 YAML 파일 하나하나를 *Workflow*로 인식한다. 하나의 Workflow는 다음 계층 구조를 가진다.

```
Workflow (yml 파일 1개)
 └─ Trigger (on: 어떤 이벤트에 실행할지)
 └─ Job (병렬로 실행되는 작업 단위, 여러 개 가능)
     └─ Step (Job 안에서 순차적으로 실행되는 명령/액션, 여러 개 가능)
```

- *Trigger(on:)*: 이 workflow가 언제 실행될지 정의한다. push, pull_request, workflow_dispatch(수동 실행 버튼), schedule(cron 기반 정기 실행) 등이 있다.
- *Job*: 하나의 독립된 실행 환경(runner)에서 돌아가는 작업 묶음. 기본적으로 *Job은 서로 병렬로 실행*되며, needs:로 순서(의존관계)를 강제할 수 있다. 예를 들어 "테스트 Job이 성공해야 배포 Job이 실행된다"를 needs: test로 표현한다.
- *Step*: Job 안에서 위에서 아래로 *순차적으로* 실행되는 최소 단위. 두 가지 방식이 있다.
  - run: — 셸 명령어를 직접 실행 (./gradlew build 같은)
  - uses: — 다른 사람(또는 GitHub)이 이미 만들어둔 재사용 가능한 *Action*을 가져다 씀 (actions/checkout@v4 같은)
- *Runner*: Job이 실제로 실행되는 컴퓨터(가상 머신 또는 컨테이너). runs-on: ubuntu-latest처럼 지정한다.

> 즉 전반적으로 
>  1. 트리거 설정 : 트리거를 통해 개발자가 수정한 부분을 이벤트로 감지함(target branch에 pr/push등을 감지, github의 웹훅 이벤트를 모두 감지함)
>  2. Runner : runs on 설정을 통해 github actions는 설정한 이미지를 통해 새로운 VM을 프로비저닝하게 됨(이때 VM설정에 대해 이미지를 제외한 모든 부분을 github actions에 맞기는 GitHub-hosted runner과 AWS EC2에 VM을 등록하여 사용하는 self-hosted runner방식으로 나뉨)
>  3. 

## 1-1. Runner는 왜 매번 "새 컴퓨터"처럼 동작하는가
GitHub-hosted runner(ubuntu-latest 등)의 핵심 원리는 *에페메럴(ephemeral, 일회성)* 이라는 것이다. Job이 시작될 때마다 GitHub이 완전히 깨끗한 가상 머신을 새로 프로비저닝하고, Job이 끝나면 그 VM은 통째로 파괴된다. 즉:

- 이전 실행에서 설치한 패키지, 만들어둔 파일이 다음 실행에 남아있지 않는다 (그래서 매번 actions/checkout으로 코드를 새로 받아오고, 의존성을 새로 설치해야 한다).
- 이게 왜 중요하냐면, *"이 서버에만 설치된 무언가 때문에 우연히 성공한 빌드"* 를 원천 차단하기 때문이다. 매번 깨끗한 환경에서 재현되어야 진짜로 믿을 수 있는 검증이 된다.
- 반대로 이 깨끗함 때문에 매번 의존성을 새로 받는 비용이 드는데, 이건 뒤에서 설명할 *캐싱*으로 완화한다.

이 "매번 새로운 격리된 환경"이라는 개념은 사실 뒤에서 다룰 Docker의 컨테이너 격리 원리와 정확히 같은 문제의식이다 — "환경 차이로 인한 불확실성을 없앤다"는 목적이 CI/CD와 컨테이너화가 서로 강하게 엮여 있는 이유다.

# 2. Workflow 파일 문법
.github/workflows/ci.yml 같은 경로에 YAML로 작성한다. 기본 뼈대:

```yaml
name: CI                      # GitHub UI에 표시될 workflow 이름

on:                            # 트리거 조건
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:           # "Run workflow" 버튼으로 수동 실행 가능하게

jobs:
  build-and-test:              # job의 식별자(원하는 이름)
    runs-on: ubuntu-latest      # 실행 환경(runner)

    steps:
      - name: 저장소 코드 가져오기
        uses: actions/checkout@v4

      - name: JDK 21 설치
        uses: actions/setup-java@v4
        with:
          distribution: 'corretto'
          java-version: '21'

      - name: Gradle 빌드 및 테스트
        run: ./gradlew build
```

각 요소를 뜯어보면:

- on.push.branches / on.pull_request.branches: 어떤 브랜치에 push/PR이 일어났을 때만 실행할지 좁힐 수 있다. (실무에서는 보통 "PR을 열 때 CI가 돌고, main에 머지되면 CD가 도는" 흐름을 이렇게 나눠서 만든다.)
- uses: actions/checkout@v4: 이 Job의 runner는 방금 설명한대로 텅 빈 VM이라서, 저장소 코드조차 없다. 그래서 가장 먼저 이 액션으로 코드를 clone해온다. 거의 모든 workflow의 첫 step은 이것이다.
- uses: actions/setup-java@v4: JDK를 설치해주는 공식 액션. Node.js 프로젝트라면 actions/setup-node@v4를 쓰면 된다.
- run: ./gradlew build: 실제 빌드+테스트 명령. 이 커맨드가 실패(exit code != 0)하면 그 즉시 이 Job은 실패 처리되고, 이후 step은 실행되지 않는다 (기본 동작).

## 2-1. Action이 실제로 어떻게 동작하는가 (원리)
uses:로 가져다 쓰는 Action은 크게 3종류로 구현되어 있다.

1. *JavaScript Action*: Node.js 런타임 위에서 직접 실행되는 스크립트. Runner에 이미 Node가 내장돼있어서 가장 빠르게 시작된다.
2. *Docker Container Action*: Action 자체가 Dockerfile로 정의되어 있어서, 실행 시점에 이미지를 빌드(또는 pull)하고 그 컨테이너 안에서 실행된다. 환경 의존성이 명확하다는 장점이 있지만 컨테이너를 띄우는 오버헤드가 있다.
3. *Composite Action*: 여러 step을 하나로 묶어 재사용하는 것 — 사실상 "step들의 매크로"다.

actions/checkout@v4처럼 뒤에 붙는 @v4는 Git의 태그/브랜치/커밋 SHA를 가리킨다. 즉 Action도 결국 하나의 GitHub 저장소이고, 그 저장소의 특정 버전을 가져다 쓰는 것 — GitHub Actions 마켓플레이스에 있는 모든 Action은 결국 공개된 GitHub 저장소일 뿐이다.

# 3. Secrets — 민감정보를 어떻게 안전하게 쓰는가
DB 비밀번호, Toss 시크릿 키, 배포 서버 SSH 키 같은 값을 YAML 파일에 평문으로 적으면 안 된다 (YAML 파일 자체가 공개 저장소면 그대로 노출된다). GitHub Actions는 이를 위해 *Secrets* 기능을 제공한다.

- 저장 위치: 저장소 Settings → Secrets and variables → Actions 에서 등록. GitHub 서버에 *암호화되어 저장*되고, workflow 실행 시점에만 복호화되어 해당 Job의 환경변수로 주입된다.
- 사용법:
```yaml
steps:
  - name: 배포용 시크릿 사용 예시
    env:
      TOSS_SECRET_KEY: ${{ secrets.TOSS_SECRET_KEY }}
    run: echo "이 값은 로그에 자동으로 마스킹된다"
```
- *로그 자동 마스킹*: Secret로 등록된 값이 로그에 출력되려고 하면 GitHub이 자동으로 별표 문자로 치환해서 가려준다. 단, 이건 완벽한 보안장치가 아니라 "실수 방지용"이라는 걸 알아둬야 한다 (base64 인코딩해서 출력하는 식으로 우회하면 노출될 수 있음).
- *Environment별 Secret 분리*: environments(예: production, staging)를 만들면 그 환경 전용 Secret을 따로 두고, "이 environment에 배포하려면 특정 사람의 승인이 필요하다" 같은 게이트도 걸 수 있다. 프로덕션 DB 비밀번호와 개발용 비밀번호를 이렇게 분리하는 게 정석이다.

# 4. 여러 Job을 엮기 — needs와 아티팩트
CI(빌드+테스트)와 CD(배포)를 하나의 workflow 안에서 순서대로 실행하고 싶을 때:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./gradlew test

  build-and-push-image:
    needs: test              # test Job이 성공해야만 이 Job이 시작됨
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Docker 이미지 빌드 & 레지스트리 push
        run: |
          docker build -t myregistry/shopping-mall-api:${{ github.sha }} .
          docker push myregistry/shopping-mall-api:${{ github.sha }}

  deploy:
    needs: build-and-push-image
    runs-on: ubuntu-latest
    environment: production   # 승인 게이트를 걸 수 있는 environment
    steps:
      - name: 서버에 배포
        run: echo "여기서 실제 배포 스크립트 실행 (SSH, kubectl 등)"
```

- needs:는 Job 간 *의존성 그래프*를 만든다. test → build-and-push-image → deploy 순서로 강제되고, 앞 단계가 실패하면 뒷 Job은 아예 시작되지 않는다.
- Job은 기본적으로 서로 다른 (그리고 격리된) runner에서 실행되기 때문에, 한 Job에서 만든 파일(빌드 결과물)이 다음 Job에는 그대로 안 남아있다. 이걸 넘겨주려면 actions/upload-artifact / actions/download-artifact를 쓴다.

```yaml
      - name: 빌드 결과물 업로드
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: build/libs/*.jar
```

# 5. 캐싱 — 매번 새 환경인데 왜 빌드가 매번 오래 안 걸리는가
Runner가 매번 깨끗한 VM이라는 건 매번 Gradle 의존성(수백 MB)을 처음부터 다시 다운로드해야 한다는 뜻이기도 하다. 이걸 그대로 두면 CI가 느려져서 "빨리 피드백 받는다"는 CI의 목적 자체가 훼손된다. 그래서 actions/cache를 쓴다.

```yaml
      - name: Gradle 캐시 복원
        uses: actions/cache@v4
        with:
          path: ~/.gradle/caches
          key: gradle-${{ hashFiles('**/*.gradle*', 'gradle/wrapper/gradle-wrapper.properties') }}
          restore-keys: |
            gradle-
```

원리는 [[Redis]] 노트에서 이미 다룬 캐시 히트/미스 개념과 완전히 같다.

- key는 *의존성 파일들의 내용을 해시한 값*으로 만든다. build.gradle이 바뀌지 않았다면 해시값도 그대로라서 *캐시 히트* — 이전에 저장해둔 .gradle/caches 디렉터리를 그대로 복원해서 다운로드를 건너뛴다.
- build.gradle이 바뀌면 해시값이 달라져서 *캐시 미스* — restore-keys의 접두사(prefix) 매칭으로 "완전히 같지는 않지만 비슷한" 이전 캐시를 일단 가져오고, 그 위에 새로 필요한 의존성만 추가로 받는다 (증분 다운로드).
- 캐시는 저장소별로 GitHub이 관리하는 별도 저장 공간에 있고, 일정 기간 안 쓰이면 자동으로 만료된다.

# 6. GitHub-hosted vs Self-hosted Runner
| | GitHub-hosted | Self-hosted |
|---|---|---|
| 실행 환경 | GitHub이 관리하는 VM (매번 새로 생성/파괴) | 내가 직접 관리하는 서버/컴퓨터 |
| 비용 | public repo는 무료, private repo는 분당 과금 | 내 서버 비용만 (Actions 자체는 무료) |
| 사전 설치 소프트웨어 | Ubuntu/Windows/macOS 기본 이미지 (Java, Node 등 웬만한 건 이미 깔려있음) | 내가 직접 원하는 대로 세팅 |
| 특수 하드웨어 필요시(GPU 등) | 제한적 | 자유로움 |
| 보안 | GitHub이 격리 관리 | 내가 직접 격리/보안 관리해야 함 |

지금 이 프로젝트 규모(개인 프로젝트, MySQL/Redis 로컬 실행)에서는 GitHub-hosted runner로 충분하다. Self-hosted는 보통 "회사 내부망에 있는 DB에 접근해야 한다" 같은 네트워크 제약이나 비용 문제가 생겼을 때 고려한다.

# 7. 실전 예시 — 이 프로젝트(Spring Boot + Next.js) 기준 전체 workflow
```yaml
name: CI-CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'corretto'
          java-version: '21'
      - name: Gradle 캐시
        uses: actions/cache@v4
        with:
          path: ~/.gradle/caches
          key: gradle-${{ hashFiles('backend/**/*.gradle*') }}
      - name: 빌드 & 테스트
        working-directory: backend/shopping-mall-api
        run: ./gradlew build

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/shopping-mall-web/package-lock.json
      - name: 의존성 설치 & 빌드
        working-directory: frontend/shopping-mall-web
        run: |
          npm ci
          npm run build

  build-and-push-image:
    needs: [backend-test, frontend-build]   # 둘 다 통과해야 진행
    if: github.ref == 'refs/heads/main'      # main에 실제로 push된 경우에만 (PR에서는 배포 X)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Docker 로그인
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: 백엔드 이미지 빌드 & push
        run: |
          docker build -t myrepo/shopping-mall-api:${{ github.sha }} backend/shopping-mall-api
          docker push myrepo/shopping-mall-api:${{ github.sha }}

  deploy:
    needs: build-and-push-image
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: 배포 서버에 SSH 접속해서 최신 이미지로 재기동
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            docker pull myrepo/shopping-mall-api:${{ github.sha }}
            docker compose up -d
```

이 예시에서 짚어야 할 실무 포인트:

- backend-test와 frontend-build는 서로 관련 없는 작업이라 *병렬로 동시에 실행*된다 (Job 기본 동작). 둘 다 필요한 build-and-push-image만 needs: [backend-test, frontend-build]로 둘 다 기다린다.
- if: github.ref == 'refs/heads/main': PR 단계에서는 테스트/빌드까지만 하고(CI), 실제로 main에 머지된 push에서만 이미지 빌드/배포(CD)까지 가도록 조건을 건 것 — "검증 안 된 브랜치는 배포 단계 근처도 못 간다"는 0번 원칙을 코드로 강제한 부분.
- docker/login-action, appleboy/ssh-action 같은 건 전부 마켓플레이스에 있는 제3자(하지만 널리 쓰이는) Action이다.

# 8. 실제로 GitHub 저장소에서 어떻게 쓰는가 (UI 사용법)
지금까지는 YAML을 "어떻게 작성하는가"였고, 이번엔 그 YAML이 실제로 GitHub 웹 화면에서 어떻게 보이고 조작되는지다.

1. *워크플로 파일을 만드는 방법*: 저장소 루트에 .github/workflows/ci.yml 경로로 파일을 만들어서 main(또는 아무 브랜치)에 push하기만 하면 된다 — 별도로 "이 저장소에 Actions를 켠다" 같은 설정이 필요 없다. GitHub이 이 경로를 보고 자동으로 인식한다.
2. *실행 결과 확인*: 저장소 페이지 상단 탭 중 *Actions* 탭에서 지금까지 실행된 모든 workflow 이력을 볼 수 있다. 각 실행(run)을 클릭하면 Job → Step 단위로 펼쳐지는 트리 구조로 로그를 볼 수 있고, 실패한 step은 빨간색으로 표시되며 클릭하면 그 step의 콘솔 출력을 그대로 볼 수 있다.
3. *재실행(Re-run)*: 일시적인 네트워크 오류 등으로 실패했을 때, 코드를 다시 push하지 않고도 Actions 탭의 해당 run에서 *Re-run jobs* 버튼으로 그대로 다시 실행할 수 있다.
4. *수동 실행(workflow_dispatch)*: 2번에서 다룬 on.workflow_dispatch를 켜두면, Actions 탭 좌측에서 해당 workflow를 선택했을 때 *Run workflow* 버튼이 나타나서 push 없이도 원하는 시점에 수동으로 실행할 수 있다 (배포처럼 신중해야 하는 작업에 자주 씀).
5. *PR과의 연동*: on.pull_request가 걸린 workflow는 PR을 열거나 새 커밋을 push할 때마다 자동으로 실행되고, PR 화면 하단에 각 워크플로/Job이 ✅(성공) / ❌(실패) / 🟡(진행중) 상태로 표시된다 — 리뷰어가 코드를 읽기 전에 이미 "테스트는 통과했는지"를 한눈에 볼 수 있게 해준다.
6. *머지를 강제로 막기 (Branch Protection Rule)*: 저장소 Settings → Branches → Branch protection rule에서 main 브랜치에 *"Require status checks to pass before merging"* 을 켜고 방금 만든 workflow(예: backend-test)를 필수 체크로 지정하면, *CI가 실패한 PR은 아예 Merge 버튼이 비활성화*된다. 이게 바로 0번에서 말한 "검증 안 된 변경은 배포 단계까지 못 간다"는 원칙을 GitHub 설정으로 강제하는 실제 방법이다.
7. *Environment 승인 게이트*: 4번(environment: production)에서 다룬 것처럼, Settings → Environments에서 production environment에 *Required reviewers*를 지정해두면, 그 environment를 쓰는 Job은 지정된 사람이 Actions 탭에서 직접 *Approve* 버튼을 눌러야만 실행이 이어진다 — 자동배포(CD)이지만 마지막 단계에서만 사람 승인을 끼워넣고 싶을 때 쓰는 방법이다.

# 9. 왜 지금 이 프로젝트에 필요한가
지금은 "IntelliJ 재시작 → 브라우저 확인"을 손으로 반복하고 있다. 저장소 규모가 커지고 기능이 늘어날수록 다음 문제가 생긴다.

1. 배포 전에 매번 전체 기능을 수동으로 확인하는 건 시간이 늘어날수록 감당이 안 된다 (지금 하고 있는 E2E 수동 점검이 그 예시다).
2. 여러 사람이 협업하게 되면 "내 로컬에서는 됐다"가 더 이상 신뢰할 수 있는 검증이 아니게 된다.
3. 배포 자체가 사람 손을 타면, 배포 절차를 잊어버리거나 순서를 실수하는 사고가 반드시 생긴다.

로드맵에 있는 순서(웹서버 E2E 완료 → GitHub Actions/CI-CD/Docker/K8s)가 합리적인 이유가 이것 — 기능이 어느정도 안정된 다음에 "이 기능을 안전하게, 반복 가능하게 배포하는 절차" 자체를 자동화하는 단계로 넘어가는 게 맞다.
