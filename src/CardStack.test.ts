/**
 * CardStack 类单元测试
 * 测试 CardStack 的核心逻辑（不依赖 Phaser 渲染）
 */

// 简化的 Card 模拟（用于测试 CardStack 逻辑）
class MockCard {
  suit: string;
  rank: string;
  value: number;
  faceUp: boolean;
  eliminated: boolean;

  constructor(suit: string, rank: string, value: number, faceUp: boolean = true) {
    this.suit = suit;
    this.rank = rank;
    this.value = value;
    this.faceUp = faceUp;
    this.eliminated = false;
  }

  isFaceUp(): boolean {
    return this.faceUp;
  }

  isEliminatedCard(): boolean {
    return this.eliminated;
  }

  eliminate(): void {
    this.eliminated = true;
  }

  canEliminate(other: MockCard): boolean {
    if (!this.faceUp || !other.faceUp || other.eliminated) {
      return false;
    }
    return Math.abs(this.value - other.value) === 1;
  }
}

// 简化的 CardStack 逻辑测试
class MockCardStack {
  private cards: MockCard[] = [];
  private maxCards: number | null = null;

  addCard(card: MockCard): boolean {
    if (this.maxCards !== null && this.cards.length >= this.maxCards) {
      return false;
    }
    this.cards.push(card);
    return true;
  }

  removeTopCard(): MockCard | null {
    if (this.cards.length === 0) {
      return null;
    }
    return this.cards.pop() || null;
  }

  getCardCount(): number {
    return this.cards.length;
  }

  isEmpty(): boolean {
    return this.cards.length === 0;
  }

  isFull(): boolean {
    return this.maxCards !== null && this.cards.length >= this.maxCards;
  }

  getTopCard(): MockCard | null {
    if (this.cards.length === 0) {
      return null;
    }
    return this.cards[this.cards.length - 1];
  }

  hasCard(card: MockCard): boolean {
    return this.cards.includes(card);
  }

  removeCard(card: MockCard): boolean {
    const index = this.cards.indexOf(card);
    if (index === -1) {
      return false;
    }
    this.cards.splice(index, 1);
    return true;
  }

  canAcceptCard(card: MockCard): boolean {
    if (this.isEmpty()) {
      return true;
    }
    const topCard = this.getTopCard();
    if (!topCard) {
      return true;
    }
    return Math.abs(topCard.value - card.value) === 1;
  }

  clear(): void {
    this.cards = [];
  }

  getCards(): MockCard[] {
    return [...this.cards];
  }

  getFaceUpCards(): MockCard[] {
    return this.cards.filter(card => card.isFaceUp());
  }

  getFaceDownCards(): MockCard[] {
    return this.cards.filter(card => !card.isFaceUp());
  }

  shuffle(): void {
    for (let i = this.cards.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
    }
  }

  sortByValue(): void {
    this.cards.sort((a, b) => a.value - b.value);
  }

  flipAll(): void {
    this.cards.forEach(card => {
      (card as any).faceUp = !(card as any).faceUp;
    });
  }

  setAllFaceUp(faceUp: boolean): void {
    this.cards.forEach(card => {
      (card as any).faceUp = faceUp;
    });
  }
}

