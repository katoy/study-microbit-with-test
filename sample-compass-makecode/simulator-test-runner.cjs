const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const RESULT_PATTERN = /MAKECODE_TEST_RESULT total=(\d+) passed=(\d+) failed=(\d+)/;

function parseTestResult(output) {
  const match = output.match(RESULT_PATTERN);
  if (!match) {
    throw new Error('MakeCode simulator did not report a result');
  }

  const result = {
    total: Number(match[1]),
    passed: Number(match[2]),
    failed: Number(match[3]),
  };

  if (result.total !== result.passed + result.failed) {
    throw new Error('MakeCode simulator reported inconsistent test counts');
  }
  if (result.failed > 0) {
    throw new Error(`${result.failed} MakeCode test(s) failed`);
  }

  return result;
}

function run(command, args, options) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, options);
    let output = '';

    child.stdout.on('data', (chunk) => {
      const text = chunk.toString();
      output += text;
      process.stdout.write(text);
    });
    child.stderr.on('data', (chunk) => {
      const text = chunk.toString();
      output += text;
      process.stderr.write(text);
    });
    child.on('error', reject);
    child.on('close', (code, signal) => {
      if (code !== 0) {
        reject(
          new Error(
            `pxt run exited with ${signal ? `signal ${signal}` : `code ${code}`}`
          )
        );
        return;
      }
      resolve(output);
    });
  });
}

async function runSimulatorTests(projectDirectory = __dirname) {
  const pxtModules = path.join(projectDirectory, 'pxt_modules');
  if (!fs.existsSync(pxtModules)) {
    throw new Error('pxt_modules is missing; run pxt install before the simulator tests');
  }

  const buildDirectory = path.join(projectDirectory, 'built');
  fs.mkdirSync(buildDirectory, { recursive: true });
  const testDirectory = fs.mkdtempSync(path.join(buildDirectory, 'simulator-tests-'));

  try {
    fs.copyFileSync(
      path.join(projectDirectory, 'compass.ts'),
      path.join(testDirectory, 'compass.ts')
    );
    fs.copyFileSync(
      path.join(projectDirectory, 'test.ts'),
      path.join(testDirectory, 'test.ts')
    );
    fs.writeFileSync(
      path.join(testDirectory, 'main.ts'),
      'compassTests.runAllTests();\n',
      'utf8'
    );
    fs.writeFileSync(
      path.join(testDirectory, 'pxt.json'),
      `${JSON.stringify(
        {
          name: 'sample-compass-makecode-tests',
          dependencies: { core: '*' },
          files: ['main.ts', 'compass.ts', 'test.ts'],
          preferredEditor: 'tsprj',
        },
        null,
        2
      )}\n`,
      'utf8'
    );
    fs.symlinkSync(pxtModules, path.join(testDirectory, 'pxt_modules'), 'dir');

    const output = await run('pxt', ['run'], {
      cwd: testDirectory,
      env: process.env,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    return parseTestResult(output);
  } finally {
    fs.rmSync(testDirectory, { recursive: true, force: true });
  }
}

if (require.main === module) {
  runSimulatorTests()
    .then((result) => {
      console.log(
        `MakeCode simulator tests passed: ${result.passed}/${result.total}`
      );
    })
    .catch((error) => {
      console.error(`MakeCode simulator tests failed: ${error.message}`);
      process.exitCode = 1;
    });
}

module.exports = { parseTestResult, runSimulatorTests };
