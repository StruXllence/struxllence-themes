"""Build custom WOFF and TTF Icon Fonts for StruXllence Product Icon Themes.
Generates font files and character mappings compliant with VS Code Product Icon Theme API.
"""
import os
import math
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

BASE_DIR = r"c:\Users\srini\Desktop\On Screen\StruXllence\vs-themes"
FONTS_DIR = os.path.join(BASE_DIR, "icons", "product-icons", "fonts")
os.makedirs(FONTS_DIR, exist_ok=True)

# Character Map (Private Use Area unicode points)
GLYPH_MAP = {
    0xE001: ("explorer", "view-explorer"),
    0xE002: ("search", "view-search"),
    0xE003: ("scm", "view-scm"),
    0xE004: ("debug", "view-debug"),
    0xE005: ("extensions", "view-extensions"),
    0xE006: ("gear", "settings-gear"),
    0xE007: ("account", "account"),
    0xE008: ("bell", "bell"),
    0xE009: ("terminal", "terminal"),
    0xE00A: ("split", "split-horizontal"),
    0xE00B: ("close", "close"),
    0xE00C: ("chevron_right", "chevron-right"),
    0xE00D: ("chevron_down", "chevron-down"),
    0xE00E: ("folder", "folder"),
    0xE00F: ("file", "file"),
    0xE010: ("refresh", "refresh"),
    0xE011: ("filter", "filter"),
    0xE012: ("play", "play")
}

def draw_rect(pen, x1, y1, x2, y2):
    pen.moveTo((x1, y1))
    pen.lineTo((x2, y1))
    pen.lineTo((x2, y2))
    pen.lineTo((x1, y2))
    pen.closePath()

def draw_circle(pen, cx, cy, r, segments=16):
    pts = []
    for i in range(segments):
        th = 2 * math.pi * i / segments
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()

