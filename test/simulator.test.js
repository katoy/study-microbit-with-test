const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const test = require('node:test');
const { chromium } = require('playwright');

const projectRoot = path.resolve(__dirname, '..');

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const EXPECTED_DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];

const EMPTY_PATTERN = [
  '.....',
  '.....',
  '.....',
  '.....',
  '.....'
].join('\n');

const EXPECTED_PATTERNS_TS = {
  0: [ // 北 N
    '..#..',
    '.###.',
    '#.#.#',
    '.....',
    '.....'
  ].join('\n'),
  45: EMPTY_PATTERN,  // NE
  90: [ // 東 E
    '..#..',
    '..##.',
    '..#..',
    '..##.',
    '..#..'
  ].join('\n'),
  135: EMPTY_PATTERN, // SE
  180: [ // 南 S
    '..#..',
    '.....',
    '#.#.#',
    '.###.',
    '..#..'
  ].join('\n'),
  225: EMPTY_PATTERN, // SW
  270: [ // 西 W
    '..#..',
    '.##..',
    '..#..',
    '.##..',
    '..#..'
  ].join('\n'),
  315: EMPTY_PATTERN  // NW
};

const EXPECTED_PATTERNS_PY = {
  0: [ // 北 N
    '..#..',
    '.###.',
    '#.#.#',
    '..#..',
    '..#..'
  ].join('\n'),
  45: [ // 北東 NE
    '..###',
    '...##',
    '..#.#',
    '.#...',
    '#....'
  ].join('\n'),
  90: [ // 東 E
    '..#..',
    '...#.',
    '#####',
    '...#.',
    '..#..'
  ].join('\n'),
  135: [ // 南東 SE
    '#....',
    '.#...',
    '..#.#',
    '...##',
    '..###'
  ].join('\n'),
  180: [ // 南 S
    '..#..',
    '..#..',
    '#.#.#',
    '.###.',
    '..#..'
  ].join('\n'),
  225: [ // 南西 SW
    '....#',
    '...#.',
    '#.#..',
    '##...',
    '###..'
  ].join('\n'),
  270: [ // 西 W
    '..#..',
    '.#...',
    '#####',
    '.#...',
    '..#..'
  ].join('\n'),
  315: [ // 北西 NW
    '###..',
    '##...',
    '#.#..',
    '...#.',
    '....#'
  ].join('\n')
};

async function getLedPattern(frame) {
  return await frame.evaluate(() => {
    const leds = document.querySelectorAll('rect.sim-led');
    let grid = [];
    for (let y = 0; y < 5; y++) {
      let row = '';
      for (let x = 0; x < 5; x++) {
        const led = Array.from(leds).find(l => {
          const title = l.querySelector('title');
          return title && title.textContent === `(${x},${y})`;
        });
        if (led) {
          const style = led.getAttribute('style') || '';
          const fill = led.getAttribute('fill') || '';
          const isLit = style.includes('opacity: 1') || fill === '#ff0000' || fill === 'rgb(255, 0, 0)' || style.includes('opacity:1');
          row += isLit ? '#' : '.';
        } else {
          row += '.';
        }
      }
      grid.push(row);
    }
    return grid.join('\n');
  });
}

