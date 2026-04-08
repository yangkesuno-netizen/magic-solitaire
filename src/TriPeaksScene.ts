import Phaser from 'phaser';
import { Card } from './Card';
import { Pyramid } from './Pyramid';
import { Stock } from './Stock';
import { GameUI } from './GameUI';

/**
 * Tri-Peaks 游戏主场景
 * 实现完整的 Tri-Peaks Solitaire 游戏流程
 */
export class TriPeaksScene extends Phaser.Scene {
  private pyramid!: Pyramid;
  private stock!: Stock;
  private gameUI!: GameUI;
  private cardsEliminated: number = 0;
  private winText!: Phaser.GameObjects.Text;
  private gameOverText!: Phaser.GameObjects.Text;
  private isGameOver: boolean = false;

  constructor() {
    super({ key: 'TriPeaksScene' });
  }

  create(): void {
    // 创建牌组
    const deck = this.createDeck();
    
    // 洗牌
    this.shuffleDeck(deck);

    // 发 28 张牌到金字塔
    const pyramidCards = deck.splice(0, 28);
    
    // 剩余 24 张牌到发牌堆
    const stockCards = deck;

    // 创建金字塔 (屏幕中央偏上)
    this.pyramid = new Pyramid(this, 400, 200);
    this.pyramid.create(pyramidCards);

    // 创建发牌堆 (屏幕左下)
    this.stock = new Stock(this, 150, 450);
    this.stock.initialize(stockCards);

    // 创建 UI
    this.createUI();

    // 设置发牌堆点击事件
    this.setupStockClick();

    // 设置金字塔卡牌点击事件
    this.setupPyramidClick();

    console.log('🎮 Tri-Peaks Scene created!');
  }

  /**
   * 创建一副完整的 52 张牌
   */
  private createDeck(): Card[] {
    const suits: Array<'hearts' | 'diamonds' | 'clubs' | 'spades'> = 
      ['hearts', 'diamonds', 'clubs', 'spades'];
    const ranks: Array<'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K'> = 
      ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
    const values: Record<string, number> = {
      'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
      'J': 11, 'Q': 12, 'K': 13
    };

    const deck: Card[] = [];

    for (const suit of suits) {
      for (const rank of ranks) {
        const card = new Card(this, 0, 0, {
          suit,
          rank,
          value: values[rank],
          faceUp: false
        });
        deck.push(card);
      }
    }

    return deck;
  }

  /**
   * 洗牌 (Fisher-Yates 算法)
   */
  private shuffleDeck(deck: Card[]): void {
    for (let i = deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }
  }

  /**
   * 创建 UI
   */
  private createUI(): void {
    // 使用 GameUI 管理类
    this.gameUI = new GameUI(this);
    this.gameUI.create();

    // 胜利文本 (初始隐藏)
    this.winText = this.add.text(400, 300, '🎉 YOU WIN! 🎉', {
      fontSize: '48px',
      fontFamily: 'Arial',
      color: '#ffd700',
      stroke: '#000000',
      strokeThickness: 6
    });
    this.winText.setOrigin(0.5);
    this.winText.setVisible(false);

    // 游戏结束文本 (初始隐藏)
    this.gameOverText = this.add.text(400, 300, 'GAME OVER', {
      fontSize: '48px',
      fontFamily: 'Arial',
      color: '#ff4444',
      stroke: '#000000',
      strokeThickness: 6
    });
    this.gameOverText.setOrigin(0.5);
    this.gameOverText.setVisible(false);

    // 重新开始按钮 (初始隐藏)
    const restartButton = this.add.text(400, 380, 'Play Again', {
      fontSize: '24px',
      fontFamily: 'Arial',
      color: '#ffffff',
      backgroundColor: '#4a4a6a',
      padding: { x: 20, y: 10 }
    });
    restartButton.setOrigin(0.5);
    restartButton.setVisible(false);
    restartButton.setInteractive({ useHandCursor: true });
    restartButton.on('pointerdown', () => {
      this.scene.restart();
    });

    // 胜利时显示
    this.events.on('win', () => {
      this.winText.setVisible(true);
      restartButton.setVisible(true);
      this.gameUI.showVictory();
    });

    // 游戏结束时显示
    this.events.on('gameOver', () => {
      this.gameOverText.setVisible(true);
      restartButton.setVisible(true);
      this.gameUI.showGameOver();
    });
  }

  /**
   * 设置发牌堆点击事件
   */
  private setupStockClick(): void {
    // 创建一个不可见的点击区域
    const stockClickZone = this.add.zone(150, 450, 100, 140)
      .setOrigin(0)
      .setInteractive({ useHandCursor: true });

    stockClickZone.on('pointerdown', () => {
      this.dealCard();
    });
  }

