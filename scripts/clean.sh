#!/bin/bash

# Clean up intermediate files and build artifacts
# 中間ファイルやビルド成果物を削除
#
# Usage:
#   ./scripts/clean.sh              # 全プロジェクトをクリーンアップ
#   ./scripts/clean.sh --dry-run    # 削除候補のみ表示
#   ./scripts/clean.sh sample-compass          # sample-compass のみ
#   ./scripts/clean.sh sample-compass-ts       # sample-compass-ts のみ
#   ./scripts/clean.sh sample-compass-makecode # sample-compass-makecode のみ

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TARGET_DIR=""
DRY_RUN=false

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=true
      ;;
    sample-compass|sample-compass-ts|sample-compass-makecode)
      if [ -n "$TARGET_DIR" ]; then
        echo -e "${RED}❌ Error: Specify only one project target.${NC}"
        exit 1
      fi
      TARGET_DIR="$arg"
      ;;
    *)
      echo -e "${RED}❌ Error: Unknown argument: $arg${NC}"
      exit 1
      ;;
  esac
done

# Validate target directory if specified
if [ -n "$TARGET_DIR" ]; then
  FULL_PATH="$PROJECT_ROOT/$TARGET_DIR"
  if [ ! -d "$FULL_PATH" ]; then
    echo -e "${RED}❌ Error: Directory not found: $TARGET_DIR${NC}"
    echo ""
    echo -e "${BLUE}Valid targets:${NC}"
    echo "  ./scripts/clean.sh                        # Clean all projects"
    echo "  ./scripts/clean.sh sample-compass         # Clean Python project"
    echo "  ./scripts/clean.sh sample-compass-ts      # Clean TypeScript project"
    echo "  ./scripts/clean.sh sample-compass-makecode # Clean MakeCode project"
    exit 1
  fi
  SEARCH_PATH="$FULL_PATH"
  TARGET_NAME="$TARGET_DIR"
else
  SEARCH_PATH="$PROJECT_ROOT"
  TARGET_NAME="all projects"
fi

echo "🧹 Cleaning up intermediate files for: $TARGET_NAME"
if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}Dry run: no files will be removed.${NC}"
fi
echo ""

is_tracked_path() {
  local candidate="$1"
  local relative_path="${candidate#"$PROJECT_ROOT"/}"

  git -C "$PROJECT_ROOT" ls-files --error-unmatch -- "$relative_path" >/dev/null 2>&1
}

remove_candidate() {
  local candidate="$1"

  if is_tracked_path "$candidate"; then
    echo -e "${YELLOW}  Preserving tracked path: $candidate${NC}"
  elif [ "$DRY_RUN" = true ]; then
    echo "  Would remove: $candidate"
  elif [ -d "$candidate" ]; then
    rm -rf -- "$candidate"
    echo "  Removed: $candidate"
  else
    rm -f -- "$candidate"
    echo "  Removed: $candidate"
  fi
}

CLEANUP_BOUNDARY_NAMES=(
  "__pycache__"
  ".pytest_cache"
  ".ruff_cache"
  ".mypy_cache"
  "htmlcov"
  "*.egg-info"
  ".venv"
  "dist"
  "build"
  ".tox"
  "built"
  "node_modules"
  "pxt_modules"
  ".jest-cache"
  ".pxt"
  ".nyc_output"
  ".cache"
  "coverage"
)
CLEANUP_BOUNDARY_FIND_ARGS=()
for boundary_name in "${CLEANUP_BOUNDARY_NAMES[@]}"; do
  if [ "${#CLEANUP_BOUNDARY_FIND_ARGS[@]}" -gt 0 ]; then
    CLEANUP_BOUNDARY_FIND_ARGS+=( -o )
  fi
  CLEANUP_BOUNDARY_FIND_ARGS+=( -name "$boundary_name" )
done
unset boundary_name

