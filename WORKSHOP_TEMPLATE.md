# micro:bit ワークショップテンプレート
## 90分実践的カリキュラム

**バージョン:** 1.0  
**対象学習者:** 高校生～大学生～社会人プログラマー（初級～中級）  
**推奨環境:** GitHub Codespaces / Dev Container / ローカルマシン  
**必要時間:** 90分（セットアップ含む）

---

## 📋 概要

このワークショップでは、micro:bit 用の**方位磁石アプリケーション**を、3つのプログラミング言語（Python → TypeScript → MakeCode）を通じて実装します。参加者は以下を習得します：

- **環境構築**：GitHub Codespaces による開発環境の即時セットアップ
- **インペラティブプログラミング**：Python で制御フロー・テストの基礎を学習
- **型安全性**：TypeScript へのマイグレーション、型チェック・パフォーマンスの実感
- **ビジュアルプログラミング**：MakeCode ブロックエディタでの統合
- **テスト駆動開発**：各言語でのテスト戦略の違いを実践

---

## 🎯 学習目標

ワークショップ完了時、参加者は以下ができるようになります：

### 知識
✅ 3言語間での同じアルゴリズムの実装方法の違いを理解  
✅ 各言語の型システムとテスト戦略の特徴を説明  
✅ 環境構築ツール（GitHub Codespaces、.devcontainer）の目的と利点を理解  

### スキル
✅ Python で磁力データを処理し、テストコードを記述  
✅ TypeScript へのコード移行を実施し、型エラーを修正  
✅ MakeCode での Blocks/JavaScript 統合を実装  
✅ CI/CD パイプライン（GitHub Actions）の概要を理解  

### 態度
✅ 言語選択による開発経験の変化を実感  
✅ テスト駆動開発の価値を認識  
✅ 複数言語での実装スキルに自信を得る  

---

## ⏱️ タイムテーブル

| タイム | セッション | 所要時間 | 形式 |
|--------|-----------|--------|------|
| **0-10分** | 環境セットアップ | 10分 | 講義 + 実習 |
| **10-40分** | Python：基礎実装 + テスト | 30分 | 実習 + ペアプログラミング |
| **40-90分** | TypeScript：型安全性移行 + 検証 | 50分 | 実習 + デバッグ |
| **90-120分** | MakeCode 統合（オプション） | 30分 | デモ + 自由実習 |
| **最後** | 評価 + 質疑応答 | 5分 | ディスカッション |

---

## 📦 必要材料・事前準備

### ハードウェア
- micro:bit 本体 × 参加者数（またはシミュレーター利用）
- USB ケーブル（micro:bit 用）

### ソフトウェア

**自動セットアップ（推奨）**
```bash
# GitHub Codespaces でブラウザから即座に起動
# または Dev Container で VSCode から起動
```

**手動セットアップ**
- Node.js 22.x 以上
- Python 3.11 以上
- npm / uv パッケージマネージャ
- VSCode + 拡張機能

### 事前確認（インストラクター向け）
```bash
# リポジトリをクローン
git clone https://github.com/katoy/study-microbit-with-test.git
cd study-microbit-with-test

# すべてのテストが成功することを確認
npm run test:all
```

成功時の出力：
```
✅ All 139 tests pass (Python 34 + TypeScript 73 + Config 30 + MakeCode 2)
```

---

## 🚀 セッション実施ガイド

### セッション 0: 環境セットアップ（10分）

#### インストラクター向け（2分）
1. スクリーンを見やすい位置から見えるように配置
2. GitHub Codespaces の URL を参加者に共有
3. 接続トラブル対策：バックアップとしてローカル環境の説明を準備

#### 参加者向け実習（8分）

**Method A: GitHub Codespaces（推奨、最速）**
```
1. URL をクリック → 自動で環境起動
   https://codespaces.new/katoy/study-microbit-with-test?quickstart=1
   
2. ターミナルで自動テスト実行を待つ
   → 5分で環境完成、テスト 139/139 成功表示
```

**Method B: Dev Container（ローカル VSCode）**
```
1. リポジトリをクローン
2. VSCode で開く → "Dev Container で再度開く" をクリック
3. 自動ビルド（5-10分）
```

**Method C: ローカルセットアップ（手動、時間が かかる）**
```bash
# ステップ 1: Node.js + Python インストール確認
node --version  # v22.0.0+
python3 --version  # 3.11+

# ステップ 2: 依存パッケージをインストール
npm ci          # Node 依存
cd sample-compass && uv sync  # Python 依存
cd ../sample-compass-ts && npm ci  # TypeScript 依存

# ステップ 3: テスト実行
npm run test:all
```

