#!/bin/bash

# Clean up intermediate files and build artifacts
# 中間ファイルやビルド成果物を削除
#
# Usage:
#   ./scripts/clean.sh              # 全プロジェクトをクリーンアップ
#   ./scripts/clean.sh sample-compass          # sample-compass のみ
#   ./scripts/clean.sh sample-compass-ts       # sample-compass-ts のみ
#   ./scripts/clean.sh sample-compass-makecode # sample-compass-makecode のみ

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="${1:-}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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
echo ""

cleanup_dir() {
  local dir="$1"
  local pattern="$2"
  local desc="$3"
  
  if find "$dir" -maxdepth 10 -name "$pattern" -type d 2>/dev/null | grep -q .; then
    echo -e "${BLUE}📂 Removing $desc...${NC}"
    find "$dir" -maxdepth 10 -name "$pattern" -type d -exec rm -rf {} + 2>/dev/null || true
  fi
}

cleanup_file() {
  local dir="$1"
  local pattern="$2"
  local desc="$3"
  
  if find "$dir" -maxdepth 10 -name "$pattern" -type f 2>/dev/null | grep -q .; then
    echo -e "${BLUE}📄 Removing $desc...${NC}"
    find "$dir" -maxdepth 10 -name "$pattern" -type f -delete 2>/dev/null || true
  fi
}

# Python cache files
echo -e "${YELLOW}Python Cache:${NC}"
cleanup_dir "$SEARCH_PATH" "__pycache__" "Python bytecode"
cleanup_dir "$SEARCH_PATH" ".pytest_cache" "pytest cache"
cleanup_file "$SEARCH_PATH" ".coverage" "coverage data"
cleanup_dir "$SEARCH_PATH" "htmlcov" "HTML coverage reports"
cleanup_dir "$SEARCH_PATH" ".egg-info" "egg-info"

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
cleanup_file "$SEARCH_PATH" "package-lock.json" "package-lock.json"
cleanup_file "$SEARCH_PATH" "pnpm-lock.yaml" "pnpm-lock.yaml"

# Cache files
echo ""
echo -e "${YELLOW}Cache:${NC}"
cleanup_dir "$SEARCH_PATH" ".jest-cache" "Jest cache"
cleanup_dir "$SEARCH_PATH" ".pxt" "PXT cache"
cleanup_dir "$SEARCH_PATH" "coverage" "coverage directory"

# IDE and OS files (only at project level, not root)
if [ -n "$TARGET_DIR" ]; then
  echo ""
  echo -e "${YELLOW}IDE & OS Files:${NC}"
  cleanup_dir "$SEARCH_PATH" ".vscode" ".vscode"
  cleanup_dir "$SEARCH_PATH" ".idea" ".idea"
  cleanup_file "$SEARCH_PATH" ".DS_Store" ".DS_Store"
fi

# Lock files (optional)
echo ""
echo -e "${YELLOW}Lock Files:${NC}"
cleanup_file "$SEARCH_PATH" "uv.lock" "uv.lock"

echo ""
echo -e "${GREEN}✅ Cleanup complete!${NC}"
echo ""
echo -e "${BLUE}Remaining size:${NC}"
du -sh "$SEARCH_PATH" 2>/dev/null || true
echo ""
echo -e "${BLUE}To verify cleanup, run:${NC}"
echo "  find $SEARCH_PATH -name '__pycache__' -o -name '.pytest_cache' -o -name '.venv' -o -name 'node_modules' -o -name 'dist' | head -20"

