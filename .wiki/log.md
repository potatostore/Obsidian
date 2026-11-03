---
tags:
  - seed
aliases: []
created: 2026-09-25
---
# 위키 로그

추가만 하는 작업 기록. 형식: `## [YYYY-MM-DD] 종류 | 대상`

## [2026-09-25] setup | 대학생활 LLM 위키 초기 구성
- 스키마 `CLAUDE.md` 작성: 제자리 위키화, 삭제·이동 전 허락, 편집 전 백업 규칙
- 허브 14개 생성 (`Hub/`): 대학생활 → 학업·전공 지식(영역 지도 9개)·프로젝트·경험
- 기존 노트는 수정하지 않음. 허브에서 링크만 연결함 (일지·독서·창업 노트는 제외)
- `_wiki/index.md`, `_wiki/log.md`, `Experience/` 생성
- 추가 예정 허브: 독서, 진로·취업, 창업·아이디어, 일상·습관

## [2026-09-25] schema | Calendar 카테고리 추가
- 사용자 요청: 날짜 노트(할 일·경험 기록)를 그래프에서 Calendar 카테고리로 묶기
- `.obsidian-agent/wiki_calendar.py` 작성 → `Hub/Calendar.md` + `Calendar 2024/2025/2026` 생성 (날짜 노트 111개 연결, 노트 자체는 수정 안 함)
- `대학생활` 허브, `CLAUDE.md`(구조·Calendar 규칙·lint 항목), index 갱신

## [2026-09-25] setup | 한글 파일명 정규화
- `University/2-1`의 5개 파일(금융공학, 논리회로설계, 컴퓨터 자료구조, 컴퓨터구조, 컴퓨터실험2) 이름을 NFD → NFC로 바꿈 (사용자 허락, 내용 동일 확인, 원본 백업)

## [2026-09-25] ingest | 파일럿: 3-1 DB + ShoppingMall + 9월 날짜 노트
- 제자리 위키화: [[DB]] (type/course), [[ShoppingMall - 트러블 슈팅 기록]] (type/project), [[copilot-addendum]] (태그만), [[2026-09-16]]·[[2026-09-17]] (frontmatter + type/journal), [[DB(DataBase)]]·[[ORM(Oriented Relational Mapping)]]·[[Redis]] (type/concept)
- 새 개념 페이지: [[트랜잭션]], [[무결성 제약조건]] (수업 ↔ 프로젝트를 잇는 다리)
- 새 경험 페이지 7개 (`Experience/`), [[경험]]·[[데이터베이스 지도]] 허브 갱신
- 틀린 지식 목록을 사용자에게 보고함 (본문은 수정하지 않음, 승인 대기)
- 스키마 보완: 오류는 보고 후 승인 시 수정, 콜아웃 줄 종류, AI 덧붙임 파일 규칙, NFC 파일명 규칙

## [2026-09-25] schema | ingest 대상 찾기 규칙
- 대상 미지정 시 마지막 ingest 이후 바뀐 노트를 찾아 목록부터 보여주도록 추가. 노트 작성은 자유, ingest는 사후 작업임을 명시

## [2026-09-27] schema | 위키 관리 파일 숨기기
- 사용자 요청: `_wiki/` → `.wiki/`, `CLAUDE.md` → `.claude/CLAUDE.md`로 이동 (Obsidian은 점 폴더를 무시함)
- 스키마 안의 경로 갱신, 그래프 필터(`-path:"_wiki" -file:"CLAUDE"`) 제거
- 이동 전 원본은 `.obsidian-agent/cache/wiki-backup/2026-09-27/`에 백업

## [2026-10-16] ingest | 웹프로그래밍 중간고사 범위 강의자료
- 새 과목 페이지: [[웹프로그래밍]] (type/course), 사용자가 만든 빈 파일을 채움. 출처는 강의자료 PDF 3~5장(97쪽)
- 슬라이드 밖 내용은 (보충) 표시. organizer 태그 오인을 피하려고 # 바로 뒤 글자는 &#35; 엔티티로 씀
- [[학업]] 3-2에 링크 추가, index에 3-2 과목 섹션 추가

## [2026-11-02] ingest | ShoppingMall - TODO 새 페이지
- 사용자 요청으로 Project/ShoppingMall/ShoppingMall - TODO.md 생성 (type/project). 근거는 ShoppingMall 저장소 main 1e1e7f3과 docs/claude-work-log/ 기록
- [[프로젝트]] 허브의 ShoppingMall 섹션과 index 프로젝트 섹션에 링크 추가
- 클라우드 세션(Linux)에서 커밋: 새 파일명이 ASCII라 NFC/NFD 중복 위험 없음, 기존 파일은 내용만 수정. 편집 전 원본은 .obsidian-agent/cache/wiki-backup/2026-11-02/에 백업

## [2026-11-02] ingest | ShoppingMall - TODO 재구성
- 사용자 요청: 섹션을 작업 성격별(바로 할 일 / 결정 필요 / 테스트 / 기능 개발 / 인프라·데이터 / 정리)로 다시 나눔. 항목 내용은 유지, 정책 결정이 필요한 항목(멀티 디바이스, 탈퇴·삭제, 비밀번호 찾기)은 결정 필요로 이동
- 편집 전 원본은 .obsidian-agent/cache/wiki-backup/2026-11-02/Project/ShoppingMall/에 백업

## [2026-11-02] ingest | ShoppingMall - TODO 갱신 (PR 25)
- 4번 기능 개발 9개 항목을 PR 25 구현 완료로 체크, 1번에 "PR 25 머지 후" 할 일(로컬 DB 조치, E2E, API 명세서 반영) 추가, 5번에 다중 서버 스케줄러 항목 추가
- 편집 전 원본은 .obsidian-agent/cache/wiki-backup/2026-11-02/Project/ShoppingMall/ShoppingMall - TODO.before-PR25.md

## [2026-11-03] ingest | ShoppingMall - TODO 7번 추가
- PR 25 머지 반영(1번 체크), 타사 쇼핑몰 비교로 7번 "기능 개발 2차" 추가(배송지·배송 상태 → 비밀번호 변경 → 쿠폰 → 포인트 → 리뷰 순서, 그다음·의존성 필요 항목), 1~5 뼈대 PR 26 기록
- 저장소 docs/claude-work-log 삭제(PR 26)에 맞춰 근거 링크를 PR 설명·git 이력으로 변경
- 편집 전 원본은 .obsidian-agent/cache/wiki-backup/2026-11-03/Project/ShoppingMall/에 백업