  /**
   * 设置金字塔卡牌点击事件
   */
  private setupPyramidClick(): void {
    const allCards = this.pyramid.getAllCards();
    
    allCards.forEach(card => {
      // 创建一个容器用于点击检测
      const clickZone = this.add.zone(card.x, card.y, 100, 140)
        .setOrigin(0.5)
        .setInteractive({ useHandCursor: true });

      clickZone.on('pointerdown', () => {
        this.onPyramidCardClick(card);
      });
    });
  }

  /**
   * 发牌
   */
  private dealCard(): void {
    const card = this.stock.dealCard();
    if (card) {
      console.log('🃏 Dealt card:', card.getRank(), card.getSuit());
    }
  }

  /**
   * 金字塔卡牌点击处理
   */
  private onPyramidCardClick(card: Card): void {
    // 如果牌已被消除，忽略
    if (card.isEliminatedCard()) {
      return;
    }

    // 如果牌未暴露，忽略
    if (!this.pyramid.isCardExposed(card)) {
      // 可以添加视觉反馈：闪烁红色表示不可点击
      console.log('❌ Card not exposed');
      return;
    }

    // 获取废牌堆顶牌
    const wasteCard = this.stock.getTopWasteCard();

    if (!wasteCard) {
      console.log('⚠️ No waste card to match');
      return;
    }

    // 检查是否可以消除
    if (this.canEliminate(wasteCard, card)) {
      this.eliminateCards(wasteCard, card);
    } else {
      console.log('❌ Cannot eliminate');
    }
  }

  /**
   * 检查是否可以消除
   */
  private canEliminate(wasteCard: Card, pyramidCard: Card): boolean {
    // 检查牌是否朝上
    if (!wasteCard.isFaceUp() || !pyramidCard.isFaceUp()) {
      return false;
    }

    // 检查金字塔牌是否暴露
    if (!this.pyramid.isCardExposed(pyramidCard)) {
      return false;
    }

    // 检查值差是否为 ±1
    const diff = Math.abs(wasteCard.getValue() - pyramidCard.getValue());
    return diff === 1;
  }

  /**
   * 消除牌
   */
  private eliminateCards(wasteCard: Card, pyramidCard: Card): void {
    console.log('✅ Eliminating:', wasteCard.getRank(), pyramidCard.getRank());

    // 消除金字塔牌
    pyramidCard.eliminate();
    this.cardsEliminated++;

    // 从废牌堆移除
    this.stock.removeTopWasteCard();

    // 更新分数 (10 分/牌)
    this.gameUI.addScore(10);

    // 更新剩余牌数显示
    this.gameUI.updateCardsRemaining(this.stock.getCardsRemaining());

    // 检查是否胜利
    if (this.pyramid.checkWin()) {
      this.handleWin();
    } else {
      // 检查是否游戏结束（无牌可出）
      this.checkGameOver();
    }
  }

  /**
   * 处理胜利
   */
  private handleWin(): void {
    console.log('🎉 YOU WIN!');
    this.events.emit('win');
  }

  /**
   * 检查游戏结束（无牌可出）
   */
  private checkGameOver(): void {
    if (this.isGameOver) return;

    // 获取废牌堆顶牌
    const wasteCard = this.stock.getTopWasteCard();
    if (!wasteCard || !wasteCard.isFaceUp()) {
      // 如果没有废牌，检查是否能发牌
      if (!this.stock.canDeal()) {
        this.isGameOver = true;
        this.events.emit('gameOver');
      }
      return;
    }

    // 检查是否有可消除的金字塔牌
    const allCards = this.pyramid.getAllCards();
    let hasValidMove = false;

    for (const card of allCards) {
      if (!card.isEliminatedCard() && this.pyramid.isCardExposed(card)) {
        if (Math.abs(wasteCard.getValue() - card.getValue()) === 1) {
          hasValidMove = true;
          break;
        }
      }
    }

    // 如果没有有效移动且无法发牌
    if (!hasValidMove && !this.stock.canDeal()) {
      this.isGameOver = true;
      this.events.emit('gameOver');
    }
  }

  /**
   * 获取当前分数
   */
  getScore(): number {
    return this.gameUI.getScore();
  }

  /**
   * 获取已消除牌数
   */
  getCardsEliminated(): number {
    return this.cardsEliminated;
  }

  /**
   * 窗口大小变化处理
   */
  resize(width: number, height: number): void {
    this.gameUI?.resize(width, height);
  }
}
