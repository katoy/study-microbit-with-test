const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const projectRoot = path.resolve(__dirname, '..');
const canonicalDocuments = [
  'README.md',
  'MULTILANGUAGE_GUIDE.md',
  'WORKSHOP_TEMPLATE.md',
  'VIDEO_TUTORIAL_SCRIPT.md',
  'GIT_HOOKS_GUIDE.md',
  'HEX_BUILD_GUIDE.md',
  'docs/README.md',
  'sample-compass/README.md',
  'sample-compass-ts/README.md',
  'sample-compass-makecode/README.md'
];

function markdownFiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory() && entry.name !== 'node_modules') {
      return markdownFiles(fullPath);
    }
    return entry.isFile() && entry.name.endsWith('.md') ? [fullPath] : [];
  });
}

test('learner documentation contains no machine-local links or placeholders', () => {
  const offenders = [];
  for (const file of markdownFiles(projectRoot)) {
    const content = fs.readFileSync(file, 'utf8');
    if (/file:\/\/\/Users\/|YOUR_USERNAME/.test(content)) {
      offenders.push(path.relative(projectRoot, file));
    }
  }

  assert.deepEqual(offenders, []);
  assert.ok(fs.existsSync(path.join(projectRoot, 'LICENSE')));
});

test('canonical documentation has no broken relative links', () => {
  const brokenLinks = [];

  for (const relativeFile of canonicalDocuments) {
    const filePath = path.join(projectRoot, relativeFile);
    const content = fs.readFileSync(filePath, 'utf8');
    const links = content.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g);

    for (const match of links) {
      const target = match[1].trim().replace(/^<|>$/g, '');
      if (/^(https?:|mailto:|#)/.test(target)) {
        continue;
      }

      const pathWithoutAnchor = decodeURIComponent(target.split('#')[0]);
      const resolved = path.resolve(path.dirname(filePath), pathWithoutAnchor);
      if (!fs.existsSync(resolved)) {
        brokenLinks.push(`${relativeFile}: ${target}`);
      }
    }
  }

  assert.deepEqual(brokenLinks, []);
});

test('learning path documents the zero-install start and coverage limitations', () => {
  const rootReadme = fs.readFileSync(path.join(projectRoot, 'README.md'), 'utf8');
  const guide = fs.readFileSync(path.join(projectRoot, 'MULTILANGUAGE_GUIDE.md'), 'utf8');
  const workshop = fs.readFileSync(path.join(projectRoot, 'WORKSHOP_TEMPLATE.md'), 'utf8');

  assert.match(rootReadme, /ステップ 0/);
  assert.match(rootReadme, /インストール不要/);
  assert.match(guide, /入力検証/);
  assert.match(guide, /カバレッジ 100%.*バグゼロ/);
  assert.match(guide, /16 方位/);
  assert.match(workshop, /カバレッジ 100%.*バグゼロ/);

  const preparation = workshop.match(/## 準備[\s\S]*?## 時間割/)[0];
  const finalCheck = workshop.match(/## 80〜88分: 最終確認[\s\S]*?## 88〜90分/)[0];
  assert.match(preparation, /npm run verify:blocks/);
  assert.doesNotMatch(finalCheck, /npm run verify:blocks/);
});

test('each implementation README includes progressive learning exercises', () => {
  for (const relativeFile of [
    'sample-compass/README.md',
    'sample-compass-ts/README.md',
    'sample-compass-makecode/README.md'
  ]) {
    const readme = fs.readFileSync(path.join(projectRoot, relativeFile), 'utf8');
    assert.match(readme, /## 学習課題/);
    assert.match(readme, /16 方位/);
    assert.match(readme, /移動平均/);
    assert.match(readme, /傾き補正/);
    assert.match(readme, /磁気干渉/);
  }
});