def build_glyphs():
    glyphs = {}
    
    # .notdef
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, 0, 924, 800)
    draw_rect(pen, 200, 100, 824, 700)
    glyphs[".notdef"] = pen.glyph()

    # 1. Explorer (Double overlapping rectangular sheets)
    p = TTGlyphPen(None)
    draw_rect(p, 160, 100, 640, 720)
    draw_rect(p, 360, 240, 840, 860)
    glyphs["explorer"] = p.glyph()

    # 2. Search (Magnifying glass)
    p = TTGlyphPen(None)
    draw_circle(p, 420, 500, 260)
    draw_circle(p, 420, 500, 180)
    # Handle
    p.moveTo((600, 320))
    p.lineTo((840, 80))
    p.lineTo((900, 140))
    p.lineTo((660, 380))
    p.closePath()
    glyphs["search"] = p.glyph()

    # 3. SCM (Git tree branch nodes)
    p = TTGlyphPen(None)
    draw_circle(p, 320, 200, 100)
    draw_circle(p, 320, 680, 100)
    draw_circle(p, 700, 440, 100)
    draw_rect(p, 280, 200, 360, 680)
    draw_rect(p, 320, 400, 660, 480)
    glyphs["scm"] = p.glyph()

    # 4. Debug (Shield with play button)
    p = TTGlyphPen(None)
    p.moveTo((500, 840))
    p.lineTo((820, 680))
    p.lineTo((820, 360))
    p.lineTo((500, 100))
    p.lineTo((180, 360))
    p.lineTo((180, 680))
    p.closePath()
    # Inner cutout play triangle
    p.moveTo((420, 360))
    p.lineTo((660, 500))
    p.lineTo((420, 640))
    p.closePath()
    glyphs["debug"] = p.glyph()

    # 5. Extensions (4 Modular Squares)
    p = TTGlyphPen(None)
    draw_rect(p, 160, 160, 460, 460)
    draw_rect(p, 540, 160, 840, 460)
    draw_rect(p, 160, 540, 460, 840)
    draw_rect(p, 540, 540, 840, 840)
    glyphs["extensions"] = p.glyph()

    # 6. Settings Gear
    p = TTGlyphPen(None)
    draw_circle(p, 512, 480, 360)
    draw_circle(p, 512, 480, 180)
    # 4 outer teeth
    draw_rect(p, 440, 800, 584, 940)
    draw_rect(p, 440, 20, 584, 160)
    draw_rect(p, 50, 410, 190, 550)
    draw_rect(p, 834, 410, 974, 550)
    glyphs["gear"] = p.glyph()

    # 7. Account (User)
    p = TTGlyphPen(None)
    draw_circle(p, 512, 640, 160)
    p.moveTo((200, 100))
    p.lineTo((300, 380))
    p.lineTo((724, 380))
    p.lineTo((824, 100))
    p.closePath()
    glyphs["account"] = p.glyph()

    # 8. Bell (Notification)
    p = TTGlyphPen(None)
    p.moveTo((512, 860))
    p.lineTo((320, 700))
    p.lineTo((320, 360))
    p.lineTo((200, 220))
    p.lineTo((824, 220))
    p.lineTo((704, 360))
    p.lineTo((704, 700))
    p.closePath()
    draw_circle(p, 512, 140, 60)
    glyphs["bell"] = p.glyph()

    # 9. Terminal
    p = TTGlyphPen(None)
    draw_rect(p, 120, 140, 904, 820)
    draw_rect(p, 200, 220, 824, 740)
    # Prompt >_
    p.moveTo((280, 620))
    p.lineTo((420, 480))
    p.lineTo((280, 340))
    p.lineTo((340, 340))
    p.lineTo((480, 480))
    p.lineTo((340, 620))
    p.closePath()
    draw_rect(p, 520, 340, 700, 400)
    glyphs["terminal"] = p.glyph()

    # 10. Split Horizontal
    p = TTGlyphPen(None)
    draw_rect(p, 140, 140, 884, 820)
    draw_rect(p, 480, 140, 544, 820)
    glyphs["split"] = p.glyph()

    # 11. Close X
    p = TTGlyphPen(None)
    p.moveTo((220, 280))
    p.lineTo((452, 512))
    p.lineTo((220, 744))
    p.lineTo((280, 804))
    p.lineTo((512, 572))
    p.lineTo((744, 804))
    p.lineTo((804, 744))
    p.lineTo((572, 512))
    p.lineTo((804, 280))
    p.lineTo((744, 220))
    p.lineTo((512, 452))
    p.lineTo((280, 220))
    p.closePath()
    glyphs["close"] = p.glyph()

    # 12. Chevron Right
    p = TTGlyphPen(None)
    p.moveTo((360, 200))
    p.lineTo((660, 500))
    p.lineTo((360, 800))
    p.lineTo((440, 880))
    p.lineTo((820, 500))
    p.lineTo((440, 120))
    p.closePath()
    glyphs["chevron_right"] = p.glyph()

    # 13. Chevron Down
    p = TTGlyphPen(None)
    p.moveTo((200, 640))
    p.lineTo((500, 340))
    p.lineTo((800, 640))
    p.lineTo((880, 560))
    p.lineTo((500, 180))
    p.lineTo((120, 560))
    p.closePath()
    glyphs["chevron_down"] = p.glyph()

    # 14. Folder
    p = TTGlyphPen(None)
    draw_rect(p, 140, 160, 884, 760)
    draw_rect(p, 140, 700, 480, 860)
    glyphs["folder"] = p.glyph()

    # 15. File
    p = TTGlyphPen(None)
    p.moveTo((220, 120))
    p.lineTo((640, 120))
    p.lineTo((804, 284))
    p.lineTo((804, 840))
    p.lineTo((220, 840))
    p.closePath()
    glyphs["file"] = p.glyph()

    # 16. Refresh
    p = TTGlyphPen(None)
    draw_circle(p, 512, 500, 320)
    draw_circle(p, 512, 500, 220)
    draw_rect(p, 460, 140, 564, 860)
    glyphs["refresh"] = p.glyph()

    # 17. Filter
    p = TTGlyphPen(None)
    p.moveTo((160, 800))
    p.lineTo((864, 800))
    p.lineTo((580, 480))
    p.lineTo((580, 160))
    p.lineTo((444, 240))
    p.lineTo((444, 480))
    p.closePath()
    glyphs["filter"] = p.glyph()

    # 18. Play
    p = TTGlyphPen(None)
    p.moveTo((260, 140))
    p.lineTo((840, 500))
    p.lineTo((260, 860))
    p.closePath()
    glyphs["play"] = p.glyph()

    return glyphs

def build_font():
    print("Compiling StruXllence Product Icon Font (TTF and WOFF)...")
    fb = FontBuilder(1024, isTTF=True)
    
    glyph_names = [".notdef"] + [data[0] for data in GLYPH_MAP.values()]
    fb.setupGlyphOrder(glyph_names)
    
    cmap = {cp: data[0] for cp, data in GLYPH_MAP.items()}
    fb.setupCharacterMap(cmap)
    
    glyphs = build_glyphs()
    fb.setupGlyf(glyphs)
    
    metrics = {name: (1024, 0) for name in glyph_names}
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-124)
    fb.setupNameTable({
        "familyName": "StruXllence Product Icons",
        "styleName": "Regular",
        "uniqueFontIdentifier": "StruXllence:ProductIcons:2026",
        "fullName": "StruXllence Product Icons Regular",
        "psName": "StruXllenceProductIcons-Regular",
        "version": "Version 1.000"
    })
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-124, sTypoLineGap=0)
    fb.setupPost()
    
    # Save TTF
    ttf_path = os.path.join(FONTS_DIR, "struxllence-product-icons.ttf")
    fb.font.save(ttf_path)
    print(f"  [OK] Saved TTF font: {ttf_path}")
    
    # Save WOFF
    woff_path = os.path.join(FONTS_DIR, "struxllence-product-icons.woff")
    fb.font.flavor = "woff"
    fb.font.save(woff_path)
    print(f"  [OK] Saved WOFF font: {woff_path}")

if __name__ == "__main__":
    build_font()

