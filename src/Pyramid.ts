import Phaser from 'phaser';
import { Card } from './Card';

/**
 * Tri-Peaks 金字塔结构管理
 * 负责 28 张牌的布局、遮挡检测、暴露检测
 */
export class Pyramid {
  private scene: Phaser.Scene;
  private cards: Card[][] = []; // 5 行，每行 1-5 张牌
  private x: number;
  private y: number;
  private rowSpacing: number = 30; // 行间距
  private colSpacing: number = 60; // 列间距

  constructor(scene: Phaser.Scene, x: number, y: number) {
    this.scene = scene;
    this.x = x;
    this.y = y;
  }

  /**
   * 创建金字塔布局 (28 张牌)
   * @param deck 洗好的牌组
   */
  create(deck: Card[]): void {
    let cardIndex = 0;
    const rows = 5;

    for (let row = 0; row < rows; row++) {
      const cardsInRow = row + 1;
      this.cards[row] = [];
      
      // 计算该行起始 X 坐标 (居中)
      const rowWidth = (cardsInRow - 1) * this.colSpacing;
      const startX = this.x - rowWidth / 2;

      for (let col = 0; col < cardsInRow; col++) {
        if (cardIndex >= deck.length) break;

        const x = startX + col * this.colSpacing;
        const y = this.y + row * this.rowSpacing;

        const card = deck[cardIndex];
        card.setPosition(x, y);
        card.setDepth(100 + row); // 越往下层级越高
        
        // 最下面一行 (row 4) 的牌面朝上，其他朝下
        if (row === rows - 1) {
          card.setFaceUp(true);
        } else {
          card.setFaceUp(false);
        }

        this.cards[row][col] = card;
        this.scene.add.existing(card);
        
        cardIndex++;
      }
    }
  }

  /**
   * 检查牌是否暴露 (可以被消除)
   * 暴露条件：不被上一行的牌遮挡
   */
  isCardExposed(card: Card): boolean {
    const position = this.getCardPosition(card);
    if (!position) return false;

    const { row, col } = position;

    // 最上面一行 (row 0) 总是暴露
    if (row === 0) {
      return true;
    }

    // 检查上一行的牌是否遮挡
    // 每张牌最多被上一行的 2 张牌遮挡
    const prevRow = row - 1;
    if (prevRow >= 0 && prevRow < this.cards.length) {
      // 检查左上方的牌
      if (col > 0 && this.cards[prevRow][col - 1]) {
        const prevCard = this.cards[prevRow][col - 1];
        if (!prevCard.isEliminatedCard()) {
          return false;
        }
      }
      // 检查右上方的牌
      if (col < this.cards[prevRow].length && this.cards[prevRow][col]) {
        const prevCard = this.cards[prevRow][col];
        if (!prevCard.isEliminatedCard()) {
          return false;
        }
      }
    }

    return true;
  }

  /**
   * 获取牌在金字塔中的位置
   */
  getCardPosition(card: Card): { row: number; col: number } | null {
    for (let row = 0; row < this.cards.length; row++) {
      for (let col = 0; col < this.cards[row].length; col++) {
        if (this.cards[row][col] === card) {
          return { row, col };
        }
      }
    }
    return null;
  }

  /**
   * 获取金字塔中所有牌
   */
  getAllCards(): Card[] {
    const allCards: Card[] = [];
    for (const row of this.cards) {
      for (const card of row) {
        allCards.push(card);
      }
    }
    return allCards;
  }

  /**
   * 获取金字塔中剩余未消除的牌数
   */
  getRemainingCards(): number {
    let count = 0;
    for (const row of this.cards) {
      for (const card of row) {
        if (!card.isEliminatedCard()) {
          count++;
        }
      }
    }
    return count;
  }

  /**
   * 检查是否胜利 (所有牌都被消除)
   */
  checkWin(): boolean {
    return this.getRemainingCards() === 0;
  }

  /**
   * 获取指定位置的牌
   */
  getCardAt(row: number, col: number): Card | null {
    if (row >= 0 && row < this.cards.length && 
        col >= 0 && col < this.cards[row].length) {
      return this.cards[row][col];
    }
    return null;
  }

  /**
   * 重置金字塔 (所有牌恢复)
   */
  reset(): void {
    for (const row of this.cards) {
      for (const card of row) {
        card.resetSelection();
        // 不恢复消除状态，因为这是新游戏
      }
    }
  }
}
