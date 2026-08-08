# study-microbit-with-test

micro:bit 用のシンプルな方位磁石アプリケーション学習プロジェクト

3つのサンプル実装を含んでいます：
- **sample-compass**: Python による実装（micro:bit API を使用）
- **sample-compass-ts**: TypeScript による実装（Jest テスト付き）
- **sample-compass-makecode**: MakeCode Editor 用の実装

## プロジェクト構成

```
.
├── sample-compass/           # Python 実装
│   ├── compass.py           # メインのコンパス実装
│   ├── test_compass.py      # pytest によるテスト
│   └── README.md
├── sample-compass-ts/       # TypeScript 実装
│   ├── src/                 # ソースコード
│   ├── test/                # Jest テスト
│   ├── package.json         # npm 依存関係
│   ├── tsconfig.json        # TypeScript 設定
│   ├── jest.config.js       # Jest 設定
│   └── README.md
└── sample-compass-makecode/ # MakeCode 実装
    ├── pxt.json            # PXT 設定
    └── README.md
```

## セットアップ

### Python 環境（sample-compass）

```bash
cd sample-compass
pip install pytest
```

### TypeScript 環境（sample-compass-ts）

```bash
cd sample-compass-ts
npm install
```

## テスト実行

### Python テスト

```bash
cd sample-compass
pytest test_compass.py -v
```

### TypeScript テスト

```bash
cd sample-compass-ts
npm test
```

### カバレッジレポート

```bash
cd sample-compass-ts
npm run test:coverage
```

## ビルド（TypeScript）

```bash
cd sample-compass-ts
npm run build
```

## CI/CD

このプロジェクトは GitHub Actions を使用して自動的にテストを実行します。

- **Python テスト**: `sample-compass/` のテストが実行されます
- **TypeScript テスト**: `sample-compass-ts/` のテストが実行されます

詳細は `.github/workflows/` を参照してください。

## ライセンス

MIT

## 参考リンク

- [micro:bit 公式ドキュメント](https://microbit.org/)
- [MicroPython Documentation](https://microbit-micropython.readthedocs.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
