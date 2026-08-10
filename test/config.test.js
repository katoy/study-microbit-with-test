import { test } from 'node:test';
import { strict as assert } from 'node:assert';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const rootDir = new URL('..', import.meta.url).pathname;

test('package.json: root has required scripts', () => {
  const pkg = JSON.parse(
    readFileSync(join(rootDir, 'package.json'), 'utf8')
  );

  const requiredScripts = [
    'test',
    'test:python',
    'test:ts',
    'test:makecode',
    'lint',
    'build:hex',
  ];

  for (const script of requiredScripts) {
    assert.ok(pkg.scripts[script], `Missing script: ${script}`);
  }
});

test('package.json: workspace includes all subprojects', () => {
  const pkg = JSON.parse(
    readFileSync(join(rootDir, 'package.json'), 'utf8')
  );

  const requiredWorkspaces = [
    'projects/sample-compass-ts',
    'projects/sample-compass-makecode',
  ];

  for (const workspace of requiredWorkspaces) {
    assert.ok(
      pkg.workspaces.includes(workspace),
      `Missing workspace: ${workspace}`
    );
  }
});

test('Node.js and Python versions pinned in .tool-versions', () => {
  const toolVersions = readFileSync(
    join(rootDir, '.tool-versions'),
    'utf8'
  ).trim();

  assert.match(toolVersions, /^python\s+3\.12\.8$/m, 'Python 3.12.8 required');
  assert.match(toolVersions, /^node\s+22\.23\.2$/m, 'Node 22.23.2 required');
});
