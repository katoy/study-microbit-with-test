# GitHub Actionsでの統合・シミュレーターテスト

`.github/workflows/integration-tests.yml` は、次のテストを実行します。

- Python: モック化したmicro:bit APIとアプリケーションの統合テスト
- TypeScript: Node.js上で複数のCompass APIを組み合わせる統合テスト
- MakeCode: コンパイル確認とPXT内蔵シミュレーターでの方位判定テスト

## ローカルでの再現

リポジトリルートから全テストを実行できます。

```bash
npm run test:all
```

MakeCodeだけを確認する場合は次を実行します。

```bash
cd sample-compass-makecode
npm ci
npm test
```

## 保証しない範囲

CIは実機、USB転送、ブラウザ版MakeCode EditorのUIを操作しません。これらが必要なリリースでは、生成したHEXの実機転送とセンサー・ボタン・LED表示の手動確認を別途行ってください。

MakeCodeテストの詳細は [SIMULATOR_TEST_GUIDE.md](./SIMULATOR_TEST_GUIDE.md) を参照してください。
