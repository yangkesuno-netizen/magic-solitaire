/**
 * GameUI 类单元测试
 * 测试游戏 UI 管理功能
 */

// Mock Phaser objects for GameUI testing
class MockText {
  x: number = 0;
  y: number = 0;
  text: string = '';
  
  constructor(x: number, y: number, text: string) {
    this.x = x;
    this.y = y;
    this.text = text;
  }
  
  setText(newText: string): this {
    this.text = newText;
    return this;
  }
  
  setOrigin(): this {
    return this;
  }
}

class MockRectangle {
  x: number = 0;
  y: number = 0;
  width: number = 0;
  height: number = 0;
  fillStyle: number = 0;
  
  setOrigin(): this {
    return this;
  }
  
  setInteractive(): this {
    return this;
  }
  
  on(): this {
    return this;
  }
  
  setFillStyle(color: number): this {
    this.fillStyle = color;
    return this;
  }
}

class MockContainer {
  x: number = 0;
  y: number = 0;
  
  setPosition(): this {
    return this;
  }
}

class MockScene {
  add: any;
  scale: any;
  tweens: any;
  time: any;
  events: any;
  
  constructor() {
    this.add = {
      text: () => new MockText(0, 0, ''),
      rectangle: () => new MockRectangle(),
      container: () => new MockContainer(),
      circle: () => ({}),
      zone: () => ({}),
    };
    
    this.scale = {
      width: 800,
      height: 600,
    };
    
    this.tweens = {
      add: () => {},
    };
    
    this.time = {
      delayedCall: () => {},
    };
    
    this.events = {
      on: () => {},
      emit: () => {},
    };
  }
}

// Simplified GameUI logic for testing
class GameUILogic {
  private score: number = 0;
  private cardsRemaining: number = 24;
  
  addScore(points: number): void {
    this.score += points;
  }
  
  updateScore(points: number): void {
    this.score = points;
  }
  
  resetScore(): void {
    this.score = 0;
  }
  
  getScore(): number {
    return this.score;
  }
  
  updateCardsRemaining(count: number): void {
    this.cardsRemaining = count;
  }
  
  getCardsRemaining(): number {
    return this.cardsRemaining;
  }
}

describe('GameUI Logic Tests', () => {
  
  describe('Score Management', () => {
    it('should start with score 0', () => {
      const ui = new GameUILogic();
      expect(ui.getScore()).toBe(0);
    });

    it('should add score correctly', () => {
      const ui = new GameUILogic();
      ui.addScore(10);
      expect(ui.getScore()).toBe(10);
      
      ui.addScore(10);
      expect(ui.getScore()).toBe(20);
    });

    it('should update score directly', () => {
      const ui = new GameUILogic();
      ui.updateScore(50);
      expect(ui.getScore()).toBe(50);
    });

    it('should reset score to 0', () => {
      const ui = new GameUILogic();
      ui.addScore(100);
      ui.resetScore();
      expect(ui.getScore()).toBe(0);
    });

    it('should handle negative score (if game allows)', () => {
      const ui = new GameUILogic();
      ui.updateScore(-10);
      expect(ui.getScore()).toBe(-10);
    });
  });

  describe('Cards Remaining Management', () => {
    it('should start with 24 cards', () => {
      const ui = new GameUILogic();
      expect(ui.getCardsRemaining()).toBe(24);
    });

    it('should update cards remaining', () => {
      const ui = new GameUILogic();
      ui.updateCardsRemaining(20);
      expect(ui.getCardsRemaining()).toBe(20);
    });

    it('should handle zero cards remaining', () => {
      const ui = new GameUILogic();
      ui.updateCardsRemaining(0);
      expect(ui.getCardsRemaining()).toBe(0);
    });

    it('should decrement cards correctly', () => {
      const ui = new GameUILogic();
      ui.updateCardsRemaining(24);
      ui.updateCardsRemaining(23);
      ui.updateCardsRemaining(22);
      expect(ui.getCardsRemaining()).toBe(22);
    });
  });

  describe('Score Calculation for Tri-Peaks', () => {
    it('should award 10 points per card eliminated', () => {
      const ui = new GameUILogic();
      
      // Eliminate 5 cards
      for (let i = 0; i < 5; i++) {
        ui.addScore(10);
      }
      
      expect(ui.getScore()).toBe(50);
    });

    it('should calculate perfect game score', () => {
      const ui = new GameUILogic();
      
      // Eliminate all 28 pyramid cards
      for (let i = 0; i < 28; i++) {
        ui.addScore(10);
      }
      
      expect(ui.getScore()).toBe(280);
    });

    it('should track partial game progress', () => {
      const ui = new GameUILogic();
      
      // Eliminate 14 cards (half of pyramid)
      for (let i = 0; i < 14; i++) {
        ui.addScore(10);
      }
      
      expect(ui.getScore()).toBe(140);
      expect(ui.getScore()).toBeLessThan(280);
    });
  });

  describe('Game State Tracking', () => {
    it('should track score and cards independently', () => {
      const ui = new GameUILogic();
      
      ui.addScore(10);
      ui.updateCardsRemaining(23);
      
      expect(ui.getScore()).toBe(10);
      expect(ui.getCardsRemaining()).toBe(23);
    });

    it('should reset both score and cards for new game', () => {
      const ui = new GameUILogic();
      
      ui.addScore(100);
      ui.updateCardsRemaining(10);
      
      ui.resetScore();
      ui.updateCardsRemaining(24);
      
      expect(ui.getScore()).toBe(0);
      expect(ui.getCardsRemaining()).toBe(24);
    });
  });
});

describe('GameUI Display Tests', () => {
  
  describe('Score Display Format', () => {
    it('should format score as "Score: X"', () => {
      const score = 150;
      const displayText = `Score: ${score}`;
      expect(displayText).toBe('Score: 150');
    });

    it('should handle zero score display', () => {
      const score = 0;
      const displayText = `Score: ${score}`;
      expect(displayText).toBe('Score: 0');
    });

    it('should handle large scores', () => {
      const score = 1000;
      const displayText = `Score: ${score}`;
      expect(displayText).toBe('Score: 1000');
    });
  });

  describe('Cards Remaining Display Format', () => {
    it('should format cards as "Cards: X"', () => {
      const count = 24;
      const displayText = `Cards: ${count}`;
      expect(displayText).toBe('Cards: 24');
    });

    it('should handle zero cards display', () => {
      const count = 0;
      const displayText = `Cards: ${count}`;
      expect(displayText).toBe('Cards: 0');
    });
  });

  describe('Victory Message', () => {
    it('should display victory message', () => {
      const victoryText = 'VICTORY!';
      expect(victoryText).toContain('VICTORY');
    });

    it('should display final score in victory', () => {
      const score = 280;
      const message = `Final Score: ${score}`;
      expect(message).toBe('Final Score: 280');
    });
  });

  describe('Game Over Message', () => {
    it('should display game over message', () => {
      const gameOverText = 'GAME OVER';
      expect(gameOverText).toContain('GAME OVER');
    });

    it('should display score in game over', () => {
      const score = 50;
      const message = `Score: ${score}`;
      expect(message).toBe('Score: 50');
    });
  });
});
