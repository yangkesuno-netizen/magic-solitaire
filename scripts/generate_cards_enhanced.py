"""
Generate high-quality playing cards with enhanced magical academy style
Better borders, gradients, decorations, and typography
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import math

def create_gradient_background(width, height):
    """Create a subtle gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Subtle cream to warm white gradient
    for y in range(height):
        # Interpolate between cream colors
        ratio = y / height
        r = int(253 + (255 - 253) * ratio)
        g = int(250 + (252 - 250) * ratio)
        b = int(245 + (250 - 245) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def draw_ornate_border(draw, width, height, margin=35):
    """Draw an ornate magical academy border with multiple layers"""
    
    # Layer 1: Outer dark gold border
    outer_color = (184, 134, 11)  # Dark goldenrod
    for i in range(5):
        rect = [margin - i, margin - i, width - margin + i, height - margin + i]
        draw.rectangle(rect, outline=outer_color, width=1)
    
    # Layer 2: Main gold border
    main_gold = (255, 215, 0)  # Gold
    for i in range(3):
        offset = 5 + i * 2
        rect = [margin + offset, margin + offset, width - margin - offset, height - margin - offset]
        draw.rectangle(rect, outline=main_gold, width=2)
    
    # Layer 3: Inner decorative line (thin)
    inner_color = (218, 165, 32)  # Goldenrod
    rect = [margin + 15, margin + 15, width - margin - 15, height - margin - 15]
    draw.rectangle(rect, outline=inner_color, width=1)
    
    # Layer 4: Innermost line (very thin)
    rect = [margin + 18, margin + 18, width - margin - 18, height - margin - 18]
    draw.rectangle(rect, outline=main_gold, width=1)

def draw_corner_decoration(draw, x, y, size, color):
    """Draw an ornate corner decoration with star and swirls"""
    # Main star
    points = []
    for i in range(10):
        angle = math.pi * 2 * i / 10 - math.pi / 2
        r = size if i % 2 == 0 else size / 2.5
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        points.append((px, py))
    
    draw.polygon(points, fill=color)
    
    # Small decorative dots around star
    dot_color = (255, 223, 100)  # Light gold
    for i in range(4):
        angle = math.pi * 2 * i / 4
        dx = x + (size + 8) * math.cos(angle)
        dy = y + (size + 8) * math.sin(angle)
        draw.ellipse([dx-2, dy-2, dx+2, dy+2], fill=dot_color)

def draw_decorative_corners(draw, width, height, margin):
    """Draw decorative elements in all four corners"""
    gold = (255, 215, 0)
    star_size = 18
    
    corners = [
        (margin + 25, margin + 25),  # Top-left
        (width - margin - 25, margin + 25),  # Top-right
        (margin + 25, height - margin - 25),  # Bottom-left
        (width - margin - 25, height - margin - 25),  # Bottom-right
    ]
    
    for cx, cy in corners:
        draw_corner_decoration(draw, cx, cy, star_size, gold)

def draw_mystical_symbols(draw, width, height):
    """Draw subtle mystical symbols in the background"""
    # Very subtle decorative circles
    center_x, center_y = width // 2, height // 2
    
    # Concentric circles (very faint)
    faint_gold = (255, 215, 0, 15)  # Gold with low alpha
    for radius in [150, 200, 250]:
        # Create a separate image for alpha blending
        circle_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle_img)
        circle_draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], outline=(255, 215, 0, 30), width=2)
        
        # Blend with main image
        draw.bitmap((0, 0), circle_img.convert('L'))

def create_card(rank, suit, suit_color, template_img, output_path):
    """Create a single card using template as base"""
    
    # Start with template if available, otherwise create new
    if template_img and os.path.exists(template_img):
        img = Image.open(template_img).convert('RGB')
    else:
        # Create gradient background
        img = create_gradient_background(768, 1024)
    
    draw = ImageDraw.Draw(img)
    
    width, height = 768, 1024
    margin = 40
    
    # Draw ornate border
    draw_ornate_border(draw, width, height, margin)
    
    # Draw decorative corners
    draw_decorative_corners(draw, width, height, margin)
    
    # Suit symbol mapping
    suit_symbols = {
        'hearts': '♥',
        'diamonds': '♦',
        'clubs': '♣',
        'spades': '♠'
    }
    
    symbol = suit_symbols[suit]
    
    # Try to load better fonts
    try:
        font_rank = ImageFont.truetype("arial.ttf", 72)
        font_suit = ImageFont.truetype("arial.ttf", 48)
        font_center = ImageFont.truetype("arial.ttf", 140)
    except:
        font_rank = ImageFont.load_default()
        font_suit = font_rank
        font_center = font_rank
    
    # Top-left: Rank + Suit
    draw.text((margin + 20, margin + 20), rank, fill=suit_color, font=font_rank)
    draw.text((margin + 25, margin + 85), symbol, fill=suit_color, font=font_suit)
    
    # Center: Large elegant suit symbol
    center_x = width // 2
    center_y = height // 2
    draw.text((center_x, center_y), symbol, fill=suit_color, font=font_center, anchor="mm")
    
    # Bottom-right: Rank + Suit (create rotated element)
    bottom_elem = Image.new('RGBA', (120, 120), (0, 0, 0, 0))
    bottom_draw = ImageDraw.Draw(bottom_elem)
    bottom_draw.text((15, 15), rank, fill=suit_color, font=font_rank)
    bottom_draw.text((20, 80), symbol, fill=suit_color, font=font_suit)
    bottom_elem = bottom_elem.rotate(180, expand=False)
    
    paste_x = width - margin - 100
    paste_y = height - margin - 100
    img.paste(bottom_elem, (paste_x, paste_y), bottom_elem)
    
    # Add subtle shadow to center symbol for depth
    # (Optional enhancement)
    
    # Save with high quality
    img.save(output_path, 'PNG', optimize=True, quality=95)
    print(f"[OK] {rank}_{suit}")

def generate_all_cards():
    """Generate all 52 cards"""
    output_dir = "public/assets/cards"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check for template
    template_path = os.path.join(output_dir, "template.png")
    if os.path.exists(template_path):
        print(f"Using template: {template_path}")
    else:
        print("No template found, creating from scratch...")
    
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    
    suit_colors = {
        'hearts': (200, 10, 40),     # Deep crimson
        'diamonds': (200, 10, 40),   # Deep crimson
        'clubs': (20, 20, 20),       # Rich black
        'spades': (20, 20, 20)       # Rich black
    }
    
    print("\n" + "="*60)
    print("Generating 52 HIGH-QUALITY playing cards...")
    print("="*60 + "\n")
    
    count = 0
    for suit in suits:
        for rank in ranks:
            filename = f"{rank}_{suit}.png"
            output_path = os.path.join(output_dir, filename)
            
            create_card(rank, suit, suit_colors[suit], template_path, output_path)
            count += 1
    
    print("\n" + "="*60)
    print(f"[DONE] Generated {count} cards")
    print("="*60)

if __name__ == "__main__":
    generate_all_cards()
