const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');
const workflow = fs.readFileSync(
  path.join(projectRoot, '.github/workflows/security.yml'),
  'utf8'
);

test('security workflow does not suppress scanner failures', () => {
  assert.doesNotMatch(workflow, /continue-on-error:/);
  assert.doesNotMatch(workflow, /\|\| true/);
  assert.doesNotMatch(workflow, /@master/);
  assert.match(workflow, /exit-code: '1'/);
});

test('security workflow audits every dependency ecosystem in the repository', () => {
  assert.match(workflow, /node scripts\/audit-npm\.js/);
  assert.match(workflow, /uvx pip-audit@2\.10\.1/);
  assert.match(workflow, /uvx bandit@1\.9\.4/);
  assert.ok(fs.existsSync(path.join(projectRoot, 'package-lock.json')));
  assert.ok(
    fs.existsSync(path.join(projectRoot, 'sample-compass-ts/package-lock.json'))
  );
  assert.ok(
    fs.existsSync(
      path.join(projectRoot, 'sample-compass-makecode/package-lock.json')
    )
  );
  assert.ok(fs.existsSync(path.join(projectRoot, 'sample-compass/uv.lock')));
});

test('Trivy is pinned to the known-safe immutable release commit', () => {
  assert.match(
    workflow,
    /aquasecurity\/trivy-action@57a97c7e7821a5776cebc9bb87c984fa69cba8f1/
  );
  assert.match(workflow, /version: v0\.69\.3/);
});

test('every GitHub Action is pinned to an immutable commit SHA', () => {
  const workflowDirectory = path.join(projectRoot, '.github/workflows');
  const workflowFiles = fs
    .readdirSync(workflowDirectory)
    .filter((name) => name.endsWith('.yml'));

  for (const workflowFile of workflowFiles) {
    const contents = fs.readFileSync(
      path.join(workflowDirectory, workflowFile),
      'utf8'
    );
    for (const match of contents.matchAll(/uses:\s*[^\s#]+@([^\s#]+)/g)) {
      assert.match(
        match[1],
        /^[0-9a-f]{40}$/,
        `${workflowFile} contains a mutable action ref: ${match[0]}`
      );
    }
  }
});
