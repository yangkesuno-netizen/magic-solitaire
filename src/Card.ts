import Phaser from 'phaser';

export type CardSuit = 'hearts' | 'diamonds' | 'clubs' | 'spades';
export type CardRank = 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K';

export interface CardData {
  suit: CardSuit;
  rank: CardRank;
  value: number; // For Tri-Peaks: A=1, 2-10=2-10, J=11, Q=12, K=13
  faceUp: boolean;
}

export class Card extends Phaser.GameObjects.Container {
  private suit: CardSuit;
  private rank: CardRank;
  private value: number;
  private faceUp: boolean;
  private backTexture!: Phaser.GameObjects.Image;
  private frontContainer!: Phaser.GameObjects.Container;
  private suitColor: number;
  private isSelected: boolean = false;
  private isEliminated: boolean = false;

  constructor(scene: Phaser.Scene, x: number, y: number, data: CardData) {
    super(scene, x, y);
    
    this.suit = data.suit;
    this.rank = data.rank;
    this.value = data.value;
    this.faceUp = data.faceUp;
    
    // Set suit color
    this.suitColor = (data.suit === 'hearts' || data.suit === 'diamonds') ? 0xff0000 : 0x000000;
    
    this.setSize(100, 140);
    this.createBack();
    this.createFront();
    this.updateDisplay();
    
    // Add click interaction
    this.setInteractive(new Phaser.Geom.Rectangle(-50, -70, 100, 140), Phaser.Geom.Rectangle.Contains);
    this.on('pointerdown', this.onClick, this);
    
    scene.add.existing(this);
  }

  private createBack(): void {
    // Card back
    this.backTexture = this.scene.add.image(0, 0, 'card-back');
    this.backTexture.setDisplaySize(100, 140);
    this.add(this.backTexture);
  }

  private createFront(): void {
    this.frontContainer = this.scene.add.container(0, 0);
    
    // Use AI-generated card front image
    const textureKey = `card-${this.rank}-${this.suit}`;
    
    // Check if texture exists
    if (this.scene.textures.exists(textureKey)) {
      const cardImage = this.scene.add.image(0, 0, textureKey);
      cardImage.setDisplaySize(100, 140);
      this.frontContainer.add(cardImage);
    } else {
      // Fallback to graphics rendering
      // Card background (white rounded rectangle)
      const bg = this.scene.add.rectangle(0, 0, 100, 140, 0xffffff);
      bg.setStrokeStyle(2, 0x000000);
      this.frontContainer.add(bg);
      
      // Top-left rank and suit
      const topLeftRank = this.scene.add.text(-40, -60, this.rank, {
        fontFamily: 'Arial',
        fontSize: '24px',
        color: '#' + this.suitColor.toString(16).padStart(6, '0'),
        fontStyle: 'bold',
      });
      this.frontContainer.add(topLeftRank);
      
      const topLeftSuit = this.scene.add.text(-40, -40, this.getSuitSymbol(), {
        fontFamily: 'Arial',
        fontSize: '20px',
        color: '#' + this.suitColor.toString(16).padStart(6, '0'),
      });
      this.frontContainer.add(topLeftSuit);
      
      // Center suit (large)
      const centerSuit = this.scene.add.text(0, 0, this.getSuitSymbol(), {
        fontFamily: 'Arial',
        fontSize: '48px',
        color: '#' + this.suitColor.toString(16).padStart(6, '0'),
      });
      centerSuit.setOrigin(0.5);
      this.frontContainer.add(centerSuit);
      
      // Bottom-right rank and suit (rotated 180 degrees)
      const bottomRightRank = this.scene.add.text(40, 60, this.rank, {
        fontFamily: 'Arial',
        fontSize: '24px',
        color: '#' + this.suitColor.toString(16).padStart(6, '0'),
        fontStyle: 'bold',
      });
      bottomRightRank.setOrigin(0.5);
      bottomRightRank.setRotation(Math.PI);
      this.frontContainer.add(bottomRightRank);
      
      const bottomRightSuit = this.scene.add.text(40, 40, this.getSuitSymbol(), {
        fontFamily: 'Arial',
        fontSize: '20px',
        color: '#' + this.suitColor.toString(16).padStart(6, '0'),
      });
      bottomRightSuit.setOrigin(0.5);
      bottomRightSuit.setRotation(Math.PI);
      this.frontContainer.add(bottomRightSuit);
    }
    
    this.add(this.frontContainer);
  }

  private getSuitSymbol(): string {
    switch (this.suit) {
      case 'hearts': return '♥';
      case 'diamonds': return '♦';
      case 'clubs': return '♣';
      case 'spades': return '♠';
    }
  }

  private updateDisplay(): void {
    this.backTexture.setVisible(!this.faceUp);
    this.frontContainer.setVisible(this.faceUp);
  }

  private onClick(): void {
    if (!this.faceUp || this.isEliminated) return;
    
    // Emit event for game logic to handle
    this.scene.events.emit('card-clicked', this);
    
    // Visual feedback
    if (!this.isSelected) {
      this.frontContainer.setScale(1.05);
      this.isSelected = true;
    } else {
      this.frontContainer.setScale(1);
      this.isSelected = false;
    }
  }

  public flip(): void {
    this.faceUp = !this.faceUp;
    this.updateDisplay();
  }

  public setFaceUp(faceUp: boolean): void {
    this.faceUp = faceUp;
    this.updateDisplay();
  }

  public isFaceUp(): boolean {
    return this.faceUp;
  }

  public getSuit(): CardSuit {
    return this.suit;
  }

  public getRank(): CardRank {
    return this.rank;
  }

  public getValue(): number {
    return this.value;
  }

  public eliminate(): void {
    this.isEliminated = true;
    this.scene.tweens.add({
      targets: this,
      alpha: 0,
      scale: 1.2,
      duration: 300,
      onComplete: () => {
        this.setVisible(false);
      },
    });
  }

  public isEliminatedCard(): boolean {
    return this.isEliminated;
  }

  public resetSelection(): void {
    this.isSelected = false;
    this.frontContainer.setScale(1);
  }

  // Check if this card can eliminate another card (difference of 1)
  public canEliminate(other: Card): boolean {
    if (!this.faceUp || !other.isFaceUp() || other.isEliminatedCard()) {
      return false;
    }
    return Math.abs(this.value - other.getValue()) === 1;
  }
}
