/**
 * compass.ts のユニットテスト
 * Jest を使用した包括的なテストスイート
 */

import { Compass, Direction, CompassState } from '../src/compass';

describe('Compass クラス', () => {
  let compass: Compass;

  beforeEach(() => {
    compass = new Compass();
  });

  describe('初期化', () => {
    test('コンストラクタが正しく初期化される', () => {
      expect(compass.getIsCalibrated()).toBe(false);
    });

    test('未キャリブレーション状態で getHeading() はエラーを投げる', () => {
      expect(() => compass.getHeading()).toThrow('Compass not calibrated');
    });

    test('未キャリブレーション状態で getDirection() はエラーを投げる', () => {
      expect(() => compass.getDirection()).toThrow('Compass not calibrated');
    });
  });

  describe('キャリブレーション', () => {
    test('calibrate() を呼び出すとキャリブレーション状態が true になる', () => {
      expect(compass.getIsCalibrated()).toBe(false);
      compass.calibrate();
      expect(compass.getIsCalibrated()).toBe(true);
    });
  });

  describe('方位角の設定と取得', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('setHeading() で方位角が正しく設定される', () => {
      compass.setHeading(45);
      expect(compass.getHeading()).toBe(45);
    });

    test('setHeading() で負の値がエラーになる', () => {
      expect(() => compass.setHeading(-1)).toThrow(
        '方位角は 0-359 度である必要があります'
      );
    });

    test('setHeading() で 360 度以上がエラーになる', () => {
      expect(() => compass.setHeading(360)).toThrow(
        '方位角は 0-359 度である必要があります'
      );
    });

    test('setHeading() で NaN がエラーになる', () => {
      expect(() => compass.setHeading(Number.NaN)).toThrow(
        '方位角は 0-359 度である必要があります'
      );
    });
  });

  describe('北方向（N）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('0 度は北（N）', () => {
      compass.setHeading(0);
      expect(compass.getDirection()).toBe('N');
    });

    test('22 度は北（N）', () => {
      compass.setHeading(22);
      expect(compass.getDirection()).toBe('N');
    });

    test('337.5 度以上は北（N）', () => {
      compass.setHeading(338);
      expect(compass.getDirection()).toBe('N');
    });

    test('359 度は北（N）', () => {
      compass.setHeading(359);
      expect(compass.getDirection()).toBe('N');
    });
  });

  describe('北東方向（NE）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('45 度は北東（NE）', () => {
      compass.setHeading(45);
      expect(compass.getDirection()).toBe('NE');
    });

    test('22.5 度は北東（NE）', () => {
      compass.setHeading(22.5);
      expect(compass.getDirection()).toBe('NE');
    });

    test('67 度は北東（NE）', () => {
      compass.setHeading(67);
      expect(compass.getDirection()).toBe('NE');
    });
  });

  describe('東方向（E）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('90 度は東（E）', () => {
      compass.setHeading(90);
      expect(compass.getDirection()).toBe('E');
    });

    test('67.5 度は東（E）', () => {
      compass.setHeading(67.5);
      expect(compass.getDirection()).toBe('E');
    });

    test('112 度は東（E）', () => {
      compass.setHeading(112);
      expect(compass.getDirection()).toBe('E');
    });
  });

  describe('南東方向（SE）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('135 度は南東（SE）', () => {
      compass.setHeading(135);
      expect(compass.getDirection()).toBe('SE');
    });

    test('112.5 度は南東（SE）', () => {
      compass.setHeading(112.5);
      expect(compass.getDirection()).toBe('SE');
    });

    test('157 度は南東（SE）', () => {
      compass.setHeading(157);
      expect(compass.getDirection()).toBe('SE');
    });
  });

  describe('南方向（S）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('180 度は南（S）', () => {
      compass.setHeading(180);
      expect(compass.getDirection()).toBe('S');
    });

    test('157.5 度は南（S）', () => {
      compass.setHeading(157.5);
      expect(compass.getDirection()).toBe('S');
    });

    test('202 度は南（S）', () => {
      compass.setHeading(202);
      expect(compass.getDirection()).toBe('S');
    });
  });

  describe('南西方向（SW）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('225 度は南西（SW）', () => {
      compass.setHeading(225);
      expect(compass.getDirection()).toBe('SW');
    });

    test('202.5 度は南西（SW）', () => {
      compass.setHeading(202.5);
      expect(compass.getDirection()).toBe('SW');
    });

    test('247 度は南西（SW）', () => {
      compass.setHeading(247);
      expect(compass.getDirection()).toBe('SW');
    });
  });

  describe('西方向（W）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('270 度は西（W）', () => {
      compass.setHeading(270);
      expect(compass.getDirection()).toBe('W');
    });

    test('247.5 度は西（W）', () => {
      compass.setHeading(247.5);
      expect(compass.getDirection()).toBe('W');
    });

    test('292 度は西（W）', () => {
      compass.setHeading(292);
      expect(compass.getDirection()).toBe('W');
    });
  });

  describe('北西方向（NW）の判定', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('315 度は北西（NW）', () => {
      compass.setHeading(315);
      expect(compass.getDirection()).toBe('NW');
    });

    test('292.5 度は北西（NW）', () => {
      compass.setHeading(292.5);
      expect(compass.getDirection()).toBe('NW');
    });

    test('337 度は北西（NW）', () => {
      compass.setHeading(337);
      expect(compass.getDirection()).toBe('NW');
    });
  });

  describe('境界値テスト', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    test('22.5 度は NE と N の境界', () => {
      compass.setHeading(22.4);
      expect(compass.getDirection()).toBe('N');
      compass.setHeading(22.5);
      expect(compass.getDirection()).toBe('NE');
    });

    test('67.5 度は E と NE の境界', () => {
      compass.setHeading(67.4);
      expect(compass.getDirection()).toBe('NE');
      compass.setHeading(67.5);
      expect(compass.getDirection()).toBe('E');
    });

    test('202.5 度は SW と S の境界', () => {
      compass.setHeading(202.4);
      expect(compass.getDirection()).toBe('S');
      compass.setHeading(202.5);
      expect(compass.getDirection()).toBe('SW');
    });

    test('337.5 度は NW と N の境界', () => {
      compass.setHeading(337.4);
      expect(compass.getDirection()).toBe('NW');
      compass.setHeading(337.5);
      expect(compass.getDirection()).toBe('N');
    });
  });

  describe('静的メソッド headingToDirection', () => {
    test('45 度は NE を返す', () => {
      const direction = Compass.headingToDirection(45);
      expect(direction).toBe('NE');
    });

    test('90 度は E を返す', () => {
      const direction = Compass.headingToDirection(90);
      expect(direction).toBe('E');
    });

    test('180 度は S を返す', () => {
      const direction = Compass.headingToDirection(180);
      expect(direction).toBe('S');
    });

    test('270 度は W を返す', () => {
      const direction = Compass.headingToDirection(270);
      expect(direction).toBe('W');
    });

    test.each([Number.NaN, Number.POSITIVE_INFINITY, -1, 360])(
      '無効な方位角 %s はエラーになる',
      (heading) => {
        expect(() => Compass.headingToDirection(heading)).toThrow(
          '方位角は 0-359 度である必要があります'
        );
      }
    );
  });

  describe('状態取得メソッド', () => {
    test('getState() が正しい状態を返す', () => {
      compass.calibrate();
      compass.setHeading(90);

      const state: CompassState = compass.getState();

      expect(state.heading).toBe(90);
      expect(state.direction).toBe('E');
      expect(state.isCalibrated).toBe(true);
    });

    test('getState() が複数回呼び出されても一貫性がある', () => {
      compass.calibrate();
      compass.setHeading(225);

      const state1 = compass.getState();
      const state2 = compass.getState();

      expect(state1).toEqual(state2);
      expect(state1.direction).toBe('SW');
      expect(state2.direction).toBe('SW');
    });
  });

  describe('複合シナリオ', () => {
    test('キャリブレーション後に複数の方向を判定できる', () => {
      compass.calibrate();

      const directions: Array<[number, Direction]> = [
        [0, 'N'],
        [45, 'NE'],
        [90, 'E'],
        [135, 'SE'],
        [180, 'S'],
        [225, 'SW'],
        [270, 'W'],
        [315, 'NW'],
      ];

      directions.forEach(([heading, expected]) => {
        compass.setHeading(heading);
        expect(compass.getDirection()).toBe(expected);
        expect(compass.getIsCalibrated()).toBe(true);
      });
    });
  });
});
