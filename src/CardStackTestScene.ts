import Phaser from 'phaser';
import { Card, CardSuit, CardRank } from './Card';
import { CardStack } from './CardStack';

export class CardStackTestScene extends Phaser.Scene {
  constructor() {
    super({ key: 'CardStackTestScene' });
  }

  preload(): void {
    // Create card back texture
    const graphics = this.make.graphics();
    
    graphics.fillStyle(0x7c3aed);
    graphics.fillRect(0, 0, 100, 140);
    
    graphics.lineStyle(4, 0xa78bfa, 1);
    graphics.strokeRect(10, 10, 80, 120);
    
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
    this.add.text(width / 2, 40, 'CardStack Class Test', {
      fontFamily: 'Arial',
      fontSize: '32px',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Create CardStack instances
    const deckStack = new CardStack(this, {
      x: 150,
      y: height / 2,
      maxCards: -1,
      faceUp: false,
      spread: 5,
      clickable: true,
    });

    const discardStack = new CardStack(this, {
      x: width - 150,
      y: height / 2,
      maxCards: -1,
      faceUp: true,
      spread: 10,
      clickable: true,
    });

    // Create a deck of cards
    const suits: CardSuit[] = ['hearts', 'diamonds', 'clubs', 'spades'];
    const ranks: CardRank[] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
    const values: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

    let cardIndex = 0;
    suits.forEach((suit) => {
      ranks.forEach((rank, rankIdx) => {
        const card = new Card(this, 150, height / 2, {
          suit,
          rank,
          value: values[rankIdx],
          faceUp: false,
        });
        deckStack.addCard(card);
        cardIndex++;
      });
    });

    // Labels
    this.add.text(150, height / 2 + 200, 'Deck (52 cards)', {
      fontFamily: 'Arial',
      fontSize: '18px',
      color: '#a2eeef',
    }).setOrigin(0.5);

    this.add.text(width - 150, height / 2 + 200, 'Discard Pile', {
      fontFamily: 'Arial',
      fontSize: '18px',
      color: '#a2eeef',
    }).setOrigin(0.5);

    // Instructions
    this.add.text(width / 2, height - 80, 'Click deck to draw | Click discard to remove', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#888888',
    }).setOrigin(0.5);

    // Card count display
    const deckCountText = this.add.text(150, height / 2 - 200, 'Cards: 52', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#ffffff',
    }).setOrigin(0.5);

    const discardCountText = this.add.text(width - 150, height / 2 - 200, 'Cards: 0', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#ffffff',
    }).setOrigin(0.5);

    // Make deck stack clickable
    deckStack.setInteractive(new Phaser.Geom.Rectangle(-50, -70, 100, 140), Phaser.Geom.Rectangle.Contains);
    deckStack.on('pointerdown', () => {
      const card = deckStack.removeTopCard();
      if (card) {
        card.setFaceUp(true);
        discardStack.addCard(card);
        
        // Update counts
        deckCountText.setText(`Cards: ${deckStack.getCardCount()}`);
        discardCountText.setText(`Cards: ${discardStack.getCardCount()}`);
        
        console.log(`Drew card: ${card.getRank()} of ${card.getSuit()}`);
      }
    });

    // Make discard stack clickable
    discardStack.setInteractive(new Phaser.Geom.Rectangle(-50, -70, 100, 140), Phaser.Geom.Rectangle.Contains);
    discardStack.on('pointerdown', () => {
      const card = discardStack.removeTopCard();
      if (card) {
        card.destroy();
        
        // Update counts
        deckCountText.setText(`Cards: ${deckStack.getCardCount()}`);
        discardCountText.setText(`Cards: ${discardStack.getCardCount()}`);
        
        console.log('Removed card from discard');
      }
    });

    // Shuffle button
    const shuffleButton = this.add.rectangle(width / 2, height - 140, 150, 40, 0x0075ca)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => shuffleButton.setFillStyle(0x005a9e))
      .on('pointerout', () => shuffleButton.setFillStyle(0x0075ca))
      .on('pointerdown', () => {
        // Return all discard cards to deck
        const discardCards = discardStack.getCards();
        discardCards.forEach(card => {
          discardStack.removeCard(card);
          card.setFaceUp(false);
          deckStack.addCard(card);
        });
        
        // Shuffle deck
        deckStack.shuffle();
        
        // Update counts
        deckCountText.setText(`Cards: ${deckStack.getCardCount()}`);
        discardCountText.setText(`Cards: ${discardStack.getCardCount()}`);
        
        console.log('Deck shuffled!');
      });

    this.add.text(width / 2, height - 140, 'Shuffle Deck', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#ffffff',
    }).setOrigin(0.5);

    // Back button
    const backButton = this.add.rectangle(80, 40, 120, 40, 0x0075ca)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => backButton.setFillStyle(0x005a9e))
      .on('pointerout', () => backButton.setFillStyle(0x0075ca))
      .on('pointerdown', () => {
        this.scene.start('MainScene');
      });

    this.add.text(80, 40, '← Back', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#ffffff',
    }).setOrigin(0.5);

    console.log('✅ CardStackTestScene created');
    console.log(`   Deck: ${deckStack.getCardCount()} cards`);
    console.log(`   Discard: ${discardStack.getCardCount()} cards`);
  }

  update(): void {
    // Game loop
  }
}
