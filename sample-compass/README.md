# sample-compass

micro:bit 用のシンプルな方位磁石アプリケーション

## 機能

- 🧭 **方位角検出**: 0-359 度の方位角を取得
- 🗺️ **8 方位判定**: 北（N）、北東（NE）、東（E）、南東（SE）、南（S）、南西（SW）、西（W）、北西（NW）
- 🔄 **キャリブレーション**: ボタンA でコンパスをキャリブレーション

## インストール

micro:bit Python Editor（https://python.microbit.org）で `compass.py` の内容をコピー＆ペーストして、micro:bit に転送してください。

## 使用方法

1. micro:bit 上で実行すると、LED ディスプレイに現在の方向と角度が表示されます
2. ボタンA を押すとコンパスをキャリブレーションします

## テスト

```bash
pip install pytest pytest-cov
pytest test_compass.py -v
```

## テストカバレッジ

```bash
pytest test_compass.py --cov=. --cov-report=html
```

## CI/CD

GitHub Actions で自動的に pytest を実行します。

- Python 3.8 - 3.11 で実行
- カバレッジレポートを Codecov にアップロード

## ライセンス

MIT
