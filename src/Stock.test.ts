/**
 * Stock 类单元测试
 * 测试发牌堆和废牌堆逻辑
 */

// Mock Card for Stock tests
class StockMockCard {
  suit: string;
  rank: string;
  value: number;
  faceUp: boolean;

  constructor(suit: string, rank: string, value: number, faceUp: boolean = false) {
    this.suit = suit;
    this.rank = rank;
    this.value = value;
    this.faceUp = faceUp;
  }

  setFaceUp(faceUp: boolean): void {
    this.faceUp = faceUp;
  }

  isFaceUp(): boolean {
    return this.faceUp;
  }
}

// Simplified Stock logic for testing
class StockLogic {
  private stockCards: StockMockCard[] = [];
  private wasteCards: StockMockCard[] = [];
  private isCyclic: boolean = true;

  initialize(cards: StockMockCard[]): void {
    this.stockCards = [...cards];
    this.wasteCards = [];
  }

  dealCard(): StockMockCard | null {
    if (this.stockCards.length === 0) {
      if (this.isCyclic && this.wasteCards.length > 0) {
        this.redeal();
        return this.dealCard();
      }
      return null;
    }

    const card = this.stockCards.pop() || null;
    if (card) {
      card.setFaceUp(true);
      this.wasteCards.push(card);
    }
    return card;
  }

  redeal(): void {
    // Move all waste cards back to stock
    while (this.wasteCards.length > 0) {
      const card = this.wasteCards.pop();
      if (card) {
        card.setFaceUp(false);
        this.stockCards.push(card);
      }
    }
  }

  getTopWasteCard(): StockMockCard | null {
    if (this.wasteCards.length === 0) {
      return null;
    }
    return this.wasteCards[this.wasteCards.length - 1];
  }

  getCardsRemaining(): number {
    return this.stockCards.length;
  }

  canDeal(): boolean {
    return this.stockCards.length > 0 || (this.isCyclic && this.wasteCards.length > 0);
  }

  removeTopWasteCard(): StockMockCard | null {
    return this.wasteCards.pop() || null;
  }

  setCyclic(cyclic: boolean): void {
    this.isCyclic = cyclic;
  }
}

