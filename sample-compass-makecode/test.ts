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
  }
}

// コンパステスト
namespace compassTests {
  export function runAllTests(): void {
    console.log('方位磁石テスト開始...\n');

    testInitialization();
    testNorthDirection();
    testNorthEastDirection();
    testEastDirection();
    testSouthEastDirection();
    testSouthDirection();
    testSouthWestDirection();
    testWestDirection();
    testNorthWestDirection();
    testBoundaryValues();

    tests.summary();
  }

  function testInitialization(): void {
    console.log('初期化テスト');
    // MakeCode では初期状態で北を指す
    tests.assertEqual(Compass.getDirection(), 'N', '初期方角は北（N）');
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
}
