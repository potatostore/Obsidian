#!/usr/bin/env python3
import os
import re
from collections import Counter
from organizer import ObsidianNote, VaultOrganizer

# Stopwords/Filter to ignore date files or generic non-review notes when learning standard keys
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

class StyleLearner:
    def __init__(self, vault_path):
        self.vault_path = os.path.abspath(vault_path)
        self.organizer = VaultOrganizer(self.vault_path)
        self.rules_path = os.path.join(self.vault_path, ".obsidian-agent", "formatting_rules.md")
        
    def learn_style(self):
        self.organizer.scan_vault()
        
        if not self.organizer.notes:
            print("⚠ 스캔할 메모가 존재하지 않습니다.")
            return

        print("\n🧠 회원님의 메모 작성 스타일을 분석하는 중...")

        # 1. Analyze YAML keys
        all_keys = []
        yaml_note_count = 0
        for title, note in self.organizer.notes.items():
            # Skip daily note patterns if they pollute standard book/knowledge metadata
            if DATE_PATTERN.match(title):
                continue
            if note.has_frontmatter:
                yaml_note_count += 1
                all_keys.extend(note.frontmatter.keys())
                
        key_counts = Counter(all_keys)
        # Standard keys are keys that appear in at least 15% of notes with YAML frontmatter
        threshold = max(2, int(yaml_note_count * 0.15))
        standard_keys = [key for key, count in key_counts.items() if count >= threshold]
        
        # 2. Analyze Heading styles
        # Count headings with space (e.g. "# Heading") vs without space (e.g. "#Heading")
        heading_with_space = 0
        heading_without_space = 0
        
        # Regex to detect hashtags vs headings
        # Heading: starts with 1-6 '#' followed by space
        # Hashtag: starts with '#' followed directly by words, no spaces
        for title, note in self.organizer.notes.items():
            lines = note.body_content.split('\n')
            in_code_block = False
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                
                # Check markdown headers
                # We identify headers by looking at # at start of line
                if line.strip().startswith('#'):
                    # Check if there is a space after the '#' symbols
                    match = re.match(r'^(#{1,6})(\s+)(.*)$', line.strip())
                    if match:
                        heading_with_space += 1
                    else:
                        # Check if it starts with '#' and contains a space later (which means it was probably a heading without space)
                        # e.g., "#1. Intro"
                        match_no_space = re.match(r'^(#{1,6})([^#\s]+)\s+(.*)$', line.strip())
                        if match_no_space:
                            heading_without_space += 1

        # 3. Analyze Highlight styles
        highlight_with_space = 0
        highlight_without_space = 0
        
        for title, note in self.organizer.notes.items():
            # Find highlights ==text== vs == text ==
            # highlight with space: == text ==
            h_spaces = re.findall(r'==\s+[^=]+\s+==', note.body_content)
            # highlight without space: ==text==
            h_no_spaces = re.findall(r'==[^\s=][^=]*[^\s=]==', note.body_content)
            
            highlight_with_space += len(h_spaces)
            highlight_without_space += len(h_no_spaces)

        # 4. Determine Dominant Styles & Generate Rules
        print("✔ 분석이 완료되었습니다. 스타일 프로필:")
        
        # Heading decision
        total_headings = heading_with_space + heading_without_space
        prefer_heading_space = True
        if total_headings > 0:
            space_ratio = heading_with_space / total_headings
            print(f"  • 제목 작성 방식: 공백 있음 ({heading_with_space}회) vs 공백 없음 ({heading_without_space}회) [비율: {space_ratio:.1%}]")
            if space_ratio < 0.5:
                prefer_heading_space = False
        else:
            print("  • 제목 작성 방식: 감지된 제목 없음 (공백 있음 기본값 설정)")
            
        # Highlight decision
        total_highlights = highlight_with_space + highlight_without_space
        prefer_highlight_no_space = True
        if total_highlights > 0:
            no_space_ratio = highlight_without_space / total_highlights
            print(f"  • 하이라이트 방식: 공백 없음 ({highlight_without_space}회) vs 공백 있음 ({highlight_with_space}회) [비율: {no_space_ratio:.1%}]")
            if no_space_ratio < 0.5:
                prefer_highlight_no_space = False
        else:
            print("  • 하이라이트 방식: 감지된 하이라이트 없음 (공백 없음 기본값 설정)")

        print(f"  • 가장 많이 감지된 메타데이터(YAML) 키들: {', '.join(standard_keys)}")

        # 5. Write the formatting_rules.md based on parsed style
        self.generate_rules_file(standard_keys, prefer_heading_space, prefer_highlight_no_space)
        print(f"\n✔ 회원님의 고유 스타일에 맞춘 룰셋이 생성되었습니다: `.obsidian-agent/formatting_rules.md`")
        
        # 6. Search for Outliers
        self.report_outliers(standard_keys, prefer_heading_space, prefer_highlight_no_space)

    def generate_rules_file(self, yaml_keys, prefer_heading_space, prefer_highlight_no_space):
        heading_status = "[Enabled]" if prefer_heading_space else "[Disabled]"
        highlight_status = "[Enabled]" if prefer_highlight_no_space else "[Disabled]"
        
        formatted_keys = "\n".join([f"        - `{key}`: 회원님의 빈출 메타데이터" for key in yaml_keys])
        
        rules_content = f"""# 🔮 회원님 맞춤형 Obsidian 작성 규칙 (Formatting Rules)

이 파일은 에이전트가 회원님의 기존 작성 습관(Style)을 학습하여 **자동으로 추출한 고유 규칙 정의서**입니다.
이 룰셋을 바탕으로 규격에서 벗어난 "아웃라이어(Outlier)" 노트들을 탐색하고 안전하게 교정합니다.

---

## 🏁 1. 제목 문법 규칙 (Heading Rules)

*   **규칙 ID**: `RULE_HEADING_SPACE`
    *   **설명**: `#`, `##` 등 제목 표시용 샵 뒤에 공백이 없는 오류(예: `#1. 개요`)를 자동으로 감지해 공백을 추가(`# 1. 개요`)합니다. 
    *   **주의**: `#대제목`이나 `#단어`처럼 뒤에 공백이 전혀 없고 본문에 단독으로 적혀 검색 태그로 동작하는 해시태그는 절대 건드리지 않고 원본을 안전하게 보호합니다.
    *   **상태**: `{heading_status}`

---

## 🏁 2. 메타데이터 필수 규칙 (Metadata Rules)

*   **규칙 ID**: `RULE_REQUIRED_FRONTMATTER`
    *   **설명**: 모든 지식 노트 상단에 회원님이 가장 자주 쓰시는 필수 YAML Frontmatter 규격을 확보합니다.
    *   **회원님 보관소 맞춤형 필수 항목**:
{formatted_keys}
    *   **기본 주입 항목**:
        *   `tags`: 누락 시 `[seed]` 자동 주입
        *   `aliases`: 누락 시 `[]` 자동 주입
        *   `created`: 누락 시 파일 최초 작성일(`YYYY-MM-DD`) 자동 주입
    *   **상태**: `[Enabled]`

---

## 🏁 3. 하이라이트 문법 규칙 (Highlight Rules)

*   **규칙 ID**: `RULE_HIGHLIGHT_SPACES`
    *   **설명**: 하이라이트 표시 기호(`==`) 내부 양끝의 공백을 제거하여 렌더링 오차를 방지합니다.
    *   **작동 예시**: `== 하이라이트 ==` ➡️ `==하이라이트==`
    *   **상태**: `{highlight_status}`
"""
        with open(self.rules_path, 'w', encoding='utf-8') as f:
            f.write(rules_content)

    def report_outliers(self, yaml_keys, check_heading, check_highlight):
        print("\n🔍 회원님의 규칙에서 벗어난 아웃라이어(Outlier) 노트 스캔 결과:")
        outlier_count = 0
        
        for title, note in self.organizer.notes.items():
            if DATE_PATTERN.match(title):
                continue
                
            reasons = []
            
            # YAML Key check
            if note.has_frontmatter:
                missing_keys = [k for k in yaml_keys if k not in note.frontmatter]
                if missing_keys:
                    reasons.append(f"필수 메타데이터 누락 ({', '.join(missing_keys)})")
            else:
                reasons.append("YAML 메타데이터 블록(Frontmatter) 없음")
                
            # Heading Spacing Outliers
            if check_heading:
                lines = note.body_content.split('\n')
                in_code_block = False
                for line in lines:
                    if line.strip().startswith('```'):
                        in_code_block = not in_code_block
                        continue
                    if in_code_block:
                        continue
                    # Check if it looks like a heading without space
                    match = re.match(r'^(#{1,6})([^#\s]+)\s+(.*)$', line.strip())
                    if match:
                        reasons.append(f"제목 공백 오류: `{line.strip()}`")
                        break

            # Highlight Spacing Outliers
            if check_highlight:
                h_spaces = re.findall(r'==\s+[^=]+\s+==', note.body_content)
                if h_spaces:
                    reasons.append(f"하이라이트 공백 오류 ({len(h_spaces)}곳)")

            if reasons:
                outlier_count += 1
                print(f"  [{outlier_count}] [[{title}]]")
                for r in reasons:
                    print(f"      ↳ {r}")
                if outlier_count >= 10:
                    print(f"      ...외에 {len(self.organizer.notes) - outlier_count}개의 노트가 더 감지되었습니다.")
                    break
                    
        print(f"\n💡 위 리스트는 회원님의 고유 스타일에 부합하지 않는 아웃라이어 후보입니다.")
        print(f"   `python3 .obsidian-agent/organizer.py --standardize --no-dry-run`을 실행하면")
        # Update the rules status dictionary in VaultOrganizer
        print("   위 아웃라이어 노트들이 자동으로 학습된 룰셋에 맞게 완벽하게 교정됩니다!")

if __name__ == "__main__":
    import sys
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault = os.path.dirname(script_dir)
    if len(sys.argv) > 1:
        vault = sys.argv[1]
    learner = StyleLearner(vault)
    learner.learn_style()
