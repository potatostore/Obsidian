#!/bin/bash

# Navigate to the Vault root directory (parent of .obsidian-agent)
CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_DIR="$( dirname "$CDIR" )"
cd "$VAULT_DIR"

# Helper function to send macOS native notifications
notify() {
    local title="🔮 Obsidian Sync"
    local message="$1"
    local sound="$2"
    if [ -n "$sound" ]; then
        osascript -e "display notification \"$message\" with title \"$title\" sound name \"$sound\""
    else
        osascript -e "display notification \"$message\" with title \"$title\""
    fi
}

echo "=========================================================="
echo "      🔮 Obsidian Agent: Sync & Launch System 🔮"
echo "=========================================================="

notify "🔄 GitHub에서 최신 메모 동기화 중..."

# 1. PRE-RUN: Safety Sync (Pull and Rebase)
echo "🔄 [1/3] Syncing latest notes from GitHub..."
git fetch origin

# Check local vs remote status
LOCAL=$(git rev-parse @ 2>/dev/null)
REMOTE=$(git rev-parse @{u} 2>/dev/null)
BASE=$(git merge-base @ @{u} 2>/dev/null)

if [ -z "$LOCAL" ] || [ -z "$REMOTE" ]; then
    echo "⚠ Git tracking is not fully configured or remote is missing. Pulling default..."
    git pull
    notify "✔ 동기화 준비 완료. 옵시디언을 실행합니다."
elif [ "$LOCAL" = "$REMOTE" ]; then
    echo "✔ Vault is already up-to-date with GitHub."
    notify "✔ 최신 버정입니다. 옵시디언을 실행합니다."
elif [ "$LOCAL" = "$BASE" ]; then
    echo "🔄 Fetching new changes (Fast-Forward)..."
    git pull --rebase
    notify "🔄 새 메모 다운로드 완료! 옵시디언을 실행합니다."
elif [ "$REMOTE" = "$BASE" ]; then
    echo "✔ Local edits exist. Ready to sync on close."
    notify "✔ 로컬 변경사항이 존재합니다. 종료 시 업로드됩니다."
else
    echo "⚠ Local and GitHub notes have diverged. Attempting auto-rebase..."
    if git pull --rebase; then
        echo "✔ Auto-rebase successful!"
        notify "🔄 병합 완료! 옵시디언을 실행합니다."
    else
        echo "❌ Merge conflict detected! Please resolve conflicts before opening Obsidian."
        notify "❌ 동기화 충돌 발생! 터미널에서 충돌을 해결해 주세요." "Basso"
        exit 1
    fi
fi

# 2. RUN: Launch Obsidian and Block until Terminated
echo "🚀 [2/3] Launching Obsidian... (Waiting for exit...)"
# The -W flag makes macOS wait until the process exits
open -W -a Obsidian

# 3. POST-RUN: Safe Auto-Sync (Add, Commit, and Push)
echo "📝 [3/3] Obsidian closed. Checking for modifications..."
notify "📝 옵시디언 종료됨. 변경사항 스캔 중..."

# Get current branch
BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")

if [[ -n $(git status --porcelain) ]]; then
    echo "✨ Modifications detected! Staging files..."
    git add .
    
    COMMIT_MSG="chore(sync): auto-sync on close from $(hostname -s) [$(date '+%Y-%m-%d %H:%M:%S')]"
    git commit -m "$COMMIT_MSG"
    
    echo "🚀 Pushing changes to GitHub ($BRANCH)..."
    notify "🚀 변경사항을 GitHub에 업로드 중..."
    
    if git push origin "$BRANCH"; then
        echo "✔ Success! Vault successfully synced and backed up."
        notify "✔ 동기화 성공! 모든 메모가 GitHub에 안전하게 저장되었습니다." "Glass"
    else
        echo "❌ Push failed! Check your network connection. Local changes are committed safely."
        notify "❌ 업로드 실패! 네트워크를 확인해 주세요. 로컬에는 안전하게 저장되었습니다." "Basso"
    fi
else
    echo "✔ No modifications made. Vault is clean."
    notify "✔ 변경사항이 없습니다. 동기화를 종료합니다."
fi
echo "=========================================================="