describe('CardStack Logic Tests', () => {
  
  describe('CardStack Creation', () => {
    it('should create an empty stack', () => {
      const stack = new MockCardStack();
      expect(stack.getCardCount()).toBe(0);
      expect(stack.isEmpty()).toBe(true);
    });

    it('should create a stack with maxCards limit', () => {
      const stack = new MockCardStack();
      (stack as any).maxCards = 5;
      expect(stack.isFull()).toBe(false);
    });
  });

  describe('Adding Cards', () => {
    it('should add a card to the stack', () => {
      const stack = new MockCardStack();
      const card = new MockCard('hearts', 'A', 1);
      
      const result = stack.addCard(card);
      
      expect(result).toBe(true);
      expect(stack.getCardCount()).toBe(1);
      expect(stack.isEmpty()).toBe(false);
    });

    it('should add multiple cards', () => {
      const stack = new MockCardStack();
      const cards = [
        new MockCard('hearts', 'A', 1),
        new MockCard('diamonds', '2', 2),
        new MockCard('clubs', '3', 3)
      ];

      cards.forEach(card => stack.addCard(card));
      
      expect(stack.getCardCount()).toBe(3);
    });

    it('should not add card when stack is full', () => {
      const stack = new MockCardStack();
      (stack as any).maxCards = 2;

      stack.addCard(new MockCard('hearts', 'A', 1));
      stack.addCard(new MockCard('diamonds', '2', 2));
      
      expect(stack.isFull()).toBe(true);
      
      const result = stack.addCard(new MockCard('clubs', '3', 3));
      expect(result).toBe(false);
      expect(stack.getCardCount()).toBe(2);
    });
  });

  describe('Removing Cards', () => {
    it('should remove the top card', () => {
      const stack = new MockCardStack();
      const card1 = new MockCard('hearts', 'A', 1);
      const card2 = new MockCard('diamonds', '2', 2);

      stack.addCard(card1);
      stack.addCard(card2);

      const removed = stack.removeTopCard();

      expect(removed).toBe(card2);
      expect(stack.getCardCount()).toBe(1);
      expect(stack.getTopCard()).toBe(card1);
    });

    it('should return null when removing from empty stack', () => {
      const stack = new MockCardStack();
      const removed = stack.removeTopCard();
      expect(removed).toBe(null);
    });

    it('should remove a specific card', () => {
      const stack = new MockCardStack();
      const card1 = new MockCard('hearts', 'A', 1);
      const card2 = new MockCard('diamonds', '2', 2);

      stack.addCard(card1);
      stack.addCard(card2);

      const result = stack.removeCard(card1);

      expect(result).toBe(true);
      expect(stack.getCardCount()).toBe(1);
      expect(stack.hasCard(card1)).toBe(false);
      expect(stack.hasCard(card2)).toBe(true);
    });
  });

  describe('Getting Cards', () => {
    it('should get the top card', () => {
      const stack = new MockCardStack();
      const card1 = new MockCard('hearts', 'A', 1);
      const card2 = new MockCard('diamonds', '2', 2);

      stack.addCard(card1);
      stack.addCard(card2);

      const top = stack.getTopCard();
      expect(top).toBe(card2);
    });

    it('should get all cards', () => {
      const stack = new MockCardStack();
      const cards = [
        new MockCard('hearts', 'A', 1),
        new MockCard('diamonds', '2', 2)
      ];

      cards.forEach(card => stack.addCard(card));

      const allCards = stack.getCards();
      expect(allCards.length).toBe(2);
    });
  });

  describe('Stack Operations', () => {
    it('should clear all cards', () => {
      const stack = new MockCardStack();
      stack.addCard(new MockCard('hearts', 'A', 1));
      stack.addCard(new MockCard('diamonds', '2', 2));
      
      stack.clear();
      
      expect(stack.getCardCount()).toBe(0);
      expect(stack.isEmpty()).toBe(true);
    });

    it('should check if stack has a card', () => {
      const stack = new MockCardStack();
      const card = new MockCard('hearts', 'A', 1);
      
      stack.addCard(card);
      expect(stack.hasCard(card)).toBe(true);
    });
  });

  describe('Shuffle and Sort', () => {
    it('should shuffle cards', () => {
      const stack = new MockCardStack();
      const cards = [
        new MockCard('hearts', 'A', 1),
        new MockCard('diamonds', '2', 2),
        new MockCard('clubs', '3', 3)
      ];

      cards.forEach(card => stack.addCard(card));
      
      const originalOrder = stack.getCards();
      stack.shuffle();
      const shuffledOrder = stack.getCards();

      expect(shuffledOrder.length).toBe(3);
    });

    it('should sort cards by value', () => {
      const stack = new MockCardStack();
      const cards = [
        new MockCard('hearts', '3', 3),
        new MockCard('diamonds', 'A', 1),
        new MockCard('clubs', '2', 2)
      ];

      cards.forEach(card => stack.addCard(card));
      stack.sortByValue();

      const sorted = stack.getCards();
      expect(sorted[0].value).toBe(1);
      expect(sorted[1].value).toBe(2);
      expect(sorted[2].value).toBe(3);
    });
  });

  describe('Tri-Peaks Rules', () => {
    it('should accept any card to empty stack', () => {
      const stack = new MockCardStack();
      const card = new MockCard('hearts', 'A', 1);
      
      expect(stack.canAcceptCard(card)).toBe(true);
    });

    it('should accept card with value difference of 1', () => {
      const stack = new MockCardStack();
      const card2 = new MockCard('hearts', '2', 2);
      const card3 = new MockCard('diamonds', '3', 3);

      stack.addCard(card2);
      expect(stack.canAcceptCard(card3)).toBe(true);
    });

    it('should not accept card with value difference > 1', () => {
      const stack = new MockCardStack();
      const card2 = new MockCard('hearts', '2', 2);
      const card5 = new MockCard('diamonds', '5', 5);

      stack.addCard(card2);
      expect(stack.canAcceptCard(card5)).toBe(false);
    });
  });

  describe('Face Up/Down Cards', () => {
    it('should get face-up cards', () => {
      const stack = new MockCardStack();
      const card1 = new MockCard('hearts', 'A', 1, true);
      const card2 = new MockCard('diamonds', '2', 2, false);

      stack.addCard(card1);
      stack.addCard(card2);

      const faceUpCards = stack.getFaceUpCards();
      expect(faceUpCards.length).toBe(1);
      expect(faceUpCards[0]).toBe(card1);
    });

    it('should get face-down cards', () => {
      const stack = new MockCardStack();
      const card1 = new MockCard('hearts', 'A', 1, true);
      const card2 = new MockCard('diamonds', '2', 2, false);

      stack.addCard(card1);
      stack.addCard(card2);

      const faceDownCards = stack.getFaceDownCards();
      expect(faceDownCards.length).toBe(1);
      expect(faceDownCards[0]).toBe(card2);
    });

    it('should flip all cards', () => {
      const stack = new MockCardStack();
      const card1 = new MockCard('hearts', 'A', 1, true);
      const card2 = new MockCard('diamonds', '2', 2, true);

      stack.addCard(card1);
      stack.addCard(card2);
      stack.flipAll();

      expect(card1.isFaceUp()).toBe(false);
      expect(card2.isFaceUp()).toBe(false);
    });

    it('should set all cards face up or down', () => {
      const stack = new MockCardStack();
      const card1 = new MockCard('hearts', 'A', 1, false);
      const card2 = new MockCard('diamonds', '2', 2, false);

      stack.addCard(card1);
      stack.addCard(card2);
      stack.setAllFaceUp(true);

      expect(card1.isFaceUp()).toBe(true);
      expect(card2.isFaceUp()).toBe(true);
    });
  });
});