describe('Stock Logic Tests', () => {
  
  describe('Stock Initialization', () => {
    it('should initialize with 24 cards', () => {
      const stock = new StockLogic();
      const cards = Array.from({ length: 24 }, () => 
        new StockMockCard('hearts', 'A', 1, false)
      );

      stock.initialize(cards);
      
      expect(stock.getCardsRemaining()).toBe(24);
    });

    it('should start with all cards face down', () => {
      const stock = new StockLogic();
      const cards = Array.from({ length: 24 }, () => 
        new StockMockCard('hearts', 'A', 1, false)
      );

      stock.initialize(cards);
      
      const allFaceDown = cards.every(card => !card.isFaceUp());
      expect(allFaceDown).toBe(true);
    });
  });

  describe('Dealing Cards', () => {
    it('should deal one card to waste pile', () => {
      const stock = new StockLogic();
      const card = new StockMockCard('hearts', 'A', 1, false);
      stock.initialize([card]);

      const dealtCard = stock.dealCard();

      expect(dealtCard).toBe(card);
      expect(card.isFaceUp()).toBe(true);
      expect(stock.getCardsRemaining()).toBe(0);
    });

    it('should deal multiple cards', () => {
      const stock = new StockLogic();
      const cards = [
        new StockMockCard('hearts', 'A', 1, false),
        new StockMockCard('diamonds', '2', 2, false),
        new StockMockCard('clubs', '3', 3, false)
      ];
      stock.initialize(cards);

      stock.dealCard();
      stock.dealCard();

      expect(stock.getCardsRemaining()).toBe(1);
    });

    it('should turn card face up when dealt', () => {
      const stock = new StockLogic();
      const card = new StockMockCard('hearts', 'A', 1, false);
      stock.initialize([card]);

      stock.dealCard();

      expect(card.isFaceUp()).toBe(true);
    });
  });

  describe('Redeal (Cyclic)', () => {
    it('should redeal waste cards back to stock', () => {
      const stock = new StockLogic();
      const cards = [
        new StockMockCard('hearts', 'A', 1, false),
        new StockMockCard('diamonds', '2', 2, false)
      ];
      stock.initialize(cards);

      // Deal all cards
      stock.dealCard();
      stock.dealCard();

      expect(stock.getCardsRemaining()).toBe(0);

      // Redeal
      stock.redeal();

      expect(stock.getCardsRemaining()).toBe(2);
    });

    it('should turn cards face down when redealt', () => {
      const stock = new StockLogic();
      const card = new StockMockCard('hearts', 'A', 1, false);
      stock.initialize([card]);

      stock.dealCard();
      expect(card.isFaceUp()).toBe(true);

      stock.redeal();
      expect(card.isFaceUp()).toBe(false);
    });

    it('should automatically redeal when stock is empty and cyclic', () => {
      const stock = new StockLogic();
      const card = new StockMockCard('hearts', 'A', 1, false);
      stock.initialize([card]);
      stock.setCyclic(true);

      // Deal the only card
      stock.dealCard();
      expect(stock.getCardsRemaining()).toBe(0);

      // Try to deal again - should trigger automatic redeal
      const dealtCard = stock.dealCard();
      
      expect(dealtCard).toBe(card);
    });
  });

  describe('Waste Pile', () => {
    it('should get top waste card', () => {
      const stock = new StockLogic();
      const card1 = new StockMockCard('hearts', 'A', 1, false);
      const card2 = new StockMockCard('diamonds', '2', 2, false);
      stock.initialize([card1, card2]);

      stock.dealCard();
      stock.dealCard();

      const topWaste = stock.getTopWasteCard();
      
      // Using pop(): card2 dealt first (bottom), card1 dealt second (top)
      expect(topWaste).toBe(card1);
      expect(topWaste?.isFaceUp()).toBe(true);
    });

    it('should return null when waste pile is empty', () => {
      const stock = new StockLogic();
      stock.initialize([]);

      const topWaste = stock.getTopWasteCard();
      
      expect(topWaste).toBe(null);
    });

    it('should remove top waste card', () => {
      const stock = new StockLogic();
      const card = new StockMockCard('hearts', 'A', 1, false);
      stock.initialize([card]);

      stock.dealCard();
      const removed = stock.removeTopWasteCard();

      expect(removed).toBe(card);
      expect(stock.getTopWasteCard()).toBe(null);
    });
  });

  describe('Can Deal Check', () => {
    it('should return true when stock has cards', () => {
      const stock = new StockLogic();
      stock.initialize([new StockMockCard('hearts', 'A', 1, false)]);

      expect(stock.canDeal()).toBe(true);
    });

    it('should return true when waste has cards and cyclic', () => {
      const stock = new StockLogic();
      stock.initialize([new StockMockCard('hearts', 'A', 1, false)]);
      stock.dealCard();
      stock.setCyclic(true);

      expect(stock.canDeal()).toBe(true);
    });

    it('should return false when no cards and not cyclic', () => {
      const stock = new StockLogic();
      stock.initialize([new StockMockCard('hearts', 'A', 1, false)]);
      stock.dealCard();
      stock.setCyclic(false);

      expect(stock.canDeal()).toBe(false);
    });
  });

  describe('Non-Cyclic Mode', () => {
    it('should not redeal when not cyclic', () => {
      const stock = new StockLogic();
      const card = new StockMockCard('hearts', 'A', 1, false);
      stock.initialize([card]);
      stock.setCyclic(false);

      stock.dealCard();
      const dealtAgain = stock.dealCard();

      expect(dealtAgain).toBe(null);
    });
  });
});
