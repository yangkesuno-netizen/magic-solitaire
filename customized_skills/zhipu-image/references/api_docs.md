# Zhipu AI CogView API Documentation

## Overview

CogView is Zhipu AI's text-to-image generation model, offering high-quality image generation with a generous free tier.

## Authentication

All API requests require a Bearer token in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

Get your free API key at: https://open.bigmodel.cn/

## Base URL

```
https://open.bigmodel.cn/api/paas/v4
```

## Image Generation Endpoint

### POST /images/generations

Generate images from text prompts.

#### Request Body

```json
{
  "model": "cogview-3",
  "prompt": "A beautiful sunset over mountains",
  "n": 1,
  "size": "1024x1024",
  "quality": "standard",
  "style": "digital_art"
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | Yes | Model name: "cogview-3" |
| prompt | string | Yes | Image description (max 500 chars) |
| n | integer | No | Number of images (1-4, default: 1) |
| size | string | No | Image dimensions (default: "1024x1024") |
| quality | string | No | "standard" or "high" (default: "standard") |
| style | string | No | Style preset (see below) |

#### Size Options

| Size | Aspect Ratio | Best For |
|------|--------------|----------|
| 1024x1024 | 1:1 | Square images, avatars |
| 768x1344 | 9:16 | Mobile wallpapers, portraits |
| 864x1152 | 3:4 | Portraits, vertical content |
| 1344x768 | 16:9 | Desktop wallpapers, landscapes |
| 1152x864 | 4:3 | Presentations, standard photos |

#### Style Options

| Style | Description |
|-------|-------------|
| "" (empty) | Default balanced style |
| "anime" | Anime/manga style |
| "digital_art" | Digital illustration |
| "oil_painting" | Oil painting effect |
| "watercolor" | Watercolor painting |
| "sketch" | Pencil/charcoal sketch |
| "3d" | 3D rendered look |

#### Response

```json
{
  "created": 1699999999,
  "data": [
    {
      "url": "https://...",
      "revised_prompt": "Enhanced version of the prompt"
    }
  ]
}
```

## Python Integration

### Basic Usage

```python
import os
from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.environ.get("ZHIPU_API_KEY"))

response = client.images.generations(
    model="cogview-3",
    prompt="一只可爱的橘猫在窗台上晒太阳",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
```

### With Error Handling

```python
from zhipuai import ZhipuAI
from zhipuai.core._errors import APIStatusError

try:
    client = ZhipuAI()
    response = client.images.generations(
        model="cogview-3",
        prompt="山水画",
        size="1024x1024"
    )
    print(f"Image URL: {response.data[0].url}")
except APIStatusError as e:
    print(f"API Error: {e.message}")
except Exception as e:
    print(f"Error: {e}")
```

## Rate Limits & Quotas

| Tier | Daily Limit | Concurrent |
|------|-------------|------------|
| Free | 100 images | 2 |
| Standard | 1000 images | 5 |
| Premium | 5000 images | 10 |

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Unauthorized | Check API key |
| 429 | Rate limited | Wait before retrying |
| 400 | Bad request | Check prompt length and parameters |
| 500 | Server error | Retry after a few seconds |

## Best Practices

### Prompt Engineering

1. **Be specific**: "A red sports car" > "A car"
2. **Add style descriptors**: "in the style of Studio Ghibli"
3. **Include lighting**: "golden hour lighting", "soft studio lighting"
4. **Specify composition**: "close-up portrait", "wide landscape shot"

### Example Prompts

```
# Portrait
"Professional headshot of a young woman, soft studio lighting, neutral background, high quality"

# Landscape
"Majestic mountain range at sunrise, golden light, misty valleys, 8k resolution"

# Product
"Sleek smartphone on marble surface, product photography, soft shadows, minimalist"

# Anime
"Anime girl with blue hair, cherry blossom background, detailed eyes, studio ghibli style"

# Chinese Style
"中国传统山水画，水墨风格，云雾缭绕的山峰，松树，留白意境"
```

## SDK Installation

```bash
pip install zhipuai
```

## Additional Resources

- Official Docs: https://open.bigmodel.cn/dev/howuse/cogview
- API Reference: https://open.bigmodel.cn/dev/api#cogview
- Pricing: https://open.bigmodel.cn/pricing