cleanup_dir() {
  local dir="$1"
  local pattern="$2"
  local desc="$3"

  while IFS= read -r -d '' candidate; do
    echo -e "${BLUE}📂 $desc:${NC}"
    remove_candidate "$candidate"
  done < <(
    find "$dir" -maxdepth 10 \
      -path "$PROJECT_ROOT/.git" -prune -o \
      -type d -name "$pattern" -prune -print0 -o \
      -type d \( "${CLEANUP_BOUNDARY_FIND_ARGS[@]}" \) -prune 2>/dev/null
  )
}

cleanup_file() {
  local dir="$1"
  local pattern="$2"
  local desc="$3"

  while IFS= read -r -d '' candidate; do
    echo -e "${BLUE}📄 $desc:${NC}"
    remove_candidate "$candidate"
  done < <(
    find "$dir" -maxdepth 10 \
      -path "$PROJECT_ROOT/.git" -prune -o \
      -type d \( "${CLEANUP_BOUNDARY_FIND_ARGS[@]}" \) -prune -o \
      -type f -name "$pattern" -print0 2>/dev/null
  )
}

# Python cache files
echo -e "${YELLOW}Python Cache:${NC}"
cleanup_dir "$SEARCH_PATH" "__pycache__" "Python bytecode"
cleanup_dir "$SEARCH_PATH" ".pytest_cache" "pytest cache"
cleanup_dir "$SEARCH_PATH" ".ruff_cache" "Ruff cache"
cleanup_dir "$SEARCH_PATH" ".mypy_cache" "Mypy cache"
cleanup_file "$SEARCH_PATH" ".coverage" "coverage data"
cleanup_file "$SEARCH_PATH" "coverage.xml" "coverage XML report"
cleanup_dir "$SEARCH_PATH" "htmlcov" "HTML coverage reports"
cleanup_dir "$SEARCH_PATH" "*.egg-info" "egg-info"

# Virtual environments
echo ""
echo -e "${YELLOW}Virtual Environments:${NC}"
cleanup_dir "$SEARCH_PATH" ".venv" "virtual environment"

# Build artifacts
echo ""
echo -e "${YELLOW}Build Artifacts:${NC}"
cleanup_dir "$SEARCH_PATH" "dist" "dist directory"
cleanup_dir "$SEARCH_PATH" "build" "build directory"
cleanup_dir "$SEARCH_PATH" ".tox" "tox cache"
cleanup_dir "$SEARCH_PATH" "built" "MakeCode built directory"

# Node.js files
echo ""
echo -e "${YELLOW}Node.js:${NC}"
cleanup_dir "$SEARCH_PATH" "node_modules" "node_modules"
cleanup_dir "$SEARCH_PATH" "pxt_modules" "PXT dependencies"

# Cache files
echo ""
echo -e "${YELLOW}Cache:${NC}"
cleanup_dir "$SEARCH_PATH" ".jest-cache" "Jest cache"
cleanup_dir "$SEARCH_PATH" ".pxt" "PXT cache"
cleanup_dir "$SEARCH_PATH" ".nyc_output" "NYC cache"
cleanup_dir "$SEARCH_PATH" ".cache" "tool cache"
cleanup_dir "$SEARCH_PATH" "coverage" "coverage directory"

# IDE and OS files (only at project level, not root)
if [ -n "$TARGET_DIR" ]; then
  echo ""
  echo -e "${YELLOW}IDE & OS Files:${NC}"
  cleanup_dir "$SEARCH_PATH" ".vscode" ".vscode"
  cleanup_dir "$SEARCH_PATH" ".idea" ".idea"
  cleanup_file "$SEARCH_PATH" ".DS_Store" ".DS_Store"
fi

echo ""
if [ "$DRY_RUN" = true ]; then
  echo -e "${GREEN}✅ Cleanup preview complete!${NC}"
else
  echo -e "${GREEN}✅ Cleanup complete!${NC}"
fi
echo ""
echo -e "${BLUE}Remaining size:${NC}"
du -sh "$SEARCH_PATH" 2>/dev/null || true
echo ""
echo -e "${BLUE}To verify cleanup, run:${NC}"
echo "  find $SEARCH_PATH -name '__pycache__' -o -name '.pytest_cache' -o -name '.venv' -o -name 'node_modules' -o -name 'dist' | head -20"
