# Copilot Instructions - study-microbit-with-test

This file helps Copilot understand the project structure, conventions, and workflows specific to this monorepo.

## Project Overview

A multi-language micro:bit compass learning project demonstrating the same "convert heading (0-359°) to 8 cardinal directions" problem in three implementations:

1. **sample-compass**: MakeCode Python (Playwright browser-automation tests)
2. **sample-compass-ts**: TypeScript/Node.js (Jest unit + integration tests)
3. **sample-compass-makecode**: MakeCode Blocks (PXT simulator tests)

**Key Theme**: Teaching by comparison—same logic, different languages and test strategies.

## Build & Test Commands

### Project Root

All commands run from the repository root unless specified:

| Task | Command |
|------|---------|
| **Full quality gate** | `npm run test:all` |
| **Python tests only** | `npm run test:python` |
| **TypeScript tests only** | `npm run test:ts` |
| **MakeCode tests only** | `npm run test:makecode` |
| **All linters** | `npm run lint` |
| **Build HEX files** | `npm run build:hex` |
| **Clean temporary files** | `npm run clean` |

### Python (sample-compass)

```bash
cd projects/sample-compass

# Syntax check only
uv run python -m py_compile src/compass_makecode.py

# Full test suite with Playwright simulator
uv run pytest test/test_simulator.py -v

# Single test
uv run pytest test/test_simulator.py -v -k "test_name"

# Coverage report
uv run pytest test/test_simulator.py --cov=src/compass_makecode.py --cov-report=html
```

**Coverage requirement**: 100% on `src/compass_makecode.py` (CI fails below 100%)

### TypeScript (sample-compass-ts)

```bash
cd projects/sample-compass-ts

# Build (TypeScript + type check)
npm run build

# All tests (unit + integration)
npm test

# Unit tests only
npm run test:unit

# Integration tests only
npm run test:integration

# Watch mode
npm run test:watch

# Coverage report
npm run test:coverage
```

**Coverage requirement**: 100% on branches, functions, lines, statements

### MakeCode (sample-compass-makecode)

```bash
cd projects/sample-compass-makecode

# PXT simulator test
npm test

# Serve editor locally
npm run serve

# Build HEX
npm run build:hex
```

## High-Level Architecture

### Monorepo Structure

- **Root `package.json`**: Workspace definitions, npm scripts aggregating subproject tests
- **Root `pyproject.toml`**: Nonexistent (each Python project has its own)
- **`.husky/`**: Pre-commit/pre-push Git hooks that run targeted tests per changed subproject
- **`.github/workflows/`**: CI pipelines (integration-tests, typescript-tests, security, repository-checks)

### Subproject Layouts

Each subproject has:
- `src/`: Implementation files
- `test/`: Test suites (Playwright for Python, Jest for TypeScript, PXT for MakeCode)
- `CLAUDE.md`: Subproject-specific AI guidelines
- Project-specific configs (tsconfig.json, jest.config.js, pyproject.toml)

### Test Strategy (3-Layer)

1. **Compile-time checks** (pre-commit hook):
   - Python: `py_compile` syntax check
   - TypeScript: `npm run build` (tsc + type-check)

2. **Automated tests** (pre-push hook + CI):
   - Python: Playwright simulator tests (MakeCode environment)
   - TypeScript: Jest unit + integration tests
   - MakeCode: PXT simulator tests

3. **Manual verification** (optional):
   - Burn HEX to real micro:bit hardware

## Key Conventions

### Testing Patterns

- **Python** (`sample-compass`): Playwright-based browser automation testing MakeCode's simulator environment
  - Test expectations defined as 5×5 LED pattern strings
  - Tests simulate compass rotation (0°, 45°, 90°, ..., 315°)
  - Code injection during test execution temporarily replaces scroll displays with `basic.clear_screen()`

- **TypeScript** (`sample-compass-ts`): Jest unit + integration tests, pure Node.js logic
  - `Direction` type: `'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW'`
  - `CompassState` interface tracks heading, direction, calibration status
  - Boundary value tests at 22.5°, 67.5°, etc.

- **MakeCode** (`sample-compass-makecode`): PXT build verification and simulator tests
  - Uses MakeCode's block-to-Python translation pipeline
  - Verifies no grey (non-editable) blocks appear
  - Confirms blocks compile without errors

### Code Quality