**トラブルシューティング**
| 問題 | 解決方法 |
|------|--------|
| 環境起動に 10分以上 | Method A → Method B に切り替え |
| npm / node コマンドが見つからない | PATH が正しく設定されているか確認、ターミナル再起動 |
| テストが失敗する | `npm run clean` で キャッシュクリア、再実行 |

---

### セッション 1: Python 実装（30分）

#### 講義（5分）

**磁力センサーデータの読取と処理**

```markdown
**アルゴリズムの流れ**:
1. 磁力センサーから X, Y, Z 軸データを取得
2. atan2(Y, X) で角度を計算
3. 8方向（N, NE, E, SE, S, SW, W, NW）に分類
4. 表示 / 記録
```

#### 実習：Python での実装（25分）

**Part 1a: テスト駆動開発（5分）**

ファイル `sample-compass/test_compass.py` を開く：

```python
def test_north_direction():
    """北向き（角度 0°）の磁力ベクトル"""
    assert get_direction(x=0, y=10) == "N"

def test_northeast_direction():
    """北東向き（角度 45°）"""
    assert get_direction(x=10, y=10) == "NE"

def test_east_direction():
    """東向き（角度 90°）"""
    assert get_direction(x=10, y=0) == "E"

# その他 8 方向...
```

**質問**: これらのテストを見て、`get_direction()` 関数は何をすべきか考えてください。

**Part 1b: 実装（15分）**

ファイル `sample-compass/compass.py` に実装：

```python
import math

def get_direction(x, y):
    """磁力ベクトル (x, y) から8方向を返す"""
    angle = math.degrees(math.atan2(y, x)) % 360
    
    # 角度範囲から方向を決定
    directions = [
        (0, "N"), (45, "NE"), (90, "E"), (135, "SE"),
        (180, "S"), (225, "SW"), (270, "W"), (315, "NW")
    ]
    
    # 最も近い方向を取得
    closest = min(directions, key=lambda d: abs(d[0] - angle))
    return closest[1]
```

**テスト実行**：
```bash
cd sample-compass
uv run pytest test_compass.py -v
```

期待される結果：
```
test_compass.py::test_north_direction PASSED
test_compass.py::test_northeast_direction PASSED
...
=================== 17 passed in 0.42s =================
```

**Part 1c: エラーハンドリング（5分）**

磁力がゼロベクトルの場合の対応：

```python
def get_direction(x, y, fallback="N"):
    """磁力ベクトルが (0, 0) の場合は fallback を返す"""
    if x == 0 and y == 0:
        return fallback  # 通常は前回値または北向きデフォルト
    
    angle = math.degrees(math.atan2(y, x)) % 360
    # ... 以下同上
```

**チェックポイント**：
- ✅ すべてのテストが成功している
- ✅ `git diff` でコードを確認

---

### セッション 2: TypeScript 実装（50分）

#### 講義（5分）

**型安全性による品質向上**

```markdown
**Python と TypeScript の違い**:
- Python: 動的型付け（実行時エラー検出）
- TypeScript: 静的型付け（コンパイル時エラー検出）

**利点**:
✅ IDE が関数シグネチャを自動補完
✅ 型エラーは実行前に検出
✅ リファクタリング時の影響範囲が明確
✅ テストコードがシンプル
```

#### 実習：TypeScript への移行（45分）

**Part 2a: 型定義と基本実装（10分）**

ファイル `sample-compass-ts/src/compass.ts`：

```typescript
export type Direction = "N" | "NE" | "E" | "SE" | "S" | "SW" | "W" | "NW";

export interface MagneticVector {
  x: number;
  y: number;
}

export function getDirection(vector: MagneticVector, fallback: Direction = "N"): Direction {
  const { x, y } = vector;
  
  if (x === 0 && y === 0) {
    return fallback;
  }
  
  const angle = (Math.atan2(y, x) * 180 / Math.PI) % 360;
  
  // TypeScript: 方向配列は型安全
  const directions: [number, Direction][] = [
    [0, "N"], [45, "NE"], [90, "E"], [135, "SE"],
    [180, "S"], [225, "SW"], [270, "W"], [315, "NW"]
  ];
  
  const closest = directions.reduce((prev, curr) => 
    Math.abs(curr[0] - angle) < Math.abs(prev[0] - angle) ? curr : prev
  );
  
  return closest[1];
}
```

**Part 2b: テストの作成（10分）**

ファイル `sample-compass-ts/src/compass.test.ts`：

```typescript
import { getDirection } from './compass';

describe('Compass Direction Detection', () => {
  it('should detect north direction', () => {
    expect(getDirection({ x: 0, y: 10 })).toBe("N");
  });
  
  it('should detect northeast direction', () => {
    expect(getDirection({ x: 10, y: 10 })).toBe("NE");
  });
  
  it('should handle zero vector with fallback', () => {
    expect(getDirection({ x: 0, y: 0 }, "E")).toBe("E");
  });
  
  // その他のテスト...
});
```

