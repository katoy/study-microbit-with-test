const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const scriptPath = path.resolve(__dirname, '..', 'sync-ai-skills.sh');

function createFixtureHome(t) {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'microbit-ai-sync-'));
  t.after(() => fs.rmSync(home, { recursive: true, force: true }));

  const skillDirectory = path.join(home, '.gemini/config/skills/example');
  fs.mkdirSync(skillDirectory, { recursive: true });
  fs.writeFileSync(
    path.join(skillDirectory, 'SKILL.md'),
    '---\nname: example\n---\n\n# Example\n',
    'utf8'
  );

  for (const target of [
    path.join(home, '.config/ai-global-rules.md'),
    path.join(home, '.cursorrules'),
    path.join(home, '.gemini/config/GEMINI.md'),
    path.join(home, '.claudecode.md')
  ]) {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, 'keep me\n', 'utf8');
  }

  return home;
}

test('AI skill sync is a non-mutating preview by default', t => {
  const home = createFixtureHome(t);

  const output = execFileSync('bash', [scriptPath], {
    env: { ...process.env, HOME: home },
    encoding: 'utf8'
  });

  assert.match(output, /dry-run/i);
  assert.equal(fs.readFileSync(path.join(home, '.cursorrules'), 'utf8'), 'keep me\n');
  assert.equal(
    fs.readFileSync(path.join(home, '.config/ai-global-rules.md'), 'utf8'),
    'keep me\n'
  );
});

test('AI skill sync backs up existing global rules before --apply', t => {
  const home = createFixtureHome(t);

  execFileSync('bash', [scriptPath, '--apply'], {
    env: { ...process.env, HOME: home },
    encoding: 'utf8'
  });

  const cursorRules = path.join(home, '.cursorrules');
  assert.ok(fs.lstatSync(cursorRules).isSymbolicLink());
  assert.ok(fs.readdirSync(home).some(name => name.startsWith('.cursorrules.backup-')));
  assert.ok(fs.readdirSync(path.join(home, '.gemini/config'))
    .some(name => name.startsWith('GEMINI.md.backup-')));
  assert.ok(fs.readdirSync(home).some(name => name.startsWith('.claudecode.md.backup-')));
  assert.ok(fs.readdirSync(path.join(home, '.config'))
    .some(name => name.startsWith('ai-global-rules.md.backup-')));
});
