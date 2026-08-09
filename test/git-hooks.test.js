const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');

for (const hookName of ['pre-commit', 'pre-push']) {
  test(`${hookName} scopes project changes to directory boundaries`, () => {
    const hook = fs.readFileSync(
      path.join(projectRoot, '.husky', hookName),
      'utf8'
    );

    for (const project of [
      'sample-compass',
      'sample-compass-ts',
      'sample-compass-makecode',
    ]) {
      assert.match(hook, new RegExp(`grep -q "\\^${project}/"`));
    }
    assert.doesNotMatch(hook, /grep -q "sample-compass"/);
  });
}

test('pre-push uses the refs supplied by Git instead of assuming origin', () => {
  const hook = fs.readFileSync(
    path.join(projectRoot, '.husky/pre-push'),
    'utf8'
  );

  assert.match(
    hook,
    /while read -r local_ref local_sha remote_ref remote_sha/
  );
  assert.match(hook, /git diff --name-only "\$remote_sha" "\$local_sha"/);
  assert.match(hook, /git ls-tree -r --name-only "\$local_sha"/);
  assert.doesNotMatch(hook, /origin\//);
});
