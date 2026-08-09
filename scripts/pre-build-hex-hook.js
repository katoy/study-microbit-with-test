const fs = require('fs');
const { spawnSync } = require('child_process');
const path = require('path');

let inputData = '';
process.stdin.on('data', chunk => {
  inputData += chunk;
});

process.stdin.on('end', () => {
  try {
    const payload = JSON.parse(inputData);
    const cmdLine = payload.toolCall?.args?.CommandLine || '';
    
    // build_hex.py または build:hex が含まれるコマンド実行時に発動
    if (cmdLine.includes('build_hex.py') || cmdLine.includes('build:hex')) {
      console.error('\n[HOOK] HEX生成が検知されました。Playwrightによるブロック表示対応HEXの自動生成（スキル）を起動します...');
      
      const scriptPath = path.join(__dirname, 'generate-blocks-hex.js');
      // Playwright スクリプトを同期実行
      const result = spawnSync('node', [scriptPath], { stdio: 'inherit' });
      
      if (result.status !== 0) {
        console.error('[HOOK] ✗ ブロック表示対応HEXの自動生成に失敗しました。通常のビルド処理を続行します。');
      } else {
        console.error('[HOOK] ✓ ブロック表示対応HEXの自動生成が正常に完了しました。\n');
      }
    }
  } catch (err) {
    console.error('[HOOK] Error in pre-build-hex-hook:', err);
  }
  
  // 本来のコマンド実行を許可する
  console.log(JSON.stringify({ decision: 'allow' }));
});
