const assert = require('node:assert/strict');
const test = require('node:test');

const { evaluateAudit } = require('../scripts/audit-npm.js');

const report = {
  vulnerabilities: {
    vulnerable_leaf: {
      name: 'vulnerable_leaf',
      severity: 'high',
      via: [
        {
          url: 'https://github.com/advisories/GHSA-aaaa-bbbb-cccc',
          severity: 'high',
        },
      ],
    },
    parent_tool: {
      name: 'parent_tool',
      severity: 'high',
      via: ['vulnerable_leaf'],
    },
  },
};

test('blocks high vulnerabilities that are not allowlisted', () => {
  const result = evaluateAudit(report, {}, new Date('2026-08-09T00:00:00Z'));

  assert.deepEqual(
    result.blocking.map((item) => item.name),
    ['vulnerable_leaf', 'parent_tool']
  );
  assert.equal(result.allowed.length, 0);
});

test('allows only the documented package chain before its review date', () => {
  const allowlist = {
    'GHSA-aaaa-bbbb-cccc': {
      packages: ['vulnerable_leaf', 'parent_tool'],
      reason: 'No patched upstream release exists.',
      reviewBy: '2026-09-01',
    },
  };

  const result = evaluateAudit(
    report,
    allowlist,
    new Date('2026-08-09T00:00:00Z')
  );

  assert.equal(result.blocking.length, 0);
  assert.deepEqual(
    result.allowed.map((item) => item.name),
    ['vulnerable_leaf', 'parent_tool']
  );
});

test('blocks allowlist entries after their review date', () => {
  const allowlist = {
    'GHSA-aaaa-bbbb-cccc': {
      packages: ['vulnerable_leaf', 'parent_tool'],
      reason: 'No patched upstream release exists.',
      reviewBy: '2026-08-08',
    },
  };

  const result = evaluateAudit(
    report,
    allowlist,
    new Date('2026-08-09T00:00:00Z')
  );

  assert.deepEqual(
    result.blocking.map((item) => item.name),
    ['vulnerable_leaf', 'parent_tool']
  );
});

test('does not expand an exception to an undocumented parent package', () => {
  const allowlist = {
    'GHSA-aaaa-bbbb-cccc': {
      packages: ['vulnerable_leaf'],
      reason: 'No patched upstream release exists.',
      reviewBy: '2026-09-01',
    },
  };

  const result = evaluateAudit(
    report,
    allowlist,
    new Date('2026-08-09T00:00:00Z')
  );

  assert.deepEqual(result.allowed.map((item) => item.name), ['vulnerable_leaf']);
  assert.deepEqual(result.blocking.map((item) => item.name), ['parent_tool']);
});
