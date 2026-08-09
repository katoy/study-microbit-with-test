# Python / TypeScript / MakeCode 複言語実装比較ガイド

このガイドでは、**同じアルゴリズム（方位磁石の8方位判定）** を3つの言語で実装し、言語の特性、テスト戦略、学習パスを比較します。

## 目次

1. [アルゴリズム概要](#アルゴリズム概要)
2. [言語別実装比較](#言語別実装比較)
3. [テスト戦略の比較](#テスト戦略の比較)
4. [学習パス](#学習パス)
5. [実装演習](#実装演習)
6. [選択ガイド](#選択ガイド)

---

## アルゴリズム概要

### 問題: 方位角 (0-359°) を8方位に判定

```
        N
       0°
    
 NW  315°  NE
  22.5° 45°

   270°  90°
W         E

 SW  225°  SE
    180°   135°
```

### ロジック: 8つの 45° セクターに分割

```
N:   337.5° - 22.5°    (北 ≈ 0°)
NE:  22.5° - 67.5°     (北東 ≈ 45°)
E:   67.5° - 112.5°    (東 ≈ 90°)
SE:  112.5° - 157.5°   (南東 ≈ 135°)
S:   157.5° - 202.5°   (南 ≈ 180°)
SW:  202.5° - 247.5°   (南西 ≈ 225°)
W:   247.5° - 292.5°   (西 ≈ 270°)
NW:  292.5° - 337.5°   (北西 ≈ 315°)
```

---

## 言語別実装比較

### 1. Python 版（実機開発向け）

**特徴**: 動的型言語、実機センサー依存、Mock でテスト

**実装例**:

```python
class Compass:
    def __init__(self):
        self._is_calibrated = False
        self._heading = None

    def calibrate(self):
        """キャリブレーション実行"""
        self._is_calibrated = True

    def get_heading(self):
        """方位角を取得（0-359°）"""
        if not self._is_calibrated:
            raise RuntimeError('Compass not calibrated')
        return self._heading  # 実機から取得、またはテストではモック値

    @staticmethod
    def _heading_to_direction(heading):
        """方位角を方向文字列に変換"""
        if heading < 22.5 or heading >= 337.5:
            return 'N'
        elif heading < 67.5:
            return 'NE'
        elif heading < 112.5:
            return 'E'
        # ... 以下同様
        return 'N'  # デフォルト

    def get_direction(self):
        """現在の方向を取得"""
        heading = self.get_heading()
        return self._heading_to_direction(heading)
```

**テスト例（Mock 環境）**:

```python
def test_get_direction_northeast(mock_compass):
    # Mock で方位角を設定
    mock_compass.compass._heading = 45
    direction = mock_compass.compass.get_direction()
    assert direction == 'NE'
```

**強み** ✅:
- 実機 micro:bit で実行可能
- 簡潔で読みやすい
- Mock テストで実機なしでテスト可能

**弱み** ❌:
- 型チェックなし（実行時エラー）
- エラーハンドリングが甘くなりやすい
- `heading` が `None` のまま使用されるバグが発生しやすい

**適用レベル**:
- ⭐⭐ 中級者（実機開発経験者）
- micro:bit で直接実行したい場合

---

### 2. TypeScript 版（ロジック検証向け）

**特徴**: 静的型言語、型安全、Node.js で実行（実機不要）

**実装例**:

```typescript
// 型定義
type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';

interface CompassState {
  isCalibrated: boolean;
  currentHeading: number;
}

class Compass {
  private state: CompassState = {
    isCalibrated: false,
    currentHeading: 0
  };

  calibrate(): void {
    this.state.isCalibrated = true;
  }

  getHeading(): number {
    if (!this.state.isCalibrated) {
      throw new Error('Compass not calibrated');
    }
    return this.state.currentHeading;
  }

  static validateHeading(heading: number): void {
    if (!Number.isFinite(heading) || heading < 0 || heading >= 360) {
      throw new Error(
        `Invalid heading: ${heading}. Must be between 0 and 359.`
      );
    }
  }

  static headingToDirection(heading: number): Direction {
    Compass.validateHeading(heading);
    
    if (heading < 22.5 || heading >= 337.5) return 'N';
    if (heading < 67.5) return 'NE';
    if (heading < 112.5) return 'E';
    // ... 以下同様
    return 'N';
  }

  getDirection(): Direction {
    return Compass.headingToDirection(this.getHeading());
  }
}
```

**テスト例（Jest）**:

```typescript
describe('Compass', () => {
  it('should validate heading input', () => {
    expect(() => {
      Compass.headingToDirection(360); // >= 360 はエラー
    }).toThrow('Invalid heading');
  });

  it('should correctly identify Northeast', () => {
    expect(Compass.headingToDirection(45)).toBe('NE');
  });
});
```

**強み** ✅:
- 型チェックでエラー検出（コンパイル時）
- Union Type で Direction を制約
- IDE でのコード補完が充実
- 厳密な入力値検証
- Node.js で実行（micro:bit 不要）

**弱み** ❌:
- コンパイルが必要
- 実機では実行不可（Node.js 環境のみ）
- 初心者には学習曲線が急

**適用レベル**:
- ⭐⭐⭐⭐ 上級者（型安全を重視）
- エンタープライズ開発、ロジック検証

---

### 3. MakeCode 版（ビジュアルプログラミング向け）

**特徴**: ビジュアルブロック + TypeScript、実機シミュレータでテスト

**実装例** (TypeScript コード):

```typescript
//% block="compass get direction" color="#E74C3C" icon="\uf14e"
//% advanced block="compass advanced set heading"
export namespace compass {
  let _isCalibrated = false;
  let _currentHeading = 0;

  //% block="calibrate compass"
  //% blockId="compass_calibrate"
  export function calibrate(): void {
    _isCalibrated = true;
  }

  //% block="get direction as text"
  //% blockId="compass_get_direction"
  export function getDirection(): string {
    if (!_isCalibrated) {
      return 'CAL'; // ユーザーフレンドリー: キャリブレーション指示
    }

    const heading = _currentHeading;
    
    if (heading < 22.5 || heading >= 337.5) return 'N';
    if (heading < 67.5) return 'NE';
    if (heading < 112.5) return 'E';
    // ... 以下同様
    return 'N';
  }

  //% block="set heading (advanced)"
  //% heading.min=0 heading.max=359
  export function setHeading(heading: number): void {
    if (heading < 0 || heading >= 360) {
      return; // 無言で無視（エラーを表示しない）
    }
    _currentHeading = heading;
  }

  export function isCalibrated(): boolean {
    return _isCalibrated;
  }

  export function getState(): string {
    return (
      `Compass State: Calibrated=${_isCalibrated}, ` +
      `Heading=${_currentHeading}°, Direction=${getDirection()}`
    );
  }
}
```

**ビジュアルブロック例**:

```
┌──────────────────────────────────┐
│ calibrate compass                │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ get direction as text            │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ set heading (advanced) to [90]   │
└──────────────────────────────────┘
```

**テスト例（シミュレータ）**:

```typescript
// test.ts
basic.showString(compass.getDirection()); // CAL (未キャリブレーション)
compass.calibrate();
compass.setHeading(45);
basic.showString(compass.getDirection()); // NE
```

**強み** ✅:
- ビジュアルエディタで直感的に操作
- ブロック ↔ TypeScript 自動変換
- キャリブレーション指示（'CAL'）でUXが優れている
- シミュレータで即座に動作確認可能
- 初心者向け（学習難度最小）

**弱み** ❌:
- ビジュアル形式の制約（複雑なロジックに不向き）
- エラーハンドリングが限定的
- PXT 環境に依存
- デバッグが困難（シミュレータのみ）

**適用レベル**:
- ⭐ 初心者～中級者
- 小中学生向け教材

---

## テスト戦略の比較

### Python: Mock ベースのユニット・統合テスト

```
┌─────────────────────────────────────────┐
│ test_compass.py (17 テスト)             │
├─────────────────────────────────────────┤
│ ✓ test_compass_init                     │
│ ✓ test_calibrate                        │
│ ✓ test_get_heading_with_mock_value      │
│ ✓ test_get_direction_north              │
│ ✓ test_get_direction_northeast          │
│ ... (8 方向すべて)                       │
│ ✓ test_display_direction_uncalibrated   │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ test_compass_integration.py (13 テスト) │
├─────────────────────────────────────────┤
│ ✓ test_complete_compass_workflow        │
│ ✓ test_all_eight_directions             │
│ ✓ test_boundary_value_transitions       │
│ ... (統合ワークフロー)                   │
└─────────────────────────────────────────┘
```

**特徴**:
- conftest.py で Mock fixture を定義
- `unittest.mock` で実機をシミュレート
- 実機なしでも 100% テスト可能
- カバレッジ 100% を達成

---

### TypeScript: Jest による厳密なテスト

```
┌─────────────────────────────────────────┐
│ compass.test.ts (48 テスト)             │
├─────────────────────────────────────────┤
│ ✓ Test: 0° is North                     │
│ ✓ Test: 45° is Northeast                │
│ ✓ Test: Invalid heading throws error    │
│ ✓ Test: NaN heading throws error        │
│ ... (型チェック込みの検証)               │
└─────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────┐
│ compass.integration.test.ts (25 テスト) │
├─────────────────────────────────────────┤
│ ✓ Multiple compass instances            │
│ ✓ State consistency under load          │
│ ✓ Rapid heading updates                 │
└─────────────────────────────────────────┘
```

**特徴**:
- 静的型チェック + ユニットテスト
- 境界値テスト（22.5°, 67.5°, 337.5° など）
- エラーケースを徹底的に検証
- IDE での即座なフィードバック

---

### MakeCode: シミュレータ自動テスト

```
┌─────────────────────────────────────────┐
│ built/simulator-tests.ts (32 テスト)    │
├─────────────────────────────────────────┤
│ LOG: ✓ 0° is N (期待値: N, 実際: N)     │
│ LOG: ✓ 45° is NE                        │
│ LOG: ✓ isCalibrated() returns true      │
│ LOG: ✓ getDirection() returns CAL       │
│ ... (ビジュアルテスト)                    │
└─────────────────────────────────────────┘
       ↓
✓ MakeCode simulator tests passed: 32/32
```

**特徴**:
- ヘッドレスシミュレータでの自動テスト
- `skipHardware` フラグで条件付き実行
- ビジュアルブロックの動作検証
- CI/CD 統合（GitHub Actions）

---

## 比較表

| 観点 | Python | TypeScript | MakeCode |
|------|--------|-----------|----------|
| **型安全** | ❌ なし | ✅ 厳密 | ⚠️ 部分的 |
| **実行環境** | micro:bit ⚡ | Node.js 🖥️ | micro:bit ⚡ |
| **テスト環境** | Mock 化 | 純粋ロジック | シミュレータ |
| **エラー戦略** | graceful-degrade | fail-fast (exception) | ユーザーフレンドリー |
| **学習難度** | ⭐⭐ 簡単 | ⭐⭐⭐⭐ 深い | ⭐ 超簡単 |
| **開発速度** | ⭐⭐⭐ 速い | ⭐⭐ 厳密 | ⭐⭐⭐⭐ 直感的 |
| **本番環境** | micro:bit ✅ | (ロジックのみ) | micro:bit ✅ |
| **テスト数** | 30個 (17+13) | 73個 (48+25) | 32個 |
| **カバレッジ** | 100% | 100% | 100% |

---

## 学習パス

### 初心者 → 中級者 → 上級者

```
┌──────────────────────────────────────────────────────┐
│ レベル 1: ビジュアル直感学習 (1-2週間)              │
├──────────────────────────────────────────────────────┤
│ MakeCode ブロックエディタで直感的に理解              │
│ ├─ 「北が0°」「45°が北東」の感覚をつかむ             │
│ ├─ ビジュアルブロックで実装                         │
│ └─ シミュレータで即座に動作確認                     │
└──────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────┐
│ レベル 2: 実装言語学習 (2-4週間)                    │
├──────────────────────────────────────────────────────┤
│ Python で実機開発とテスト駆動開発を習得             │
│ ├─ Mock を使った単体テストの設計                    │
│ ├─ conftest.py でのフィクスチャ管理               │
│ ├─ 実機（micro:bit）での動作確認                   │
│ └─ 統合テストでのワークフロー検証                  │
└──────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────┐
│ レベル 3: 型安全・エンタープライズ開発 (1ヶ月+)     │
├──────────────────────────────────────────────────────┤
│ TypeScript で厳密性と型チェックを習得              │
│ ├─ Union Type による型制約                        │
│ ├─ 入力値検証と例外処理（fail-fast）              │
│ ├─ Jest でのエッジケース検証                       │
│ ├─ IDE サポート（型補完・自動リファクタリング）    │
│ └─ エンタープライズ開発パターン                    │
└──────────────────────────────────────────────────────┘
```

### ロールモデル別パス

| ロール | 推奨順 | 理由 |
|--------|--------|------|
| **小中学生** | MakeCode → Python | ビジュアル → テキスト段階学習 |
| **高校生** | MakeCode → Python → TypeScript | 完全なステップアップ |
| **大学生** | Python → TypeScript | 実装重視 |
| **企業開発者** | TypeScript → Python → MakeCode | 型安全性重視 |
| **教育者** | 全言語 | 複言語比較能力が必須 |

---

## 実装演習

### 演習1: Python → TypeScript への「型安全化」

**目標**: Python コードを TypeScript に移植し、型チェックで品質向上を実感

**ステップ**:

1. **Python での実装確認**:
```bash
cd sample-compass
uv run pytest test_compass.py -v
```

2. **TypeScript への移植**:
```typescript
// compass-exercise.ts
// TODO: compass.py をベースに以下を実装
// 1. heading: number で型制約
// 2. Direction の Union Type
// 3. validateHeading() 関数追加
// 4. エラーハンドリングを例外に変更
```

3. **テストの記述**:
```typescript
// compass-exercise.test.ts
describe('Type Safety Exercise', () => {
  it('should reject invalid headings', () => {
    expect(() => {
      headingToDirection(360); // エラー
      headingToDirection(-1);  // エラー
      headingToDirection(NaN); // エラー
    }).toThrow();
  });
});
```

**期待される学習**:
- ✅ 型チェックの重要性
- ✅ 実行時エラーを防ぐ方法
- ✅ IDE サポートの活用

**所要時間**: 1-2時間

---

### 演習2: MakeCode での可視化と UIツール

**目標**: TypeScript 実装を MakeCode ブロックとして公開

**ステップ**:

1. **ブロック定義を追加**:
```typescript
//% block="compass get direction|as|$format"
//% format.shadow="compassDirectionFormat"
//% format.defl=CompassDirectionFormat.Text
export function getDirectionFormatted(
  format: CompassDirectionFormat
): string {
  // Text, Icon, Numeric など形式を選択
}
```

2. **ビジュアルUIを調整**:
   - アイコン: 羅針盤 🧭
   - カラーパレット: 青系（方位磁石イメージ）
   - ツールチップ: 「現在の方向を取得」

3. **シミュレータでテスト**:
```bash
cd sample-compass-makecode
npm test
```

**期待される学習**:
- ✅ TypeScript ↔ MakeCode ブロック自動変換
- ✅ UI/UX デザイン（ユーザーフレンドリー設計）
- ✅ ビジュアルプログラミング環境での開発

**所要時間**: 1.5-2時間

---

### 演習3: テスト戦略の比較と統合

**目標**: 3つの言語のテスト手法を比較し、統合テスト計画を立案

**ステップ**:

1. **各言語のテスト実行と分析**:
```bash
# Python
cd sample-compass && uv run pytest -v --cov=compass

# TypeScript
cd sample-compass-ts && npm test -- --coverage

# MakeCode
cd sample-compass-makecode && npm test
```

2. **テスト比較表を作成**:

| テスト側面 | Python | TypeScript | MakeCode |
|---------|--------|-----------|----------|
| テスト数 | 17 | 48 | 32 |
| カバレッジ | 100% | 100% | N/A |
| 実行時間 | < 100ms | < 1s | < 5s |
| テスト難度 | 簡単 | 中程度 | 簡単 |
| エッジケース | 部分的 | 完全 | 基本 |

3. **統合テスト計画**:
```markdown
# 統合テスト戦略
1. Python: Mock による単体・統合テスト（実機シミュレーション）
2. TypeScript: Jest でロジック検証（型チェック付き）
3. MakeCode: ビジュアルブロック + シミュレータ検証

## CI/CD 統合
- Pre-commit: Python & TypeScript テスト
- Pre-push: 全言語テスト + カバレッジ検証
- CI: GitHub Actions で 3言語並行実行
```

**期待される学習**:
- ✅ テスト戦略の設計
- ✅ 言語別テスト手法の使い分け
- ✅ CI/CD パイプラインの理解

**所要時間**: 2時間

---

## 選択ガイド

### 「どの言語を選べばいい？」

#### 🎯 目的別ガイド

**初めて micro:bit を学ぶ**
```
MakeCode (ビジュアル)
↓ (2-4週間後)
Python (実装言語)
```
推奨: MakeCode で直感理解 → Python で実機操作

---

**プログラミングの基礎を学びたい**
```
Python (簡潔で読みやすい)
↓ (1ヶ月後)
TypeScript (型安全性を理解)
```
推奨: Python で動作理解 → TypeScript で品質管理

---

**エンタープライズ開発スキルを習得したい**
```
TypeScript (型安全性)
↓ (並行)
Python (実装パターン)
```
推奨: TypeScript で設計 → Python で実装

---

**教育機関での導入を検討**
```
全言語を同時並行実装
（段階的な学習パスを提供）
```
推奨: 初級（MakeCode） → 中級（Python） → 上級（TypeScript）

---

#### 🏫 教育現場での使い分け

| 対象 | 推奨言語 | 期間 | 理由 |
|------|--------|------|------|
| 小学高学年 | MakeCode | 1ヶ月 | 直感的、プログラミング概念理解 |
| 中学生 | Python | 2ヶ月 | 実機、テスト駆動開発の基礎 |
| 高校生 | TypeScript | 3ヶ月 | 型安全性、エラーハンドリング |
| 大学 | 全言語 | 1セメスター | 複言語能力、設計判断 |
| 企業研修 | TypeScript → Python | 1週間 | 型安全性と実装バランス |

---

#### 💼 プロジェクト別選択基準

| シナリオ | 最適言語 | 理由 |
|--------|---------|------|
| 小規模プロトタイプ | Python | 開発速度重視 |
| 本番マイクロコントローラ | TypeScript | 型安全性 + ロジック検証 |
| デバイスファームウェア | Python | 実機ターゲット |
| ロジック検証ライブラリ | TypeScript | Node.js で配布可能 |
| 教材・ワークショップ | MakeCode | 学習効果最大化 |

---

## 補足: ファイル対応表

各言語の対応ファイル一覧:

| 内容 | Python | TypeScript | MakeCode |
|------|--------|-----------|----------|
| メイン実装 | `sample-compass/compass.py` | `sample-compass-ts/src/compass.ts` | `sample-compass-makecode/pxt.json` |
| ユニットテスト | `test_compass.py` (17個) | `test/compass.test.ts` (48個) | `built/simulator-tests` (32個) |
| 統合テスト | `test_compass_integration.py` (13個) | `test/compass.integration.test.ts` (25個) | (シミュレータ統合) |
| ビルドテスト | `test_build_hex.py` (4個) | N/A | `test/pxt-compile.test.ts` |
| テスト設定 | `conftest.py` | `jest.config.js` | `simulator-test-runner.cjs` |
| CI/CD | `.github/workflows/python-tests.yml` | `.github/workflows/typescript-tests.yml` | `.github/workflows/makecode-tests.yml` |

---

## まとめ

このプロジェクトの 3言語実装から学べること:

1. **同じアルゴリズムも言語で実装方法が異なる**
   - Python: 簡潔性
   - TypeScript: 型安全性
   - MakeCode: 直感性

2. **テスト戦略は環境に最適化される**
   - Mock (Python)
   - 型チェック (TypeScript)
   - シミュレータ (MakeCode)

3. **学習パスを段階的に設計できる**
   - 初級: ビジュアル (MakeCode)
   - 中級: 実装 (Python)
   - 上級: 品質 (TypeScript)

4. **複言語能力はエンタープライズ開発の必須スキル**
   - 言語の特性を理解
   - 最適な言語を選択
   - 設計判断の質向上

---

**次のステップ**: 上記の演習に取り組んで、各言語の特性を体験してください！

Created: 2026-08-09  
Maintained in: `/study-microbit-with-test/`
