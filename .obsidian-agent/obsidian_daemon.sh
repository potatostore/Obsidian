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

WAS_RUNNING=0

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Obsidian Daemon Started. Monitoring process..."

while true; do
    # Check if Obsidian is running in the process list
    if pgrep -x "Obsidian" > /dev/null; then
        if [ $WAS_RUNNING -eq 0 ]; then
            # Obsidian has just been launched!
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Obsidian launch detected! Initiating pull sync..."
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
                    notify "❌ 동기화 충돌 발생! 터미널에서 충돌을 수동으로 해결해야 합니다." "Basso"
                fi
            fi
            
            WAS_RUNNING=1
        fi
    else
        if [ $WAS_RUNNING -eq 1 ]; then
            # Obsidian has just closed!
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Obsidian exit detected! Initiating push sync..."
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