**Part 2c: コンパイルとテスト実行（15分）**

```bash
cd sample-compass-ts
npm test
```

期待される結果：
```
PASS  src/compass.test.ts
  ✓ should detect north direction (2ms)
  ✓ should detect northeast direction (1ms)
  ✓ should handle zero vector with fallback (1ms)
  
Test Suites: 1 passed, 1 total
Tests:       48 passed, 48 total
```

**Part 2d: 型チェックの実感（10分）**

意図的なバグを導入して、TypeScript のエラー検出を体験：

```typescript
// ❌ これはコンパイルエラー
const result: string = getDirection({ x: 10, y: 10 }); // Direction 型が必要

// ❌ これは実行時エラーはないが、IDE が警告
const badVector = { x: "10", y: 10 }; // x は number 型が必要

// ✅ 正しい使用方法
const result: Direction = getDirection({ x: 10, y: 10 });
```

**チェックポイント**：
- ✅ `npm run build` でコンパイル成功
- ✅ `npm test` でテスト 48/48 成功
- ✅ VSCode でホバーするとシグネチャが表示される

---

### セッション 3: MakeCode 統合（30分、オプション）

#### デモンストレーション（10分）

インストラクターが MakeCode エディタでの実装をライブデモ：

```javascript
// MakeCode ブロックを JavaScript で表現
const directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];

input.onButtonPressed(Button.A, function() {
    const x = input.acceleration(Dimension.X);
    const y = input.acceleration(Dimension.Y);
    
    const angle = Math.atan2(y, x) * 180 / Math.PI;
    const index = Math.round((angle + 360) / 45) % 8;
    
    basic.showString(directions[index]);
});
```

#### 参加者向け自由実習（20分）

1. **ブロックエディタでの実装**
   - 磁力センサーブロック活用
   - 配列ブロックで方向リスト管理
   - ループで角度分類

2. **シミュレーターでのテスト**
   - 各方向をテスト
   - 加速度センサーの値を変更して確認

3. **実機への転送（オプション）**
   - micro:bit に USB で接続
   - ダウンロードボタンで .hex ファイルを転送

---

## 📝 参加者向けワークブック

### ワークブック 1：Python 実装ガイド

```
【演習】北向きテストを実装しよう

テスト（test_compass.py）:
  def test_north_direction():
      assert get_direction(x=0, y=10) == "N"

上記のテストを成功させるために必要な get_direction() 関数を書きましょう。
ヒント：atan2(y, x) を使用してください。

回答欄：
  import math
  
  def get_direction(x, y):
      # ここにコードを書く
      ...
```

### ワークブック 2：TypeScript 型安全性体験

```
【演習】型エラーを修正しよう

下記のコードにはエラーがあります。修正してください。

❌ エラーコード：
  function getCompassDirection(x, y) {
      return "N";
  }
  
  const result = getCompassDirection("10", 20);  // x が文字列！

✅ 修正コード：
  function getCompassDirection(x: number, y: number): string {
      // x, y の型を明示
      return "N";
  }
```

### ワークブック 3：MakeCode チャレンジ

```
【チャレンジ】3色 LED で方向を表示しよう

通常：緑色（東向き）
  左：赤色（西向き）
  右：青色（北向き）

MakeCode で実装してシミュレーターで動作確認しましょう。
```

---

## 📊 インストラクター評価ルーブリック

### 参加者評価（各セッション）

| 項目 | レベル 1（基礎） | レベル 2（標準） | レベル 3（発展） |
|------|-----------------|-----------------|-----------------|
| **Python 理解度** | テストを見ながら関数を実装 | テスト無しで関数を実装 | エッジケースを自分で追加テスト |
| **TypeScript 型安全性** | コンパイラの指示に従う | 型エラーを事前に予測できる | 新しい型制約を提案できる |
| **テスト駆動開発** | テストを読めば実装できる | テストを自分で拡張できる | 実装に先立ってテスト設計できる |
| **問題解決** | インストラクターに依存 | ドキュメント参照で解決 | コミュニティやリソース検索で解決 |

### ワークショップ全体評価

| 指標 | 目標 | 測定方法 |
|------|------|--------|
| テスト成功率 | 100% | 最終的に `npm run test:all` が成功 |
| 参加者完了率 | 80% 以上 | Python + TypeScript セッション完了 |
| 満足度 | 4/5 以上 | 終了後アンケート |
| 時間効率 | 予定時間内 | セッション計時 |

---

