# CLAUDE.md - Development Guide for AI Assistants

このファイルは AI アシスタント（Claude、Copilot など）がこのプロジェクトで作業する際の指南書です。

## プロジェクト概要

**目的**: micro:bit 用の方位磁石アプリケーション学習プロジェクト

**構成**:
- Python 実装（sample-compass）
- TypeScript 実装（sample-compass-ts）
- MakeCode 実装（sample-compass-makecode）

## ディレクトリ構造の理解

```
study-microbit-with-test/
├── .github/workflows/     # GitHub Actions CI/CD 設定
├── sample-compass/        # Python プロジェクト
│   ├── compass.py        # main implementation
│   └── test_compass.py   # pytest tests
├── sample-compass-ts/    # TypeScript プロジェクト
│   ├── src/              # TypeScript source
│   ├── test/             # Jest tests
│   ├── package.json      # npm dependencies & scripts
│   └── jest.config.js    # Jest configuration
└── sample-compass-makecode/  # MakeCode project
```

## テスト実行方法

### Python テスト
```bash
cd sample-compass
pytest test_compass.py -v
# またはカバレッジ付き
pytest test_compass.py --cov=compass
```

### TypeScript テスト
```bash
cd sample-compass-ts
npm test
# またはカバレッジ付き
npm run test:coverage
```

## コード規約

### Python (sample-compass)
- PEP 8 に準拠
- docstring は Google スタイル
- テストは pytest を使用
- ファイル名: snake_case

### TypeScript (sample-compass-ts)
- ESLint 設定を確認してから編集
- テストは Jest を使用
- ファイル名: camelCase または snake_case
- 型定義は明示的に記述

## よくある作業

### 新しいテストを追加する

**Python の場合**:
```python
# test_compass.py に追加
def test_new_feature():
    """新機能のテスト"""
    # arrange
    compass = MockCompass()
    # act
    result = compass.some_method()
    # assert
    assert result == expected_value
```

**TypeScript の場合**:
```typescript
// test/compass.test.ts に追加
describe('Compass', () => {
  test('should handle new feature', () => {
    // arrange
    const compass = new Compass();
    // act
    const result = compass.someMethod();
    // assert
    expect(result).toBe(expectedValue);
  });
});
```

### 新機能を追加する

1. テストを先に書く（TDD）
2. テストが失敗することを確認
3. 最小限の実装を行う
4. テストが成功することを確認
5. リファクタリング

### CI/CD パイプラインをテストする

ローカルで GitHub Actions をシミュレート：
```bash
# docker が必要
act -l  # 使用可能なワークフローを表示
act     # すべてのワークフローを実行
```

## よくある問題とトラブルシューティング

### pytest が見つからない
```bash
pip install pytest pytest-cov
```

### npm dependencies のエラー
```bash
cd sample-compass-ts
rm -rf node_modules package-lock.json
npm install
npm test
```

### TypeScript のビルドエラー
```bash
cd sample-compass-ts
npm run build
# エラーメッセージから型の問題を修正
```

### テストファイルが検出されない
- Python: テストファイルは `test_*.py` または `*_test.py` として命名
- TypeScript: テストファイルは `*.test.ts` または `*.spec.ts` として命名

## 推奨される変更ワークフロー

1. ブランチを作成: `git checkout -b feature/your-feature`
2. 変更を加える
3. ローカルでテスト実行: `pytest` または `npm test`
4. テストが全て成功することを確認
5. コミット: `git commit -am "Add your feature"`
6. PR を作成（GitHub Actions が自動的に実行される）

## CI/CD 設定

`.github/workflows/` に以下が含まれています：
- Python テスト: pytest を使用して `sample-compass/` をテスト
- TypeScript テスト: Jest を使用して `sample-compass-ts/` をテスト

全てのプッシュと PR に対して自動実行されます。

## 外部リソース

- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [Jest Documentation](https://jestjs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 質問や改善提案

このファイルは継続的に改善されています。
プロジェクトのベストプラクティスを発見したら、このファイルを更新してください。
