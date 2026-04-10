import Phaser from 'phaser';

export type CardSuit = 'hearts' | 'diamonds' | 'clubs' | 'spades';
export type CardRank = 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K';

export interface CardData {
  suit: CardSuit;
  rank: CardRank;
  value: number;
  faceUp: boolean;
}

export class Card extends Phaser.GameObjects.Container {
  private suit: CardSuit;
  private rank: CardRank;
  private value: number;
  private faceUp: boolean;
  private backImage!: Phaser.GameObjects.Image;
  private frontContainer!: Phaser.GameObjects.Container;
  private suitColor: number;
  private isSelected: boolean = false;
  private isEliminated: boolean = false;

  private static readonly CARD_WIDTH = 100;
  private static readonly CARD_HEIGHT = 140;
  private static readonly MARGIN = 8;

  constructor(scene: Phaser.Scene, x: number, y: number, data: CardData) {
    super(scene, x, y);
    
    this.suit = data.suit;
    this.rank = data.rank;
    this.value = data.value;
    this.faceUp = data.faceUp;
    
    // Set suit color (crimson for red suits, dark gray for black)
    this.suitColor = (data.suit === 'hearts' || data.suit === 'diamonds') ? 0xdc143c : 0x1a1a1a;
    
    this.setSize(Card.CARD_WIDTH, Card.CARD_HEIGHT);
    this.createBack();
    this.createFront();
    this.updateDisplay();
    
    // Add click interaction
    this.setInteractive(
      new Phaser.Geom.Rectangle(-Card.CARD_WIDTH/2, -Card.CARD_HEIGHT/2, Card.CARD_WIDTH, Card.CARD_HEIGHT),
      Phaser.Geom.Rectangle.Contains
    );
    this.on('pointerdown', this.onClick, this);
    
    scene.add.existing(this);
  }

  private createBack(): void {
    this.backImage = this.scene.add.image(0, 0, 'card-back');
    this.backImage.setDisplaySize(Card.CARD_WIDTH, Card.CARD_HEIGHT);
    this.add(this.backImage);
  }

  private createFront(): void {
    this.frontContainer = this.scene.add.container(0, 0);
    
    const w = Card.CARD_WIDTH;
    const h = Card.CARD_HEIGHT;
    const m = Card.MARGIN;
    
    // ===== Background =====
    const bg = this.scene.add.rectangle(0, 0, w, h, 0xfdf6ec);
    this.frontContainer.add(bg);
    
    // ===== Multi-layer Border =====
    // Layer 1: Outer dark border
    const border1 = this.scene.add.rectangle(0, 0, w, h);
    border1.setStrokeStyle(3, 0x8b5a2b);
    this.frontContainer.add(border1);
    
    // Layer 2: Main gold border
    const border2 = this.scene.add.rectangle(0, 0, w - 6, h - 6);
    border2.setStrokeStyle(3, 0xd4af37);
    this.frontContainer.add(border2);
    
    // Layer 3: Inner gold line
    const border3 = this.scene.add.rectangle(0, 0, w - 12, h - 12);
    border3.setStrokeStyle(1, 0xffd700);
    this.frontContainer.add(border3);
    
    // ===== Corner Decorations =====
    this.drawCornerDecoration(m + 6, m + 6);
    this.drawCornerDecoration(w - m - 6, m + 6);
    this.drawCornerDecoration(m + 6, h - m - 6);
    this.drawCornerDecoration(w - m - 6, h - m - 6);
    
    // ===== Rank and Suit =====
    const suitSymbol = this.getSuitSymbol();
    
    // Top-left: Rank
    const topLeftRank = this.scene.add.text(-w/2 + m + 8, -h/2 + m + 18, this.rank, {
      fontFamily: 'Arial',
      fontSize: '22px',
      color: '#' + this.suitColor.toString(16).padStart(6, '0'),
      fontStyle: 'bold',
    });
    this.frontContainer.add(topLeftRank);
    
    // Top-left: Suit
    const topLeftSuit = this.scene.add.text(-w/2 + m + 10, -h/2 + m + 42, suitSymbol, {
      fontFamily: 'Arial',
      fontSize: '18px',
      color: '#' + this.suitColor.toString(16).padStart(6, '0'),
    });
    this.frontContainer.add(topLeftSuit);
    
    // Center: Large suit symbol
    const centerSuit = this.scene.add.text(0, 8, suitSymbol, {
      fontFamily: 'Arial',
      fontSize: '56px',
      color: '#' + this.suitColor.toString(16).padStart(6, '0'),
    });
    centerSuit.setOrigin(0.5);
    this.frontContainer.add(centerSuit);
    
    // Bottom-right: Rotated rank and suit
    const bottomContainer = this.scene.add.container(0, 0);
    
    const bottomRank = this.scene.add.text(0, 0, this.rank, {
      fontFamily: 'Arial',
      fontSize: '22px',
      color: '#' + this.suitColor.toString(16).padStart(6, '0'),
      fontStyle: 'bold',
    });
    bottomContainer.add(bottomRank);
    
    const bottomSuit = this.scene.add.text(2, 22, suitSymbol, {
      fontFamily: 'Arial',
      fontSize: '18px',
      color: '#' + this.suitColor.toString(16).padStart(6, '0'),
    });
    bottomContainer.add(bottomSuit);
    
    bottomContainer.setRotation(Math.PI);
    bottomContainer.setPosition(w/2 - 16, h/2 - 16);
    this.frontContainer.add(bottomContainer);
  }

