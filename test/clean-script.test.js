const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');
const cleanScriptPath = path.join(projectRoot, 'scripts/clean.sh');
const cleanScript = fs.readFileSync(cleanScriptPath, 'utf8');

function createFixture() {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'clean-script-test-'));
  fs.mkdirSync(path.join(fixtureRoot, 'scripts'));
  fs.copyFileSync(cleanScriptPath, path.join(fixtureRoot, 'scripts/clean.sh'));
  for (const project of [
    'sample-compass',
    'sample-compass-ts',
    'sample-compass-makecode',
  ]) {
    fs.mkdirSync(path.join(fixtureRoot, project));
  }
  execFileSync('git', ['init', '--quiet'], { cwd: fixtureRoot });
  return fixtureRoot;
}

function runClean(fixtureRoot, ...args) {
  return execFileSync(
    'bash',
    [path.join(fixtureRoot, 'scripts/clean.sh'), ...args],
    { cwd: fixtureRoot, encoding: 'utf8' }
  );
}

test('clean script never targets reproducibility lockfiles', () => {
  assert.doesNotMatch(cleanScript, /cleanup_file[^\n]+package-lock\.json/);
  assert.doesNotMatch(cleanScript, /cleanup_file[^\n]+pnpm-lock\.yaml/);
  assert.doesNotMatch(cleanScript, /cleanup_file[^\n]+uv\.lock/);
});

test('clean script protects tracked files inside cleanup directories', () => {
  assert.match(cleanScript, /git[^\n]+ls-files/);

  const fixtureRoot = createFixture();
  const trackedState = path.join(
    fixtureRoot,
    'sample-compass-makecode/.pxt/storage/state'
  );

  try {
    fs.mkdirSync(path.dirname(trackedState), { recursive: true });
    fs.writeFileSync(trackedState, 'tracked fixture');
    execFileSync('git', ['add', 'sample-compass-makecode/.pxt/storage/state'], {
      cwd: fixtureRoot,
    });

    const output = runClean(fixtureRoot, 'sample-compass-makecode');

    assert.match(
      output,
      /Preserving tracked path: .*sample-compass-makecode\/\.pxt/
    );
    assert.equal(fs.existsSync(trackedState), true);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script removes Python tool caches and coverage data', () => {
  const fixtureRoot = createFixture();
  const generatedPaths = [
    'sample-compass/.ruff_cache/state',
    'sample-compass/.mypy_cache/state',
    'sample-compass/sample_compass.egg-info/PKG-INFO',
    'sample-compass/coverage.xml',
  ];

  try {
    for (const relativePath of generatedPaths) {
      const absolutePath = path.join(fixtureRoot, relativePath);
      fs.mkdirSync(path.dirname(absolutePath), { recursive: true });
      fs.writeFileSync(absolutePath, 'generated fixture');
    }

    runClean(fixtureRoot, 'sample-compass');

    for (const relativePath of generatedPaths) {
      assert.equal(fs.existsSync(path.join(fixtureRoot, relativePath)), false);
    }
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script does not enumerate artifacts inside generated directories', () => {
  const fixtureRoot = createFixture();
  const nestedCache = path.join(
    fixtureRoot,
    'sample-compass/.venv/lib/python/coverage/__pycache__/state'
  );

  try {
    fs.mkdirSync(path.dirname(nestedCache), { recursive: true });
    fs.writeFileSync(nestedCache, 'generated fixture');

    const output = runClean(fixtureRoot, '--dry-run', 'sample-compass');

    assert.match(output, /Would remove: .*sample-compass\/\.venv/);
    assert.doesNotMatch(output, /\.venv\/.*(?:coverage|__pycache__)/);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script removes ignored JavaScript and PXT caches', () => {
  const fixtureRoot = createFixture();
  const generatedPaths = [
    'sample-compass-ts/.nyc_output/state',
    'sample-compass-ts/.cache/state',
    'sample-compass-makecode/pxt_modules/pkg/index.js',
    'sample-compass-makecode/.cache/state',
  ];

  try {
    for (const relativePath of generatedPaths) {
      const absolutePath = path.join(fixtureRoot, relativePath);
      fs.mkdirSync(path.dirname(absolutePath), { recursive: true });
      fs.writeFileSync(absolutePath, 'generated fixture');
    }

    runClean(fixtureRoot);

    for (const relativePath of generatedPaths) {
      assert.equal(fs.existsSync(path.join(fixtureRoot, relativePath)), false);
    }
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script never traverses the Git metadata directory', () => {
  const fixtureRoot = createFixture();
  const gitMetadataFixture = path.join(fixtureRoot, '.git/.venv/keep');

  try {
    fs.mkdirSync(path.dirname(gitMetadataFixture), { recursive: true });
    fs.writeFileSync(gitMetadataFixture, 'must not be removed');

    runClean(fixtureRoot);

    assert.equal(fs.existsSync(gitMetadataFixture), true);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});
