---
name: zhipu-image
description: Generate images using Zhipu AI (智谱AI) CogView API for free. Use when users want to create, generate, or edit images using Chinese AI image generation service. Supports text-to-image generation with multiple styles and aspect ratios. Free tier available with generous limits. Trigger words include "智谱", "zhipu", "CogView", "生成图片", "AI绘画", "画一张", "生成图像".
---

# Zhipu AI Image Generation

Generate high-quality images using Zhipu AI's CogView model for free.

## Quick Start

### 1. Get Free API Key

Visit https://open.bigmodel.cn/ and register an account to get free API credits.

### 2. Set API Key

```bash
set ZHIPU_API_KEY=your_api_key_here
```

### 3. Generate Image

```python
python scripts/generate_image.py --prompt "一只可爱的猫咪在草地上玩耍" --output cat.png
```

## Usage Examples

### Basic Generation
```python
python scripts/generate_image.py --prompt "山水画，中国传统风格，水墨画" --output landscape.png
```

### With Style and Size
```python
python scripts/generate_image.py --prompt "未来城市，赛博朋克风格" --style digital_art --size 1024x1024 --output cyberpunk.png
```

### Batch Generation
```python
python scripts/generate_image.py --prompt "樱花盛开的日本庭院" --count 4 --output sakura_{i}.png
```

## Available Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `--prompt` | Image description (required) | - | Any text |
| `--style` | Image style | `default` | default, anime, digital_art, oil_painting, watercolor, sketch, 3d |
| `--size` | Image dimensions | `1024x1024` | 1024x1024, 768x1344, 864x1152, 1344x768, 1152x864 |
| `--count` | Number of images | `1` | 1-4 |
| `--output` | Output filename | `generated.png` | Any path |
| `--quality` | Image quality | `standard` | standard, high |

## API Reference

See [references/api_docs.md](references/api_docs.md) for complete API documentation and advanced features.

## Rate Limits

- Free tier: 100 images/day
- Generation time: ~5-10 seconds per image
- Concurrent requests: 2 max

## Error Handling

Common errors and solutions:

| Error | Solution |
|-------|----------|
| API key invalid | Check ZHIPU_API_KEY environment variable |
| Rate limit exceeded | Wait and retry, or upgrade plan |
| Prompt too long | Limit to 500 characters |
| Content policy violation | Modify prompt to comply with guidelines |
