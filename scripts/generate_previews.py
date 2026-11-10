"""Generate high-resolution visual preview screenshots and banners
for StruXllence Themes VS Code Marketplace listing and README.
Uses authentic StruXllence 3D master emblem and official vector wordmark from codex/.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = r"c:\Users\srini\Desktop\On Screen\StruXllence\vs-themes"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
EMBLEM_PATH = r"c:\Users\srini\Desktop\On Screen\StruXllence\codex\01-logos\emblem-HD-master.png"
WORDMARK_LIGHT = r"c:\Users\srini\Desktop\On Screen\StruXllence\codex\01-logos\wordmark-light.png"
FONTS_DIR = r"c:\Users\srini\Desktop\On Screen\StruXllence\codex\source\fonts"

GRAPHITE = (30, 30, 30)
OBSIDIAN = (17, 18, 21)
INNOVATE = (245, 124, 0)
INNOVATE_LIGHT = (255, 167, 38)
CONCRETE = (231, 231, 231)
STEEL = (107, 114, 128)
PURE_WHITE = (255, 255, 255)

def get_font(weight=700, size=24):
    f_path = os.path.join(FONTS_DIR, f"Montserrat-{weight}.ttf")
    if not os.path.exists(f_path):
        f_path = os.path.join(FONTS_DIR, "Montserrat-700.ttf")
    return ImageFont.truetype(f_path, size)

def draw_blueprint_grid(draw, width, height, spacing=40, color=(245, 124, 0, 15)):
    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=color, width=1)
    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=color, width=1)

def build_extension_icon():
    print("Building Official Extension Icon (256x256)...")
    size = 512
    im_master = Image.open(EMBLEM_PATH)
    crop_emblem = im_master.crop((130, 60, 1190, 1120)).resize((size, size), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    padding = 12
    radius = 100
    mdraw.rounded_rectangle([(padding, padding), (size - padding, size - padding)], radius=radius, fill=255)
    
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    icon.paste(crop_emblem, (0, 0))
    icon.putalpha(mask)
    
    border_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(border_layer)
    bdraw.rounded_rectangle([(padding, padding), (size - padding, size - padding)], radius=radius, outline=(245, 124, 0, 220), width=4)
    bdraw.rounded_rectangle([(padding + 80, size - padding - 8), (size - padding - 80, size - padding - 4)], radius=2, fill=(245, 124, 0, 255))
    
    final_icon = Image.alpha_composite(icon, border_layer)
    final_256 = final_icon.resize((256, 256), Image.Resampling.LANCZOS)
    final_256.save(os.path.join(ASSETS_DIR, "extension-icon.png"))
    print("  [OK] Saved assets/extension-icon.png")

def build_marketplace_banner():
    print("Building Marketplace Banner (1280x400)...")
    bw, bh = 1280, 400
    im = Image.new("RGBA", (bw, bh), OBSIDIAN)
    draw = ImageDraw.Draw(im)
    draw_blueprint_grid(draw, bw, bh, spacing=40, color=(245, 124, 0, 16))
    
    # Ambient amber glow
    glow = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([(60, 40), (420, 360)], fill=(*INNOVATE, 55))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    im.paste(glow, (0, 0), glow)
    
    # Authentic 3D Master Emblem
    if os.path.exists(EMBLEM_PATH):
        im_master = Image.open(EMBLEM_PATH)
        emblem_crop = im_master.crop((130, 60, 1190, 1120)).resize((260, 260), Image.Resampling.LANCZOS)
        mask = Image.new("L", (260, 260), 0)
        ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (260, 260)], radius=40, fill=255)
        im.paste(emblem_crop, (70, (bh - 260)//2), mask)
        
    # Vertical amber divider
    draw.line([(370, 60), (370, bh - 60)], fill=INNOVATE, width=3)
    
    # Official Wordmark
    if os.path.exists(WORDMARK_LIGHT):
        wordmark = Image.open(WORDMARK_LIGHT).convert("RGBA")
        wm_h = 70
        wm_w = int(wordmark.width * (wm_h / wordmark.height))
        wordmark_resized = wordmark.resize((wm_w, wm_h), Image.Resampling.LANCZOS)
        im.paste(wordmark_resized, (410, 75), wordmark_resized)
        
    font_sub = get_font(700, 16)
    font_feat = get_font(500, 15)
    font_badge = get_font(700, 13)
    
    draw.text((415, 160), "OFFICIAL THEME & ICON SUITE FOR VISUAL STUDIO CODE", font=font_sub, fill=INNOVATE)
    
    features = [
        "◈ StruXllence Dark & Light Color Themes (WCAG AAA)",
        "◈ High-Definition Custom File Icons (Python, Rust, TS, Go)",
        "◈ Bespoke Activity Bar & Product UI Icon Font",
        "◈ Engineered for Precision, Focus & Structural Elegance"
    ]
    y_pos = 200
    for feat in features:
        draw.text((415, y_pos), feat, font=font_feat, fill=CONCRETE)
        y_pos += 30
        
    # Badges on right
    draw.rounded_rectangle([(bw - 210, 65), (bw - 60, 98)], radius=6, fill=(30, 32, 38), outline=INNOVATE, width=1)
    draw.text((bw - 195, 74), "v1.0.0 STABLE", font=font_badge, fill=PURE_WHITE)
    
    draw.rounded_rectangle([(bw - 210, 110), (bw - 60, 143)], radius=6, fill=(30, 32, 38), outline=STEEL, width=1)
    draw.text((bw - 195, 119), "VS CODE 1.74+", font=font_badge, fill=CONCRETE)

    draw.rectangle([(0, 0), (bw - 1, bh - 1)], outline=INNOVATE, width=2)
    im.convert("RGB").save(os.path.join(ASSETS_DIR, "marketplace-banner.png"), quality=98)
    print("  [OK] Saved assets/marketplace-banner.png")

def build_ide_mockup(dark_mode=True):
    name = "Dark" if dark_mode else "Light"
    print(f"Building IDE Mockup: StruXllence {name} Theme (1920x1080)...")
    
    w, h = 1920, 1080
    bg_editor = (22, 23, 27) if dark_mode else (249, 250, 251)
    bg_activity = (17, 18, 21) if dark_mode else (236, 238, 241)
    bg_sidebar = (22, 23, 27) if dark_mode else (243, 244, 246)
    bg_title = (17, 18, 21) if dark_mode else (236, 238, 241)
    bg_status = (17, 18, 21) if dark_mode else (236, 238, 241)
    border_col = (30, 32, 38) if dark_mode else (209, 213, 219)
    fg_text = (231, 231, 231) if dark_mode else (31, 41, 55)
    
    im = Image.new("RGBA", (w, h), bg_editor)
    draw = ImageDraw.Draw(im)
    
    # 1. Title Bar (0..44)
    draw.rectangle([(0, 0), (w, 44)], fill=bg_title)
    draw.line([(0, 44), (w, 44)], fill=border_col, width=1)
    draw.text((w//2 - 220, 12), f"main.py — StruXllence Engineering Workspace [StruXllence {name}]", font=get_font(500, 14), fill=STEEL if dark_mode else (75, 85, 99))
    
    # Mac/Window buttons on left
    for i, col in enumerate([(239, 68, 68), (245, 124, 0), (16, 185, 129)]):
        draw.ellipse([(18 + i*22, 16), (30 + i*22, 28)], fill=col)
        
    # Official Emblem in title bar
    if os.path.exists(EMBLEM_PATH):
        im_master = Image.open(EMBLEM_PATH)
        crop_e = im_master.crop((130, 60, 1190, 1120)).resize((26, 26), Image.Resampling.LANCZOS)
        im.paste(crop_e, (100, 9))
    draw.text((134, 12), "StruXllence IDE", font=get_font(700, 14), fill=INNOVATE)
        
    # 2. Activity Bar (0..68 wide, 44..1040)
    draw.rectangle([(0, 44), (68, h - 40)], fill=bg_activity)
    draw.line([(68, 44), (68, h - 40)], fill=border_col, width=1)
    draw.line([(0, 60), (0, 110)], fill=INNOVATE, width=4)
    icons_y = [70, 130, 190, 250, 310]
    for iy in icons_y:
        draw.rectangle([(22, iy), (46, iy + 24)], outline=INNOVATE if iy == 70 else STEEL, width=2)
        
    # 3. Sidebar (68..380 wide, 44..1040)
    draw.rectangle([(68, 44), (380, h - 40)], fill=bg_sidebar)
    draw.line([(380, 44), (380, h - 40)], fill=border_col, width=1)
    draw.text((90, 60), "EXPLORER", font=get_font(700, 13), fill=INNOVATE if dark_mode else (180, 83, 9))
    draw.text((90, 95), "▾ STRUXLLENCE-WORKSPACE", font=get_font(700, 13), fill=fg_text)
    
    tree_items = [
        ("  ▾ src", True),
        ("    ▾ analysis", True),
        ("      main.py", False),
        ("      seismic_damping.rs", False),
        ("      finite_element.ts", False),
        ("    ▾ structural_models", True),
        ("      highrise_core.json", False),
        ("      truss_geometry.yaml", False),
        ("  ▾ docs", True),
        ("    SPECIFICATION.md", False),
        ("    CALCULATIONS.pdf", False),
        ("  .env", False),
        ("  package.json", False),
        ("  README.md", False)
    ]
    ty = 130
    for label, is_folder in tree_items:
        color = INNOVATE if "main.py" in label else (fg_text if is_folder else STEEL)
        draw.text((90, ty), label, font=get_font(500, 14), fill=color)
        ty += 28
        
    # 4. Tabs Bar (380..w, 44..84)
    draw.rectangle([(380, 44), (w, 84)], fill=bg_title)
    draw.line([(380, 84), (w, 84)], fill=border_col, width=1)
    draw.rectangle([(380, 44), (560, 84)], fill=bg_editor)
    draw.line([(380, 44), (560, 44)], fill=INNOVATE, width=3)
    draw.text((410, 56), "main.py", font=get_font(700, 14), fill=fg_text)
    draw.text((535, 56), "×", font=get_font(500, 16), fill=STEEL)
    draw.text((585, 56), "seismic_damping.rs", font=get_font(500, 14), fill=STEEL)
    
    # 5. Editor Code Body (380..w, 84..h-40)
    for lno in range(1, 28):
        ly = 100 + (lno - 1) * 32
        draw.text((400, ly), f"{lno:2d}", font=get_font(500, 14), fill=INNOVATE if lno == 7 else (STEEL if dark_mode else (156, 163, 175)))
        
    hl_col = (28, 29, 35) if dark_mode else (243, 244, 246)
    draw.rectangle([(440, 100 + 6*32 - 4), (w, 100 + 7*32 - 4)], fill=hl_col)
    
    code_lines = [
        [("import", INNOVATE), (" math", fg_text), (", sys", fg_text)],
        [("from", INNOVATE), (" struxllence.fem ", (100, 181, 246) if dark_mode else (2, 132, 199)), ("import", INNOVATE), (" DynamicSolver, NonLinearTruss", (255, 209, 128) if dark_mode else (180, 83, 9))],
        [("", fg_text)],
        [("# StruXllence Parametric High-Rise Analysis Engine", STEEL)],
        [("class", INNOVATE), (" SuperTallStructuralCore", (100, 181, 246) if dark_mode else (2, 132, 199)), (":", fg_text)],
        [("    def", INNOVATE), (" __init__", (255, 209, 128) if dark_mode else (180, 83, 9)), ("(self, height_meters: ", fg_text), ("float", (100, 181, 246) if dark_mode else (2, 132, 199)), (", wind_zone: ", fg_text), ("str", (100, 181, 246) if dark_mode else (2, 132, 199)), (") -> ", fg_text), ("None", INNOVATE_LIGHT if dark_mode else (194, 65, 12)), (":", fg_text)],
        [("        self.height = height_meters", fg_text), ("  # Structural Spire: 420.0m", STEEL)],
        [("        self.damping_ratio = ", fg_text), ("0.045", INNOVATE_LIGHT if dark_mode else (194, 65, 12)), ("  # Active tuned mass damper", STEEL)],
        [("        self.solver = ", fg_text), ("DynamicSolver", (100, 181, 246) if dark_mode else (2, 132, 199)), ("(tolerance=", fg_text), ("1e-9", INNOVATE_LIGHT if dark_mode else (194, 65, 12)), (")", fg_text)],
        [("", fg_text)],
        [("    def", INNOVATE), (" calculate_seismic_drift", (255, 209, 128) if dark_mode else (180, 83, 9)), ("(self, pga_g: ", fg_text), ("float", (100, 181, 246) if dark_mode else (2, 132, 199)), (") -> ", fg_text), ("dict", (100, 181, 246) if dark_mode else (2, 132, 199)), (":", fg_text)],
        [("        \"\"\"Evaluate nonlinear inter-story drift under 2,475-yr MCE event.\"\"\"", (129, 199, 132) if dark_mode else (5, 150, 105))],
        [("        spectrum = self.solver.", fg_text), ("get_design_response_spectrum", (255, 209, 128) if dark_mode else (180, 83, 9)), ("(pga_g)", fg_text)],
        [("        drift_ratio = (spectrum.", fg_text), ("peak_displacement", (255, 209, 128) if dark_mode else (180, 83, 9)), (" / self.height)", fg_text)],
        [("        return", INNOVATE), (" {", fg_text), ("\"status\":", (129, 199, 132) if dark_mode else (5, 150, 105)), (" \"PASS - DUCTILE\"", (129, 199, 132) if dark_mode else (5, 150, 105)), (", \"drift\":", (129, 199, 132) if dark_mode else (5, 150, 105)), (" drift_ratio}", fg_text)]
    ]
    
    for idx, line_parts in enumerate(code_lines):
        cy = 100 + idx * 32
        cx = 460
        for text, color in line_parts:
            draw.text((cx, cy), text, font=get_font(500, 16), fill=color)
            cx += int(draw.textbbox((0, 0), text, font=get_font(500, 16))[2])
            
    # 6. Status Bar (0..w, h-40..h)
    draw.rectangle([(0, h - 40), (w, h)], fill=bg_status)
    draw.line([(0, h - 40), (w, h - 40)], fill=border_col, width=1)
    draw.rectangle([(0, h - 40), (140, h)], fill=INNOVATE)
    draw.text((16, h - 28), "◈ StruXllence", font=get_font(700, 13), fill=(17, 18, 21) if dark_mode else PURE_WHITE)
    draw.text((160, h - 28), "main  ✓ 0  ⚠ 0", font=get_font(500, 12), fill=STEEL)
    draw.text((w - 420, h - 28), "Spaces: 4   UTF-8   Python 3.12   StruXllence Themes", font=get_font(500, 12), fill=STEEL)
    
    fname = f"preview-{name.lower()}-theme.png"
    im.convert("RGB").save(os.path.join(ASSETS_DIR, fname), quality=98)
    print(f"  [OK] Saved assets/{fname}")

def build_icons_showcase():
    print("Building Icons Showcase (1920x1080)...")
    w, h = 1920, 1080
    im = Image.new("RGBA", (w, h), OBSIDIAN)
    draw = ImageDraw.Draw(im)
    draw_blueprint_grid(draw, w, h, spacing=45, color=(245, 124, 0, 16))
    
    # Official 3D emblem on left header
    if os.path.exists(EMBLEM_PATH):
        im_master = Image.open(EMBLEM_PATH)
        crop_e = im_master.crop((130, 60, 1190, 1120)).resize((110, 110), Image.Resampling.LANCZOS)
        mask = Image.new("L", (110, 110), 0)
        ImageDraw.Draw(mask).rounded_rectangle([(0,0),(110,110)], radius=22, fill=255)
        im.paste(crop_e, (100, 45), mask)
        
    # Official Wordmark
    if os.path.exists(WORDMARK_LIGHT):
        wm = Image.open(WORDMARK_LIGHT).convert("RGBA")
        wm_h = 52
        wm_w = int(wm.width * (wm_h / wm.height))
        wm_res = wm.resize((wm_w, wm_h), Image.Resampling.LANCZOS)
        im.paste(wm_res, (230, 50), wm_res)
        
    draw.text((235, 110), "HIGH-DEFINITION 512×512 MASTER FILE & PRODUCT ICON SUITE", font=get_font(700, 15), fill=INNOVATE)
    
    # Grid of File Icons
    icons = ["folder", "folder-open", "python", "typescript", "javascript", "rust", "c", "cpp", "csharp", "go", "java", "html", "css", "json", "markdown", "git", "docker", "database", "shell", "react", "settings", "lock", "image", "archive"]
    
    cols = 6
    cell_w, cell_h = 260, 140
    start_x, start_y = 100, 180
    
    for idx, ic in enumerate(icons):
        col = idx % cols
        row = idx // cols
        x = start_x + col * (cell_w + 30)
        y = start_y + row * (cell_h + 30)
        
        # Card
        draw.rounded_rectangle([(x, y), (x + cell_w, y + cell_h)], radius=12, fill=(28, 29, 34), outline=(55, 65, 81), width=1)
        
        # Load and paste icon
        ic_path = os.path.join(BASE_DIR, "icons", "file-icons", "png-hd", f"{ic}.png")
        if os.path.exists(ic_path):
            icon_img = Image.open(ic_path).convert("RGBA").resize((72, 72), Image.Resampling.LANCZOS)
            im.paste(icon_img, (x + 20, y + (cell_h - 72)//2), icon_img)
            
        draw.text((x + 105, y + 45), ic.upper(), font=get_font(700, 15), fill=PURE_WHITE)
        draw.text((x + 105, y + 70), "512px HD Master", font=get_font(500, 12), fill=STEEL)
        
    im.convert("RGB").save(os.path.join(ASSETS_DIR, "preview-icons-showcase.png"), quality=98)
    print("  [OK] Saved assets/preview-icons-showcase.png")

if __name__ == "__main__":
    build_extension_icon()
    build_marketplace_banner()
    build_ide_mockup(dark_mode=True)
    build_ide_mockup(dark_mode=False)
    build_icons_showcase()
    print("All assets successfully regenerated using authentic codex branding!")
