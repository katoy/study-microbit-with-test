/**
 * micro:bit 用方位磁石アプリケーション
 * MakeCode（PXT）互換実装
 */

/**
 * 方角を表す型定義
 */
type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';

/**
 * コンパスの状態を管理するインターフェース
 */
interface CompassState {
  heading: number;
  direction: Direction;
  isCalibrated: boolean;
}

/**
 * %block="コンパス" icon="\uf14e"
 */
namespace Compass {
  let _heading: number = 0;
  let _isCalibrated: boolean = false;

  /**
   * コンパスをキャリブレーションする
   * %block="コンパスをキャリブレーション"
   */
  export function calibrate(): void {
    compass.calibrate();
    _isCalibrated = true;
  }

  /**
   * 現在の方位角を取得する（0-359 度）
   * %block="コンパスの度数 (度)"
   */
  export function getHeading(): number {
    _heading = compass.heading();
    return _heading;
  }

  /**
   * 現在の方角を取得する（8 方位）
   * %block="コンパスの方角"
   */
  export function getDirection(): string {
    const heading = getHeading();
    return headingToDirection(heading);
  }

  /**
   * キャリブレーション状態を取得する
   * %block="コンパスはキャリブレーション済み"
   */
  export function isCalibrated(): boolean {
    return _isCalibrated;
  }

  /**
   * 方位角を方角文字列に変換する（内部メソッド）
   */
  export function headingToDirection(heading: number): string {
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
   * %block="コンパス状態を表示"
   */
  export function showState(): void {
    const heading = getHeading();
    const direction = getDirection();
    const calibrated = isCalibrated() ? 'OK' : 'NG';
    basic.showString(direction);
    basic.showNumber(heading);
  }
}
