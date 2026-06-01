#!/usr/bin/env python3
import os
import re
import json
import argparse
from datetime import datetime

# Regexes for parsing markdown
WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
TAG_RE = re.compile(r'(?<!\w)#([a-zA-Z가-힣0-9_\-/]+)')
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def parse_simple_yaml(yaml_str):
    """A zero-dependency parser for basic frontmatter YAML."""
    data = {}
    lines = yaml_str.split('\n')
    current_key = None
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Check for list items
        if line.startswith('-'):
            val = line[1:].strip().strip('"\'')
            if current_key and isinstance(data.get(current_key), list):
                data[current_key].append(val)
            continue
            
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            
            # Check if it starts a list
            if val == '' or val == '[]':
                data[key] = []
                current_key = key
            elif val.startswith('[') and val.endswith(']'):
                # Simple inline list parsing
                items = [x.strip().strip('"\'') for x in val[1:-1].split(',') if x.strip()]
                data[key] = items
                current_key = None
            else:
                # Standard key-value
                # Remove quotes
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                data[key] = val
                current_key = None
    return data

def dump_simple_yaml(data):
    """A zero-dependency dumper for basic frontmatter YAML."""
    lines = ["---"]
    for k, v in data.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)

class ObsidianNote:
    def __init__(self, filepath, relpath):
        self.filepath = filepath
        self.relpath = relpath
        self.title = os.path.splitext(os.path.basename(filepath))[0]
        self.content = ""
        self.frontmatter = {}
        self.tags = set()
        self.links = set()
        self.has_frontmatter = False
        self.body_content = ""
        
        self.parse_note()

    def parse_note(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except Exception as e:
            print(f"⚠ Failed to read {self.relpath}: {e}")
            return

        # Extract frontmatter
        match = FRONTMATTER_RE.match(self.content)
        if match:
            self.has_frontmatter = True
            fm_str = match.group(1)
            self.body_content = self.content[match.end():]
            try:
                self.frontmatter = parse_simple_yaml(fm_str)
            except Exception as e:
                print(f"⚠ YAML parse error in {self.relpath}: {e}")
                self.frontmatter = {}
        else:
            self.has_frontmatter = False
            self.body_content = self.content

        # Extract tags from frontmatter
        if 'tags' in self.frontmatter:
            tags_val = self.frontmatter['tags']
            if isinstance(tags_val, list):
                for t in tags_val:
                    self.tags.add(t.strip('#'))
            elif isinstance(tags_val, str):
                for t in tags_val.split(','):
                    self.tags.add(t.strip().strip('#'))

        # Extract tags from body text
        body_tags = TAG_RE.findall(self.body_content)
        for t in body_tags:
            # Filter out things that look like HEX codes or are inside codeblocks if possible
            # (Simple tag check: not purely numerical and not header syntax)
            if not t.isdigit():
                self.tags.add(t)

        # Extract wikilinks from body text
        links = WIKILINK_RE.findall(self.body_content)
        for link in links:
            self.links.add(link.strip())

class VaultOrganizer:
    def __init__(self, vault_path, dry_run=True):
        self.vault_path = os.path.abspath(vault_path)
        self.dry_run = dry_run
        self.notes = {} # title -> ObsidianNote
        
        # Load formatting rules
        self.rules_path = os.path.join(self.vault_path, ".obsidian-agent", "formatting_rules.md")
        self.rules = self.load_rules()
        
    def load_rules(self):
        """Parses the formatting_rules.md file inside .obsidian-agent/ to read status."""
        enabled_rules = {
            "RULE_HEADING_SPACE": True,
            "RULE_REQUIRED_FRONTMATTER": True,
            "RULE_HIGHLIGHT_SPACES": True
        }
        
        if not os.path.exists(self.rules_path):
            return enabled_rules
            
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for rule in enabled_rules:
                # Find RULE_ID and check status (Enabled vs Disabled)
                pattern = rf'{rule}.*?(?:Status|상태):\s*`\[(Enabled|Disabled)\]`'
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    status = match.group(1).strip().lower()
                    enabled_rules[rule] = (status == "enabled")
        except Exception as e:
            print(f"⚠ Error loading rules from formatting_rules.md: {e}")
            
        return enabled_rules

    def format_body_text(self, body):
        """Applies formatting rules to the body text line-by-line, respecting code blocks."""
        rule_heading = self.rules.get("RULE_HEADING_SPACE", True)
        rule_highlight = self.rules.get("RULE_HIGHLIGHT_SPACES", True)
        
        if not rule_heading and not rule_highlight:
            return body
            
        lines = body.split('\n')
        new_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue
                
            if not in_code_block:
                # 1. Heading Space Correction: e.g. '#대제목' -> '# 대제목'
                if rule_heading:
                    # Match heading symbols (1 to 6 #) followed directly by non-space, non-hash character
                    match = re.match(r'^(#{1,6})([^#\s])(.*)$', line)
                    if match:
                        line = f"{match.group(1)} {match.group(2)}{match.group(3)}"
                
                # 2. Highlight Spaces Correction: e.g. '== 하이라이트 ==' -> '==하이라이트=='
                if rule_highlight:
                    # Strip leading/trailing spaces inside highlights
                    line = re.sub(r'==\s*([^\s=][^=]*[^\s=])\s*==', r'==\1==', line)
                    
            new_lines.append(line)
            
        return '\n'.join(new_lines)
        
    def scan_vault(self):
        print(f"🔍 Scanning vault in: {self.vault_path}")
        note_count = 0
        for root, dirs, files in os.walk(self.vault_path):
            # Ignore hidden folders (.git, .obsidian, .obsidian-agent)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, self.vault_path)
                    note = ObsidianNote(filepath, relpath)
                    self.notes[note.title] = note
                    note_count += 1
        print(f"✔ Scan complete. Found {note_count} markdown notes.")

    def analyze_graph_health(self):
        """Analyzes vault graph connection health."""
        print("\n📈 Vault Graph Health Analysis:")
        orphans = []
        dead_ends = []
        hubs = []
        
        # Build backlink mapping
        backlinks = {title: set() for title in self.notes}
        for title, note in self.notes.items():
            for target in note.links:
                if target in backlinks:
                    backlinks[target].add(title)

        for title, note in self.notes.items():
            out_count = len(note.links)
            in_count = len(backlinks[title])
            
            if out_count == 0 and in_count == 0:
                orphans.append(title)
            elif out_count == 0:
                dead_ends.append(title)
                
            if in_count >= 5: # Notes linked to by 5 or more other notes
                hubs.append((title, in_count))

        hubs.sort(key=lambda x: x[1], reverse=True)

        print(f"  • Total Notes: {len(self.notes)}")
        print(f"  • Orphan Notes (0 links in/out): {len(orphans)}")
        for o in orphans[:10]:
            print(f"    - [[{o}]]")
        if len(orphans) > 10:
            print(f"    ... and {len(orphans) - 10} more")
            
        print(f"  • Dead-end Notes (has backlinks but links to nothing): {len(dead_ends)}")
        for d in dead_ends[:5]:
            print(f"    - [[{d}]]")
            
        print(f"  • Popular Hub Notes (referenced by 5+ files): {len(hubs)}")
        for h, count in hubs[:5]:
            print(f"    - [[{h}]] ({count} references)")
            
        return {
            "orphans": orphans,
            "dead_ends": dead_ends,
            "hubs": hubs,
            "backlinks": backlinks
        }

    def standardize_metadata(self):
        """Standardizes frontmatter and body format in all notes based on rules (dry-run by default)."""
        print(f"\n🧹 Enforcing Formatting Rules (Dry-Run: {self.dry_run})...")
        print(f"  • Heading space formatting: {'[ON]' if self.rules.get('RULE_HEADING_SPACE') else '[OFF]'}")
        print(f"  • YAML metadata validation: {'[ON]' if self.rules.get('RULE_REQUIRED_FRONTMATTER') else '[OFF]'}")
        print(f"  • Highlight text formatting: {'[ON]' if self.rules.get('RULE_HIGHLIGHT_SPACES') else '[OFF]'}")
        
        modified_count = 0
        
        for title, note in self.notes.items():
            needs_update = False
            new_fm = dict(note.frontmatter)
            
            # 1. Apply Metadata Frontmatter Rules
            if self.rules.get("RULE_REQUIRED_FRONTMATTER", True):
                # Ensure 'tags' exists
                if 'tags' not in new_fm:
                    new_fm['tags'] = sorted(list(note.tags)) if note.tags else ['seed']
                    needs_update = True
                else:
                    current_fm_tags = set()
                    if isinstance(new_fm['tags'], list):
                        current_fm_tags = set(new_fm['tags'])
                    elif isinstance(new_fm['tags'], str):
                        current_fm_tags = set([t.strip() for t in new_fm['tags'].split(',') if t.strip()])
                    
                    merged_tags = sorted(list(current_fm_tags.union(note.tags)))
                    if not merged_tags:
                        merged_tags = ['seed']
                    if merged_tags != new_fm['tags']:
                        new_fm['tags'] = merged_tags
                        needs_update = True
                
                # Ensure 'aliases' list exists
                if 'aliases' not in new_fm:
                    new_fm['aliases'] = []
                    needs_update = True
                    
                # Ensure 'created' date exists
                if 'created' not in new_fm:
                    ctime = os.path.getctime(note.filepath)
                    date_str = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d')
                    new_fm['created'] = date_str
                    needs_update = True

            # 2. Apply Body Formatting Rules (Headings, Highlights)
            formatted_body = self.format_body_text(note.body_content)
            # Remove leading whitespace from body content
            formatted_body_cleaned = formatted_body.lstrip()
            orig_body_cleaned = note.body_content.lstrip()
            
            if formatted_body_cleaned != orig_body_cleaned:
                needs_update = True

            if needs_update:
                modified_count += 1
                
                # Reconstruct content
                if self.rules.get("RULE_REQUIRED_FRONTMATTER", True) or note.has_frontmatter:
                    fm_block = dump_simple_yaml(new_fm)
                    new_content = f"{fm_block}\n{formatted_body_cleaned}"
                else:
                    new_content = formatted_body_cleaned
                
                if self.dry_run:
                    print(f"  [DRY RUN] Would format note: [[{title}]]")
                else:
                    try:
                        with open(note.filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"  ✔ Formatted [[{title}]]")
                    except Exception as e:
                        print(f"  ❌ Error formatting [[{title}]]: {e}")
                        
        if self.dry_run:
            print(f"  [DRY RUN] Proposed formatting for {modified_count} notes.")
        else:
            print(f"  ✔ Finished formatting {modified_count} notes.")

def main():
    parser = argparse.ArgumentParser(description="Obsidian Vault Organizer Tool")
    parser.add_argument("--vault", type=str, default="..", help="Path to your Obsidian Vault (defaults to parent directory)")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Perform dry-run without writing changes")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Disable dry-run mode and write changes")
    parser.add_argument("--standardize", action="store_true", default=False, help="Run metadata standardizer")
    
    args = parser.parse_args()
    
    # Resolve default vault path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_path = args.vault
    if vault_path == "..":
        vault_path = os.path.dirname(script_dir)
        
    organizer = VaultOrganizer(vault_path, dry_run=args.dry_run)
    organizer.scan_vault()
    organizer.analyze_graph_health()
    
    if args.standardize:
        organizer.standardize_metadata()

if __name__ == "__main__":
    main()

