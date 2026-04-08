import Phaser from 'phaser';
import './style.css';
import { CardTestScene } from './CardTestScene';

// Main Game Scene
class MainScene extends Phaser.Scene {
  constructor() {
    super({ key: 'MainScene' });
  }

  preload(): void {
    // Load assets will be added here
  }

  create(): void {
    const { width, height } = this.scale;

    // Title text
    this.add.text(width / 2, height / 3, 'Magic Solitaire', {
      fontFamily: 'Arial',
      fontSize: '48px',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Subtitle
    this.add.text(width / 2, height / 2, 'Tri-Peaks Challenge', {
      fontFamily: 'Arial',
      fontSize: '24px',
      color: '#a2eeef',
    }).setOrigin(0.5);

    // Start button
    const startButton = this.add.rectangle(width / 2, height * 0.65, 200, 60, 0x0075ca)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => startButton.setFillStyle(0x005a9e))
      .on('pointerout', () => startButton.setFillStyle(0x0075ca))
      .on('pointerdown', () => {
        console.log('Game started!');
      });

    this.add.text(width / 2, height * 0.65, 'START GAME', {
      fontFamily: 'Arial',
      fontSize: '20px',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Test Card button
    const testButton = this.add.rectangle(width / 2, height * 0.78, 200, 50, 0x7c3aed)
      .setInteractive({ useHandCursor: true })
      .on('pointerover', () => testButton.setFillStyle(0x5b21b6))
      .on('pointerout', () => testButton.setFillStyle(0x7c3aed))
      .on('pointerdown', () => {
        this.scene.start('CardTestScene');
      });

    this.add.text(width / 2, height * 0.78, 'TEST CARDS', {
      fontFamily: 'Arial',
      fontSize: '18px',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Instructions
    this.add.text(width / 2, height * 0.85, 'Click cards to eliminate them', {
      fontFamily: 'Arial',
      fontSize: '16px',
      color: '#888888',
    }).setOrigin(0.5);

    console.log('✅ MainScene created!');
  }

  update(): void {
    // Game loop
  }
}

// Game configuration
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: window.innerWidth,
  height: window.innerHeight,
  parent: 'app',
  backgroundColor: '#1a1a2e',
  scene: [MainScene, CardTestScene],
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

// Create game instance
const game = new Phaser.Game(config);

// Handle window resize
window.addEventListener('resize', () => {
  game.scale.resize(window.innerWidth, window.innerHeight);
});

console.log('🎮 Magic Solitaire initialized!');
