# Custom Claude Code Skills

このディレクトリには、micro:bit 教育プロジェクト向けの カスタムスキルが含まれています。

## 利用可能なスキル

### 1. microbit-generate-blocks-hex

**説明**: Python または TypeScript の micro:bit ソースコードから MakeCode Web エディタ経由で「ブロック表示対応の HEX ファイル」を自動生成します。

**特徴**:
- Playwright ブラウザ自動操作による自動生成
- Python と TypeScript の両対応
- ライフサイクルフック統合により自動実行

**生成ファイル**:
- **Python 版**: `sample-compass/dist/hex/blocks.hex`
- **TypeScript/MakeCode 版**: `sample-compass-makecode/built/blocks.hex`

**手動実行**:
```bash
node ./scripts/generate-blocks-hex.js
```

**詳細**: [microbit-generate-blocks-hex/SKILL.md](./microbit-generate-blocks-hex/SKILL.md)

---

## スキル管理

### グローバル設定への登録

カスタムスキルを claude, agy, codex, copilot のグローバル設定に登録・削除するには、スキル管理スクリプトを使用します：

```bash
# claude に登録
scripts/manage-global-skills.sh add claude

# agy に登録
scripts/manage-global-skills.sh add agy

# 複数のエージェントに一度に登録
scripts/manage-global-skills.sh add claude agy codex copilot

# claude から削除
scripts/manage-global-skills.sh remove claude

# 全エージェントから削除
scripts/manage-global-skills.sh remove claude agy codex copilot

# 現在のステータスを確認
scripts/manage-global-skills.sh status
```

詳細は [scripts/manage-global-skills.sh](../scripts/manage-global-skills.sh) を参照してください。

---

## 開発ガイド

### 新しいスキルを追加する場合

1. `skills/` ディレクトリに新規フォルダを作成
2. `SKILL.md` ファイルを以下の形式で作成：
   ```markdown
   ---
   name: スキル名
   description: スキルの説明
   ---
   
   # スキルタイトル
   ...
   ```
3. 実装コードをプロジェクトに追加
4. `skills/README.md` を更新
5. `scripts/manage-global-skills.sh` で必要に応じてグローバル設定に追加

---

## ライセンス

MIT
