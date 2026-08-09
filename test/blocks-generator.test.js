const assert = require('node:assert/strict');
const test = require('node:test');

const {
  evaluateBlocksConversionStatus
} = require('../scripts/generate-blocks-hex');

test('block conversion accepts an editable workspace without errors', () => {
  assert.doesNotThrow(() => evaluateBlocksConversionStatus({
    errorDialogCount: 0,
    greyBlockCount: 0,
    workspaceCount: 1
  }));
});

test('block conversion rejects MakeCode compilation errors', () => {
  assert.throws(
    () => evaluateBlocksConversionStatus({
      errorDialogCount: 1,
      greyBlockCount: 0,
      workspaceCount: 1
    }),
    /conversion error/i
  );
});

test('block conversion rejects non-editable grey blocks', () => {
  assert.throws(
    () => evaluateBlocksConversionStatus({
      errorDialogCount: 0,
      greyBlockCount: 2,
      workspaceCount: 1
    }),
    /grey block/i
  );
});

test('block conversion requires a rendered Blockly workspace', () => {
  assert.throws(
    () => evaluateBlocksConversionStatus({
      errorDialogCount: 0,
      greyBlockCount: 0,
      workspaceCount: 0
    }),
    /workspace/i
  );
});
