const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');
const rootPackage = require(path.join(projectRoot, 'package.json'));
const typeScriptPackage = require(path.join(
  projectRoot,
  'sample-compass-ts/package.json'
));
const makeCodePackage = require(path.join(
  projectRoot,
  'sample-compass-makecode/package.json'
));

test('device HEX builds use only the Python and MakeCode toolchains', () => {
  assert.match(rootPackage.scripts['build:hex'], /build:hex:python/);
  assert.match(rootPackage.scripts['build:hex'], /build:hex:makecode/);
  assert.ok(!Object.hasOwn(rootPackage.scripts, 'build:hex:ts'));
  assert.ok(!Object.hasOwn(typeScriptPackage.scripts, 'build:hex'));
  assert.equal(makeCodePackage.scripts['build:hex'], 'npm run build');
});

test('MakeCode tests execute in the simulator from root scripts and CI', () => {
  assert.match(rootPackage.scripts.test, /test:makecode/);
  assert.equal(
    rootPackage.scripts['test:makecode'],
    'cd sample-compass-makecode && npm test'
  );
  assert.match(makeCodePackage.scripts.test, /test:simulator/);

  const workflow = fs.readFileSync(
    path.join(projectRoot, '.github/workflows/integration-tests.yml'),
    'utf8'
  );
  assert.match(workflow, /working-directory: \.\/sample-compass-makecode[\s\S]*npm test/);
  assert.doesNotMatch(workflow, /npm run build \|\| true/);
});

test('TypeScript lint preserves the compiler exit code', () => {
  assert.equal(
    rootPackage.scripts['lint:ts'],
    'cd sample-compass-ts && npm run build'
  );
});

test('Python README documents only implemented Compass methods', () => {
  const readme = fs.readFileSync(
    path.join(projectRoot, 'sample-compass/README.md'),
    'utf8'
  );

  for (const method of ['calibrate', 'get_heading', 'get_direction', 'display_direction']) {
    assert.match(readme, new RegExp(`\\b${method}\\(`));
  }
  for (const missingMethod of ['set_heading', 'get_calibrated', 'get_state']) {
    assert.doesNotMatch(readme, new RegExp(`\\b${missingMethod}\\(`));
  }
});

test('mocked workflows are named integration tests rather than end-to-end tests', () => {
  assert.equal(
    rootPackage.scripts['integration:python'],
    'cd sample-compass && uv run pytest test_compass_integration.py -v'
  );
  assert.equal(
    rootPackage.scripts['integration:ts'],
    'cd sample-compass-ts && npm run test:integration'
  );
  assert.equal(
    typeScriptPackage.scripts['test:integration'],
    "jest --testPathPattern='integration'"
  );
  assert.ok(!Object.keys(rootPackage.scripts).some((name) => name.includes('e2e')));
  assert.ok(!Object.keys(typeScriptPackage.scripts).some((name) => name.includes('e2e')));

  assert.ok(fs.existsSync(path.join(projectRoot, 'sample-compass/test_compass_integration.py')));
  assert.ok(fs.existsSync(path.join(
    projectRoot,
    'sample-compass-ts/test/compass.integration.test.ts'
  )));
  assert.ok(fs.existsSync(path.join(projectRoot, '.github/workflows/integration-tests.yml')));
});

test('README test counts match the current TypeScript suites', () => {
  const rootReadme = fs.readFileSync(path.join(projectRoot, 'README.md'), 'utf8');
  const typeScriptReadme = fs.readFileSync(
    path.join(projectRoot, 'sample-compass-ts/README.md'),
    'utf8'
  );

  assert.doesNotMatch(rootReadme, /133\/133/);
  assert.match(typeScriptReadme, /ユニットテスト（47 個）/);
  assert.match(typeScriptReadme, /統合テスト[^\n]*25/);
});

test('TypeScript development and CI use the supported Node 22 line', () => {
  const toolVersions = fs.readFileSync(
    path.join(projectRoot, 'sample-compass-ts/.tool-versions'),
    'utf8'
  );
  const typeScriptWorkflow = fs.readFileSync(
    path.join(projectRoot, '.github/workflows/typescript-tests.yml'),
    'utf8'
  );
  const integrationWorkflow = fs.readFileSync(
    path.join(projectRoot, '.github/workflows/integration-tests.yml'),
    'utf8'
  );

  assert.equal(toolVersions.trim(), 'node 22.23.2');
  assert.doesNotMatch(typeScriptWorkflow, /node-version: '20\.x'/);
  assert.doesNotMatch(integrationWorkflow, /node-version: '20\.x'/);
});
