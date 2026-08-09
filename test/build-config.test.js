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

test('device HEX builds use only the MakeCode toolchain', () => {
  assert.equal(rootPackage.scripts['build:hex'], 'npm run build:hex:makecode');
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

test('MakeCode exposes no test-only block parameter or unused microphone dependency', () => {
  const compassSource = fs.readFileSync(
    path.join(projectRoot, 'sample-compass-makecode/src/compass.ts'),
    'utf8'
  );
  const simulatorRunner = fs.readFileSync(
    path.join(projectRoot, 'sample-compass-makecode/simulator-test-runner.cjs'),
    'utf8'
  );

  assert.doesNotMatch(compassSource, /calibrate\(skipHardware/);
  assert.match(compassSource, /export function calibrate\(\): void/);
  assert.match(compassSource, /export function calibrateForTest\(\): void/);
  assert.doesNotMatch(simulatorRunner, /microphone:/);

  const pxtConfig = JSON.parse(
    fs.readFileSync(path.join(projectRoot, 'sample-compass-makecode/pxt.json'), 'utf8')
  );
  assert.equal(Object.hasOwn(pxtConfig.dependencies, 'microphone'), false);

  // targetVersions が無いと PXT が旧バージョン向けの upgrade ルールを適用し、
  // pxt install のたびに microphone 依存を書き戻して pxt.json が汚れる
  assert.ok(pxtConfig.targetVersions);
  assert.match(pxtConfig.targetVersions.target, /^\d+\.\d+\.\d+$/);

  // シミュレーターテスト用の一時プロジェクトにも同じ抑止が必要
  assert.match(simulatorRunner, /targetVersions: projectConfig\.targetVersions/);
});

test('TypeScript lint preserves the compiler exit code', () => {
  assert.equal(
    rootPackage.scripts['lint:ts'],
    'cd sample-compass-ts && npm run build'
  );
});



test('mocked workflows are named integration tests rather than end-to-end tests', () => {
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

  assert.ok(fs.existsSync(path.join(
    projectRoot,
    'sample-compass-ts/test/compass.integration.test.ts'
  )));
  assert.ok(fs.existsSync(path.join(projectRoot, '.github/workflows/integration-tests.yml')));
});

test('canonical READMEs use executable checks instead of frozen test totals', () => {
  const rootReadme = fs.readFileSync(path.join(projectRoot, 'README.md'), 'utf8');
  const typeScriptReadme = fs.readFileSync(
    path.join(projectRoot, 'sample-compass-ts/README.md'),
    'utf8'
  );

  assert.match(rootReadme, /npm run test:all/);
  assert.match(typeScriptReadme, /npm test/);
  for (const readme of [rootReadme, typeScriptReadme]) {
    assert.doesNotMatch(readme, /\b\d+\/\d+\s+(PASS|成功)/);
  }
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
