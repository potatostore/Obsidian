#!/bin/bash

# Navigate to the Vault root directory (parent of .obsidian-agent)
CDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VAULT_DIR="$( dirname "$CDIR" )"
cd "$VAULT_DIR"

echo "=========================================================="
echo "      🔮 Obsidian Agent: Sync & Launch System 🔮"
echo "=========================================================="

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
elif [ "$LOCAL" = "$REMOTE" ]; then
    echo "✔ Vault is already up-to-date with GitHub."
elif [ "$LOCAL" = "$BASE" ]; then
    echo "🔄 Fetching new changes (Fast-Forward)..."
    git pull --rebase
elif [ "$REMOTE" = "$BASE" ]; then
    echo "✔ Local edits exist. Ready to sync on close."
else
    echo "⚠ Local and GitHub notes have diverged. Attempting auto-rebase..."
    if git pull --rebase; then
        echo "✔ Auto-rebase successful!"
    else
        echo "❌ Merge conflict detected! Please resolve conflicts before opening Obsidian."
        exit 1
    fi
fi

# 2. RUN: Launch Obsidian and Block until Terminated
echo "🚀 [2/3] Launching Obsidian... (Waiting for exit...)"
# The -W flag makes macOS wait until the process exits
open -W -a Obsidian

# 3. POST-RUN: Safe Auto-Sync (Add, Commit, and Push)
echo "📝 [3/3] Obsidian closed. Checking for modifications..."

# Get current branch
BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")

if [[ -n $(git status --porcelain) ]]; then
    echo "✨ Modifications detected! Staging files..."
    git add .
    
    COMMIT_MSG="chore(sync): auto-sync on close from $(hostname -s) [$(date '+%Y-%m-%d %H:%M:%S')]"
    git commit -m "$COMMIT_MSG"
    
    echo "🚀 Pushing changes to GitHub ($BRANCH)..."
    if git push origin "$BRANCH"; then
        echo "✔ Success! Vault successfully synced and backed up."
    else
        echo "❌ Push failed! Check your network connection. Local changes are committed safely."
    fi
else
    echo "✔ No modifications made. Vault is clean."
fi
echo "=========================================================="
