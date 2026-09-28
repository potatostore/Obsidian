#!/bin/bash

# Navigate to the Vault root directory
CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_DIR="$( dirname "$CDIR" )"
cd "$VAULT_DIR"

# Ensure cache directory exists for logs
mkdir -p "$CDIR/cache"

notify() {
    local title="🔮 Obsidian Sync Daemon"
    local message="$1"
    local sound="$2"
    if [ -n "$sound" ]; then
        osascript -e "display notification \"$message\" with title \"$title\" sound name \"$sound\""
    else
        osascript -e "display notification \"$message\" with title \"$title\""
    fi
}

# Returns 0 (true) when a rebase/merge/cherry-pick is mid-flight, or HEAD is
# detached (which also happens mid-rebase). In that state we must NOT run
# `git add`/`git commit`/`git pull` — doing so is what created the tangled
# history this patch fixes (auto-sync kept committing on top of an unresolved
# rebase every time Obsidian was opened/closed).
is_git_op_in_progress() {
    if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ] || \
       [ -f ".git/MERGE_HEAD" ] || [ -f ".git/CHERRY_PICK_HEAD" ]; then
        return 0
    fi
    if ! git symbolic-ref -q HEAD > /dev/null; then
        return 0
    fi
    return 1
}

WAS_RUNNING=0

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Obsidian Daemon Started. Monitoring process..."

while true; do
    # Check if Obsidian is running in the process list
    if pgrep -x "Obsidian" > /dev/null; then
        if [ $WAS_RUNNING -eq 0 ]; then
            # Obsidian has just been launched!
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Obsidian launch detected! Initiating pull sync..."

            if is_git_op_in_progress; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Skipped: a previous rebase/merge is still unresolved."
                notify "⏸️ 이전 동기화 충돌이 아직 해결되지 않았습니다. Working Copy 앱에서 직접 열어 해결해주세요." "Basso"
                WAS_RUNNING=1
                sleep 3
                continue
            fi

            notify "🔄 Obsidian이 실행되었습니다. GitHub에서 최신 메모를 동기화합니다..."

            git fetch origin

            LOCAL=$(git rev-parse @ 2>/dev/null)
            REMOTE=$(git rev-parse @{u} 2>/dev/null)
            BASE=$(git merge-base @ @{u} 2>/dev/null)

            if [ -z "$LOCAL" ] || [ -z "$REMOTE" ]; then
                git pull
                notify "✔ 동기화 완료! 즐거운 메모 시간 되세요."
            elif [ "$LOCAL" = "$REMOTE" ]; then
                notify "✔ 보관소가 이미 최신 버전 상태입니다."
            elif [ "$LOCAL" = "$BASE" ]; then
                git pull --rebase
                notify "🔄 새 메모 다운로드 완료! 보관소가 최신화되었습니다."
            else
                # Attempt auto-rebase
                if git pull --rebase; then
                    notify "✔ 자동 병합 성공! 최신 메모가 로드되었습니다."
                else
                    notify "❌ 동기화 충돌 발생! Working Copy 앱에서 직접 열어 충돌을 수동으로 해결해야 합니다. 해결 전까지 자동 동기화는 건너뜁니다." "Basso"
                fi
            fi

            WAS_RUNNING=1
        fi
    else
        if [ $WAS_RUNNING -eq 1 ]; then
            # Obsidian has just closed!
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Obsidian exit detected! Initiating push sync..."

            if is_git_op_in_progress; then
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] Skipped: a rebase/merge is still unresolved, refusing to commit/push on top of it."
                notify "⏸️ 이전 동기화 충돌이 아직 해결되지 않아 자동 커밋을 건너뛰었습니다. Working Copy 앱에서 직접 해결해주세요." "Basso"
                WAS_RUNNING=0
                sleep 3
                continue
            fi

            notify "📝 Obsidian이 종료되었습니다. 변경사항 스캔 및 업로드를 시작합니다..."

            BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")
            
            if [[ -n $(git status --porcelain) ]]; then
                git add .
                COMMIT_MSG="chore(sync): auto-sync on close from $(hostname -s) [$(date '+%Y-%m-%d %H:%M:%S')]"
                git commit -m "$COMMIT_MSG"
                
                if git push origin "$BRANCH"; then
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Auto-push successful!"
                    notify "✔ 동기화 성공! 모든 메모가 GitHub에 안전하게 백업되었습니다." "Glass"
                else
                    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push failed!"
                    notify "❌ 업로드 실패! 인터넷을 확인하세요. 로컬에는 안전하게 저장되었습니다." "Basso"
                fi
            else
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] No modifications found."
                notify "✔ 변경사항이 없습니다. 백그라운드 동기화를 완료합니다."
            fi
            
            WAS_RUNNING=0
        fi
    fi
    
    # Poll every 3 seconds to preserve CPU cycles
    sleep 3
done
