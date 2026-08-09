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
      console.error('\n[WORKSPACE HOOK] HEX生成の実行を検知しました。Playwrightによるブロック表示対応HEXの自動生成をバックグラウンドで開始します...');
      
      const scriptPath = path.join(__dirname, 'generate-blocks-hex.js');
      const result = spawnSync('node', [scriptPath], { stdio: 'inherit' });
      
      if (result.status !== 0) {
        console.error('[WORKSPACE HOOK] ✗ ブロック表示対応HEXの自動生成に失敗しました。');
      } else {
        console.error('[WORKSPACE HOOK] ✓ ブロック表示対応HEXの自動生成が正常に完了しました。\n');
      }
    }
  } catch (err) {
    console.error('[WORKSPACE HOOK] Error in hook runner:', err);
  }
  
  // 本来のコマンド実行を許可する
  console.log(JSON.stringify({ decision: 'allow' }));
});
