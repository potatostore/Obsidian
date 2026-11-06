---
created: 2026-11-06
branch: main
commit: ecc7bf8
tags: [nimda, spring-modulith, modular-monolith, refactoring, event]
---

# Spring Modulith — 개념 정리 & NIMDA 레거시 리팩토링

하나의 배포 단위(모놀리스)를 유지하면서, 내부를 강제되는 경계를 가진 모듈로 나누기 위한 Spring 공식 프로젝트 정리.
후반부는 NIMDA cite 백엔드의 좋아요 → 알림, 게시글 삭제, 공지 알림 흐름을 실제로 모듈리스 구조로 바꾼 코드.

- 대상: backend-spring/src/main/java/com/nimda/cite/ (judgeServer는 구조 문제만 언급)
- 기준 버전: Spring Boot 3.2.0 → Spring Modulith 1.1.x (1.1.12)
- 관련 노트: [[PR 컨벤션]]
- 상태: 학습용 설계안. 아직 코드에 반영하지 않음

## 한눈에 보기

| 구분 | 내용 |
|---|---|
| [[#1. 왜 나왔나 — 해결하려는 문제\|왜 나왔나]] | 모놀리스의 경계 붕괴 vs MSA의 분산 비용 사이의 중간 지점 |
| [[#2. 핵심 개념\|핵심 개념]] | Application Module, API vs internal, NamedInterface, verify, 이벤트, 모듈 테스트, 문서화 |
| [[#3. 언제 이벤트로 바꾸고 언제 직접 호출하나\|이벤트 vs 직접 호출]] | 결과값이 필요한가 / 실패를 같이 해야 하는가 |
| [[#4. NIMDA 현재 상태 진단\|현재 상태 진단]] | 패키지 구조 문제, 순환 의존, 이벤트 사용 방식 문제 |
| [[#5. 리팩토링 ① 도입 준비 — 의존성 & 검증 테스트\|① 도입 준비]] | pom, ModularityTests, 패키지 재배치 |
| [[#6. 리팩토링 ② 모듈 공개 API 만들기\|② 공개 API]] | UserReader, BoardReader, NamedInterface |
| [[#7. 리팩토링 ③ 좋아요 → 알림을 모듈 이벤트로\|③ 좋아요 알림]] | BoardLikedEvent + @ApplicationModuleListener |
| [[#8. 리팩토링 ④ 게시글 삭제 — 순환 의존 끊기\|④ 게시글 삭제]] | BoardDeletedEvent, 의존성 역전(SPI) |
| [[#9. 리팩토링 ⑤ 공지 알림 — 동기 직접 호출 제거\|⑤ 공지 알림]] | NoticePostedEvent |
| [[#10. 모듈 테스트\|모듈 테스트]] | @ApplicationModuleTest + Scenario |
| [[#11. 동작 변화 & 주의점\|동작 변화]] | 커밋 후 비동기 실행, Event Publication Registry |
| [[#12. 남은 과제\|남은 과제]] | 아직 남는 순환, ID 참조 전환 |

---

## 1. 왜 나왔나 — 해결하려는 문제

| 선택지 | 장점 | 문제 |
|---|---|---|
| 전통적 모놀리스 | 단순한 배포, 로컬 트랜잭션, 쉬운 디버깅 | 패키지 경계는 관례일 뿐 컴파일러가 막지 않음 → 서로의 Repository, Entity를 마구 참조하는 Big Ball of Mud |
| 마이크로서비스 (MSA) | 경계가 물리적으로 강제됨 | 네트워크 호출, 분산 트랜잭션, 배포·관측 비용. 경계를 잘못 그으면 되돌리기 매우 어려움 |
| 모듈러 모놀리스 | 배포는 하나, 내부 경계는 강제 | 경계를 지키게 할 도구가 필요 → **Spring Modulith** |

- Spring Modulith는 새로운 런타임 프레임워크가 아니라, 기존 Spring Boot 앱 위에서 모듈 경계를 **검증(verify) · 테스트 · 문서화**하게 해 주는 도구 모음
- 목표: 나중에 MSA로 떼어내더라도 경계가 이미 깨끗한 상태로 만드는 것. 떼어내지 않아도 유지보수성이 좋아짐
- 핵심 문장: **"다른 모듈의 내부를 만지지 않는다."** 이벤트는 그걸 지키기 위한 수단 중 하나일 뿐

---

## 2. 핵심 개념

### 2-1. Application Module

| 항목 | 설명 |
|---|---|
| 모듈 단위 | @SpringBootApplication 클래스가 있는 패키지의 **바로 아래 하위 패키지 하나 = 모듈 하나** |
| 예시 | com.nimda.cite.board, com.nimda.cite.like, com.nimda.cite.user 가 각각 모듈 |
| 공개 API | 모듈 **최상위 패키지**에 있는 public 타입 (예: com.nimda.cite.board.BoardReader) |
| internal | 모듈의 **하위 패키지** 전부 (board.repository, board.service, board.entity …). Java에서 public이어도 다른 모듈이 참조하면 위반 |
| NamedInterface | 하위 패키지를 일부러 공개하고 싶을 때 package-info.java에 @NamedInterface("이름")을 붙임. 다른 모듈은 "board::entity" 처럼 이름으로 참조 |
| allowedDependencies | 모듈 package-info.java의 @ApplicationModule(allowedDependencies = …)로 "이 모듈이 의존해도 되는 모듈" 화이트리스트 지정 (선택) |

### 2-2. 검증 — ApplicationModules.verify()

테스트 코드 한 줄로 아래를 검사. 위반 시 테스트 실패 + 위반 목록 출력.

| 검사 항목 | 예시 위반 |
|---|---|
| 모듈 간 순환 의존 | board → like 이면서 like → board |
| 다른 모듈 internal 타입 참조 | like.service가 board.repository.BoardRepository 주입 |
| 허용되지 않은 의존 | allowedDependencies에 없는 모듈 참조 |

### 2-3. 모듈 간 이벤트 — @ApplicationModuleListener

| 항목 | 설명 |
|---|---|
| 정체 | @Async + @Transactional(propagation = REQUIRES_NEW) + @TransactionalEventListener 를 합친 어노테이션 |
| 실행 시점 | 발행한 쪽 트랜잭션이 **커밋된 후** |
| 실행 방식 | 별도 스레드, 별도 트랜잭션 → 리스너가 실패해도 원래 작업은 롤백되지 않음 |
| 이벤트 위치 | **발행하는 모듈의 최상위 패키지** (발행자의 공개 API). 소비자가 발행자에 의존하는 방향이 정상 |
| 이벤트 내용 | 엔티티가 아니라 **ID와 값**만 담은 record. 다른 스레드/트랜잭션에서 읽히고, Registry에 JSON으로 저장되기 때문 |

### 2-4. Event Publication Registry

| 항목 | 설명 |
|---|---|
| 역할 | 이벤트 발행 시 "이 리스너에게 전달해야 함"을 DB(event_publication 테이블)에 같은 트랜잭션으로 기록, 리스너 성공 시 완료 처리 |
| 효과 | 리스너가 실패하거나 서버가 죽어도 미완료 이벤트가 남아 재처리 가능 (Transactional Outbox와 유사) |
| 의존성 | spring-modulith-starter-jpa |
| NIMDA 주의 | Flyway를 쓰므로 event_publication 테이블 마이그레이션 추가 필요 (스키마는 적용 시점 버전 문서 기준으로 작성) |

### 2-5. 모듈 테스트 & 문서화

| 기능 | 설명 |
|---|---|
| @ApplicationModuleTest | 해당 모듈의 빈만 띄우는 통합 테스트. BootstrapMode로 의존 모듈까지 띄울지 선택 |
| Scenario | "이 동작을 하면 이 이벤트가 나간다"를 검증하는 테스트 API |
| Documenter | 모듈 의존 관계를 PlantUML / C4 다이어그램, 모듈 캔버스로 자동 생성 (target/spring-modulith-docs) |

---

## 3. 언제 이벤트로 바꾸고 언제 직접 호출하나

**모든 의존을 이벤트로 바꾸는 게 아니다.** 모듈 내부 의존(Controller → Service → Repository)은 그대로 둔다.
다른 모듈을 부르는 코드만 아래 두 질문으로 분류한다.

> ① 호출 결과값이 지금 바로 필요한가?
> ② 그 작업이 실패하면 내 작업도 실패해야 하는가?

| 분류 | 방법 | NIMDA 예시 |
|---|---|---|
| 조회 (결과값 필요) | 상대 모듈의 **공개 API 직접 호출** | 좋아요 누를 때 사용자·게시글 조회 → UserReader, BoardReader |
| 함께 성공/실패해야 하는 명령 | 상대 모듈 공개 API **직접 호출**, 같은 트랜잭션 | 프로필 꾸미기 구매 시 포인트 차감 (부족하면 구매 실패) |
| 후속 반응 (실패해도 원래 작업은 성공) | **이벤트** | 좋아요 → 알림, 댓글 → 알림, 공지 등록 → 전체 알림, 게시글 삭제 → 좋아요 정리 |
| 서로 너무 얽혀 있음 | **모듈 합치기** | alarm + notification → notification 하나로 |

---

## 4. NIMDA 현재 상태 진단

### 4-1. 패키지 구조 문제

| 문제 | 내용 | 해결 |
|---|---|---|
| 루트 패키지가 3개 | com.nimda.cite (메인 클래스), judgeServer, redis. @EnableJpaRepositories / @EntityScan으로 억지로 묶는 중 | judgeServer, redis를 com.nimda.cite 아래로 이동 (또는 @Modulithic(additionalPackages = "judgeServer")) |
| domain 한 단계 | com.nimda.cite 직계가 config, user, common, domain, eventListener → **domain 전체가 모듈 하나** | domain.board → board 처럼 한 단계 올리기 (IDE 패키지 이동, 동작 변화 없음) |
| alarm / notification 분리 | 서로 의존(alarm → notification 4, notification → alarm 1) | notification 모듈로 합치기 |

### 4-2. 모듈 간 import 현황 (cite 기준, 리팩토링 전)

| 모듈 | 의존하는 모듈 (import 수) |
|---|---|
| board | user 10, tag 5, profiledecoration 4, comment 3, attachment 3, like 2, alarm 1 |
| like | user 12, board 7, comment 6, notification 4, alarm 3 |
| comment | user 5, board 3, like 2, alarm 2 |
| alarm | user 8, notification 4, board 3 |
| notification | user 4, alarm 1 |
| point | user 7, board 4, profiledecoration 2 |
| user | profiledecoration 3, point 2 |

순환 쌍: board↔like, board↔comment, board↔tag, board↔alarm, alarm↔notification, like↔comment, user↔point, user↔profiledecoration, (judge) group↔groupMember

### 4-3. 좋아요 → 알림 흐름의 문제 (리팩토링 대상)

| # | 문제 | 위치 | 결과 |
|---|---|---|---|
| 1 | 다른 모듈 Repository 직접 주입 | BoardLikeService의 BoardRepository, UserRepository | board, user 내부 구조가 바뀌면 like도 깨짐 |
| 2 | AlarmService 주입하지만 사용 안 함 | BoardLikeService | 쓸데없는 like → alarm 의존 |
| 3 | Notification 객체를 만들고 버림 | BoardLikeService.toggleLike | dead code + like → notification 의존 |
| 4 | 이벤트 클래스가 소비자 패키지에 있음 | alarm/Event/PushLikeButtonEvent | 발행자(like, comment)가 소비자(alarm)에 의존하는 역방향 |
| 5 | 이벤트에 엔티티(Board, User)를 그대로 담음 | PushLikeButtonEvent, AddChildCommentEvent | @Async 다른 스레드에서 LAZY 프록시 접근 → LazyInitializationException 위험 |
| 6 | @EventListener + @Async | AlarmService 핸들러 4개 | 발행 즉시 다른 스레드에서 실행 → **커밋 전에 알림이 나감**. 좋아요가 롤백돼도 알림은 감. 실패 시 재처리 불가 |
| 7 | 공지 알림 동기 직접 호출 | BoardService → alarmService.sendNoticeToAll | 전체 유저 루프가 게시글 저장 트랜잭션 안에서 실행 → 응답 지연, 알림 실패 시 글 작성 롤백. 이미 있는 NoticePostEvent는 안 쓰임 |
| 8 | 게시글 삭제 시 다른 모듈 Repository 직접 호출 | BoardService.boardDelete의 commentRepository, boardLikeRepository | board↔like, board↔comment 순환의 원인 |

---

## 5. 리팩토링 ① 도입 준비 — 의존성 & 검증 테스트

### pom.xml 추가

~~~xml
<properties>
    <java.version>17</java.version>
    <spring-modulith.version>1.1.12</spring-modulith.version> <!-- Boot 3.2 대응 라인 -->
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.modulith</groupId>
            <artifactId>spring-modulith-bom</artifactId>
            <version>${spring-modulith.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <!-- 모듈 모델, @ApplicationModuleListener 등 -->
    <dependency>
        <groupId>org.springframework.modulith</groupId>
        <artifactId>spring-modulith-starter-core</artifactId>
    </dependency>
    <!-- Event Publication Registry (JPA) -->
    <dependency>
        <groupId>org.springframework.modulith</groupId>
        <artifactId>spring-modulith-starter-jpa</artifactId>
    </dependency>
    <!-- verify, Documenter, @ApplicationModuleTest, Scenario -->
    <dependency>
        <groupId>org.springframework.modulith</groupId>
        <artifactId>spring-modulith-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
~~~

### 검증 + 문서화 테스트

~~~java
package com.nimda.cite;

import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.docs.Documenter;

class ModularityTests {

    ApplicationModules modules = ApplicationModules.of(NimdaCiteApplication.class);

    @Test
    void verifiesModularStructure() {
        modules.forEach(System.out::println); // 인식된 모듈 목록 확인용
        modules.verify();                      // 순환, internal 접근 위반 시 실패
    }

    @Test
    void writeDocumentation() {
        new Documenter(modules)
                .writeModulesAsPlantUml()            // 전체 모듈 의존 다이어그램
                .writeIndividualModulesAsPlantUml()  // 모듈별 다이어그램
                .writeModuleCanvases();              // 모듈별 공개 API, 이벤트 목록
    }
}
~~~

- 처음엔 verifiesModularStructure가 **실패하는 게 정상**. 실패 목록 = 리팩토링 TODO 리스트
- 리팩토링 전 다이어그램을 뽑아 두면 전후 비교 자료가 됨

### 패키지 재배치 (동작 변화 없음)

~~~text
리팩토링 전                                 리팩토링 후
com.nimda.cite                              com.nimda.cite
├── NimdaCiteApplication                    ├── NimdaCiteApplication
├── config / common / user                  ├── config / common / user
├── eventListener                           ├── board/
└── domain/                                 │   ├── BoardReader            ← 공개 API
    ├── board/                              │   ├── BoardDeletedEvent      ← 공개 이벤트
    ├── like/                               │   ├── NoticePostedEvent      ← 공개 이벤트
    ├── comment/                            │   ├── BoardReactionCounter   ← 공개 SPI
    ├── alarm/                              │   ├── entity/  (@NamedInterface "entity")
    ├── notification/                       │   └── controller/ service/ repository/ (internal)
    └── ...                                 ├── like/
judgeServer/  (루트 밖)                      │   ├── BoardLikedEvent        ← 공개 이벤트
redis/        (루트 밖)                      │   └── entity/ service/ repository/ (internal)
                                            ├── notification/          ← alarm 흡수
                                            ├── comment/ ...
                                            └── judge/                 ← judgeServer 이동
~~~

---

## 6. 리팩토링 ② 모듈 공개 API 만들기

다른 모듈이 Repository 대신 쓰는 **조회용 공개 API**. 모듈 최상위 패키지에 둔다.

### user 모듈 — UserReader

~~~java
package com.nimda.cite.user;   // 최상위 패키지 = 공개 API

import com.nimda.cite.common.exception.NotFoundException;
import com.nimda.cite.common.exception.errorcode.user.UserErrorCode;
import com.nimda.cite.user.entity.User;
import com.nimda.cite.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserReader {

    private final UserRepository userRepository; // 같은 모듈이므로 OK

    public User getUser(Long userId) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new NotFoundException(UserErrorCode.USER_NOT_FOUND));
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
}
~~~

### board 모듈 — BoardReader

~~~java
package com.nimda.cite.board;

import com.nimda.cite.board.entity.Board;
import com.nimda.cite.board.repository.BoardRepository;
import com.nimda.cite.common.exception.NotFoundException;
import com.nimda.cite.common.exception.errorcode.domain.BoardErrorCode;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class BoardReader {

    private final BoardRepository boardRepository;

    public Board getBoard(Long boardId) {
        return boardRepository.findById(boardId)
                .orElseThrow(() -> new NotFoundException(BoardErrorCode.BOARD_NOT_FOUND));
    }
}
~~~

### 엔티티 공개 — NamedInterface (타협안)

BoardLike가 @ManyToOne User, @ManyToOne Board를 갖고 있어서 like 모듈은 User, Board 엔티티 타입이 필요하다.
엔티티 패키지는 internal이므로, 당장은 NamedInterface로 **명시적으로 공개**하고 장기적으로 ID 참조로 바꾼다.

~~~java
// user/entity/package-info.java
@org.springframework.modulith.NamedInterface("entity")
package com.nimda.cite.user.entity;
~~~

~~~java
// board/entity/package-info.java
@org.springframework.modulith.NamedInterface("entity")
package com.nimda.cite.board.entity;
~~~

common 모듈도 같은 방식으로 exception, response 등 하위 패키지에 NamedInterface를 붙인다. (Modulith 1.2부터는 @ApplicationModule(type = OPEN)으로 모듈 전체를 열 수 있음)

### (선택) 허용 의존 화이트리스트

~~~java
// like/package-info.java
@org.springframework.modulith.ApplicationModule(
        displayName = "좋아요",
        allowedDependencies = {"board", "board::entity", "user", "user::entity", "common::exception"}
)
package com.nimda.cite.like;
~~~

- 지정하지 않아도 "공개 API / NamedInterface만 참조 + 순환 금지"는 검사된다
- 지정하면 like가 notification을 import하는 순간 테스트가 실패 → 의존 방향을 문서처럼 고정

---

## 7. 리팩토링 ③ 좋아요 → 알림을 모듈 이벤트로

### Before — BoardLikeService (발췌)

~~~java
package com.nimda.cite.domain.like.service;

import com.nimda.cite.domain.alarm.Event.PushLikeButtonEvent;     // 소비자 패키지의 이벤트
import com.nimda.cite.domain.alarm.service.AlarmService;          // 쓰지도 않는 의존
import com.nimda.cite.domain.board.repository.BoardRepository;    // board 내부
import com.nimda.cite.domain.notification.entity.Notification;    // notification 내부
import com.nimda.cite.user.repository.UserRepository;             // user 내부
// ...

@Service
@RequiredArgsConstructor
public class BoardLikeService {

    private final BoardLikeRepository boardLikeRepository;
    private final BoardRepository boardRepository;
    private final UserRepository userRepository;
    private final AlarmService alarmService;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public String toggleLike(Long userId, Long boardId) {
        User liker = userRepository.findById(userId).orElseThrow(
                () -> new NotFoundException(UserErrorCode.USER_NOT_FOUND));
        Board board = boardRepository.findById(boardId).orElseThrow(
                () -> new NotFoundException(BoardErrorCode.BOARD_NOT_FOUND));

        Optional<BoardLike> like = boardLikeRepository.findByBoardAndLiker(board, liker);

        if (like.isPresent()) {
            boardLikeRepository.delete(like.get());
            return "좋아요 취소 완료";
        } else {
            boardLikeRepository.save(BoardLike.builder().liker(liker).board(board).author(board.getAuthor()).build());

            if (!board.getAuthor().getId().equals(userId)) {
                Notification notification = Notification.builder()   // 만들고 버려짐
                        .recipient(board.getAuthor())
                        // ...
                        .build();

                eventPublisher.publishEvent(new PushLikeButtonEvent(this,
                        board, board.getAuthor(), liker));           // 엔티티를 그대로 전달
            }
            return "좋아요 완료";
        }
    }
}
~~~

### Before — 이벤트 & 리스너

~~~java
// alarm/Event/PushLikeButtonEvent.java  — 소비자(alarm) 쪽에 있음
public class PushLikeButtonEvent extends ApplicationEvent {
    private Board board;      // 엔티티
    private User recipient;   // LAZY 프록시일 수 있음 (board.getAuthor())
    private User sender;
    // ...
}

// alarm/service/AlarmService.java
@EventListener
@Async   // 발행 즉시 다른 스레드에서 실행 → 커밋 전에 알림 발송
public void handlePushLikeButtonEvent(PushLikeButtonEvent event) {
    Notification notification = Notification.builder()
            .recipient(event.getRecipient())
            .sender(event.getSender())
            .message(event.getSender().getName() + "님이 내 게시글을 좋아합니다.-" + event.getBoard().getTitle())
            // ...
            .build();
    this.send(notification);
}
~~~

### After — 이벤트는 발행자(like) 모듈의 공개 API로

~~~java
package com.nimda.cite.like;   // like 모듈 최상위 = 공개

/**
 * 게시글에 좋아요가 눌렸다 (자기 글 좋아요는 발행하지 않음).
 * 엔티티 대신 ID와 값만 담는다 → 다른 스레드/트랜잭션, Registry 직렬화에 안전.
 */
public record BoardLikedEvent(
        Long boardId,
        String boardTitle,
        Long boardAuthorId,
        Long likerId,
        String likerName
) {}
~~~

### After — BoardLikeService

~~~java
package com.nimda.cite.like.service;

import com.nimda.cite.board.BoardReader;          // board 공개 API
import com.nimda.cite.board.entity.Board;         // board::entity (NamedInterface)
import com.nimda.cite.like.BoardLikedEvent;       // 자기 모듈 이벤트
import com.nimda.cite.like.entity.BoardLike;
import com.nimda.cite.like.repository.BoardLikeRepository;
import com.nimda.cite.user.UserReader;            // user 공개 API
import com.nimda.cite.user.entity.User;           // user::entity (NamedInterface)
import lombok.RequiredArgsConstructor;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class BoardLikeService {

    private final BoardLikeRepository boardLikeRepository;
    private final BoardReader boardReader;
    private final UserReader userReader;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public String toggleLike(Long userId, Long boardId) {
        User liker = userReader.getUser(userId);
        Board board = boardReader.getBoard(boardId);

        Optional<BoardLike> like = boardLikeRepository.findByBoardAndLiker(board, liker);
        if (like.isPresent()) {
            boardLikeRepository.delete(like.get());
            return "좋아요 취소 완료";
        }

        boardLikeRepository.save(BoardLike.builder()
                .liker(liker).board(board).author(board.getAuthor()).build());

        Long authorId = board.getAuthor().getId();
        if (!authorId.equals(userId)) {   // 자신이 누른 좋아요는 알림 X (기존 규칙 유지)
            eventPublisher.publishEvent(new BoardLikedEvent(
                    boardId, board.getTitle(), authorId, liker.getId(), liker.getName()));
        }
        return "좋아요 완료";
    }

    @Transactional(readOnly = true)
    public long getLikeCount(Long boardId) {
        boardReader.getBoard(boardId);   // 존재 검증 (기존 동작 유지)
        return boardLikeRepository.countByBoardId(boardId);
    }

    // isUserLiked, getTotalLikesReceived 등 나머지 메서드도
    // userRepository.findById → userReader.getUser, boardRepository.findById → boardReader.getBoard 치환
}
~~~

### After — notification 모듈의 리스너

~~~java
package com.nimda.cite.notification.service;

import com.nimda.cite.like.BoardLikedEvent;            // 소비자가 발행자의 이벤트에 의존 (정방향)
import com.nimda.cite.notification.entity.Notification;
import com.nimda.cite.notification.enums.NotificationType;
import com.nimda.cite.user.UserReader;
import lombok.RequiredArgsConstructor;
import org.springframework.modulith.events.ApplicationModuleListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
class NotificationEventHandler {   // package-private: 다른 모듈이 직접 부를 일 없음

    private final AlarmService alarmService;   // 같은 모듈 (alarm 흡수)
    private final UserReader userReader;

    @ApplicationModuleListener   // 커밋 후 + 비동기 + 새 트랜잭션 + Registry 기록
    void on(BoardLikedEvent event) {
        Notification notification = Notification.builder()
                .recipient(userReader.getUser(event.boardAuthorId()))  // 새 트랜잭션에서 다시 조회
                .sender(userReader.getUser(event.likerId()))
                .message(event.likerName() + "님이 내 게시글을 좋아합니다.-" + event.boardTitle()) // 프론트 파싱 형식 유지
                .notificationType(NotificationType.PushLikeButtonAtBoard)
                .relatedEntityId(event.boardId())
                .relatedUrl("/board/view/" + event.boardId())
                .isRead(false)
                .build();

        alarmService.send(notification);   // DB 저장 + SSE 전송 (기존 로직 그대로)
    }
}
~~~

### 무엇이 바뀌었나

| 항목 | Before | After |
|---|---|---|
| like가 의존하는 모듈 | board(내부), user(내부), notification(내부), alarm(내부) | board(API + entity), user(API + entity) |
| 이벤트 위치 | alarm/Event (소비자) | like 최상위 (발행자) |
| 이벤트 내용 | Board, User 엔티티 | ID, 제목, 이름 (값) |
| 리스너 실행 시점 | 발행 즉시, 커밋 전 | **커밋 후** |
| 좋아요 롤백 시 | 알림이 이미 나갔을 수 있음 | 알림 안 나감 |
| 알림 실패 시 | 로그만 남고 끝 | Registry에 미완료로 남음 → 재처리 가능 |
| dead code | Notification 생성 후 버림, AlarmService 미사용 주입 | 제거 |

---

## 8. 리팩토링 ④ 게시글 삭제 — 순환 의존 끊기

board → like 의존은 두 군데에서 생긴다. 성격이 다르므로 다르게 푼다.

| 위치 | 성격 | 해결 |
|---|---|---|
| BoardService.boardDelete의 boardLikeRepository.deleteAllByBoardId | 후속 정리 (반응) | **이벤트** BoardDeletedEvent |
| BoardController의 boardLikeService.getLikeCount, isUserLiked | 조회 (결과값 필요) | **의존성 역전(SPI)** — board가 인터페이스를 정의, like가 구현 |

### Before

~~~java
// board/service/BoardService.java
@Transactional
public void boardDelete(Long id) {
    Board board = findBoard(id);
    board.setStatus(BoardStatus.DELETED);
    boardRepository.save(board);

    commentRepository.deleteAllByBoardId(id);     // comment 내부 직접 호출
    boardLikeRepository.deleteAllByBoardId(id);   // like 내부 직접 호출
}

// board/controller/BoardController.java
private final BoardLikeService boardLikeService;  // like 모듈 서비스 직접 의존
long likeCount = boardLikeService.getLikeCount(board.getId());
~~~

### After — 삭제는 이벤트로

~~~java
package com.nimda.cite.board;

public record BoardDeletedEvent(Long boardId) {}
~~~

~~~java
// board/service/BoardService.java
@Transactional
public void boardDelete(Long id) {
    Board board = findBoard(id);
    board.setStatus(BoardStatus.DELETED);   // soft delete
    boardRepository.save(board);

    eventPublisher.publishEvent(new BoardDeletedEvent(id));   // 누가 정리하는지 board는 모름
}
~~~

~~~java
package com.nimda.cite.like.service;

import com.nimda.cite.board.BoardDeletedEvent;
import com.nimda.cite.like.repository.BoardLikeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.modulith.events.ApplicationModuleListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
class BoardLikeCleaner {

    private final BoardLikeRepository boardLikeRepository;

    @ApplicationModuleListener
    void on(BoardDeletedEvent event) {
        boardLikeRepository.deleteAllByBoardId(event.boardId());
    }
}
// comment 모듈에도 같은 형태의 CommentCleaner를 둔다
~~~

- 게시글은 soft delete라 좋아요 정리가 커밋 직후 비동기로 일어나도 문제 없음
- 만약 "반드시 같은 트랜잭션에서 지워야 한다"면 리스너에 @ApplicationModuleListener 대신 @EventListener를 쓰면 된다 (동기, 같은 트랜잭션). 이벤트로 의존 방향은 끊으면서 원자성은 유지

### After — 좋아요 수 조회는 의존성 역전

~~~java
package com.nimda.cite.board;   // board가 "필요한 기능"을 인터페이스로 공개

public interface BoardReactionCounter {
    long countLikes(Long boardId);
    boolean isLiked(Long boardId, Long userId);
}
~~~

~~~java
package com.nimda.cite.like.service;

import com.nimda.cite.board.BoardReactionCounter;   // like → board (정방향)
import com.nimda.cite.like.repository.BoardLikeRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
@RequiredArgsConstructor
@Transactional(readOnly = true)
class BoardLikeCounter implements BoardReactionCounter {

    private final BoardLikeRepository boardLikeRepository;

    @Override
    public long countLikes(Long boardId) {
        return boardLikeRepository.countByBoardId(boardId);
    }

    @Override
    public boolean isLiked(Long boardId, Long userId) {
        return userId != null && boardLikeRepository.existsByBoardIdAndLikerId(boardId, userId);
    }
}
~~~

~~~java
// board/controller/BoardController.java
private final BoardReactionCounter reactionCounter;   // 자기 모듈의 인터페이스에만 의존

private BoardResponseDTO toDetailResponse(Board board, User user) {
    long likeCount = reactionCounter.countLikes(board.getId());
    boolean liked = user != null && reactionCounter.isLiked(board.getId(), user.getId());
    // ...
}
~~~

| 방법 | 장점 | 단점 |
|---|---|---|
| **SPI (위 코드)** | 스키마 변경 없음, 코드 이동만 | 구현체가 없으면 기동 실패 (like 모듈이 반드시 있어야 함) |
| 화면 조합용 상위 모듈 | board, like, comment가 서로 모름 | 게시글 상세/목록 API를 새 모듈로 옮겨야 함 |
| 반정규화 (Board.likeCount 컬럼) | 목록 조회 시 N+1 카운트 쿼리 제거 | Flyway 마이그레이션 + 정합성 관리 필요 |

---

## 9. 리팩토링 ⑤ 공지 알림 — 동기 직접 호출 제거

### Before

~~~java
// board/service/BoardService.java
@Autowired
private AlarmService alarmService;   // board → alarm 의존

// 저장 트랜잭션 안에서 전체 유저에게 알림 저장 + SSE 전송
if (board.getCategory() != null && board.getCategory().getName().contains("공지")) {
    alarmService.sendNoticeToAll(board.getId(), board.getTitle(), author.getId());
}
~~~

### After

~~~java
package com.nimda.cite.board;

public record NoticePostedEvent(Long boardId, String boardTitle, Long authorId) {}
~~~

~~~java
// board/service/BoardService.java  — AlarmService 의존 제거
if (board.getCategory() != null && board.getCategory().getName().contains("공지")) {
    eventPublisher.publishEvent(new NoticePostedEvent(board.getId(), board.getTitle(), author.getId()));
}
~~~

~~~java
// notification/service/NotificationEventHandler.java 에 추가
@ApplicationModuleListener
void on(NoticePostedEvent event) {
    alarmService.sendNoticeToAll(event.boardId(), event.boardTitle(), event.authorId());
}
~~~

~~~java
// notification/service/AlarmService.java — userRepository 대신 UserReader
public void sendNoticeToAll(Long boardId, String boardTitle, Long authorId) {
    User sender = userReader.getUser(authorId);
    for (User recipient : userReader.getAllUsers()) {
        if (recipient.getId().equals(authorId)) continue;
        // 알림 저장 + SSE 전송 (기존 로직 그대로)
    }
}
~~~

- 게시글 작성 응답이 전체 유저 수와 무관해짐
- 알림 전송이 실패해도 공지 글은 저장됨
- 쓰이지 않던 alarm/Event/NoticePostEvent는 삭제

---

## 10. 모듈 테스트

~~~java
package com.nimda.cite.like;

import com.nimda.cite.like.service.BoardLikeService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.modulith.test.ApplicationModuleTest;
import org.springframework.modulith.test.ApplicationModuleTest.BootstrapMode;
import org.springframework.modulith.test.Scenario;
import org.springframework.test.context.jdbc.Sql;

@ApplicationModuleTest(BootstrapMode.DIRECT_DEPENDENCIES)   // like + 직접 의존 모듈(board, user)만 기동
@Sql("/like-test-data.sql")   // 작성자 1, 좋아요 누를 유저 2, 게시글 10
class BoardLikeModuleTests {

    @Autowired
    BoardLikeService boardLikeService;

    @Test
    void 남의_글에_좋아요하면_BoardLikedEvent가_발행된다(Scenario scenario) {
        scenario.stimulate(() -> boardLikeService.toggleLike(2L, 10L))
                .andWaitForEventOfType(BoardLikedEvent.class)
                .matchingMappedValue(BoardLikedEvent::boardAuthorId, 1L)
                .toArrive();
    }
}
~~~

- notification 모듈은 기동되지 않음 → like 모듈 테스트가 알림 로직에 영향받지 않음
- 테스트 DB(H2)와 Flyway 설정은 적용 단계에서 맞춰야 함

---

## 11. 동작 변화 & 주의점

| 항목 | 내용 |
|---|---|
| 알림 시점 | 커밋 전 → 커밋 후. 사용자 입장에서 차이는 거의 없음 |
| 좋아요 정리 시점 | 게시글 삭제와 같은 트랜잭션 → 커밋 직후 별도 트랜잭션 (soft delete라 영향 없음) |
| @EnableAsync | NimdaCiteApplication에 이미 있음. 스레드 풀 크기는 별도 설정 권장 (기본 SimpleAsyncTaskExecutor 대체) |
| event_publication 테이블 | Flyway 마이그레이션 추가 필요. 완료된 레코드 정리 정책도 정해야 함 |
| 미완료 이벤트 재처리 | 기동 시 재발행 옵션 또는 IncompleteEventPublications로 수동 재처리 |
| 알림 메시지 형식 | "이름님이 내 게시글을 좋아합니다.-제목" 형식 유지 → 프론트 파싱 영향 없음 |

---

## 12. 남은 과제

| 과제 | 내용 |
|---|---|
| like ↔ comment 순환 | 댓글 좋아요(CommentLike)가 like 모듈에 있음 → comment 모듈로 옮기거나 같은 방식(SPI/이벤트)으로 분리 |
| user ↔ point, user ↔ profiledecoration | 회원가입 시 포인트/장식 초기화 등 → user가 UserRegisteredEvent 발행, 나머지가 구독 |
| board → tag, attachment, profiledecoration | 조회 API / SPI로 정리 |
| 엔티티 간 @ManyToOne 모듈 경계 넘기 | NamedInterface는 임시 타협. 장기적으로 userId, boardId ID 참조로 전환 |
| judgeServer 편입 | com.nimda.cite.judge로 이동 후 group ↔ groupMember 순환 정리 (합치기 유력) |
| 진행 순서 | 의존성 + ModularityTests 추가 → 패키지 재배치 → alarm/notification 병합 → 좋아요 알림 → 삭제 → 공지 → 나머지 순환 |
