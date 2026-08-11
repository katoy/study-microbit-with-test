# micro:bit 方位磁石を 3 つの環境で学ぶ（180 分コース）

**所要時間**: 180 分（3 時間）  
**対象**: 初級～中級の開発者・教育者  
**到達目標**: 同じ仕様を 3 つの環境（MakeCode、Python、TypeScript）で比較し、テスト駆動開発、境界値、入力検証の重要性を理解する

---

## 📋 全体構成（180 分）

| セクション | 時間 | 内容 |
|-----------|------|------|
| [導入・共通仕様](#導入-15-分) | 15 分 | コース概要、共通仕様、環境確認 |
| [1. MakeCode](#1-makecode-45-分) | 45 分 | 実機 API、シミュレーター、演習 |
| [2. Python](#2-python-45-分) | 45 分 | モックテスト、pytest、演習 |
| [3. TypeScript](#3-typescript-45-分) | 45 分 | 型と入力検証、ユニットテスト、演習 |
| [比較・振り返り](#比較-30-分) | 30 分 | 3 環境の比較、カバレッジ陥穽、質疑応答 |

---

## 導入（15 分）

### コース概要（3 分）

このコースでは、**同じ仕様を 3 つの異なる環境で実装・テスト**し、以下を学びます：

✅ **テスト駆動開発（TDD）** — 仕様を最初に読み、境界値テストを設計する  
✅ **入力検証** — 型が正しくても実行時検証が必要な理由  
✅ **環境の違いを活かすテスト設計** — 実機、モック、型システムそれぞれの強み  
✅ **カバレッジと品質の関係** — 100% カバレッジでも見逃される欠陥

### 共通仕様（12 分）

#### 方位磁石の基本仕様

MicroPython の `compass.heading()` は北を 0 度として **0 ～ 360 度**を返し、未校正なら校正シーケンスを開始します。

本教材の方位変換関数は、**有限な 0 度以上 360 度未満**を入力仕様とし、実機 API の 360 度を 0 度へ正規化した後、**45 度幅の 8 方位へ変換**します。

#### 8 方位の範囲表

| 方位 | 範囲 | 代表値 |
|-----|------|--------|
| **N** | 337.5° 以上 **OR** 22.5° 未満 | 0°, 359° |
| **NE** | 22.5° 以上 67.5° 未満 | 45° |
| **E** | 67.5° 以上 112.5° 未満 | 90° |
| **SE** | 112.5° 以上 157.5° 未満 | 135° |
| **S** | 157.5° 以上 202.5° 未満 | 180° |
| **SW** | 202.5° 以上 247.5° 未満 | 225° |
| **W** | 247.5° 以上 292.5° 未満 | 270° |
| **NW** | 292.5° 以上 337.5° 未満 | 315° |

#### ⚠️ 重要：0 度付近の境界条件

**0 度付近は 360 度をまたぎます**。条件は以下のように書きます：

```
heading < 22.5 || heading >= 337.5  ✅ 正しい
（heading < 22.5 || heading > 337.5）❌ 337.5 を見逃す
```

この「境界値の正確さ」がこのコースの中核です。

---

## 1. MakeCode（45 分）

**対象ディレクトリ**: [`sample-compass-makecode`](../../projects/sample-compass-makecode/)

### 実機 API と PXT シミュレーター（10 分）

MakeCode 版は **実機 API を直接使用**します。

```typescript
const heading = input.compassHeading();  // 0～360 度を返す
```

⚠️ **注意**: `input.acceleration()` は傾き・加速度であり、磁北の方位角ではありません。

#### 主要な制御フロー

1. **起動時**: `CAL` と操作案内を表示
2. **ボタン A**: `Compass.calibrate()` で校正開始
3. **ボタン B**: 現在の方位と角度を確認
4. **forever ループ**: LED に方位矢印を表示
5. **自動テスト**: `setHeadingForTest()` で実機入力をモック

### 環境確認・テスト実行（10 分）

```bash
cd sample-compass-makecode
npm ci
npm run test
```

**実行される処理**:
- ✅ PXT ビルド（MakeCode コンパイル）
- ✅ Node.js テストランナー（4 テスト）
- ✅ PXT シミュレーター内での 35 テスト
  - 8 方位判定（各方向 3～5 値ずつ）
  - 境界値（22.4°, 67.4°, 202.4°, 337.4°）
  - エラー処理（負数、範囲外、NaN）
  - キャリブレーション状態

**期待される出力**:
```
test:runner      (Node.js テスト)           4/4 成功
test:compile     (PXT コンパイル)           成功
test:simulator   (PXT シミュレーター)        35/35 成功
```

### 演習 1：境界値を読み取る（15 分）

📄 [`sample-compass-makecode/test/test.ts`](../../projects/sample-compass-makecode/test/test.ts) を開く

**タスク**:

1. **337.5 の境界**を探す（コード内で検索）
   ```
   setHeadingForTest(337.5)
   ```
   期待値は何か？ なぜそう思うか？

2. **その直前の値**（337.4）を見つけ、期待値を比較する
   ```
   setHeadingForTest(337.4)
   ```
   
3. **説明を書く**: なぜ 337.5 と 337.4 で方位が変わるのか、範囲表を使って説明する

4. **追加テストを提案**: 22.5 の境界で同じ比較をしてみる

---

## 2. Python（45 分）

**対象ディレクトリ**: [`sample-compass`](../../projects/sample-compass/)

### 実装の構成（8 分）

このディレクトリには、**目的が異なる 2 種類の Python** があります：

| ファイル | API | 用途 |
|---------|-----|------|
| `src/compass.py` | `from microbit import compass, display, button` | MicroPython 実機、PC 上の pytest |
| `src/compass_makecode.py` | `input`, `basic` グローバル API | MakeCode Python、ブロック相互変換 |

PC には `microbit` モジュールがないため、**`conftest.py` がテスト中だけモックを提供**します。

```python
# PC上でのモック例
@pytest.fixture
def compass_mock():
    with patch('compass.compass.heading', return_value=45):
        yield
```

### 環境確認・テスト実行（12 分）

```bash
cd sample-compass
uv sync
uv run pytest test/ -v --cov=compass_makecode
```

**実行される処理**:
- ✅ Python 環境セットアップ（uv）
- ✅ 43 個のユニットテスト（< 1 秒）
- ✅ 1 個のシミュレーターテスト（30～40 秒）
- ✅ カバレッジ計測（100% 必須）

**期待される出力**:
```
====== 44 passed in 32.55s ======
Name                      Stmts   Miss  Cover
src/compass_makecode.py      62      0   100%
```

### 演習 2：モックテストで境界値を追加する（15 分）

📄 [`sample-compass/test/test_coverage.py`](../../projects/sample-compass/test/test_coverage.py) を開く

**タスク**:

1. `test_heading_to_direction_boundaries` テスト関数を見つける
   
2. **現在のテストを読む**（どんな値を test しているか）
   
3. **337.4 と 337.5 の期待値を追加**する:
   ```python
   (337.4, 'NW'),
   (337.5, 'N'),   # ← これを追加
   ```

4. テストを実行し、追加した値が PASS するか確認：
   ```bash
   uv run pytest test/test_coverage.py::TestGetDirectionString -v
   ```

5. **逆に、22.5 の境界も追加テスト**してみる

### ミニディスカッション（10 分）

MakeCode（実機テスト）と Python（モックテスト）の違いを考える：

❓ **Q**: MakeCode のテストに実機や PXT シミュレーターが必要な理由は？  
💡 **A**: `input.compassHeading()` が実装の中にあり、その戻り値を注入してテストする仕組みが PXT API に限定されるから。

❓ **Q**: Python のモックテストが高速な理由は？  
💡 **A**: センサーやシミュレーター処理をスキップし、関数の入力と出力だけを検査するから。

❓ **Q**: Python モックが実機動作を完全には保証しない理由は？  
💡 **A**: `compass.is_calibrated()` の実装、実際のセンサー誤差、キャリブレーション後の状態変化を mock では再現できないから。

---

## 3. TypeScript（45 分）

**対象ディレクトリ**: [`sample-compass-ts`](../../projects/sample-compass-ts/)

### 型と入力検証の設計（10 分）

TypeScript 版は **Node.js 上で動く純粋な学習モデル**であり、実機 API を呼びません。

```typescript
export type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';
```

**8 つの文字列リテラル型**で、不正な値（`'NORTH'`, `'north'`）をコンパイル時に拒否します。

```typescript
interface CompassState {
  heading: number;       // 0～359（検査済み）
  direction: Direction;  // union 型で 8 値のみ
  isCalibrated: boolean;
}
```

#### 型が正しくても実行時検証が必要な理由

```typescript
// ❌ 型チェックに通る危険な値
const heading: number = NaN;
const heading2: number = Infinity;
const heading3: number = -5;
const heading4: number = 360;
```

**TypeScript の `number` 型は** `NaN`, `Infinity`, 負数, 360° をすべて許容します。  
**実行時検証で初めて**、これらの不正な入力を拒否できます。

### 環境確認・テスト実行（10 分）

```bash
cd sample-compass-ts
npm ci
npm run build    # TypeScript → JavaScript コンパイル
npm test         # Jest ユニット + 統合テスト
```

**実行される処理**:
- ✅ TypeScript コンパイル（型チェック）
- ✅ 2 テストスイート（ユニット + 統合）
- ✅ 74 テストケース
- ✅ カバレッジ計測（100%）

**期待される出力**:
```
Test Suites: 2 passed, 2 total
Tests:       74 passed, 74 total
Coverage:
  Statements   : 100% ( 62/62 )
  Branches     : 100% ( 48/48 )
  Functions    : 100% ( 8/8 )
  Lines        : 100% ( 62/62 )
```

### 演習 3：不正入力をテストで保証する（15 分）

📄 [`sample-compass-ts/test/compass.test.ts`](../../projects/sample-compass-ts/test/compass.test.ts) を開く

**タスク**:

1. **NaN テストを探す**：
   ```typescript
   expect(() => Compass.headingToDirection(NaN)).toThrow();
   ```
   なぜこのテストが必要か？

2. **Infinity テストも確認**：
   ```typescript
   expect(() => Compass.headingToDirection(Infinity)).toThrow();
   ```

3. **負数テスト**（-1, -5）を見つけ、期待動作をまとめる

4. **追加テストを書く**：
   - 360 度は許可されているか？ テストを追加し、確認する
   - もし 360 度が通れば、なぜバグなのか説明する

### ディスカッション：型 vs 実行時検証（10 分）

❓ **Q**: TypeScript なら型で`NaN`を防げないか？  
💡 **A**: `const heading: number = NaN` は型チェックで許容される。型システムは値の集合をチェックするが、`NaN` も `number` の一部だから。

❓ **Q**: 実行時検証の代わりに入力を制限（ファイアウォール）できないか？  
💡 **A**: 外部 API、ユーザー入力、並行処理などから不正な値は常に流入しうる。レイヤーを分け、変換関数に入ってくる前に検査する必要がある。

❓ **Q**: MakeCode や Python での検証はどう違うか？  
💡 **A**: MakeCode は `ERR` をブロック UI に返す。Python は `ValueError` 例外を上げる。設計判断として、環境に合わせている。

---

## 比較（30 分）

### 3 環境の差分表（5 分）

| 観点 | MakeCode | MicroPython | Node TypeScript |
|------|----------|------------|-----------------|
| **実機 API** | `input.compassHeading()` | `compass.heading()` | なし |
| **入力方法** | 実機／PXT シミュレーター | 実機／pytest モック | メソッド呼び出し |
| **未校正の表現** | `CAL` LED 表示 | `ValueError` 例外 | 例外 throw |
| **操作フロー** | A で校正 → B で確認 → LED 更新 | A で校正 → B で確認 → LED 更新 | コンソール入力 |
| **エラー処理** | 範囲外・NaN は `ERR` | 範囲外・NaN は例外 | 範囲外・NaN・∞ は例外 |
| **テスト速度** | 遅い（50 秒） | 速い（< 1 秒） | 高速（< 1 秒） |
| **強み** | ビジュアル、実機イベント | 実機互換、短いコード | 型安全、純粋ロジック |
| **弱点** | Static Python 制約 | PC にモック必要 | 実機 HEX に直結しない |

**有効な入力範囲は 3 つすべてで同じ**（0 度以上 360 度未満）ですが、**エラー時の処理パターンが異なる**のは、利用環境に合わせた設計判断です。

### ケーススタディ：カバレッジ 100% でも見逃される欠陥（15 分）

#### 問題提示（2 分）

3 実装すべてが「**カバレッジ 100%**」を達成していても、以下のバグを見逃す可能性があります：

❌ **バグ 1**: `-1` を入力した時の期待値が異なるのに、テストが不十分  
❌ **バグ 2**: MakeCode Web 用 `compass_makecode.py` は CI 対象外なので、改変しても CI が通る  
❌ **バグ 3**: 仕様変更（例：16 方位への拡張）の時、既存テストが邪魔になる  

#### 演習：予想→確認→考察（10 分）

**ステップ 1: 予想（3 分）**

テストコードを見る前に、次の不正入力に対する 3 実装の期待結果を予想します：

| 入力値 | MakeCode | MicroPython | TypeScript |
|--------|----------|-------------|-----------|
| `-5` | ? | ? | ? |
| `400` | ? | ? | ? |
| `NaN` | ? | ? | ? |

**ステップ 2: 確認（4 分）**

各実装のテストを開き、実際の期待値を記録します：

```bash
cd sample-compass-makecode && npm run test:simulator 2>&1 | grep -A 5 "無効な方位角テスト"
cd ../sample-compass && uv run pytest test/test_coverage.py -v -k invalid
cd ../sample-compass-ts && npm test -- --testNamePattern="invalid"
```

**ステップ 3: 考察（3 分）**

- 予想と実際がどう違ったか？
- その違いが生じた理由は？
- もし仕様が「負数は最後の有効値を保つ」に変わったら、どのテストを修正する必要があるか？

#### Python CI の落とし穴（3 分）

```yaml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["test"]
```

**CI のカバレッジコマンド**:
```bash
pytest --cov=compass_makecode --cov-report=term-missing
```

💡 **注意**: `compass_makecode.py` は測定対象（MakeCode Web 貼り付け用）ですが、  
実は `conftest.py` のモック実装がバグでも、CI は通ります。  
（モックが測定対象に含まれないから）

---

## まとめと振り返り（10 分）

### チェックリスト：このコースで学んだこと

- [ ] 0 度付近の境界条件（`< 22.5 || >= 337.5`）を説明できる
- [ ] PXT シミュレーターとモックテストの速度の違いを説明できる
- [ ] TypeScript の `number` 型でも `NaN` や `Infinity` を許容する理由を説明できる
- [ ] 3 実装でエラー処理が異なる理由（利用環境への適応）を説明できる
- [ ] カバレッジ 100% でもバグが隠れる例を 2 つ以上あげられる
- [ ] 各環境のテスト速度トレードオフを理解している
- [ ] 次に拡張したい機能（16 方位、傾き補正など）を考えている

### 次のステップ（発展課題）

境界値テストを通じて基礎を固めた後、次の順で仕様を広げます：

1. **16 方位** — 11.25 度ごとの新しい境界値と、N, NNE, NE, ENE... 名前を追加
2. **移動平均** — 359° と 1° の平均が 180° になる円環問題を解決
3. **傾き補正** — 加速度センサーと組み合わせ、水平でない場合の補正を設計
4. **磁気干渉検出** — 実機を金属に近づけ、値の揺れを観察・記録

### 質疑応答・意見交換（5 分）

- コース内容で不明な点
- 実務での類似パターン
- 他言語（Rust、Go など）での同様の設計
- 実機マイクロコントローラー上の実装経験