  private drawCornerDecoration(x: number, y: number): void {
    const size = 12;
    const graphics = this.scene.add.graphics();
    
    // Diamond shape
    graphics.fillStyle(0xffd700, 1);
    graphics.fillPoints([
      { x: x, y: y - size/2 },
      { x: x + size/2, y: y },
      { x: x, y: y + size/2 },
      { x: x - size/2, y: y },
    ]);
    
    // Outline
    graphics.lineStyle(1, 0xb8860b, 1);
    graphics.strokePoints([
      { x: x, y: y - size/2 },
      { x: x + size/2, y: y },
      { x: x, y: y + size/2 },
      { x: x - size/2, y: y },
      { x: x, y: y - size/2 },
    ]);
    
    this.frontContainer.add(graphics);
  }

  private getSuitSymbol(): string {
    const symbols: Record<CardSuit, string> = {
      hearts: '♥',
      diamonds: '♦',
      clubs: '♣',
      spades: '♠',
    };
    return symbols[this.suit];
  }

  private onClick(): void {
    if (this.isEliminated) return;
    
    this.scene.events.emit('card-clicked', this);
    
    if (!this.isSelected) {
      this.select();
    } else {
      this.deselect();
    }
  }

  select(): void {
    if (this.isSelected) return;
    this.isSelected = true;
    
    // Add green glow
    const glow = this.scene.add.rectangle(0, 0, Card.CARD_WIDTH - 4, Card.CARD_HEIGHT - 4);
    glow.setStrokeStyle(3, 0x00ff00, 0.8);
    this.frontContainer.add(glow);
  }

  deselect(): void {
    this.isSelected = false;
    this.frontContainer.removeAll(true);
    this.createFront();
  }

  eliminate(): void {
    this.isEliminated = true;
    
    this.scene.tweens.add({
      targets: this.frontContainer,
      alpha: 0,
      duration: 300,
      ease: 'Power2',
    });
  }

  flip(faceUp: boolean): void {
    this.faceUp = faceUp;
    this.updateDisplay();
  }

  setFaceUp(faceUp: boolean): void {
    this.faceUp = faceUp;
    this.updateDisplay();
  }

  private updateDisplay(): void {
    this.backImage.setVisible(!this.faceUp);
    this.frontContainer.setVisible(this.faceUp);
  }

  isFaceUp(): boolean {
    return this.faceUp;
  }

  getValue(): number {
    return this.value;
  }

  getSuit(): CardSuit {
    return this.suit;
  }

  getRank(): CardRank {
    return this.rank;
  }

  isEliminatedCard(): boolean {
    return this.isEliminated;
  }

  resetSelection(): void {
    this.isSelected = false;
    this.deselect();
  }

  getData(): CardData {
    return {
      suit: this.suit,
      rank: this.rank,
      value: this.value,
      faceUp: this.faceUp,
    };
  }
}
