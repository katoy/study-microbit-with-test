/**
 * compass.ts のユニットテスト
 * MakeCode テストフレームワーク互換
 */

// テストユーティリティ
namespace tests {
  let totalTests = 0;
  let passedTests = 0;
  let failedTests = 0;

  export function assert(condition: boolean, message: string): void {
    totalTests++;
    if (condition) {
      passedTests++;
      console.log(`✓ ${message}`);
    } else {
      failedTests++;
      console.log(`✗ ${message}`);
    }
  }

  export function assertEqual(actual: any, expected: any, message: string): void {
    const passed = actual === expected;
    assert(passed, `${message} (期待値: ${expected}, 実際: ${actual})`);
  }

  export function summary(): void {
    console.log(`\n===============================`);
    console.log(`テスト結果: ${passedTests}/${totalTests} 成功`);
    console.log(`失敗: ${failedTests}`);
    console.log(`===============================`);
    console.log(`MAKECODE_TEST_RESULT total=${totalTests} passed=${passedTests} failed=${failedTests}`);
  }
}

// コンパステスト
namespace compassTests {
  export function runAllTests(): void {
    console.log('方位磁石テスト開始...\n');

    testNorthDirection();
    testNorthEastDirection();
    testEastDirection();
    testSouthEastDirection();
    testSouthDirection();
    testSouthWestDirection();
    testWestDirection();
    testNorthWestDirection();
    testBoundaryValues();
    testInvalidHeadings();
    testCalibrationAndErrors();

    tests.summary();
  }

  function testNorthDirection(): void {
    console.log('\n北方向（N）テスト');
    tests.assertEqual(Compass.headingToDirection(0), 'N', '0 度は北（N）');
    tests.assertEqual(Compass.headingToDirection(22), 'N', '22 度は北（N）');
    tests.assertEqual(Compass.headingToDirection(359), 'N', '359 度は北（N）');
  }

  function testNorthEastDirection(): void {
    console.log('\n北東方向（NE）テスト');
    tests.assertEqual(Compass.headingToDirection(22.5), 'NE', '22.5 度は北東（NE）');
    tests.assertEqual(Compass.headingToDirection(45), 'NE', '45 度は北東（NE）');
    tests.assertEqual(Compass.headingToDirection(67), 'NE', '67 度は北東（NE）');
  }

  function testEastDirection(): void {
    console.log('\n東方向（E）テスト');
    tests.assertEqual(Compass.headingToDirection(67.5), 'E', '67.5 度は東（E）');
    tests.assertEqual(Compass.headingToDirection(90), 'E', '90 度は東（E）');
    tests.assertEqual(Compass.headingToDirection(112), 'E', '112 度は東（E）');
  }

  function testSouthEastDirection(): void {
    console.log('\n南東方向（SE）テスト');
    tests.assertEqual(Compass.headingToDirection(112.5), 'SE', '112.5 度は南東（SE）');
    tests.assertEqual(Compass.headingToDirection(135), 'SE', '135 度は南東（SE）');
    tests.assertEqual(Compass.headingToDirection(157), 'SE', '157 度は南東（SE）');
  }

  function testSouthDirection(): void {
    console.log('\n南方向（S）テスト');
    tests.assertEqual(Compass.headingToDirection(157.5), 'S', '157.5 度は南（S）');
    tests.assertEqual(Compass.headingToDirection(180), 'S', '180 度は南（S）');
    tests.assertEqual(Compass.headingToDirection(202), 'S', '202 度は南（S）');
  }

  function testSouthWestDirection(): void {
    console.log('\n南西方向（SW）テスト');
    tests.assertEqual(Compass.headingToDirection(202.5), 'SW', '202.5 度は南西（SW）');
    tests.assertEqual(Compass.headingToDirection(225), 'SW', '225 度は南西（SW）');
    tests.assertEqual(Compass.headingToDirection(247), 'SW', '247 度は南西（SW）');
  }

  function testWestDirection(): void {
    console.log('\n西方向（W）テスト');
    tests.assertEqual(Compass.headingToDirection(247.5), 'W', '247.5 度は西（W）');
    tests.assertEqual(Compass.headingToDirection(270), 'W', '270 度は西（W）');
    tests.assertEqual(Compass.headingToDirection(292), 'W', '292 度は西（W）');
  }

  function testNorthWestDirection(): void {
    console.log('\n北西方向（NW）テスト');
    tests.assertEqual(Compass.headingToDirection(292.5), 'NW', '292.5 度は北西（NW）');
    tests.assertEqual(Compass.headingToDirection(315), 'NW', '315 度は北西（NW）');
    tests.assertEqual(Compass.headingToDirection(337), 'NW', '337 度は北西（NW）');
  }

  function testBoundaryValues(): void {
    console.log('\n境界値テスト');
    tests.assertEqual(Compass.headingToDirection(22.4), 'N', '22.4 度は N と NE の境界');
    tests.assertEqual(Compass.headingToDirection(67.4), 'NE', '67.4 度は NE と E の境界');
    tests.assertEqual(Compass.headingToDirection(202.4), 'S', '202.4 度は S と SW の境界');
    tests.assertEqual(Compass.headingToDirection(337.4), 'NW', '337.4 度は NW と N の境界');
  }

  function testInvalidHeadings(): void {
    console.log('\n無効な方位角テスト');
    tests.assertEqual(Compass.headingToDirection(-5), 'ERR', '-5 度は無効');
    tests.assertEqual(Compass.headingToDirection(400), 'ERR', '400 度は無効');
    tests.assertEqual(Compass.headingToDirection(NaN), 'ERR', 'NaN は無効');
  }

  function testCalibrationAndErrors(): void {
    console.log('\nキャリブレーションとエラーのテスト');
    
    // 初期状態は simulator-test-runner.cjs 内で pxt run される時点では
    // _isCalibrated が false のまま
    tests.assertEqual(Compass.isCalibrated(), false, '初期状態は未校正');
    tests.assertEqual(Compass.getDirection(), 'CAL', '未校正状態の getDirection() は CAL');
    
    // テスト専用 API でハードウェア API の呼び出しをスキップする
    Compass.calibrateForTest();
    tests.assertEqual(Compass.isCalibrated(), true, '校正後は isCalibrated() が true');
    
    // テスト用のダミー方位角を設定して正常動作確認
    Compass.setHeadingForTest(0);
    tests.assertEqual(Compass.getDirection(), 'N', '校正後のデフォルト角(0)は北(N)');
  }
}
