import Phaser from 'phaser';

/**
 * 游戏 UI 管理
 * 负责分数、剩余牌数、控制按钮等 UI 元素
 */
export class GameUI {
  private scene: Phaser.Scene;
  private scoreText!: Phaser.GameObjects.Text;
  private cardsRemainingText!: Phaser.GameObjects.Text;
  private score: number = 0;
  private restartButton!: Phaser.GameObjects.Container;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }

  /**
   * 创建所有 UI 元素
   */
  create(): void {
    this.createScoreDisplay();
    this.createCardsRemainingDisplay();
    this.createRestartButton();
  }

  /**
   * 创建分数显示
   */
  private createScoreDisplay(): void {
    // 分数标签
    this.scoreText = this.scene.add.text(20, 20, 'Score: 0', {
      fontFamily: 'Arial',
      fontSize: '24px',
      color: '#ffffff',
      fontStyle: 'bold',
    });

    // 背景面板
    this.scene.add.rectangle(
      this.scoreText.x - 10,
      this.scoreText.y + 15,
      this.scoreText.width + 20,
      this.scoreText.height + 10,
      0x000000,
      0.5
    ).setOrigin(0, 0);
  }

  /**
   * 创建剩余牌数显示
   */
  private createCardsRemainingDisplay(): void {
    const { width } = this.scene.scale;

    this.cardsRemainingText = this.scene.add.text(width - 20, 20, 'Cards: 24', {
      fontFamily: 'Arial',
      fontSize: '24px',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(1, 0);

    // 背景面板
    this.scene.add.rectangle(
      this.cardsRemainingText.x - this.cardsRemainingText.width - 10,
      this.cardsRemainingText.y + 15,
      this.cardsRemainingText.width + 20,
      this.cardsRemainingText.height + 10,
      0x000000,
      0.5
    ).setOrigin(0, 0);
  }

  /**
   * 创建重新开始按钮
   */
  private createRestartButton(): void {
    const { width, height } = this.scene.scale;

    // 按钮背景
    const buttonWidth = 150;
    const buttonHeight = 50;
    const buttonX = width - buttonWidth - 20;
    const buttonY = height - buttonHeight - 20;

    const buttonBg = this.scene.add.rectangle(
      buttonX + buttonWidth / 2,
      buttonY + buttonHeight / 2,
      buttonWidth,
      buttonHeight,
      0x0075ca
    ).setInteractive({ useHandCursor: true });

    // 按钮文字
    const buttonText = this.scene.add.text(
      buttonX + buttonWidth / 2,
      buttonY + buttonHeight / 2,
      'RESTART',
      {
        fontFamily: 'Arial',
        fontSize: '18px',
        color: '#ffffff',
        fontStyle: 'bold',
      }
    ).setOrigin(0.5);

    // 悬停效果
    buttonBg.on('pointerover', () => {
      buttonBg.setFillStyle(0x005a9e);
    });

    buttonBg.on('pointerout', () => {
      buttonBg.setFillStyle(0x0075ca);
    });

    // 点击效果
    buttonBg.on('pointerdown', () => {
      buttonBg.setFillStyle(0x004a8e);
    });

    buttonBg.on('pointerup', () => {
      buttonBg.setFillStyle(0x005a9e);
    });

    // 点击事件 - 重新开始游戏
    buttonBg.on('pointerdown', () => {
      this.scene.scene.restart();
    });

    this.restartButton = this.scene.add.container(0, 0, [buttonBg, buttonText]);
  }

  /**
   * 更新分数
   */
  updateScore(points: number): void {
    this.score = points;
    this.scoreText.setText(`Score: ${this.score}`);
  }

  /**
   * 增加分数
   */
  addScore(points: number): void {
    this.score += points;
    this.updateScore(this.score);
  }

  /**
   * 重置分数
   */
  resetScore(): void {
    this.score = 0;
    this.updateScore(0);
  }

  /**
   * 获取当前分数
   */
  getScore(): number {
    return this.score;
  }

  /**
   * 更新剩余牌数
   */
  updateCardsRemaining(count: number): void {
    this.cardsRemainingText.setText(`Cards: ${count}`);
  }

  /**
   * 显示胜利界面
   */
  showVictory(): void {
    const { width, height } = this.scene.scale;

    // 半透明背景
    this.scene.add.rectangle(
      width / 2,
      height / 2,
      width,
      height,
      0x000000,
      0.7
    );

    // 胜利文字
    this.scene.add.text(width / 2, height / 2 - 50, 'VICTORY!', {
      fontFamily: 'Arial',
      fontSize: '64px',
      color: '#ffd700',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // 最终分数
    this.scene.add.text(width / 2, height / 2 + 20, `Final Score: ${this.score}`, {
      fontFamily: 'Arial',
      fontSize: '32px',
      color: '#ffffff',
    }).setOrigin(0.5);

    // 创建庆祝粒子（简单版本：多个小圆点）
    this.createConfetti(width, height);

    // 3 秒后显示重新开始提示
    this.scene.time.delayedCall(3000, () => {
      this.scene.add.text(width / 2, height / 2 + 100, 'Click RESTART to play again', {
        fontFamily: 'Arial',
        fontSize: '20px',
        color: '#a2eeef',
      }).setOrigin(0.5);
    });
  }

  /**
   * 创建庆祝彩带效果
   */
  private createConfetti(width: number, height: number): void {
    const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff];

    for (let i = 0; i < 50; i++) {
      const x = Phaser.Math.Between(0, width);
      const y = Phaser.Math.Between(-50, height / 2);
      const color = Phaser.Utils.Array.GetRandom(colors);
      const size = Phaser.Math.Between(5, 15);

      const confetti = this.scene.add.circle(x, y, size, color);

      // 下落动画
      this.scene.tweens.add({
        targets: confetti,
        y: height + 50,
        duration: Phaser.Math.Between(2000, 4000),
        ease: 'Linear',
        delay: i * 50,
      });

      // 旋转动画
      this.scene.tweens.add({
        targets: confetti,
        angle: 360,
        duration: Phaser.Math.Between(1000, 2000),
        ease: 'Linear',
        repeat: -1,
      });
    }
  }

  /**
   * 显示游戏结束（无牌可出）
   */
  showGameOver(): void {
    const { width, height } = this.scene.scale;

    // 半透明背景
    this.scene.add.rectangle(
      width / 2,
      height / 2,
      width,
      height,
      0x000000,
      0.7
    );

    // 游戏结束文字
    this.scene.add.text(width / 2, height / 2 - 50, 'GAME OVER', {
      fontFamily: 'Arial',
      fontSize: '64px',
      color: '#ff4444',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // 最终分数
    this.scene.add.text(width / 2, height / 2 + 20, `Score: ${this.score}`, {
      fontFamily: 'Arial',
      fontSize: '32px',
      color: '#ffffff',
    }).setOrigin(0.5);

    // 提示文字
    this.scene.time.delayedCall(2000, () => {
      this.scene.add.text(width / 2, height / 2 + 100, 'Click RESTART to try again', {
        fontFamily: 'Arial',
        fontSize: '20px',
        color: '#a2eeef',
      }).setOrigin(0.5);
    });
  }

  /**
   * 响应窗口大小变化
   */
  resize(width: number, height: number): void {
    // 更新分数位置
    this.scoreText.setPosition(20, 20);

    // 更新剩余牌数位置
    this.cardsRemainingText.setPosition(width - 20, 20);

    // 更新重新开始按钮位置
    if (this.restartButton) {
      const buttonWidth = 150;
      const buttonHeight = 50;
      this.restartButton.setPosition(width - buttonWidth - 20, height - buttonHeight - 20);
    }
  }
}
