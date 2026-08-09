const assert = require('node:assert/strict');
const { execFileSync, spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');

function isIgnoredBy(ignoreFile, candidate) {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'gitignore-test-'));

  try {
    fs.copyFileSync(path.join(projectRoot, ignoreFile), path.join(fixtureRoot, '.gitignore'));
    execFileSync('git', ['init', '--quiet'], { cwd: fixtureRoot });

    const result = spawnSync(
      'git',
      ['check-ignore', '--no-index', '--quiet', candidate],
      { cwd: fixtureRoot }
    );
    assert.equal(result.error, undefined);
    return result.status === 0;
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
}

test('root ignore protects local environments and generated caches', () => {
  for (const candidate of [
    '.env.production',
    '.venv/bin/python',
    '.ruff_cache/state',
    '.mypy_cache/state',
    '.tox/state',
    '.pxt/state',
    'coverage/result.json',
    '.jest-cache/state',
  ]) {
    assert.equal(isIgnoredBy('.gitignore', candidate), true, candidate);
  }
  assert.equal(isIgnoredBy('.gitignore', '.env.example'), false);
});

test('Python ignore is safe when the project is used independently', () => {
  for (const candidate of [
    '.env.production',
    '.venv/bin/python',
    '.ruff_cache/state',
    '.mypy_cache/state',
    '.tox/state',
  ]) {
    assert.equal(isIgnoredBy('sample-compass/.gitignore', candidate), true, candidate);
  }
  assert.equal(
    isIgnoredBy('sample-compass/.gitignore', '.env.example'),
    false
  );
});

test('TypeScript ignore keeps tools visible and ignores only generated JavaScript', () => {
  assert.equal(
    isIgnoredBy('sample-compass-ts/.gitignore', 'scripts/tool.js'),
    false
  );
  assert.equal(
    isIgnoredBy('sample-compass-ts/.gitignore', 'jest.config.js'),
    false
  );
  assert.equal(
    isIgnoredBy('sample-compass-ts/.gitignore', 'dist/generated.js'),
    true
  );
  assert.equal(
    isIgnoredBy('sample-compass-ts/.gitignore', '.jest-cache/state'),
    true
  );
  assert.equal(
    isIgnoredBy('sample-compass-ts/.gitignore', '.env.test'),
    true
  );
});

test('MakeCode ignore keeps tools visible and excludes PXT state', () => {
  assert.equal(
    isIgnoredBy('sample-compass-makecode/.gitignore', 'tool.js'),
    false
  );
  assert.equal(
    isIgnoredBy('sample-compass-makecode/.gitignore', '.pxt/state'),
    true
  );
  assert.equal(
    isIgnoredBy('sample-compass-makecode/.gitignore', 'built/output.js'),
    true
  );
  assert.equal(
    isIgnoredBy('sample-compass-makecode/.gitignore', '.nyc_output/state'),
    true
  );
  assert.equal(
    isIgnoredBy('sample-compass-makecode/.gitignore', '.env.development'),
    true
  );
});

test('no existing tracked file is hidden by the repository ignore rules', () => {
  const output = execFileSync(
    'git',
    ['ls-files', '-ci', '--exclude-standard', '-z'],
    { cwd: projectRoot, encoding: 'utf8' }
  );
  const existingIgnoredFiles = output
    .split('\0')
    .filter(Boolean)
    .filter((file) => fs.existsSync(path.join(projectRoot, file)));

  assert.deepEqual(existingIgnoredFiles, []);
});
