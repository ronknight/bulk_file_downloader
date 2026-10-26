#!/bin/bash
# Archive the project into a timestamped snapshot under archive/.
# Usage: ./archive-project.sh [project_path] [archive_path]

PROJECT_PATH="${1:-.}"
ARCHIVE_PATH="${2:-./archive}"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
ARCHIVE_FOLDER="$ARCHIVE_PATH/$TIMESTAMP"

mkdir -p "$ARCHIVE_PATH"
if [ -d "$ARCHIVE_FOLDER" ]; then
    echo "Archive directory already exists: $ARCHIVE_FOLDER"
    exit 1
fi
mkdir -p "$ARCHIVE_FOLDER"

EXCLUDE_PATTERNS=(".git" "archive" ".venv" "__pycache__" "*.pyc" ".DS_Store" "node_modules" "target" "build" "dist")

should_exclude() {
    local item="$1"
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        case "$item" in
            $pattern) return 0 ;;
        esac
    done
    return 1
}

cd "$PROJECT_PATH" || exit 1
total_items=0
for item in * .*; do
    [ "$item" = "." ] || [ "$item" = ".." ] && continue
    [ ! -e "$item" ] && continue
    should_exclude "$item" && continue
    if [ -d "$item" ]; then cp -r "$item" "$ARCHIVE_FOLDER/"; else cp "$item" "$ARCHIVE_FOLDER/"; fi
    ((total_items++))
done

echo "Archive created at: $ARCHIVE_FOLDER ($total_items items)"
