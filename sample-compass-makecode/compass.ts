/**
 * micro:bit 用方位磁石アプリケーション
 * MakeCode（PXT）互換実装
 */

/**
 * 方角を表す型定義
 */
type CompassDirection = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';

/**
 * コンパスの状態を管理するインターフェース
 */
interface CompassState {
  heading: number;
  direction: CompassDirection;
  isCalibrated: boolean;
}

//% color="#E74C3C" icon="\uf14e" block="コンパス"
namespace Compass {
  let _heading: number = 0;
  let _isCalibrated: boolean = false;
  let _isTestMode: boolean = false;

  /**
   * コンパスをキャリブレーションする
   */
  //% block="コンパスをキャリブレーション"
  export function calibrate(): void {
    calibrateInternal(false);
  }

  /**
   * テスト用：ハードウェア API を呼ばずにキャリブレーション済みにする
   */
  export function calibrateForTest(): void {
    calibrateInternal(true);
  }

  function calibrateInternal(skipHardware: boolean): void {
    if (!skipHardware && !_isTestMode) {
      input.calibrateCompass();
    }
    _isCalibrated = true;
  }

  /**
   * テスト用：シミュレータテスト環境でのテストモードを有効にし、度数を設定する
   */
  export function setHeadingForTest(heading: number): void {
    _heading = heading;
    _isTestMode = true;
    _isCalibrated = true;
  }

  /**
   * 現在の方位角を取得する（0-359 度）
   */
  //% block="コンパスの度数 (度)"
  export function getHeading(): number {
    if (!_isTestMode) {
      _heading = input.compassHeading();
    }
    // 公式 API の範囲外でも壊れないかを考える、防御的プログラミングの練習
    if (_heading < 0) {
      _isCalibrated = false;
    }
    return _heading;
  }

  /**
   * 現在の方角を取得する（8 方位）
   */
  //% block="コンパスの方角"
  export function getDirection(): string {
    if (!_isCalibrated) {
      return 'CAL';
    }
    const heading = getHeading();
    if (heading < 0) {
      return 'ERR';
    }
    return headingToDirection(heading);
  }

  /**
   * キャリブレーション状態を取得する
   */
  //% block="コンパスはキャリブレーション済み"
  export function isCalibrated(): boolean {
    return _isCalibrated;
  }

  /**
   * 方位角を方角文字列に変換する（内部メソッド）
   */
  //% block="方位角 $heading 度の方角"
  //% heading.min=0 heading.max=359
  export function headingToDirection(heading: number): string {
    if (heading != heading || heading < 0 || heading >= 360) {
      return 'ERR';
    }

    if (heading < 22.5 || heading >= 337.5) {
      return 'N';
    } else if (heading < 67.5) {
      return 'NE';
    } else if (heading < 112.5) {
      return 'E';
    } else if (heading < 157.5) {
      return 'SE';
    } else if (heading < 202.5) {
      return 'S';
    } else if (heading < 247.5) {
      return 'SW';
    } else if (heading < 292.5) {
      return 'W';
    } else {
      return 'NW';
    }
  }

  /**
   * デバッグ用：現在の状態を表示
   */
  //% block="コンパス状態を表示"
  export function showState(): void {
    if (!_isCalibrated) {
      basic.showString('CAL?');
      return;
    }
    const heading = getHeading();
    const direction = getDirection();
    basic.showString(direction);
    basic.showNumber(heading);
  }
}
