코드를 작성하다 보면 이전에 작성했던 코드를 다시 보거나, 되돌리고 싶은 경우가 발생한다.
혹은 내가 작성한 코드를 보다 간편하게 저장하고 관리하고 싶을 수도 있다.

위 두 경우를 모두 충족시키기 위해서 다음과 같은 선택지가 존재하는데,

1. 코드를 수정할 때마다 수정된 코드들을 따로 저장하여 날짜별로 구분하고, 이를 파일에 저장한다.
2. Git을 사용한다.

즉, Git은 이전의 코드를 확인하고, 수정된 코드들을 쉽게 저장하기 위해 사용된다.

물론 더 많은 기능들이 존재하고, 다른 목적을 위해서 Git을 선택하기도 하기에 배우면서 알아보자.

---

# 1. Git Setting

1. Git을 설치한다. (자신의 운영체제에 맞추어서 설치하고, macos는 homebrew를 통해 설치)
2. Git 유저세팅을 진행한다.
```Git
git config --global user.email "본인 git 이메일"
git config --global user.name "본인 git 이름"
```

# 2. Add, Commit

1. 우선 본인이 작업할(한) 소스파일을 IDE를 통해 열어준다.
2. IDE Terminal 혹은 console에 git init을 친다. (해당 소스파일을 git이 추적한다.)
3. 파일을 다음과 같은 명령어로 git에 현재상태를 저장한다.
```git
git add "파일명"
git commit -m "message" 
```

Add만 하면 Git에 추가한다는 뜻이라고 생각하는데 왜 commit 명령어를 통해 답글과 비슷한 것을 달아줘야 할까?

Git의 파일 저장 작동원리를 보면 이해하기 편하다.

처음에 git init을 통해 작업 중인 프로젝트 하나를 git이 추적하도록 만들었다.

해당 프로젝트 내부에서 본인이 수정한 파일과 같이 업로드하고 싶은 파일들을 골라내 staging area에 넣는 작업이 git add이고, 이러한 작업을 staging이라고 한다.

staging area에 존재하는 파일들을 이제 repository라고 하는 git에 존재하는 가상의 저장소에 저장을 할 것인데, 이 작업을 git commit명령어를 통해 진행한다.

![[Pasted image 20250813143155.png]]

이처럼 staging과 commit을 통해 repository에 파일을 기록하는 것을 버전 생성이라고 하고, 이는 [[EC2(Amazon Elastic Compute Cloud)]]에 snapshot과 동일한 작업을 진행한다.

#### Git Add

```git
git add . //작업폴더 내 모든 파일을 staging
git add "file" //작업폴더 내 특정 파일을 staging
```

#### Git commit

```git
git commit -m "message" //message와 함께 staging된 버전을 repository에 저장
```

- commit시에는 현재 버전을 알려주는 commit ID와 함께 repository에 저장된다.

#### 추가 사항
1. staging할 때, 여러 파일들을 동시에 할 수 있다. (git add "file1" "file2" ...)
2. 작업폴더의 모든 파일들을 동시에 staging할 경우 git add . 을 치면 된다.
3. 현재 staging된 파일이나, 이전 파일에 비교되어 변경된 파일 등을 알고 싶으면 git status를 치면된다. (당연히 git init을 통해 추적이 시작된 파일에 한해서만 가능하다.)
4. git restore을 통해 staging된 파일을 취소할 수 있다.(당연히 git restore . 도 가능하다.)
5. git log --all --oneline을 통해 작업폴더가 여태 commit한 내용들과 commit ID를 확인 가능하다.

즉 Add/Commit작업은 작업폴더의 현재 상태의 버전을 생성하여 git에 업로드하는 작업이다.

# Git diff

가장 최근에 commit한 버전과 현재 파일과의 차이점을 터미널에서 보여주는데, 터미널에서 텍스트로 모든 내용의 변경점, 차이점을 보여주는 것은 가독성도 떨어지고 매우 힘듦.

따라서 git diff명령어에서 가독성을 추가하여 git difftool이라는 명령어가 만들어졌다.

#### Git diff

```git
git diff //현재 작업폴더의 버전과 가장 최근에 commit한 버전과의 차이점을 터미널에서 문자열로 알려준다.
```

- h,j,a,k로 이동 가능하고, q키를 통해 종료한다.

#### Git difftool

```git
git difftool //Vim에디터를 통해 가장 최근 버전과 현재 버전과의 차이점을 알려준다.
git difftool "commit ID" // commit ID에 해당하는 버전과 현재 버전과의 차이점을 알려준다.
```

- Vim editor를 터미널에 구현하여 git diff보다 가독성이 뛰어난 텍스트로 비교해준다.

최근에는 에디터에서 git을 지원하는 경우가 많고, 많은 기능 중 위처럼 git diff의 가독성을 그래프로 표현하는 기능 등을 지원하는 기능이 많다.