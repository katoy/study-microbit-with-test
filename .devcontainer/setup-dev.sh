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
NC='\033[0m' # No Color

# Step 1: Node.js packages (the Dev Container features provide system tools)
echo ""
echo -e "${BLUE}📦 Step 1: Installing Node.js dependencies...${NC}"
npm ci --no-progress --no-audit > /dev/null 2>&1

# TypeScript
echo "  → TypeScript dependencies"
npm --prefix sample-compass-ts ci --no-progress --no-audit > /dev/null 2>&1

# MakeCode
echo "  → MakeCode dependencies"
npm --prefix sample-compass-makecode ci --no-progress --no-audit > /dev/null 2>&1

echo -e "${GREEN}✅ Node.js dependencies installed${NC}"

# Step 2: Python setup with uv
echo ""
echo -e "${BLUE}📦 Step 2: Setting up Python environment...${NC}"

# Install uv package manager
python -m pip install --user -q --no-cache-dir uv

# Python project setup
echo "  → Python dependencies (uv sync)"
uv sync --project sample-compass -q
echo -e "${GREEN}✅ Python environment configured${NC}"

# Step 3: Git hooks setup
echo ""
echo -e "${BLUE}🔧 Step 3: Configuring Git hooks...${NC}"
npm run prepare > /dev/null 2>&1
echo -e "${GREEN}✅ Git hooks configured${NC}"

# Step 4: Verify the complete local quality gate
echo ""
echo -e "${BLUE}🧪 Step 4: Running the complete test suite...${NC}"
npm run test:all

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
