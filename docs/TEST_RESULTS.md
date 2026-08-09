## テスト実行結果スクリーンショット・図解

> [!WARNING]
> 以下は過去の実行例です。件数と出力は現在のテストスイートと異なる場合があります。最新結果はリポジトリのルートで `npm run test:all` を実行して確認してください。

### Python テスト実行例 (pytest)

```
sample-compass$ uv run pytest test_compass.py test_compass_integration.py test_build_hex.py -v

============================== test session starts ==============================
platform darwin -- Python 3.12.11, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/katoy/github/study-microbit-with-test/sample-compass
collected 34 items

test_compass.py::TestCompass::test_compass_init PASSED                   [  2%]
test_compass.py::TestCompass::test_calibrate PASSED                      [  5%]
test_compass.py::TestCompass::test_get_heading PASSED                    [  8%]
test_compass.py::TestCompass::test_get_direction_north PASSED            [ 11%]
test_compass.py::TestCompass::test_get_direction_northeast PASSED        [ 14%]
test_compass.py::TestCompass::test_get_direction_east PASSED             [ 17%]
test_compass.py::TestCompass::test_get_direction_southeast PASSED        [ 20%]
test_compass.py::TestCompass::test_get_direction_south PASSED            [ 23%]
test_compass.py::TestCompass::test_get_direction_southwest PASSED        [ 26%]
test_compass.py::TestCompass::test_get_direction_west PASSED             [ 29%]
test_compass.py::TestCompass::test_get_direction_northwest PASSED        [ 32%]
test_compass.py::TestCompass::test_heading_to_direction_boundaries PASSED [ 35%]
test_compass.py::TestCompass::test_heading_to_direction_edge_cases PASSED [ 38%]
test_compass.py::TestCompass::test_display_direction PASSED              [ 41%]
test_compass.py::TestCompass::test_display_direction_uncalibrated PASSED [ 44%]
test_compass.py::TestCompass::test_get_heading_with_exception PASSED     [ 47%]
test_compass.py::TestCompass::test_get_heading_with_numeric_value PASSED [ 50%]
test_build_hex.py::test_validate_microbit_hex_rejects_a_file_without_firmware_data PASSED [ 52%]
test_build_hex.py::test_validate_microbit_hex_accepts_valid_intel_hex_data PASSED [ 55%]
test_build_hex.py::test_create_hex_does_not_replace_a_compiler_failure_with_a_dummy_file PASSED [ 58%]
test_build_hex.py::test_create_hex_rejects_non_flashable_compiler_output PASSED [ 61%]
test_compass_integration.py::TestCompassIntegration::test_complete_compass_workflow PASSED [ 64%]
test_compass_integration.py::TestCompassIntegration::test_all_eight_directions PASSED [ 67%]
test_compass_integration.py::TestCompassIntegration::test_boundary_value_transitions PASSED [ 70%]
test_compass_integration.py::TestCompassIntegration::test_north_wrap_around PASSED [ 73%]
test_compass_integration.py::TestCompassIntegration::test_continuous_rotation_simulation PASSED [ 76%]
test_compass_integration.py::TestCompassIntegration::test_rapid_direction_queries PASSED [ 79%]
test_compass_integration.py::TestCompassIntegration::test_multiple_compass_instances PASSED [ 82%]
test_compass_integration.py::TestCompassIntegration::test_calibration_state_persistence PASSED [ 85%]
test_compass_integration.py::TestCompassIntegration::test_performance_stress_test PASSED [ 88%]
test_compass_integration.py::TestCompassIntegration::test_direction_consistency_across_queries PASSED [ 91%]
test_compass_integration.py::TestCompassIntegration::test_comprehensive_workflow_with_state_verification PASSED [ 94%]
test_compass_integration.py::TestCompassIntegration::test_main_function_workflow PASSED [ 97%]
test_compass_integration.py::TestCompassIntegration::test_main_function_entry_point PASSED [100%]

============================== 34 passed in 0.13s ==============================
coverage: 100%, 50 statements
```

✅ **結果**: 34/34 PASS (100%) | カバレッジ: 100%

---

### TypeScript テスト実行例 (Jest)

