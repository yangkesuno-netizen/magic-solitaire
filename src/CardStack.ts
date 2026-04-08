import Phaser from 'phaser';
import { Card } from './Card';

export interface CardStackConfig {
  x: number;
  y: number;
  maxCards?: number; // -1 for unlimited
  faceUp?: boolean;
  spread?: number; // Vertical spread between cards
  clickable?: boolean;
}

export class CardStack extends Phaser.GameObjects.Container {
  private cards: Card[] = [];
  private maxCards: number;
  private spread: number;
  private topCard: Card | null = null;

  constructor(scene: Phaser.Scene, config: CardStackConfig) {
    super(scene, config.x, config.y);
    
    this.maxCards = config.maxCards ?? -1;
    this.spread = config.spread ?? 0;
    
    scene.add.existing(this);
  }

  /**
   * Add a card to the stack
   */
  public addCard(card: Card): boolean {
    if (this.maxCards !== -1 && this.cards.length >= this.maxCards) {
      return false;
    }

    this.cards.push(card);
    this.updatePositions();
    this.updateTopCard();
    
    return true;
  }

  /**
   * Add multiple cards to the stack
   */
  public addCards(cards: Card[]): void {
    cards.forEach(card => this.addCard(card));
  }

  /**
   * Remove and return the top card
   */
  public removeTopCard(): Card | null {
    if (this.cards.length === 0) {
      return null;
    }

    const card = this.cards.pop();
    if (card) {
      this.updatePositions();
      this.updateTopCard();
    }
    
    return card ?? null;
  }

  /**
   * Remove a specific card from the stack
   */
  public removeCard(card: Card): boolean {
    const index = this.cards.indexOf(card);
    if (index === -1) {
      return false;
    }

    this.cards.splice(index, 1);
    this.updatePositions();
    this.updateTopCard();
    
    return true;
  }

  /**
   * Get the top card
   */
  public getTopCard(): Card | null {
    return this.topCard;
  }

  /**
   * Get all cards in the stack
   */
  public getCards(): Card[] {
    return [...this.cards];
  }

  /**
   * Get the number of cards
   */
  public getCardCount(): number {
    return this.cards.length;
  }

  /**
   * Check if the stack is empty
   */
  public isEmpty(): boolean {
    return this.cards.length === 0;
  }

  /**
   * Check if the stack is full (if maxCards is set)
   */
  public isFull(): boolean {
    return this.maxCards !== -1 && this.cards.length >= this.maxCards;
  }

  /**
   * Clear all cards from the stack
   */
  public clear(): void {
    this.cards.forEach(card => card.destroy());
    this.cards = [];
    this.topCard = null;
  }

  /**
   * Flip all cards in the stack
   */
  public flipAll(): void {
    this.cards.forEach(card => card.flip());
  }

  /**
   * Set all cards to face up or face down
   */
  public setAllFaceUp(faceUp: boolean): void {
    this.cards.forEach(card => card.setFaceUp(faceUp));
  }

  /**
   * Get the card at a specific index
   */
  public getCardAt(index: number): Card | null {
    if (index < 0 || index >= this.cards.length) {
      return null;
    }
    return this.cards[index];
  }

  /**
   * Update card positions based on spread
   */
  private updatePositions(): void {
    this.cards.forEach((card, index) => {
      card.y = index * this.spread;
      card.setDepth(index);
    });
  }

  /**
   * Update the top card reference
   */
  private updateTopCard(): void {
    this.topCard = this.cards.length > 0 ? this.cards[this.cards.length - 1] : null;
  }

  /**
   * Check if a card is in this stack
   */
  public hasCard(card: Card): boolean {
    return this.cards.includes(card);
  }

  /**
   * Get the index of a card
   */
  public getCardIndex(card: Card): number {
    return this.cards.indexOf(card);
  }

  /**
   * Shuffle the cards in the stack
   */
  public shuffle(): this {
    // Fisher-Yates shuffle
    for (let i = this.cards.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
    }
    this.updatePositions();
    return this;
  }

  /**
   * Sort cards by value
   */
  public sortByValue(): void {
    this.cards.sort((a, b) => a.getValue() - b.getValue());
    this.updatePositions();
  }

  /**
   * Sort cards by suit then value
   */
  public sortBySuitAndValue(): void {
    const suitOrder = { 'spades': 0, 'hearts': 1, 'diamonds': 2, 'clubs': 3 };
    this.cards.sort((a, b) => {
      const suitDiff = suitOrder[a.getSuit()] - suitOrder[b.getSuit()];
      return suitDiff !== 0 ? suitDiff : a.getValue() - b.getValue();
    });
    this.updatePositions();
  }

  /**
   * Check if this stack can accept a card (for Tri-Peaks rules)
   */
  public canAcceptCard(card: Card): boolean {
    if (!this.topCard) {
      return true; // Empty stack can accept any card
    }
    return Math.abs(this.topCard.getValue() - card.getValue()) === 1;
  }

  /**
   * Get all face-up cards in the stack
   */
  public getFaceUpCards(): Card[] {
    return this.cards.filter(card => card.isFaceUp());
  }

  /**
   * Get all face-down cards in the stack
   */
  public getFaceDownCards(): Card[] {
    return this.cards.filter(card => !card.isFaceUp());
  }

  /**
   * Create a visual highlight for the top card
   */
  public highlightTopCard(): void {
    if (this.topCard) {
      this.scene.tweens.add({
        targets: this.topCard,
        scaleX: 1.05,
        scaleY: 1.05,
        duration: 200,
        yoyo: true,
        repeat: 1,
      });
    }
  }

  /**
   * Animate a card being added to the stack
   */
  public animateAddCard(card: Card, fromX: number, fromY: number): void {
    card.setPosition(fromX, fromY);
    card.setVisible(true);
    
    this.scene.tweens.add({
      targets: card,
      x: 0,
      y: (this.cards.length - 1) * this.spread,
      duration: 300,
      ease: 'Power2',
      onComplete: () => {
        this.updatePositions();
      },
    });
  }
}
