"""
Generate all 52 playing cards with unified magical academy style
Pure PIL programmatic generation - no AI needed
Style: Golden borders, elegant design, consistent across all cards
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math

def draw_star(draw, x, y, size, color):
    """Draw a 5-pointed star"""
    points = []
    for i in range(10):
        angle = math.pi * 2 * i / 10 - math.pi / 2
        r = size if i % 2 == 0 else size / 2
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        points.append((px, py))
    
    draw.polygon(points, fill=color)

def draw_decorative_corners(draw, width, height, margin, color):
    """Draw decorative corner elements"""
    corner_size = 25
    corners = [
        (margin + 20, margin + 20),
        (width - margin - 20, margin + 20),
        (margin + 20, height - margin - 20),
        (width - margin - 20, height - margin - 20)
    ]
    
    for cx, cy in corners:
        draw_star(draw, cx, cy, corner_size, color)

def create_card_frame(draw, width, height, margin=40):
    """Draw elegant magical academy frame"""
    # Multiple layered borders for elegant look
    border_colors = [
        (218, 165, 32),   # Dark goldenrod
        (255, 215, 0),    # Gold
        (218, 165, 32),   # Dark goldenrod
    ]
    
    for i, color in enumerate(border_colors):
        offset = i * 3
        rect = [
            margin - offset,
            margin - offset,
            width - margin + offset,
            height - margin + offset
        ]
        draw.rectangle(rect, outline=color, width=3)
    
    # Decorative corners
    draw_decorative_corners(draw, width, height, margin, (255, 215, 0))

def create_card(rank, suit, suit_color, output_path):
    """Create a single playing card"""
    width, height = 768, 1024
    margin = 50
    
    # Create base image with off-white background (parchment-like)
    bg_color = (253, 250, 245)  # Warm off-white
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw elegant frame
    create_card_frame(draw, width, height, margin)
    
    # Suit symbol mapping
    suit_symbols = {
        'hearts': '♥',
        'diamonds': '♦',
        'clubs': '♣',
        'spades': '♠'
    }
    
    symbol = suit_symbols[suit]
    
    # Load fonts
    try:
        font_rank = ImageFont.truetype("arial.ttf", 64)
        font_suit = ImageFont.truetype("arial.ttf", 42)
        font_center = ImageFont.truetype("arial.ttf", 120)
    except:
        font_rank = ImageFont.load_default()
        font_suit = font_rank
        font_center = font_rank
    
    # Top-left: Rank + Suit
    draw.text((margin + 15, margin + 15), rank, fill=suit_color, font=font_rank)
    draw.text((margin + 20, margin + 75), symbol, fill=suit_color, font=font_suit)
    
    # Center: Large suit symbol
    center_x = width // 2
    center_y = height // 2
    draw.text((center_x, center_y), symbol, fill=suit_color, font=font_center, anchor="mm")
    
    # Bottom-right: Rank + Suit (upside down orientation)
    # We'll draw it rotated 180 degrees
    bottom_margin = margin + 15
    
    # For bottom, we create a small rotated image
    bottom_text_size = 100
    bottom_img = Image.new('RGBA', (bottom_text_size, bottom_text_size), (0, 0, 0, 0))
    bottom_draw = ImageDraw.Draw(bottom_img)
    
    # Draw rank
    bottom_draw.text((10, 10), rank, fill=suit_color, font=font_rank)
    bottom_draw.text((15, 70), symbol, fill=suit_color, font=font_suit)
    
    # Rotate 180 degrees
    bottom_img = bottom_img.rotate(180)
    
    # Paste onto main image
    paste_x = width - margin - 80
    paste_y = height - margin - 80
    img.paste(bottom_img, (paste_x, paste_y), bottom_img)
    
    # Save with optimization
    img.save(output_path, 'PNG', optimize=True, quality=90)
    print(f"[OK] {rank}_{suit} -> {output_path}")

def generate_all_cards():
    """Generate all 52 cards"""
    output_dir = "public/assets/cards"
    os.makedirs(output_dir, exist_ok=True)
    
    # Remove old AI-generated cards first
    old_files = ['A_hearts.png', 'K_hearts.png', 'Q_hearts.png', 
                 'A_diamonds.png', 'K_diamonds.png', 'Q_diamonds.png',
                 'A_clubs.png', 'K_clubs.png', 'Q_clubs.png',
                 'A_spades.png', 'K_spades.png', 'Q_spades.png']
    
    for old_file in old_files:
        old_path = os.path.join(output_dir, old_file)
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f"[CLEAN] Removed old: {old_file}")
    
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    suit_colors = {
        'hearts': (220, 20, 60),    # Crimson red
        'diamonds': (220, 20, 60),  # Crimson red
        'clubs': (25, 25, 25),      # Near black
        'spades': (25, 25, 25)      # Near black
    }
    
    print("\n" + "="*60)
    print("Generating 52 unified playing cards...")
    print("="*60 + "\n")
    
    count = 0
    for suit in suits:
        for rank in ranks:
            filename = f"{rank}_{suit}.png"
            output_path = os.path.join(output_dir, filename)
            
            create_card(rank, suit, suit_colors[suit], output_path)
            count += 1
    
    print("\n" + "="*60)
    print(f"[DONE] Generated {count} cards in {output_dir}")
    print("="*60)

if __name__ == "__main__":
    generate_all_cards()