```
sample-compass-ts$ npm test

> sample-compass-ts@1.0.0 test
> jest --runInBand

PASS test/compass.test.ts
  Compass クラス
    初期化
      ✓ コンストラクタが正しく初期化される (2 ms)
      ✓ 未キャリブレーション状態で getHeading() はエラーを投げる (8 ms)
      ✓ 未キャリブレーション状態で getDirection() はエラーを投げる (1 ms)
    キャリブレーション
      ✓ calibrate() を呼び出すとキャリブレーション状態が true になる
    方位角の設定と取得
      ✓ setHeading() で方位角が正しく設定される
      ✓ setHeading() で負の値がエラーになる (1 ms)
      ✓ setHeading() で 360 度以上がエラーになる
      ✓ setHeading() で NaN がエラーになる (1 ms)
    北方向（N）の判定
      ✓ 0 度は北（N）
      ✓ 22 度は北（N）
      ✓ 337.5 度以上は北（N）
      ✓ 359 度は北（N）

  Compass Integration Test Suite
    Complete compass workflow
      ✓ should initialize compass and verify it throws errors when not calibrated (7 ms)
      ✓ should calibrate and maintain state
      ✓ should update heading and reflect direction change (1 ms)
    Direction detection across all 8 cardinal/intercardinal directions
      ✓ should correctly identify North (0°)
      ✓ should correctly identify Northeast (45°)
      ✓ should correctly identify East (90°)
      ✓ should correctly identify Southeast (135°)
      ✓ should correctly identify South (180°)
      ✓ should correctly identify Southwest (225°)
      ✓ should correctly identify West (270°)
      ✓ should correctly identify Northwest (315°)

Test Suites: 2 passed, 2 total
Tests:       73 passed, 73 total
Snapshots:   0 total
Time:        0.908 s, estimated 2 s
Ran all test suites.
```

✅ **結果**: 73/73 PASS (100%)

---

### MakeCode シミュレータテスト実行例

```
sample-compass-makecode$ npm test

> sample-compass-makecode@1.0.0 test
> npm run test:runner && npm run test:compile && npm run test:simulator

LOG: 方位磁石テスト開始...
LOG: 北方向（N）テスト
LOG: ✓ 0 度は北（N） (期待値: N, 実際: N)
LOG: ✓ 22 度は北（N） (期待値: N, 実際: N)
LOG: ✓ 359 度は北（N） (期待値: N, 実際: N)
LOG: 北東方向（NE）テスト
LOG: ✓ 22.5 度は北東（NE） (期待値: NE, 実際: NE)
LOG: ✓ 45 度は北東（NE） (期待値: NE, 実際: NE)
LOG: ✓ 67 度は北東（NE） (期待値: NE, 実際: NE)
LOG: 東方向（E）テスト
LOG: ✓ 67.5 度は東（E） (期待値: E, 実際: E)
LOG: ✓ 90 度は東（E） (期待値: E, 実際: E)
LOG: ✓ 112 度は東（E） (期待値: E, 実際: E)
LOG: 南東方向（SE）テスト
LOG: ✓ 112.5 度は南東（SE） (期待値: SE, 実際: SE)
LOG: ✓ 135 度は南東（SE） (期待値: SE, 実際: SE)
LOG: ✓ 157 度は南東（SE） (期待値: SE, 実際: SE)
LOG: 南方向（S）テスト
LOG: ✓ 157.5 度は南（S） (期待値: S, 実際: S)
LOG: ✓ 180 度は南（S） (期待値: S, 実際: S)
LOG: ✓ 202 度は南（S） (期待値: S, 実際: S)
LOG: 南西方向（SW）テスト
LOG: ✓ 202.5 度は南西（SW） (期待値: SW, 実際: SW)
LOG: ✓ 225 度は南西（SW） (期待値: SW, 実際: SW)
LOG: ✓ 247 度は南西（SW） (期待値: SW, 実際: SW)
LOG: 西方向（W）テスト
LOG: ✓ 247.5 度は西（W） (期待値: W, 実際: W)
LOG: ✓ 270 度は西（W） (期待値: W, 実際: W)
LOG: ✓ 292 度は西（W） (期待値: W, 実際: W)
LOG: 北西方向（NW）テスト
LOG: ✓ 292.5 度は北西（NW） (期待値: NW, 実際: NW)
LOG: ✓ 315 度は北西（NW） (期待値: NW, 実際: NW)
LOG: ✓ 337 度は北西（NW） (期待値: NW, 実際: NW)
LOG: 境界値テスト
LOG: ✓ 22.4 度は N と NE の境界 (期待値: N, 実際: N)
LOG: ✓ 67.4 度は NE と E の境界 (期待値: NE, 実際: NE)
LOG: ✓ 202.4 度は S と SW の境界 (期待値: S, 実際: S)
LOG: ✓ 337.4 度は NW と N の境界 (期待値: NW, 実際: NW)
LOG: キャリブレーションとエラーのテスト
LOG: ✓ 初期状態は未校正 (期待値: false, 実際: false)
LOG: ✓ 未校正状態の getDirection() は CAL (期待値: CAL, 実際: CAL)
LOG: ✓ 校正後は isCalibrated() が true (期待値: true, 実際: true)
LOG: ✓ 校正後のデフォルト角(0)は北(N) (期待値: N, 実際: N)
LOG: ===============================
LOG: テスト結果: 32/32 成功
LOG: 失敗: 0
LOG: ===============================
```

