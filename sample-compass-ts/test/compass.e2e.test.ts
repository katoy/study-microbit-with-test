/**
 * E2E テスト: Compass アプリケーション統合テスト
 * 
 * 実際のユースケースに基づいたテストを実施する
 */

import { Compass, Direction, CompassState } from '../src/compass';

describe('Compass E2E Test Suite', () => {
  let compass: Compass;

  beforeEach(() => {
    compass = new Compass();
  });

  describe('Complete compass workflow', () => {
    it('should initialize compass and perform basic heading check', () => {
      // Arrange
      const compass = new Compass();

      // Act
      const initialState = compass.getState();

      // Assert
      expect(initialState.heading).toBe(0);
      expect(initialState.isCalibrated).toBe(false);
      expect(initialState.direction).toBe('N');
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
    it('should reject invalid headings (negative)', () => {
      compass.calibrate();
      expect(() => compass.setHeading(-1)).toThrow(
        '方位角は 0-359 度である必要があります'
      );
    });

    it('should reject invalid headings (>= 360)', () => {
      compass.calibrate();
      expect(() => compass.setHeading(360)).toThrow(
        '方位角は 0-359 度である必要があります'
      );
    });

    it('should reject invalid headings (way out of range)', () => {
      compass.calibrate();
      expect(() => compass.setHeading(720)).toThrow(
        '方位角は 0-359 度である必要があります'
      );
    });
  });

  describe('Performance under load', () => {
    it('should handle rapid heading updates efficiently', () => {
      compass.calibrate();

      const startTime = Date.now();

      for (let i = 0; i < 10000; i++) {
        compass.setHeading((i * 13) % 360);
        compass.getDirection();
      }

      const endTime = Date.now();
      const duration = endTime - startTime;

      // Should complete 10000 operations quickly
      expect(duration).toBeLessThan(1000);
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
    it('should execute main function without errors', () => {
      // Import main after Compass is defined
      const { main } = require('../src/compass');

      // Arrange & Act
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      // Act
      main();

      // Assert
      expect(consoleSpy).toHaveBeenCalled();
      const callArgs = consoleSpy.mock.calls[0][0];
      expect(callArgs).toMatch(/方角/);
      expect(callArgs).toMatch(/度数/);

      // Cleanup
      consoleSpy.mockRestore();
    });

    it('should initialize compass and get state in main', () => {
      // Import main after Compass is defined
      const { main } = require('../src/compass');

      // Arrange
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

      // Act
      main();

      // Assert
      expect(consoleSpy).toHaveBeenCalledTimes(1);
      const output = consoleSpy.mock.calls[0][0];
      expect(output).toContain('N');  // Initial direction should be N

      // Cleanup
      consoleSpy.mockRestore();
    });
  });
});
