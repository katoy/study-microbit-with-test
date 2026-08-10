const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getBlocksHexOutputPaths(rootDirectory) {
  return {
    python: path.join(
      rootDirectory,
      'projects/sample-compass/dist/hex/blocks.hex'
    ),
    makecode: path.join(
      rootDirectory,
      'projects/sample-compass-makecode/built/blocks.hex'
    )
  };
}

function evaluateBlocksConversionStatus({
  errorDialogCount,
  greyBlockCount,
  workspaceCount
}) {
  if (errorDialogCount > 0) {
    throw new Error('MakeCode reported a block conversion error');
  }
  if (greyBlockCount > 0) {
    throw new Error(`MakeCode produced ${greyBlockCount} non-editable grey block(s)`);
  }
  if (workspaceCount < 1) {
    throw new Error('MakeCode did not render a Blockly workspace');
  }
}

async function verifyBlocksConversion(page) {
  const status = {
    errorDialogCount: await page
      .locator('.ui.modal.error:visible, .compilation-error-widget:visible')
      .count(),
    greyBlockCount: await page
      .locator('g.blocklyDraggable.blocklyDisabled, g.ui-grey-block')
      .count(),
    workspaceCount: await page
      .locator('.blocklyWorkspace, svg.blocklySvg')
      .count()
  };

  evaluateBlocksConversionStatus(status);
  return status;
}