- **Python**: PEP 8 + type hints + docstrings; Ruff for linting/formatting
- **TypeScript**: ESLint + Prettier; strict TypeScript with `tsconfig.json`
- **MakeCode Python**: Static Python subset (constraints on classes, decorators, complex control flow)

### Git Hooks (Husky)

**Pre-commit**:
- Checks only changed subprojects
- Python: `uv run python -m py_compile`
- TypeScript: `npm run build`
- Aborts commit on failure

**Pre-push**:
- Python: `uv run pytest test/test_simulator.py -v`
- TypeScript: `npm test`
- Aborts push on test failure

See `.husky/` directory for exact implementations.

### HEX File Generation

- `npm run build:hex` generates blocks (not source) HEX files
- Output: `sample-compass-makecode/built/binary.hex` (MakeCode version)
- Uses Playwright to verify block conversion in MakeCode editor
- Detects conversion errors and grey blocks during build step

### Tool Versions

Managed centrally in `.tool-versions` (asdf format):
- Python 3.12.8
- Node.js 22.23.2

Use `asdf install` to sync local environment.

## Development Workflow

### Making Changes

1. **Edit code** in the relevant subproject
2. **Run targeted tests**:
   ```bash
   # Python changes
   cd projects/sample-compass
   uv run pytest test/test_simulator.py -v

   # TypeScript changes
   cd projects/sample-compass-ts
   npm test
   ```
3. **Commit** → pre-commit hook validates syntax
4. **Push** → pre-push hook runs full test suite
5. **GitHub Actions** runs full CI pipeline

### Adding Tests

- **Python**: Add function to `test/test_simulator.py`; use Playwright `page` fixture
- **TypeScript**: Add to `test/compass.test.ts` (unit) or `test/compass.integration.test.ts` (integration)
- **MakeCode**: Add to `test/` directory; follow PXT test conventions

### Refactoring

1. Run full test suite: `npm run test:all`
2. Verify coverage remains at 100%
3. Ensure pre-commit/pre-push hooks pass locally before pushing

## Important Files & References

| File | Purpose |
|------|---------|
| `README.md` | Public overview, quick-start, command reference |
| `projects/sample-compass/CLAUDE.md` | Python project specifics (MakeCode API, Static Python constraints) |
| `projects/sample-compass-ts/CLAUDE.md` | TypeScript project specifics (type definitions, test strategy) |
| `.husky/pre-commit`, `pre-push` | Git hook implementations |
| `.github/workflows/*.yml` | CI/CD pipeline definitions |
| `scripts/generate-blocks-hex.js` | Playwright-based HEX build verification |
| `scripts/clean.sh` | Removes temporary files (dist/, .coverage/, node_modules/, .venv/) |
| `.tool-versions` | asdf tool version pinning |

## Common Tasks

### Verify All Tests Pass Locally

```bash
npm run test:all
```

Runs all lints and tests in correct dependency order. Fails fast if any check fails.

### Run Single Test Type

```bash
# Python only
npm run test:python

# TypeScript only
npm run test:ts

# MakeCode only
npm run test:makecode
```

### Build HEX for Micro:bit

```bash
npm run build:hex
```

Validates MakeCode block conversion and outputs `.hex` file.

### Clean Generated Files

```bash
./scripts/clean.sh --dry-run  # Show what will be deleted
./scripts/clean.sh            # Delete temporary files
```

### Debug Test Failures

- **Python test fails**: Check Playwright connection; run `uv run pytest test/test_simulator.py -v -s` for detailed output
- **TypeScript test fails**: Check `npm run build` compiles; inspect stack trace with `npm test -- --verbose`
- **MakeCode test fails**: Verify `npm --prefix sample-compass-makecode run build:hex` succeeds; check error dialog/grey blocks

## CI/CD Pipelines

- **integration-tests.yml**: Python Playwright tests (pre-push hook + CI)
- **typescript-tests.yml**: TypeScript Jest tests + coverage to codecov
- **security.yml**: npm dependency audit (allowlist in `security/npm-audit-allowlist.json`)
- **repository-checks.yml**: Config validation, file integrity

## Language & Format Preferences

- **Documentation**: Markdown, Japanese inline with English technical terms
- **Python**: PEP 8, type hints, MakeCode Static Python subset
- **TypeScript**: Strict mode, JSDoc, single quotes, semicolons
- **Commit messages**: Japanese context + English technical detail, include `Co-authored-by: Copilot` trailer
