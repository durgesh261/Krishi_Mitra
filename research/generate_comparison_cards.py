"""
Generate Side-by-Side Visual Comparison Cards for all 5 Indian Regional Benchmark Crops
Creates high-resolution comparative graphics:
[Healthy Leaf Photo] | [Healthy Attention] || [Diseased Leaf Photo] | [Diseased Attention]
"""

import os
from PIL import Image, ImageDraw, ImageFont

ART_DIR = r"C:\Users\durge\.gemini\antigravity-ide\brain\ca070edd-896e-4030-bf74-fa219df28898"

crops = [
    {
        "id": "wheat",
        "title": "North India: Wheat (गेहूँ) - Punjab / Haryana Belt",
        "healthy_desc": "Healthy Foliage (NDVI: 0.692 | Yield: 50.17 q/ha)",
        "diseased_desc": "Stripe Rust Outbreak (NDVI: 0.621 | Yield: 27.67 q/ha, -44.7%)",
        "pathology_notes": "Healthy: Clean parallel veins, vibrant chlorophyll. Diseased: Yellow-orange linear urediniospore pustules."
    },
    {
        "id": "rice",
        "title": "South & East India: Rice / Paddy (धान) - Cauvery / Bengal Delta",
        "healthy_desc": "Healthy Foliage (NDVI: 0.728 | Yield: 58.65 q/ha)",
        "diseased_desc": "Rice Blast Disease (NDVI: 0.698 | Yield: 40.83 q/ha, -29.0%)",
        "pathology_notes": "Healthy: Smooth deep green lamina. Diseased: Spindle-shaped necrotic lesions with gray ash centers."
    },
    {
        "id": "cotton",
        "title": "Central & West India: Cotton (कपास) - Vidarbha / Gujarat",
        "healthy_desc": "Healthy Foliage (NDVI: 0.681 | Yield: 25.95 q/ha)",
        "diseased_desc": "Alternaria Leaf Blight (NDVI: 0.511 | Yield: 16.01 q/ha, -38.4%)",
        "pathology_notes": "Healthy: Broad green palmate leaves. Diseased: Concentric circular necrotic spots with purple margins."
    },
    {
        "id": "groundnut",
        "title": "West India: Groundnut / Peanut (मूंगफली) - Saurashtra Belt",
        "healthy_desc": "Healthy Foliage (NDVI: 0.639 | Yield: 30.61 q/ha)",
        "diseased_desc": "Tikka Leaf Spot (NDVI: 0.397 | Yield: 17.48 q/ha, -41.7%)",
        "pathology_notes": "Healthy: Oval pinnate green leaflets. Diseased: Dark brown/black necrotic spots with chlorotic yellow halos."
    },
    {
        "id": "maize",
        "title": "Central & South India: Maize / Corn (मक्का) - Karnataka / MP",
        "healthy_desc": "Healthy Foliage (NDVI: 0.711 | Yield: 63.26 q/ha)",
        "diseased_desc": "Northern Leaf Blight (NDVI: 0.603 | Yield: 38.58 q/ha, -38.3%)",
        "pathology_notes": "Healthy: Crisp parallel-veined strap leaf. Diseased: Cigar-shaped grayish-tan elongated necrotic lesions."
    }
]

for c in crops:
    cid = c["id"]
    h_img_path = os.path.join(ART_DIR, f"{cid}_healthy.jpg")
    h_cam_path = os.path.join(ART_DIR, f"{cid}_healthy_gradcam.jpg")
    d_img_path = os.path.join(ART_DIR, f"{cid}_diseased.jpg")
    d_cam_path = os.path.join(ART_DIR, f"{cid}_diseased_gradcam.jpg")

    im_h = Image.open(h_img_path).convert('RGB').resize((400, 400))
    im_h_cam = Image.open(h_cam_path).convert('RGB').resize((400, 400))
    im_d = Image.open(d_img_path).convert('RGB').resize((400, 400))
    im_d_cam = Image.open(d_cam_path).convert('RGB').resize((400, 400))

    # Canvas dimensions: 4 images in a 2x2 grid or 1x4 strip
    # Let's do 2 columns: Left = HEALTHY (Photo + Grad-CAM), Right = DISEASED (Photo + Grad-CAM)
    # Width = 840, Height = 950
    card = Image.new('RGB', (860, 960), color=(255, 255, 255))
    draw = ImageDraw.Draw(card)

    # Header Bar
    draw.rectangle([(0, 0), (860, 70)], fill=(27, 94, 32))
    
    # Try default or standard font
    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_sub = ImageFont.truetype("arial.ttf", 15)
        font_meta = ImageFont.truetype("arial.ttf", 13)
        font_badge = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_title = font_sub = font_meta = font_badge = ImageFont.load_default()

    draw.text((20, 12), c["title"], fill=(255, 255, 255), font=font_title)
    draw.text((20, 42), "Krishi Mitra Multi-Spectral AI & Visual Pathology Comparison", fill=(165, 214, 167), font=font_meta)

    # Column 1 Header: HEALTHY
    draw.rectangle([(20, 85), (420, 125)], fill=(232, 245, 233))
    draw.text((35, 95), "✓ NO SYMPTOMS (HEALTHY)", fill=(46, 125, 50), font=font_badge)

    # Column 2 Header: DISEASED
    draw.rectangle([(440, 85), (840, 125)], fill=(255, 235, 238))
    draw.text((455, 95), "⚠ DISEASE DETECTED (PATHOLOGY)", fill=(198, 40, 40), font=font_badge)

    # Paste Photos (Row 1)
    card.paste(im_h, (20, 135))
    card.paste(im_d, (440, 135))

    # Row 1 Labels
    draw.rectangle([(20, 540), (420, 565)], fill=(240, 240, 240))
    draw.text((30, 544), "Macro Field Photograph", fill=(60, 60, 60), font=font_meta)

    draw.rectangle([(440, 540), (840, 565)], fill=(240, 240, 240))
    draw.text((450, 544), "Infected Field Photograph", fill=(60, 60, 60), font=font_meta)

    # Paste Grad-CAM Attention Heatmaps (Row 2)
    card.paste(im_h_cam, (20, 575))
    card.paste(im_d_cam, (440, 575))

    # Bottom Summary Strip
    draw.rectangle([(0, 890), (860, 960)], fill=(245, 245, 245))
    draw.text((20, 898), "Healthy Metric: " + c["healthy_desc"], fill=(46, 125, 50), font=font_meta)
    draw.text((20, 918), "Outbreak Alert: " + c["diseased_desc"], fill=(198, 40, 40), font=font_meta)
    draw.text((20, 938), "Visual Delta: " + c["pathology_notes"], fill=(80, 80, 80), font=font_meta)

    out_path = os.path.join(ART_DIR, f"{cid}_comparison_card.jpg")
    card.save(out_path, quality=92)
    print(f"[OK] Generated {cid}_comparison_card.jpg")

print("All 5 comparison cards generated successfully!")
