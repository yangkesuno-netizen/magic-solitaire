import Phaser from 'phaser';
import { Card, CardSuit, CardRank } from './Card';

export class CardTestScene extends Phaser.Scene {
  constructor() {
    super({ key: 'CardTestScene' });
  }

  preload(): void {
    // Create card back texture programmatically
    const graphics = this.make.graphics();
    
    // Card back design (magic theme - purple with star)
    graphics.fillStyle(0x7c3aed);
    graphics.fillRect(0, 0, 100, 140);
    
    graphics.lineStyle(4, 0xa78bfa, 1);
    graphics.strokeRect(10, 10, 80, 120);
    
    // Star in center
    graphics.fillStyle(0xffffff, 0.3);
    this.drawStar(graphics, 50, 70, 5, 30, 15);
    
    graphics.generateTexture('card-back', 100, 140);
    graphics.destroy();
  }

  private drawStar(
    graphics: Phaser.GameObjects.Graphics,
    cx: number,
    cy: number,
    spikes: number,
    outerRadius: number,
    innerRadius: number
  ): void {
    let rot = Math.PI / 2 * 3;
    let x = cx;
    let y = cy;
    const step = Math.PI / spikes;

    graphics.beginPath();
    graphics.moveTo(cx, cy - outerRadius);
    
    for (let i = 0; i < spikes; i++) {
      x = cx + Math.cos(rot) * outerRadius;
      y = cy + Math.sin(rot) * outerRadius;
      graphics.lineTo(x, y);
      rot += step;

      x = cx + Math.cos(rot) * innerRadius;
      y = cy + Math.sin(rot) * innerRadius;
      graphics.lineTo(x, y);
      rot += step;
    }
    
    graphics.lineTo(cx, cy - outerRadius);
    graphics.closePath();
    graphics.fillPath();
  }

  create(): void {
    const { width, height } = this.scale;

    // Title
    this.add.text(width / 2, 50, 'Card Class Test', {
      fontFamily: 'Arial',
      fontSize: '32px',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Create test cards
    const cards: Card[] = [];
    const suits: CardSuit[] = ['hearts', 'diamonds', 'clubs', 'spades'];
    const ranks: CardRank[] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];

    // Display all suits in a row
    const startX = width / 2 - 150;
    const y = height / 2 - 50;

    suits.forEach((suit, index) => {
      const card = new Card(this, startX + index * 100, y, {
        suit,
        rank: 'A',
        value: 1,
        faceUp: true,
      });
      cards.push(card);
    });

    // Display all ranks in a column
    const x2 = width / 2 + 150;
    const startY2 = height / 2 - 200;

    for (let i = 0; i < 8; i++) {
      const card = new Card(this, x2, startY2 + i * 75, {
        suit: 'hearts',
        rank: ranks[i],
        value: i + 1,
        faceUp: true,
      });
      cards.push(card);
    }

    // Add some face-down cards
    for (let i = 0; i < 3; i++) {
      const card = new Card(this, startX + i * 100, height - 150, {
        suit: 'spades',
        rank: 'K',
        value: 13,
        faceUp: false,
      });
      cards.push(card);
    }

    // Instructions
    this.add.text(width / 2, height - 50, 'Click cards to test interaction', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#888888',
    }).setOrigin(0.5);

    // Listen for card click events
    this.events.on('card-clicked', (card: Card) => {
      console.log(`Card clicked: ${card.getRank()} of ${card.getSuit()}`);
      
      // Flip card on click if it's face down
      if (!card.isFaceUp()) {
        card.flip();
      }
    });

    // Back button
    const backButton = this.add.rectangle(80, 50, 120, 40, 0x0075ca)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => backButton.setFillStyle(0x005a9e))
      .on('pointerout', () => backButton.setFillStyle(0x0075ca))
      .on('pointerdown', () => {
        this.scene.start('MainScene');
      });

    this.add.text(80, 50, '← Back', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#ffffff',
    }).setOrigin(0.5);

    console.log('✅ CardTestScene created with', cards.length, 'test cards');
  }

  update(): void {
    // Game loop
  }
}
