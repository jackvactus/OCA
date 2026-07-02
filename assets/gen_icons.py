from pathlib import Path
from PIL import Image, ImageDraw

assets = Path(__file__).parent
icons = [
    (16, 'favicon-16x16.png'),
    (32, 'favicon-32x32.png'),
    (180, 'apple-touch-icon.png'),
    (32, 'favicon.ico')
]

for size, name in icons:
    img = Image.new('RGBA', (size, size), (231, 76, 60, 255))
    draw = ImageDraw.Draw(img)
    margin = max(2, size // 10)
    draw.ellipse((margin, margin, size - margin, size - margin), fill=(255, 255, 255, 255))
    inner = int(size * 0.44)
    x0 = (size - inner) // 2
    y0 = (size - inner) // 2
    x1 = x0 + inner
    y1 = y0 + inner
    draw.ellipse((x0, y0, x1, y1), fill=(231, 76, 60, 255))
    img.save(assets / name)
    print('created', name)
