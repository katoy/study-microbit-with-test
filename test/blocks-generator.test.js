const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const {
  evaluateBlocksConversionStatus,
  getBlocksHexOutputPaths
} = require('../scripts/generate-blocks-hex');

test('block HEX outputs use the program-name-independent blocks.hex name', () => {
  const rootDirectory = path.resolve('/workspace/project');
  const outputPaths = getBlocksHexOutputPaths(rootDirectory);

  assert.equal(
    outputPaths.python,
    path.join(rootDirectory, 'sample-compass/dist/hex/blocks.hex')
  );
  assert.equal(
    outputPaths.makecode,
    path.join(rootDirectory, 'sample-compass-makecode/built/blocks.hex')
  );
});

test('the MakeCode block HEX output does not overwrite the PXT build output', () => {
  const rootDirectory = path.resolve('/workspace/project');
  const outputPaths = getBlocksHexOutputPaths(rootDirectory);
  const pxtOutputPath = path.join(
    rootDirectory,
    'sample-compass-makecode/built/binary.hex'
  );

  assert.notEqual(outputPaths.makecode, pxtOutputPath);
});

test('the generator skill documents the fixed blocks.hex output paths', () => {
  const skill = fs.readFileSync(
    path.resolve(__dirname, '../skills/microbit-generate-blocks-hex/SKILL.md'),
    'utf8'
  );

  assert.match(skill, /sample-compass\/dist\/hex\/blocks\.hex/);
  assert.match(skill, /sample-compass-makecode\/built\/blocks\.hex/);
  assert.doesNotMatch(
    skill,
    /compass_makecode_blocks|binary_blocks|dist\/hex\/binary\.hex/
  );
});

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
