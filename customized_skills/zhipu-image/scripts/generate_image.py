#!/usr/bin/env python3
"""
Zhipu AI Image Generation Script
Generate images using CogView API for free
"""

import argparse
import os
import sys
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path


def generate_image(prompt: str, style: str = "default", size: str = "1024x1024", 
                   count: int = 1, quality: str = "standard") -> list:
    """
    Generate images using Zhipu AI CogView API
    
    Args:
        prompt: Image description
        style: Image style (default, anime, digital_art, oil_painting, watercolor, sketch, 3d)
        size: Image size (1024x1024, 768x1344, 864x1152, 1344x768, 1152x864)
        count: Number of images (1-4)
        quality: Image quality (standard, high)
    
    Returns:
        List of base64 encoded image strings
    """
    api_key = os.environ.get('ZHIPU_API_KEY')
    if not api_key:
        raise ValueError("ZHIPU_API_KEY environment variable not set. Get free key at https://open.bigmodel.cn/")
    
    # Map style names to API values
    style_map = {
        "default": "",
        "anime": "anime",
        "digital_art": "digital_art",
        "oil_painting": "oil_painting",
        "watercolor": "watercolor",
        "sketch": "sketch",
        "3d": "3d"
    }
    
    # Validate size
    valid_sizes = ["1024x1024", "768x1344", "864x1152", "1344x768", "1152x864"]
    if size not in valid_sizes:
        raise ValueError(f"Invalid size {size}. Must be one of: {', '.join(valid_sizes)}")
    
    # Build request
    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"
    
    payload = {
        "model": "cogview-3",
        "prompt": prompt,
        "n": min(max(count, 1), 4),  # Clamp between 1-4
        "size": size,
        "quality": quality
    }
    
    if style and style != "default":
        payload["style"] = style_map.get(style, "")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Make request
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if 'data' in result:
                return [item['url'] for item in result['data']]
            else:
                raise Exception(f"API error: {result.get('error', 'Unknown error')}")
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise Exception(f"HTTP Error {e.code}: {error_body}")
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")


def download_image(url: str, output_path: str) -> str:
    """Download image from URL and save to file"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=60) as response:
            image_data = response.read()
            
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(image_data)
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Failed to download image: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='Generate images using Zhipu AI CogView')
    parser.add_argument('--prompt', '-p', required=True, help='Image description prompt')
    parser.add_argument('--style', '-s', default='default', 
                       choices=['default', 'anime', 'digital_art', 'oil_painting', 'watercolor', 'sketch', '3d'],
                       help='Image style')
    parser.add_argument('--size', default='1024x1024',
                       choices=['1024x1024', '768x1344', '864x1152', '1344x768', '1152x864'],
                       help='Image size')
    parser.add_argument('--count', '-n', type=int, default=1, help='Number of images (1-4)')
    parser.add_argument('--output', '-o', default='generated.png', help='Output filename')
    parser.add_argument('--quality', '-q', default='standard', choices=['standard', 'high'],
                       help='Image quality')
    
    args = parser.parse_args()
    
    # Validate count
    if args.count < 1 or args.count > 4:
        print("Error: Count must be between 1 and 4")
        sys.exit(1)
    
    print(f"Generating {args.count} image(s)...")
    print(f"Prompt: {args.prompt}")
    print(f"Style: {args.style}")
    print(f"Size: {args.size}")
    print(f"Quality: {args.quality}")
    print()
    
    try:
        # Generate images
        image_urls = generate_image(
            prompt=args.prompt,
            style=args.style,
            size=args.size,
            count=args.count,
            quality=args.quality
        )
        
        # Download and save images
        saved_files = []
        for i, url in enumerate(image_urls):
            if args.count > 1:
                # Multiple files with index
                output_path = args.output.replace('{i}', str(i+1))
                if '{i}' not in args.output:
                    name, ext = os.path.splitext(args.output)
                    output_path = f"{name}_{i+1}{ext}"
            else:
                output_path = args.output
            
            print(f"Downloading image {i+1}/{len(image_urls)}...")
            saved_path = download_image(url, output_path)
            saved_files.append(saved_path)
            print(f"Saved: {saved_path}")
        
        print()
        print(f"Success! Generated {len(saved_files)} image(s)")
        
        # Return file paths for further processing
        return saved_files
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
