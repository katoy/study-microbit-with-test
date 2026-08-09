const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');
const rootPackage = require(path.join(projectRoot, 'package.json'));

test('the local all-tests command enforces the documented coverage threshold', () => {
  assert.match(rootPackage.scripts['test:all'], /test:coverage/);
  assert.match(rootPackage.scripts['test:coverage:python'], /--cov-fail-under=100/);
});

test('repository checks run configuration tests in CI', () => {
  const workflowPath = path.join(
    projectRoot,
    '.github/workflows/repository-checks.yml'
  );
  assert.ok(fs.existsSync(workflowPath));

  const workflow = fs.readFileSync(workflowPath, 'utf8');
  assert.match(workflow, /permissions:\s*\n\s*contents: read/);
  assert.match(workflow, /npm run test:config/);
  assert.match(workflow, /bash -n \.devcontainer\/setup-dev\.sh/);
  assert.match(workflow, /bash -n sync-ai-skills\.sh/);
});

test('Dev Container setup is non-root, non-duplicating, and fail-fast', () => {
  const setup = fs.readFileSync(
    path.join(projectRoot, '.devcontainer/setup-dev.sh'),
    'utf8'
  );

  assert.doesNotMatch(setup, /\bapt-get\b/);
  assert.equal((setup.match(/npm ci --no-progress --no-audit/g) || []).length, 1);
  assert.doesNotMatch(setup, /\|\|\s*(true|echo)/);
  assert.match(setup, /npm run test:all/);
});
