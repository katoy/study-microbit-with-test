# CLAUDE.md - Python Compass Project Guide

このファイルは AI アシスタントが sample-compass プロジェクトで作業する際のガイドです。

## プロジェクト概要

MakeCodeのブロックへ変換できるStatic Python (`compass_makecode.py`) を扱っています。

## ディレクトリ構造

```
sample-compass/
├── src/
│   └── compass_makecode.py  # MakeCode Python
├── test/
│   └── test_simulator.py    # Playwright シミュレーターテスト
├── pyproject.toml           # uv project configuration
├── CLAUDE.md                # このファイル
├── README.md
└── .tool-versions           # Python version management (3.11.5)
```

## コンパイルチェック

```bash
uv run python -m py_compile src/compass_makecode.py
```

## テスト実行

```bash
uv run pytest test/test_simulator.py -v -s
```
