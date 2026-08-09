const assert = require('node:assert/strict');
const { execFileSync, spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');
const cleanScriptPath = path.join(projectRoot, 'scripts/clean.sh');
const cleanScript = fs.readFileSync(cleanScriptPath, 'utf8');

function initializeFixture(fixtureRoot) {
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
}

function createFixture() {
  const fixtureRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'clean-script-test-'));
  initializeFixture(fixtureRoot);
  return fixtureRoot;
}

function createNamedFixture(rootName) {
  const fixtureParent = fs.mkdtempSync(
    path.join(os.tmpdir(), 'clean-script-named-test-')
  );
  const fixtureRoot = path.join(fixtureParent, rootName);
  fs.mkdirSync(fixtureRoot);
  initializeFixture(fixtureRoot);
  return { fixtureParent, fixtureRoot };
}

function runClean(fixtureRoot, ...args) {
  return execFileSync(
    'bash',
    [path.join(fixtureRoot, 'scripts/clean.sh'), ...args],
    { cwd: fixtureRoot, encoding: 'utf8' }
  );
}

function runCleanResult(fixtureRoot, args = [], env = {}) {
  return spawnSync(
    'bash',
    [path.join(fixtureRoot, 'scripts/clean.sh'), ...args],
    {
      cwd: fixtureRoot,
      encoding: 'utf8',
      env: { ...process.env, ...env },
    }
  );
}

test('clean script never targets reproducibility lockfiles', () => {
  assert.doesNotMatch(cleanScript, /cleanup_file[^\n]+package-lock\.json/);
  assert.doesNotMatch(cleanScript, /cleanup_file[^\n]+pnpm-lock\.yaml/);
  assert.doesNotMatch(cleanScript, /cleanup_file[^\n]+uv\.lock/);
});

test('clean script protects tracked files inside cleanup directories', () => {
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

test('clean script never removes a project root named like a cleanup directory', () => {
  const { fixtureParent, fixtureRoot } = createNamedFixture('build');
  const scriptFixture = path.join(fixtureRoot, 'scripts/clean.sh');

  try {
    runClean(fixtureRoot);

    assert.equal(fs.existsSync(fixtureRoot), true);
    assert.equal(fs.existsSync(scriptFixture), true);
  } finally {
    fs.rmSync(fixtureParent, { recursive: true, force: true });
  }
});

test('clean script fails closed when Git cannot verify tracked paths', () => {
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

    const result = runCleanResult(
      fixtureRoot,
      ['sample-compass-makecode'],
      { GIT_DIR: path.join(fixtureRoot, 'missing-git-dir') }
    );

    assert.notEqual(result.status, 0);
    assert.equal(fs.existsSync(trackedState), true);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script reports find failures instead of claiming success', () => {
  const fixtureRoot = createFixture();
  const fakeBin = path.join(fixtureRoot, 'fake-bin');
  const fakeFind = path.join(fakeBin, 'find');

  try {
    fs.mkdirSync(fakeBin);
    fs.writeFileSync(fakeFind, '#!/bin/sh\nexit 7\n');
    fs.chmodSync(fakeFind, 0o755);

    const result = runCleanResult(
      fixtureRoot,
      ['sample-compass'],
      { PATH: `${fakeBin}${path.delimiter}${process.env.PATH}` }
    );

    assert.notEqual(result.status, 0);
    assert.doesNotMatch(result.stdout, /Cleanup complete!/);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script refuses candidates outside the selected project', () => {
  const fixtureRoot = createFixture();
  const fakeBin = path.join(fixtureRoot, 'fake-bin');
  const fakeFind = path.join(fakeBin, 'find');
  const outsideDirectory = path.join(fixtureRoot, 'sample-compass-ts/dist');
  const outsideArtifact = path.join(outsideDirectory, 'artifact.js');

  try {
    fs.mkdirSync(fakeBin);
    fs.writeFileSync(
      fakeFind,
      '#!/bin/sh\nprintf "%s\\000" "$CLEAN_CANDIDATE"\n'
    );
    fs.chmodSync(fakeFind, 0o755);
    fs.mkdirSync(outsideDirectory, { recursive: true });
    fs.writeFileSync(outsideArtifact, 'must remain');

    const result = runCleanResult(
      fixtureRoot,
      ['sample-compass'],
      {
        CLEAN_CANDIDATE: outsideDirectory,
        PATH: `${fakeBin}${path.delimiter}${process.env.PATH}`,
      }
    );

    assert.notEqual(result.status, 0);
    assert.equal(fs.existsSync(outsideArtifact), true);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script preserves local IDE settings', () => {
  const fixtureRoot = createFixture();
  const vscodeSettings = path.join(
    fixtureRoot,
    'sample-compass/.vscode/settings.json'
  );
  const ideaWorkspace = path.join(
    fixtureRoot,
    'sample-compass/.idea/workspace.xml'
  );

  try {
    for (const localSetting of [vscodeSettings, ideaWorkspace]) {
      fs.mkdirSync(path.dirname(localSetting), { recursive: true });
      fs.writeFileSync(localSetting, 'local setting');
    }

    runClean(fixtureRoot, 'sample-compass');

    assert.equal(fs.existsSync(vscodeSettings), true);
    assert.equal(fs.existsSync(ideaWorkspace), true);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('clean script dry-run never removes generated artifacts', () => {
  const fixtureRoot = createFixture();
  const generatedArtifact = path.join(
    fixtureRoot,
    'sample-compass/dist/hex/blocks.hex'
  );

  try {
    fs.mkdirSync(path.dirname(generatedArtifact), { recursive: true });
    fs.writeFileSync(generatedArtifact, 'generated fixture');

    const output = runClean(fixtureRoot, '--dry-run', 'sample-compass');

    assert.match(output, /Would remove: .*sample-compass\/dist/);
    assert.equal(fs.existsSync(generatedArtifact), true);
  } finally {
    fs.rmSync(fixtureRoot, { recursive: true, force: true });
  }
});
