import Phaser from 'phaser';
import { Card } from './Card';
import { CardStack } from './CardStack';

/**
 * 发牌堆 (Stock Pile)
 * 存放剩余的 24 张牌，玩家可以点击发牌到废牌堆
 */
export class Stock {
  private stockPile: CardStack;
  private wastePile: CardStack;
  private cardsRemaining: number = 0;
  private isCyclic: boolean = true; // 是否允许循环发牌

  constructor(scene: Phaser.Scene, x: number, y: number) {

    // 创建发牌堆 (左侧)
    this.stockPile = new CardStack(scene, {
      x: x,
      y: y,
      maxCards: 24,
      clickable: true
    });

    // 创建废牌堆 (右侧，间距 120px)
    this.wastePile = new CardStack(scene, {
      x: x + 120,
      y: y,
      maxCards: 24,
      clickable: true
    });
  }

  /**
   * 初始化发牌堆
   * @param cards 剩余的牌 (24 张)
   */
  initialize(cards: Card[]): void {
    // 所有牌面朝下
    cards.forEach(card => {
      card.setFaceUp(false);
      this.stockPile.addCard(card);
    });
    this.cardsRemaining = cards.length;
  }

  /**
   * 发一张牌到废牌堆
   */
  dealCard(): Card | null {
    if (this.stockPile.isEmpty()) {
      // 如果发牌堆为空且允许循环，重新发牌
      if (this.isCyclic && !this.wastePile.isEmpty()) {
        this.redeal();
        return this.dealCard();
      }
      return null;
    }

    const card = this.stockPile.removeTopCard();
    if (card) {
      card.setFaceUp(true);
      this.wastePile.addCard(card);
      this.cardsRemaining = this.stockPile.getCardCount();
    }

    return card;
  }

  /**
   * 重新发牌 (将废牌堆的牌放回发牌堆)
   */
  redeal(): void {
    // 将废牌堆的所有牌移回发牌堆
    const cards = this.wastePile.getCards();
    
    // 从顶到底依次移回
    for (let i = cards.length - 1; i >= 0; i--) {
      const card = cards[i];
      this.wastePile.removeCard(card);
      card.setFaceUp(false);
      this.stockPile.addCard(card);
    }

    this.cardsRemaining = this.stockPile.getCardCount();
  }

  /**
   * 获取废牌堆顶牌
   */
  getTopWasteCard(): Card | null {
    return this.wastePile.getTopCard();
  }

  /**
   * 获取剩余牌数
   */
  getCardsRemaining(): number {
    return this.cardsRemaining;
  }

  /**
   * 检查是否可以发牌
   */
  canDeal(): boolean {
    return !this.stockPile.isEmpty() || (this.isCyclic && !this.wastePile.isEmpty());
  }

  /**
   * 从废牌堆移除顶牌 (用于消除)
   */
  removeTopWasteCard(): Card | null {
    const card = this.wastePile.removeTopCard();
    if (card) {
      // 不减少 cardsRemaining，因为这是已发出的牌
    }
    return card;
  }

  /**
   * 设置是否循环发牌
   */
  setCyclic(cyclic: boolean): void {
    this.isCyclic = cyclic;
  }

  /**
   * 重置发牌堆
   */
  reset(): void {
    this.stockPile.clear();
    this.wastePile.clear();
    this.cardsRemaining = 0;
  }
}
