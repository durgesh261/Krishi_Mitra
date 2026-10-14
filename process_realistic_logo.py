import os
from PIL import Image, ImageFilter
import numpy as np

def process_logo():
    src_path = r'C:\Users\durge\.gemini\antigravity-ide\brain\ca070edd-896e-4030-bf74-fa219df28898\krishi_mitra_realistic_emblem_1791974421972.jpg'
    img = Image.open(src_path).convert('RGB')
    arr = np.array(img)

    cx, cy = 511.63, 511.0
    R = 367.5

    Y, X = np.ogrid[:1024, :1024]
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)

    # Clean anti-aliased alpha mask with 1.5px transition
    alpha = np.clip((R + 0.75 - dist) / 1.5, 0.0, 1.0) * 255.0
    rgba = np.dstack([arr, alpha.astype(np.uint8)])

    # Crop tightly around circle
    margin = 8
    crop_r = int(np.ceil(R)) + margin
    x1 = int(round(cx)) - crop_r
    y1 = int(round(cy)) - crop_r
    x2 = int(round(cx)) + crop_r
    y2 = int(round(cy)) + crop_r

    cropped_rgba = rgba[y1:y2, x1:x2]
    emblem_img = Image.fromarray(cropped_rgba, 'RGBA')

    # Create subtle elegant drop shadow
    # Pad canvas by 32px
    canvas_size = emblem_img.width + 36
    shadow_canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Extract alpha mask for shadow
    alpha_mask = emblem_img.split()[3]
    shadow = Image.new('RGBA', emblem_img.size, (15, 45, 20, 110)) # dark green/charcoal shadow
    shadow.putalpha(alpha_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=8))

    # Paste shadow with subtle offset (dy=6)
    offset_x = (canvas_size - emblem_img.width) // 2
    offset_y = (canvas_size - emblem_img.height) // 2
    shadow_canvas.paste(shadow, (offset_x, offset_y + 5), shadow)
    
    # Paste clean emblem over shadow
    shadow_canvas.paste(emblem_img, (offset_x, offset_y), emblem_img)

    # Resize to 512x512
    logo_512 = shadow_canvas.resize((512, 512), Image.Resampling.LANCZOS)
    logo_512.save('static/logo.png', format='PNG')
    print("Saved static/logo.png successfully!")

    # Also save favicon.ico with multi-sizes (16, 32, 48, 64)
    ico_img = emblem_img.resize((64, 64), Image.Resampling.LANCZOS)
    ico_img.save('static/favicon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])
    print("Saved static/favicon.ico successfully!")

    # Update static/logo.svg
    import base64
    with open('static/logo.png', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" width="512" height="512">
  <image href="data:image/png;base64,{b64}" x="0" y="0" width="512" height="512" />
</svg>'''
    with open('static/logo.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("Saved static/logo.svg successfully!")

if __name__ == '__main__':
    process_logo()