async function buildBlocksHexForProject(language, sourceCode, outputPath) {
  console.log(`Starting blocks-HEX generation for ${language}...`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    locale: 'ja-JP', // 日本語 UI で実行
    acceptDownloads: true
  });
  const page = await context.newPage();

  try {
    // 1. MakeCode にアクセス
    await page.goto('https://makecode.microbit.org/', { waitUntil: 'networkidle' });
    await delay(2000);

    // 2. 新しいプロジェクトを作成
    const newProjectBtn = page.locator('.ui.card:has-text("新しいプロジェクト"), .ui.card:has-text("New Project")');
    await newProjectBtn.first().click({ force: true });
    await delay(1000);

    const projName = `compass-${language.toLowerCase()}-${Date.now()}`;
    await page.locator('input#projectNameInput').fill(projName);
    
    const createBtn = page.getByRole('button', { name: '作成' }).or(page.getByRole('button', { name: 'Create' }));
    await createBtn.first().click({ force: true });
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    await delay(3000);

    // [堅牢性向上のためのエッジケース対応]
    // 初回起動時のチュートリアル（ティーチングバブル・ガイド）やモーダル表示が操作を邪魔するため、
    // DOM からこれらを強制的に削除する
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

    // 3. エディタモードを切り替える
    if (language === 'Python') {
      try {
        await page.locator('.python-menuitem').first().click({ timeout: 3000, force: true });
      } catch (e) {
        await page.locator('#editordropdown').click({ force: true });
        await delay(500);
        await page.locator('.python-menuitem').first().click({ force: true });
      }
    } else { // TypeScript / JavaScript
      try {
        await page.locator('.javascript-menuitem').first().click({ timeout: 3000, force: true });
      } catch (e) {
        await page.locator('#editordropdown').click({ force: true });
        await delay(500);
        await page.locator('.javascript-menuitem').first().click({ force: true });
      }
    }
    await delay(2000);

    // 4. Monaco エディタにソースコードを注入
    const sourceWasInjected = await page.evaluate((code) => {
      if (typeof window.monaco !== 'undefined') {
        const models = window.monaco.editor.getModels();
        if (models && models.length > 0) {
          models[0].setValue(code);
          return true;
        }
      }
      return false;
    }, sourceCode);
    if (!sourceWasInjected) {
      throw new Error(`Unable to inject ${language} source into the MakeCode editor`);
    }
    await delay(3000); // 構文解析を待つ

    // 5. ブロック表示に戻す（これでパースが確定し、HEXにブロックメタデータが埋め込まれる）
    try {
      await page.locator('.blocks-menuitem').first().click({ timeout: 3000, force: true });
    } catch (e) {
      const convertBtn = page.getByRole('button', { name: 'プログラムをブロックに変換する。' })
        .or(page.getByRole('button', { name: 'Blocks' }));
      await convertBtn.first().click({ force: true });
    }
    await delay(5000); // ブロックレンダリング完了を待つ

    const conversionStatus = await verifyBlocksConversion(page);
    console.log(
      `✓ Editable blocks verified: ${conversionStatus.workspaceCount} workspace(s), no errors or grey blocks`
    );

    // 6. ダウンロードイベントを監視しながら直接ファイル保存を実行
    console.log(`Downloading HEX for ${language} via direct file download menu...`);
    const downloadPromise = page.waitForEvent('download', { timeout: 45000 });

    // ダウンロードコンテナ (#downloadarea) の中にある ellipsis（3点リーダー）アイコンをクリックしてメニューを展開
    const menuButton = page.locator('#downloadarea .ellipsis.icon, .download-button + .dropdown, .download-button + .button').first();
    await menuButton.click({ force: true });
    await delay(1000);

    // メニュー展開内容をログ出力（デバッグ用）
    const menuItems = await page.locator('.ui.dropdown.active .menu .item, .menu .item').allTextContents();
    console.log('Dropdown Menu Items:', menuItems);

    // 「ファイルをダウンロード」または「Download file」を明示的に選択してクリック
    const downloadFileItem = page.locator('.menu .item:has-text("ファイルとしてダウンロードする"), .menu .item:has-text("ファイルをダウンロード"), .menu .item:has-text("Download file"), .menu .item:has-text("ファイル")');
    await downloadFileItem.first().click({ force: true });

    const download = await downloadPromise;

    // 保存先ディレクトリを確保
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    await download.saveAs(outputPath);
    console.log(`✓ Blocks-compatible HEX generated successfully: ${outputPath}`);
  } catch (error) {
    console.error(`✗ Failed to generate HEX for ${language}:`, error);
    // エラー時はスクリーンショットを撮ってデバッグしやすくする
    try {
      const screenshotPath = path.join(__dirname, `../error-${language.toLowerCase()}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`Saved error screenshot to: ${screenshotPath}`);
    } catch (e) {
      console.error('Failed to take screenshot:', e);
    }
    throw error;
  } finally {
    await browser.close();
  }
}

async function main() {
  const rootDir = path.join(__dirname, '..');
  const outputPaths = getBlocksHexOutputPaths(rootDir);
  
  // 1. Python 版 (MakeCode 互換)
  const pythonPath = path.join(rootDir, 'projects/sample-compass/src/compass_makecode.py');
  if (fs.existsSync(pythonPath)) {
    const pythonCode = fs.readFileSync(pythonPath, 'utf8');
    await buildBlocksHexForProject('Python', pythonCode, outputPaths.python);
  } else {
    console.warn(`Python source not found at: ${pythonPath}`);
  }

  // 2. TypeScript/MakeCode 版
  const makecodeCompassPath = path.join(rootDir, 'projects/sample-compass-makecode/src/compass.ts');
  const makecodeMainPath = path.join(rootDir, 'projects/sample-compass-makecode/src/main.ts');
  
  if (fs.existsSync(makecodeCompassPath) && fs.existsSync(makecodeMainPath)) {
    const compassCode = fs.readFileSync(makecodeCompassPath, 'utf8');
    const mainCode = fs.readFileSync(makecodeMainPath, 'utf8');
    
    // 2つのコードを綺麗に結合する
    const tsCode = `// ==========================================\n// compass.ts\n// ==========================================\n${compassCode}\n\n// ==========================================\n// main.ts\n// ==========================================\n${mainCode}`;
    await buildBlocksHexForProject('TypeScript', tsCode, outputPaths.makecode);
  } else {
    console.warn('MakeCode TS sources not found.');
  }
}

if (require.main === module) {
  main().catch(err => {
    console.error('Build execution failed:', err);
    process.exit(1);
  });
}

module.exports = {
  buildBlocksHexForProject,
  evaluateBlocksConversionStatus,
  getBlocksHexOutputPaths,
  verifyBlocksConversion
};
