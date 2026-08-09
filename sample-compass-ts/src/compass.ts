/**
 * micro:bit 用方位磁石アプリケーション
 * TypeScript による型安全な実装
 */

/**
 * 方角を表す型定義
 */
export type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW' | 'CAL' | 'ERR';

/**
 * コンパスの状態を管理するインターフェース
 */
export interface CompassState {
  heading: number;
  direction: Direction;
  isCalibrated: boolean;
}

/**
 * micro:bit 用方位磁石クラス
 * 方位角と方角を管理する
 */
export class Compass {
  private heading: number = 0;
  private isCalibrated: boolean = false;

  constructor() {
    this.heading = 0;
    this.isCalibrated = false;
  }

  /**
   * コンパスをキャリブレーションする
   */
  public calibrate(): void {
    this.isCalibrated = true;
  }

  /**
   * 現在の方位角を取得する（0-359 度）
   * 注: 実装では内部値を返す。実デバイスでは compass.heading() を呼ぶ
   */
  public getHeading(): number {
    return this.heading;
  }

  /**
   * 方位角を設定する（テスト用）
   */
  public setHeading(heading: number): void {
    this.heading = heading;
  }

  /**
   * 現在の方角を取得する（8 方位）
   */
  public getDirection(): Direction {
    if (!this.isCalibrated) {
      return 'CAL';
    }
    const heading = this.getHeading();
    if (Number.isNaN(heading) || !Number.isFinite(heading) || heading < 0 || heading >= 360) {
      return 'ERR';
    }
    return this.headingToDirection(this.heading);
  }

  /**
   * キャリブレーション状態を取得する
   */
  public getIsCalibrated(): boolean {
    return this.isCalibrated;
  }

  /**
   * 状態を取得する
   */
  public getState(): CompassState {
    return {
      heading: this.heading,
      direction: this.getDirection(),
      isCalibrated: this.isCalibrated,
    };
  }

  /**
   * 方位角を方角文字列に変換する静的メソッド
   * @param heading - 0-359 度
   * @returns 方角（N, NE, E, SE, S, SW, W, NW, ERR）
   */
  public static headingToDirection(heading: number): Direction {
    if (Number.isNaN(heading) || !Number.isFinite(heading) || heading < 0 || heading >= 360) {
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
   * 方位角を方角文字列に変換するインスタンスメソッド
   */
  private headingToDirection(heading: number): Direction {
    return Compass.headingToDirection(heading);
  }
}

/**
 * micro:bit 上で実行する際のメイン関数
 */
export function main(): void {
  const compass = new Compass();

  // 未校正状態での取得は 'CAL' を返す
  console.log(`初期警告: ${compass.getDirection()}`);

  // キャリブレーション実行
  compass.calibrate();

  // キャリブレーション後は正常に状態取得可能
  const state = compass.getState();
  console.log(`方角: ${state.direction}, 度数: ${state.heading}°`);
}

