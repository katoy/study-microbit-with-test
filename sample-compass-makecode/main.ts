/**
 * micro:bit 方位磁石アプリケーション
 * MakeCode メインプログラム
 */

// ボタン A を押してコンパスをキャリブレーション
input.onButtonPressed(Button.A, function () {
  basic.clearScreen();
  basic.showLeds(`
    . . # . .
    . # # # .
    # # # # #
    . # # # .
    . . # . .
  `);
  Compass.calibrate();
  basic.clearScreen();
  basic.showString('OK');
});

// ボタン B を押してコンパス状態を表示
input.onButtonPressed(Button.B, function () {
  Compass.showState();
});

// 起動時にキャリブレーション指示を表示
basic.showString('COMPASS');
basic.showString('A: CAL');
basic.showString('B: CHK');

// メインループ：継続的に方向を更新
basic.forever(function () {
  const direction = Compass.getDirection();
  
  // LED スクリーンに方向を表示
  if (direction == 'N') {
    basic.showLeds(`
      . . # . .
      . # # # .
      # . # . #
      . . . . .
      . . . . .
    `);
  } else if (direction == 'E') {
    basic.showLeds(`
      . . # . .
      . . # # .
      . . # . .
      . . # # .
      . . # . .
    `);
  } else if (direction == 'S') {
    basic.showLeds(`
      . . # . .
      . . . . .
      # . # . #
      . # # # .
      . . # . .
    `);
  } else if (direction == 'W') {
    basic.showLeds(`
      . . # . .
      . # # . .
      . . # . .
      . # # . .
      . . # . .
    `);
  } else if (direction == 'CAL') {
    // キャリブレーション未完了時は 'CAL' を表示してボタンA押下を促す
    basic.showString('CAL');
  } else if (direction == 'ERR') {
    // センサー異常時は 'ERR' を表示
    basic.showString('ERR');
  } else {
    basic.showString(direction);
  }
});
