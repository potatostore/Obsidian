#!/usr/bin/env python3
"""대학생활 LLM 위키 — Calendar 허브 자동 생성기.

-Calendar- 폴더의 날짜 노트(YYYY-MM-DD.md)를 모두 찾아
Hub/Calendar.md 와 Hub/Calendar <연도>.md 를 다시 만든다.
그래프에서 날짜 노트들이 Calendar → 연도 → 날짜로 한 덩어리로 묶이게 하기 위함.

사용법 (볼트 어디서든):  python3 .obsidian-agent/wiki_calendar.py
- 날짜 노트 자체는 절대 수정하지 않는다 (읽기만 함).
- 생성되는 허브 파일은 이 스크립트가 소유하므로 손으로 편집하지 않는다.
"""
import os, re, sys, unicodedata, datetime, collections

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL_DIR = os.path.join(VAULT, '-Calendar-')
HUB_DIR = os.path.join(VAULT, 'Hub')
DATE_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
N = lambda s: unicodedata.normalize('NFC', s)


def existing_created(path, default):
    """기존 허브의 created 값을 유지한다."""
    try:
        with open(path, encoding='utf-8') as f:
            m = re.search(r'^created:\s*(\S+)', f.read(), re.M)
            if m:
                return m.group(1)
    except FileNotFoundError:
        pass
    return default


def write_hub(name, body, today):
    path = os.path.join(HUB_DIR, name + '.md')
    created = existing_created(path, today)
    text = ("---\ntags:\n  - seed\n  - type/hub\naliases: []\n"
            f"created: {created}\n---\n" + body.rstrip() + '\n')
    old = None
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            old = f.read()
    if old != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(('updated ' if old else 'created ') + name)
    else:
        print('unchanged ' + name)


def main():
    today = datetime.date.today().isoformat()
    by_year = collections.defaultdict(lambda: collections.defaultdict(list))
    others = []
    for root, dirs, files in os.walk(CAL_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if not f.endswith('.md'):
                continue
            stem = N(f[:-3])
            m = DATE_RE.match(stem)
            if m:
                by_year[m.group(1)][int(m.group(2))].append(stem)
            else:
                others.append(N(os.path.relpath(os.path.join(root, f), VAULT))[:-3])
    os.makedirs(HUB_DIR, exist_ok=True)

    years = sorted(by_year)
    note = "> 자동 생성 페이지 — `python3 .obsidian-agent/wiki_calendar.py`로 갱신. 직접 편집하지 마세요.\n"

    # --- Calendar (최상위)
    body = ("# 📅 Calendar\n\n날짜별 노트 모음. 그날의 할 일(TODO)과 겪은 일을 적은 기록이며, "
            "[[경험]] 페이지의 원천이 된다. 상위: [[대학생활]]\n\n" + note + "\n## 연도\n")
    for y in years:
        months = sorted(by_year[y])
        cnt = sum(len(v) for v in by_year[y].values())
        body += f"- [[Calendar {y}]] — {cnt}개 ({months[0]}월~{months[-1]}월)\n"
    total = sum(len(v) for y in by_year.values() for v in y.values())
    body += f"\n총 {total}개\n"
    if others:
        body += "\n## 기타 (날짜 형식이 아닌 노트)\n" + '\n'.join(f"- [[{o}]]" for o in sorted(others)) + '\n'
    write_hub('Calendar', body, today)

    # --- 연도별
    for y in years:
        body = f"# 📅 Calendar {y}\n\n{y}년 날짜 노트. 상위: [[Calendar]]\n\n" + note
        for mth in sorted(by_year[y]):
            days = sorted(by_year[y][mth])
            links = ' · '.join(f"[[{d}|{d[-2:]}일]]" for d in days)
            body += f"\n## {mth}월 ({len(days)}개)\n{links}\n"
        write_hub(f'Calendar {y}', body, today)


if __name__ == '__main__':
    sys.exit(main())