test('MakeCode web simulator runs compass_makecode.py and responds to 45 degree rotation steps', { timeout: 120000 }, async () => {
  const pythonPath = path.join(projectRoot, 'sample-compass/src/compass_makecode.py');
  assert.ok(fs.existsSync(pythonPath), 'compass_makecode.py exists');
  
  // キャリブレーション状態チェックを強制バイパスし、すべての show_string を clear_screen に置き換える
  const rawPythonCode = fs.readFileSync(pythonPath, 'utf8');
  const pythonCode = rawPythonCode
    .replace(/is_calibrated = False/g, 'is_calibrated = True')
    .replace(/if not is_calibrated:/g, 'if False:')
    .replace(/basic\.show_string\([^)]*\)/g, 'basic.clear_screen()');

  console.log('Starting Playwright simulator rotation test for Python...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    locale: 'ja-JP',
    acceptDownloads: true
  });
  const page = await context.newPage();

  // コンソールログを蓄積
  const consoleLogs = [];
  page.on('console', msg => {
    console.log(`[Browser Console] ${msg.text()}`);
    consoleLogs.push(msg.text());
  });

  try {
    // 1. MakeCode にアクセス
    await page.goto('https://makecode.microbit.org/', { waitUntil: 'networkidle' });
    await delay(2000);

    // 2. 新しいプロジェクトを作成
    const newProjectBtn = page.locator('.ui.card:has-text("新しいプロジェクト"), .ui.card:has-text("New Project")');
    await newProjectBtn.first().click({ force: true });
    await delay(1000);

    const projName = `compass-py-rot-test-${Date.now()}`;
    await page.locator('input#projectNameInput').fill(projName);
    
    const createBtn = page.getByRole('button', { name: '作成' }).or(page.getByRole('button', { name: 'Create' }));
    await createBtn.first().click({ force: true });
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    await delay(3000);

    // チュートリアルポップアップなどのクリーンアップ
    await page.evaluate(() => {
      const selectors = [
        '.teaching-bubble-container',
        '.common-focus-trap',
        '.ui.dimmer.active',
        '.ui.modal.transition.visible'
      ];
      selectors.forEach(selector => {
        const els = document.querySelectorAll(selector);
        els.forEach(el => el.remove());
      });
    });
    await delay(500);

    // 3. Python エディタモードに切り替える
    try {
      await page.locator('.python-menuitem').first().click({ timeout: 3000, force: true });
    } catch (e) {
      await page.locator('#editordropdown').click({ force: true });
      await delay(500);
      await page.locator('.python-menuitem').first().click({ force: true });
    }
    await delay(2000);

    // 4. Monaco エディタにソースコードを注入
    const sourceWasInjected = await page.evaluate((code) => {
      if (typeof window.monaco !== 'undefined') {
        const models = window.monaco.editor.getModels();
        const pyModel = models.find(m => m.uri.path.endsWith('.py') || m.uri.path.endsWith('main.py'));
        if (pyModel) {
          pyModel.setValue(code);
          return true;
        } else if (models && models.length > 0) {
          models[0].setValue(code);
          return true;
        }
      }
      return false;
    }, pythonCode);
    assert.ok(sourceWasInjected, 'Source code was injected into monaco editor');
    await delay(3000);

    // 5. ブロック表示に戻す
    try {
      await page.locator('.blocks-menuitem').first().click({ timeout: 3000, force: true });
    } catch (e) {
      const convertBtn = page.getByRole('button', { name: 'プログラムをブロックに変換する。' })
        .or(page.getByRole('button', { name: 'Blocks' }));
      await convertBtn.first().click({ force: true });
    }
    await delay(5000); // ロードを待つ

    // 6. シミュレータのロード完了を待つ
    const simIframe = page.frameLocator('iframe[title*="Simulator"]');
    const simSvg = simIframe.locator('svg').first();
    await simSvg.waitFor({ state: 'visible', timeout: 15000 });
    console.log('✓ Simulator loaded (Python)');

    // 7. 45度ずつ回転させて LED パターンをチェック
    const headings = [0, 45, 90, 135, 180, 225, 270, 315];
    const frameElement = await page.locator('iframe[title*="Simulator"]').first().elementHandle();
    const frame = await frameElement.contentFrame();

    for (let i = 0; i < headings.length; i++) {
      const heading = headings[i];
      console.log(`Setting heading to ${heading}° (Python)...`);
      await frame.evaluate((h) => {
        const board = window.pxsim.board();
        board.compassState.heading = h;
        board.updateView();
      }, heading);

      await delay(1200); // 描画更新待ち

      const ledPattern = await getLedPattern(frame);
      console.log(`LED Pattern at ${heading}° (Python):\n${ledPattern}`);

      assert.strictEqual(ledPattern, EXPECTED_PATTERNS_PY[heading], `LED pattern mismatch at ${heading}° (Python)`);
      console.log(`✓ Verified LED pattern for ${heading}° (Python)`);

      // Aボタンをクリックしてログをチェック
      consoleLogs.length = 0; // ログをクリア
      const btnA = simIframe.locator('.sim-button-group:has-text("A"), rect.sim-button-outer').first();
      await btnA.click({ force: true });

      const expectedDir = EXPECTED_DIRECTIONS[i];
      const expectedRegex = new RegExp(`Time: \\d+ms, Heading: ${heading}, Dir: ${expectedDir}`);
      
      let found = false;
      for (let attempt = 0; attempt < 25; attempt++) {
        found = consoleLogs.some(log => expectedRegex.test(log));
        if (found) break;
        await delay(200); // 0.2秒待機 (最大5秒)
      }
      assert.ok(found, `Expected console log not found for heading ${heading}. Current logs: ${consoleLogs}`);
      console.log(`✓ Verified console log output for ${heading}° (Python)`);
    }

    // 8. スクリーンショットを保存
    const screenshotDir = path.join(projectRoot, 'dist');
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }
    await simIframe.locator('.sim-embed, #board-container, svg.sim').first()
      .screenshot({ path: path.join(screenshotDir, 'rotation-test-py.png') });

  } catch (error) {
    const errorScreenshotPath = path.join(projectRoot, 'error-rotation-py.png');
    await page.screenshot({ path: errorScreenshotPath, fullPage: true });
    console.error('Python Rotation Test failed. Saved screenshot to:', errorScreenshotPath);
    throw error;
  } finally {
    await browser.close();
  }
});