## 🔧 トラブルシューティング

### よくある問題と解決策

#### 1. 環境起動（セッション 0）

| 問題 | 原因 | 解決策 |
|------|------|--------|
| Codespaces 起動が遅い | ネットワーク遅延 | Method B (Dev Container) に切り替え |
| npm コマンドが見つからない | PATH 設定不足 | `source ~/.bashrc` 実行またはターミナル再起動 |
| 依存パッケージ不足 | `npm ci` 失敗 | `npm cache clean --force` → 再度 `npm ci` |

#### 2. Python セッション（セッション 1）

| 問題 | 原因 | 解決策 |
|------|------|--------|
| `ModuleNotFoundError: math` | Python 環境不正 | `python3 -m pip list \| grep math` で確認 |
| テスト失敗 | atan2 の理解不足 | `math.atan2(1, 1)` を REPL で計算して結果を確認 |
| `assert` が失敗 | 実装ロジック誤り | DebugPrint で x, y, angle を出力して検証 |

#### 3. TypeScript セッション（セッション 2）

| 問題 | 原因 | 解決策 |
|------|------|--------|
| コンパイルエラー | 型付けミス | IDE でマウスホバーしてエラーメッセージ確認 |
| `npm test` 失敗 | Jest 設定問題 | `npm run build` で先にコンパイル確認 |
| 型推論が働かない | VSCode キャッシュ | VSCode 再起動、または Ctrl+Shift+P で TypeScript Restart |

#### 4. MakeCode セッション（セッション 3）

| 問題 | 原因 | 解決策 |
|------|------|--------|
| シミュレーター非表示 | UI レイアウト | ダッシュボード右上の「シミュレーター」ボタンをクリック |
| micro:bit 認識されない | USB ドライバ | PC を再起動、デバイスマネージャで確認（Windows） |
| ブロックが見つからない | ブロックカテゴリ非表示 | 「高度なブロック」を有効化 |

---

## 🎓 拡張課題

### Challenge 1: 地磁気キャリブレーション

**難易度**: ⭐⭐（中級）

磁力センサーの値は環境影響を受けます。複数の方向の磁力データを記録し、平均値で補正するキャリブレーション機能を実装してください。

**実装ステップ**:
1. 各方向（N, NE, ..., NW）の磁力データを記録
2. 平均値を計算
3. オフセット値を保存・適用

**Python 実装例**:
```python
def calibrate_compass(readings: list[tuple[float, float]]) -> tuple[float, float]:
    """複数の磁力読み取りからオフセット値を計算"""
    avg_x = sum(r[0] for r in readings) / len(readings)
    avg_y = sum(r[1] for r in readings) / len(readings)
    return (avg_x, avg_y)
```

### Challenge 2: 温度補償

**難易度**: ⭐⭐⭐（発展）

磁力センサーは温度に依存します。温度センサーデータを使用して、温度による誤差を補正してください。

**実装ステップ**:
1. 温度 vs. 磁力の関係式を導出
2. リアルタイム補正関数を実装
3. テストで精度向上を検証

### Challenge 3: 複数言語クロスプラットフォーム比較

**難易度**: ⭐⭐⭐⭐（上級）

Python + TypeScript + MakeCode で同じテストスイートを実行し、各言語のパフォーマンス・エラーハンドリングを比較するドキュメントを作成してください。

**分析項目**:
- 実行速度（ns 単位）
- メモリ使用量
- エラーハンドリング戦略の違い
- コード可読性スコア

---

## 📚 参考リソース

### 公式ドキュメント
- [micro:bit MicroPython API](https://microbit-micropython.readthedocs.io/)
- [MakeCode Editor](https://makecode.microbit.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### オンラインエディタ
- [MakeCode Playground](https://makecode.microbit.org/---run)
- [Python REPL](https://repl.it/languages/python3)
- [TypeScript Playground](https://www.typescriptlang.org/play)

### コミュニティ
- [micro:bit Community](https://www.microbitfoundation.org/)
- [Stack Overflow: micro:bit](https://stackoverflow.com/questions/tagged/micro%3abit)

---

## 📬 フィードバック & 改善

このワークショップテンプレートをご利用いただき、ありがとうございます。

**フィードバック方法**:
1. GitHub Issues で問題報告
2. 実施レポート（参加者数、所要時間、改善点）を PR
3. 新しい Challenge や拡張課題を提案

**推奨フィードバック項目**:
- ⏱️ 実際の所要時間（計画 vs. 実績）
- 📊 参加者の理解度分布
- 🔧 発生したトラブルと解決策
- 💡 新しい Challenge アイデア

---

**最終更新**: 2025-01  
**メンテナー**: @katoy  
**ライセンス**: MIT
