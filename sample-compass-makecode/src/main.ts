/**
 * micro:bit 方位磁石アプリケーション
 * MakeCode メインプログラム
 */

// ボタン A を押してログ出力またはキャリブレーション
input.onButtonPressed(Button.A, function () {
  if (!Compass.isCalibrated()) {
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
  } else {
    const heading = Compass.getHeading();
    const direction = Compass.getDirection();
    console.log("Time: " + input.runningTime() + "ms, Heading: " + heading + ", Dir: " + direction);
  }
});

// 起動時の指示
basic.showString('COMPASS');
basic.showString('A:LOG');

// メインループ：継続的に方向を更新
basic.forever(function () {
  if (!Compass.isCalibrated()) {
    // キャリブレーション未完了時は 'CAL' を表示して促す
    basic.showString('CAL');
    basic.pause(1000);
  } else {
    const heading = Compass.getHeading();
    if (heading < 0) {
      basic.showString('ERR');
      basic.pause(1000);
    } else {
      const direction = Compass.getDirection();
      // 8方向の矢印で表示
      if (direction == 'N') {
        basic.showArrow(ArrowNames.North);
      } else if (direction == 'NE') {
        basic.showArrow(ArrowNames.NorthEast);
      } else if (direction == 'E') {
        basic.showArrow(ArrowNames.East);
      } else if (direction == 'SE') {
        basic.showArrow(ArrowNames.SouthEast);
      } else if (direction == 'S') {
        basic.showArrow(ArrowNames.South);
      } else if (direction == 'SW') {
        basic.showArrow(ArrowNames.SouthWest);
      } else if (direction == 'W') {
        basic.showArrow(ArrowNames.West);
      } else if (direction == 'NW') {
        basic.showArrow(ArrowNames.NorthWest);
      }
      basic.pause(500);
    }
  }
});