test('MakeCode web simulator runs sample-compass-makecode (TypeScript) and responds to 45 degree rotation steps', { timeout: 120000 }, async () => {
  const tsPath = path.join(projectRoot, 'sample-compass-makecode/src/compass.ts');
  const mainPath = path.join(projectRoot, 'sample-compass-makecode/src/main.ts');
  assert.ok(fs.existsSync(tsPath), 'compass.ts exists');
  assert.ok(fs.existsSync(mainPath), 'main.ts exists');
  
  // キャリブレーションチェックと未校正化リセット判定を強制バイパスし、すべての showString を clearScreen に置き換える
  // また、Invalid block definition エラーを防ぐため、カスタムブロックアノテーション (//% ...) をすべて削除する
  const rawCompassCode = fs.readFileSync(tsPath, 'utf8');
  const compassCode = rawCompassCode
    .replace(/if\s*\(!_isCalibrated\)/g, 'if (false)')
    .replace(/if\s*\(_heading\s*<\s*0\)/g, 'if (false)')
    .replace(/\/\/%[^\n]*/g, ''); // //% メタデータコメント行を削除

  const rawMainCode = fs.readFileSync(mainPath, 'utf8');
  const mainCode = rawMainCode
    .replace(/basic\.showString\([^)]*\);/g, 'basic.clearScreen();');
    
  const tsCode = `${compassCode}\n${mainCode}`;

  console.log('Starting Playwright simulator rotation test for TypeScript...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    locale: 'ja-JP',
    acceptDownloads: true
  });
  const page = await context.newPage();

  // ブラウザ側のコンソールログを出力させて Monaco モデルのパスやエラーをトレースする
  page.on('console', msg => {
    console.log(`[Browser Console] ${msg.text()}`);
  });

  try {
    // 1. MakeCode にアクセス
    await page.goto('https://makecode.microbit.org/', { waitUntil: 'networkidle' });
    await delay(2000);

    // 2. 新しいプロジェクトを作成
    const newProjectBtn = page.locator('.ui.card:has-text("新しいプロジェクト"), .ui.card:has-text("New Project")');
    await newProjectBtn.first().click({ force: true });
    await delay(1000);

    const projName = `compass-ts-rot-test-${Date.now()}`;
    await page.locator('input#projectNameInput').fill(projName);
    
    const createBtn = page.getByRole('button', { name: '作成' }).or(page.getByRole('button', { name: 'Create' }));
    await createBtn.first().click({ force: true });
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    await delay(3000);

    // チュートリアルポップアップなどのクリーンアップ
    await page.evaluate(() => {
      const selectors = [
        '.teaching-bubble-container',
        '.common-focus-trap',
        '.ui.dimmer.active',
        '.ui.modal.transition.visible'
      ];
      selectors.forEach(selector => {
        const els = document.querySelectorAll(selector);
        els.forEach(el => el.remove());
      });
    });
    await delay(500);

    // 3. JavaScript エディタモードに切り替える
    try {
      await page.locator('.javascript-menuitem').first().click({ timeout: 3000, force: true });
    } catch (e) {
      await page.locator('#editordropdown').click({ force: true });
      await delay(500);
      await page.locator('.javascript-menuitem').first().click({ force: true });
    }
    await delay(2000);

    // 4. Monaco エディタにソースコードを注入 (明示的に .ts / main.ts のモデルを特定する)
    const sourceWasInjected = await page.evaluate((code) => {
      if (typeof window.monaco !== 'undefined') {
        const models = window.monaco.editor.getModels();
        console.log("Monaco models available:", models.map(m => m.uri.path));
        // main.ts または拡張子が .ts の編集対象モデルを探す
        const tsModel = models.find(m => m.uri.path.endsWith('main.ts') || m.uri.path.endsWith('.ts'));
        if (tsModel) {
          console.log(`Setting value to TS model: ${tsModel.uri.path}`);
          tsModel.setValue(code);
          return true;
        } else if (models && models.length > 0) {
          console.log(`TS model not found, falling back to 0th model: ${models[0].uri.path}`);
          models[0].setValue(code);
          return true;
        }
      }
      return false;
    }, tsCode);
    assert.ok(sourceWasInjected, 'Source code was injected into monaco editor');
    await delay(3000);

    // 5. ブロック表示に戻す
    try {
      await page.locator('.blocks-menuitem').first().click({ timeout: 3000, force: true });
    } catch (e) {
      const convertBtn = page.getByRole('button', { name: 'プログラムをブロックに変換する。' })
        .or(page.getByRole('button', { name: 'Blocks' }));
      await convertBtn.first().click({ force: true });
    }
    await delay(5000); // ロードを待つ

    // 6. シミュレータのロード完了を待つ
    const simIframe = page.frameLocator('iframe[title*="Simulator"]');
    const simSvg = simIframe.locator('svg').first();
    await simSvg.waitFor({ state: 'visible', timeout: 15000 });
    console.log('✓ Simulator loaded (TS)');

    // 7. 45度ずつ回転させて LED パターンをチェック
    const headings = [0, 45, 90, 135, 180, 225, 270, 315];
    const frameElement = await page.locator('iframe[title*="Simulator"]').first().elementHandle();
    const frame = await frameElement.contentFrame();

    for (const heading of headings) {
      console.log(`Setting heading to ${heading}° (TS)...`);
      await frame.evaluate((h) => {
        const board = window.pxsim.board();
        board.compassState.heading = h;
        board.updateView();
      }, heading);

      await delay(1200); // 描画更新待ち

      const ledPattern = await getLedPattern(frame);
      console.log(`LED Pattern at ${heading}° (TS):\n${ledPattern}`);

      assert.strictEqual(ledPattern, EXPECTED_PATTERNS_TS[heading], `LED pattern mismatch at ${heading}° (TS)`);
      console.log(`✓ Verified LED pattern for ${heading}° (TS)`);
    }

    // 8. スクリーンショットを保存
    const screenshotDir = path.join(projectRoot, 'dist');
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }
    await simIframe.locator('.sim-embed, #board-container, svg.sim').first()
      .screenshot({ path: path.join(screenshotDir, 'rotation-test-ts.png') });

  } catch (error) {
    const errorScreenshotPath = path.join(projectRoot, 'error-rotation-ts.png');
    await page.screenshot({ path: errorScreenshotPath, fullPage: true });
    console.error('TS Rotation Test failed. Saved screenshot to:', errorScreenshotPath);
    throw error;
  } finally {
    await browser.close();
  }
});
