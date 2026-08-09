/**
 * 統合テスト: Compass アプリケーションの複数APIを組み合わせて検証する
 * 
 * 実際のユースケースに基づいたテストを実施する
 */

import { Compass, Direction, CompassState } from '../src/compass';

describe('Compass Integration Test Suite', () => {
  let compass: Compass;

  beforeEach(() => {
    compass = new Compass();
  });

  describe('Complete compass workflow', () => {
    it('should initialize compass and verify it returns CAL and 0 when not calibrated', () => {
      // Arrange
      const compass = new Compass();

      // Act & Assert
      expect(compass.getIsCalibrated()).toBe(false);
      expect(compass.getHeading()).toBe(0);
      expect(compass.getDirection()).toBe('CAL');
      const state = compass.getState();
      expect(state.isCalibrated).toBe(false);
      expect(state.direction).toBe('CAL');
      expect(state.heading).toBe(0);
    });

    it('should calibrate and maintain state', () => {
      // Arrange
      const compass = new Compass();

      // Act
      compass.calibrate();

      // Assert
      expect(compass.getIsCalibrated()).toBe(true);
      const state = compass.getState();
      expect(state.isCalibrated).toBe(true);
    });

    it('should update heading and reflect direction change', () => {
      // Arrange
      compass.calibrate();

      // Act
      compass.setHeading(90);

      // Assert
      expect(compass.getHeading()).toBe(90);
      expect(compass.getDirection()).toBe('E');
    });
  });

  describe('Direction detection across all 8 cardinal/intercardinal directions', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    it('should correctly identify North (0°)', () => {
      compass.setHeading(0);
      expect(compass.getDirection()).toBe('N');
    });

    it('should correctly identify Northeast (45°)', () => {
      compass.setHeading(45);
      expect(compass.getDirection()).toBe('NE');
    });

    it('should correctly identify East (90°)', () => {
      compass.setHeading(90);
      expect(compass.getDirection()).toBe('E');
    });

    it('should correctly identify Southeast (135°)', () => {
      compass.setHeading(135);
      expect(compass.getDirection()).toBe('SE');
    });

    it('should correctly identify South (180°)', () => {
      compass.setHeading(180);
      expect(compass.getDirection()).toBe('S');
    });

    it('should correctly identify Southwest (225°)', () => {
      compass.setHeading(225);
      expect(compass.getDirection()).toBe('SW');
    });

    it('should correctly identify West (270°)', () => {
      compass.setHeading(270);
      expect(compass.getDirection()).toBe('W');
    });

    it('should correctly identify Northwest (315°)', () => {
      compass.setHeading(315);
      expect(compass.getDirection()).toBe('NW');
    });
  });

  describe('Boundary conditions', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    it('should handle North boundary (22.5° threshold)', () => {
      compass.setHeading(22.4);
      expect(compass.getDirection()).toBe('N');

      compass.setHeading(22.5);
      expect(compass.getDirection()).toBe('NE');
    });

    it('should handle South boundary (202.5° threshold)', () => {
      compass.setHeading(202.4);
      expect(compass.getDirection()).toBe('S');

      compass.setHeading(202.5);
      expect(compass.getDirection()).toBe('SW');
    });

    it('should handle wrap-around at North (337.5° to 0°)', () => {
      compass.setHeading(337.5);
      expect(compass.getDirection()).toBe('N');

      compass.setHeading(359);
      expect(compass.getDirection()).toBe('N');

      compass.setHeading(0);
      expect(compass.getDirection()).toBe('N');
    });
  });

  describe('Real-world scenarios', () => {
    beforeEach(() => {
      compass.calibrate();
    });

    it('should handle continuous heading updates (simulating movement)', () => {
      // Simulate 360° rotation
      const headings = [0, 45, 90, 135, 180, 225, 270, 315];
      const expectedDirections: Direction[] = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];

      headings.forEach((heading, index) => {
        compass.setHeading(heading);
        const state = compass.getState();
        expect(state.direction).toBe(expectedDirections[index]);
        expect(state.heading).toBe(heading);
      });
    });

    it('should maintain state consistency during frequent direction queries', () => {
      compass.setHeading(45);

      // Query direction multiple times
      for (let i = 0; i < 100; i++) {
        expect(compass.getDirection()).toBe('NE');
      }

      // Heading should not change
      expect(compass.getHeading()).toBe(45);
    });

    it('should provide complete state snapshot', () => {
      compass.setHeading(180);
      const state: CompassState = compass.getState();

      expect(state).toEqual({
        heading: 180,
        direction: 'S',
        isCalibrated: true,
      });
    });

    it('should support multiple compass instances independently', () => {
      const compass2 = new Compass();

      compass.calibrate();
      compass.setHeading(0);

      compass2.calibrate();
      compass2.setHeading(90);

      expect(compass.getDirection()).toBe('N');
      expect(compass2.getDirection()).toBe('E');
    });
  });

  describe('Error handling', () => {
    it('should set negative heading and get ERR direction', () => {
      compass.calibrate();
      compass.setHeading(-1);
      expect(compass.getHeading()).toBe(-1);
      expect(compass.getDirection()).toBe('ERR');
    });

    it('should set heading >= 360 and get ERR direction', () => {
      compass.calibrate();
      compass.setHeading(360);
      expect(compass.getHeading()).toBe(360);
      expect(compass.getDirection()).toBe('ERR');
    });

    it('should set way out of range heading and get ERR direction', () => {
      compass.calibrate();
      compass.setHeading(720);
      expect(compass.getHeading()).toBe(720);
      expect(compass.getDirection()).toBe('ERR');
    });
  });

  describe('Repeated updates', () => {
    it('should preserve correctness after many heading updates', () => {
      compass.calibrate();

      for (let i = 0; i < 10000; i++) {
        compass.setHeading((i * 13) % 360);
        compass.getDirection();
      }

      expect(compass.getHeading()).toBe((9999 * 13) % 360);
    });

    it('should provide consistent results across rapid state queries', () => {
      compass.calibrate();
      compass.setHeading(123);

      const states = Array.from({ length: 1000 }, () => compass.getState());

      // All states should be identical
      states.forEach((state) => {
        expect(state.heading).toBe(123);
        expect(state.direction).toBe('SE');
        expect(state.isCalibrated).toBe(true);
      });
    });
  });

  describe('Main function', () => {
    let consoleSpy: jest.SpyInstance;

    beforeEach(() => {
      consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    });

    afterEach(() => {
      consoleSpy.mockRestore();
    });

    it('should execute main function without errors', () => {
      const { main } = require('../src/compass');

      // Act
      main();

      // Assert
      expect(consoleSpy).toHaveBeenCalledTimes(2);
      expect(consoleSpy.mock.calls[0][0]).toContain('CAL');
      expect(consoleSpy.mock.calls[1][0]).toMatch(/方角/);
      expect(consoleSpy.mock.calls[1][0]).toMatch(/度数/);
    });

    it('should initialize compass and get state in main', () => {
      const { main } = require('../src/compass');

      // Act
      main();

      // Assert
      expect(consoleSpy).toHaveBeenCalledTimes(2);
      expect(consoleSpy.mock.calls[0][0]).toContain('CAL');
      expect(consoleSpy.mock.calls[1][0]).toContain('N');
    });
  });
});