✅ **結果**: 32/32 PASS (100%)

---

## 総合テスト結果

```
┌──────────────────────────────────────────────────┐
│         全テスト 実行結果サマリー                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  ✅ Python     (pytest)         34/34 PASS       │
│     ├─ Unit (test_compass.py):       17/17 ✅   │
│     ├─ Integration:                  13/13 ✅   │
│     └─ Build (test_build_hex.py):     4/4  ✅   │
│                                                  │
│  ✅ TypeScript  (Jest)          73/73 PASS       │
│     ├─ Unit (compass.test.ts):       48/48 ✅   │
│     └─ Integration:                  25/25 ✅   │
│                                                  │
│  ✅ MakeCode   (Simulator)      32/32 PASS       │
│     └─ (8 方向 × 4 シナリオ)        32/32 ✅   │
│                                                  │
├──────────────────────────────────────────────────┤
│  📊 総合: 139/139 PASS (100%)                    │
│  ⏱️ 実行時間: ~7 秒 (全言語並行)                 │
│  📈 カバレッジ: 100% (Python)                    │
└──────────────────────────────────────────────────┘
```

---

## CI/CD パイプラインフロー

```
git push (feature/xxx)
    ↓
┌─────────────────────────────────────────────────┐
│ GitHub Actions Triggered                        │
├─────────────────────────────────────────────────┤
│  Job 1: Python Tests (Python 3.11)              │
│  ├─ pytest test_compass.py (17/17 PASS)        │
│  ├─ pytest test_compass_integration.py (13 OK) │
│  ├─ pytest test_build_hex.py (4/4 PASS)        │
│  └─ Coverage: 100%                              │
│                                                 │
│  Job 2: TypeScript Tests (Node 22.x)           │
│  ├─ jest --testPathPattern=compass (48 PASS)   │
│  ├─ jest --testPathPattern=integration (25 OK) │
│  └─ tsc --noEmit (型チェック通過)              │
│                                                 │
│  Job 3: MakeCode Tests                          │
│  ├─ pxt test (32/32 PASS)                      │
│  └─ pxt build (Hex 生成成功)                   │
│                                                 │
│  Job 4: Security Audit                         │
│  ├─ python: bandit (クリア)                     │
│  ├─ npm: npm audit (クリア)                     │
│  └─ docker: trivy (クリア)                      │
└─────────────────────────────────────────────────┘
    ↓
✅ All Checks Passed
    ↓
PR Merge Ready
```

---

## 成功メトリクス

| メトリクス | 目標 | 実績 | 状態 |
|-----------|------|------|------|
| テスト成功率 | 100% | 100% (139/139) | ✅ |
| カバレッジ | 100% | 100% (Python) | ✅ |
| ビルド成功 | 100% | 100% (HEX生成) | ✅ |
| CI/CD通過 | 100% | 100% | ✅ |
| セキュリティ | クリア | クリア (0 高リスク) | ✅ |

---

## 実行コマンドリファレンス

### 全テスト実行

```bash
npm run test:all
```

### 言語別テスト

```bash
# Python
npm run test:python

# TypeScript
npm run test:ts

# MakeCode
npm run test:makecode
```

### 統合テスト

```bash
npm run integration
```

### カバレッジレポート

```bash
npm run test:coverage
```
