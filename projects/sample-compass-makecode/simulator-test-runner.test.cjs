const test = require('node:test');
const assert = require('node:assert/strict');

const { parseTestResult } = require('./simulator-test-runner.cjs');

test('accepts a complete successful MakeCode test result', () => {
  assert.deepEqual(
    parseTestResult('serial:  MAKECODE_TEST_RESULT total=3 passed=3 failed=0'),
    { total: 3, passed: 3, failed: 0 }
  );
});

test('rejects a MakeCode test result that contains failures', () => {
  assert.throws(
    () => parseTestResult('MAKECODE_TEST_RESULT total=3 passed=2 failed=1'),
    /1 MakeCode test\(s\) failed/
  );
});

test('rejects output without a MakeCode test result', () => {
  assert.throws(
    () => parseTestResult('runtime exited without a summary'),
    /did not report a result/
  );
});

test('rejects inconsistent MakeCode test counts', () => {
  assert.throws(
    () => parseTestResult('MAKECODE_TEST_RESULT total=3 passed=1 failed=0'),
    /inconsistent test counts/
  );
});
