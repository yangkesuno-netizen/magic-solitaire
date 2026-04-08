// Mock Phaser for testing
export default {
  Scene: class Scene {
    events = { emit: () => {}, on: () => {} };
    add = {
      image: () => ({ setDisplaySize: () => {} }),
      rectangle: () => ({ setStrokeStyle: () => {} }),
      text: () => ({ setOrigin: () => ({ setRotation: () => {} }) }),
      container: () => ({ add: () => {}, setScale: () => {}, setVisible: () => {} })
    };
    tweens = { add: () => {} };
  },
  GameObjects: {
    Container: class Container {
      add() {}
      setScale() {}
      setVisible() {}
      setSize() {}
      setX() {}
      setY() {}
      setPosition() {}
      setDepth() {}
      setAlpha() {}
      setRotation() {}
      setAngle() {}
      setScrollFactor() {}
      setSize() {}
      destroy() {}
    },
    Image: class Image {
      setDisplaySize() {}
      setSize() {}
      setX() {}
      setY() {}
    },
    Text: class Text {
      setOrigin() { return { setRotation: () => {} }; }
      setSize() {}
    },
    Rectangle: class Rectangle {
      setStrokeStyle() {}
      setSize() {}
    }
  },
  Tweens: {
    Tween: class Tween {}
  }
};
