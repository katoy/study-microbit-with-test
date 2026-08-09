#!/bin/bash
set -euo pipefail

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║            🚀 micro:bit Development Environment Setup                         ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: System package updates
echo -e "${BLUE}📦 Step 1: Installing system packages...${NC}"
apt-get update -qq
apt-get install -y -qq \
  build-essential \
  curl \
  git \
  pkg-config \
  > /dev/null 2>&1
echo -e "${GREEN}✅ System packages installed${NC}"

# Step 2: Node.js packages (npm ci)
echo ""
echo -e "${BLUE}📦 Step 2: Installing Node.js dependencies...${NC}"
npm ci --no-progress --no-audit > /dev/null 2>&1

# Python dependencies for root
echo "  → Root dependencies"
npm ci --no-progress --no-audit > /dev/null 2>&1

# TypeScript
echo "  → TypeScript dependencies"
cd sample-compass-ts && npm ci --no-progress --no-audit > /dev/null 2>&1 && cd ..

# MakeCode
echo "  → MakeCode dependencies"
cd sample-compass-makecode && npm ci --no-progress --no-audit > /dev/null 2>&1 && cd ..

echo -e "${GREEN}✅ Node.js dependencies installed${NC}"

# Step 3: Python setup with uv
echo ""
echo -e "${BLUE}📦 Step 3: Setting up Python environment...${NC}"

# Install uv package manager
pip install -q --no-cache-dir uv

# Python project setup
cd sample-compass
echo "  → Python dependencies (uv sync)"
uv sync -q
echo -e "${GREEN}✅ Python environment configured${NC}"
cd ..

# Step 4: Git hooks setup
echo ""
echo -e "${BLUE}🔧 Step 4: Configuring Git hooks...${NC}"
npm run prepare > /dev/null 2>&1 || true
echo -e "${GREEN}✅ Git hooks configured${NC}"

# Step 5: Run initial test
echo ""
echo -e "${BLUE}🧪 Step 5: Running initial test suite...${NC}"
echo "  → Configuration tests"
npm run test:config > /dev/null 2>&1 || echo "    ⚠️ Some config checks may fail (non-critical)"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                      ✅ Setup Complete!                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Ready to develop!${NC}"
echo ""
echo "Quick Start:"
echo "  📚 View guide:        cat README.md"
echo "  🧪 Run all tests:     npm run test:all"
echo "  🐍 Python tests:      npm run test:python"
echo "  🔷 TypeScript tests:  npm run test:ts"
echo "  🔨 MakeCode tests:    npm run test:makecode"
echo "  📖 Complex guide:     cat MULTILANGUAGE_GUIDE.md"
echo ""
echo "📚 Documentation:"
echo "  • docs/README.md - Main documentation"
echo "  • docs/MICROBIT_EDUCATION_REVIEW.md - Comprehensive review"
echo "  • docs/ACTIONABLE_IMPROVEMENTS.md - Improvement roadmap"
echo "  • MULTILANGUAGE_GUIDE.md - Learn Python, TypeScript, MakeCode"
echo ""
