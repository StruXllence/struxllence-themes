"""Generate High Definition Master Icons (512x512 PNGs and SVGs)
for StruXllence File Icon Themes and Product Icon Themes.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFilter
import resvg_py

BASE_DIR = r"c:\Users\srini\Desktop\On Screen\StruXllence\vs-themes"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HD_ASSETS_DIR = os.path.join(ASSETS_DIR, "icons-hd")

FILE_ICONS_HD = os.path.join(BASE_DIR, "icons", "file-icons", "png-hd")
FILE_ICONS_SVG = os.path.join(BASE_DIR, "icons", "file-icons", "svg")

PRODUCT_ICONS_HD = os.path.join(BASE_DIR, "icons", "product-icons", "png-hd")
PRODUCT_ICONS_SVG = os.path.join(BASE_DIR, "icons", "product-icons", "svg")

# Ensure directories exist
for p in [HD_ASSETS_DIR, FILE_ICONS_HD, FILE_ICONS_SVG, PRODUCT_ICONS_HD, PRODUCT_ICONS_SVG]:
    os.makedirs(p, exist_ok=True)

# Master Brand Colors
GRAPHITE = "#1E1E1E"
STEEL = "#6B7280"
INNOVATE = "#F57C00"
INNOVATE_LIGHT = "#FFA726"
CONCRETE = "#E7E7E7"
PURE_WHITE = "#FFFFFF"

# -------------------------------------------------------------
# 1. FILE ICONS SVG DEFINITIONS
# -------------------------------------------------------------
FILE_SVG_DEFS = {
    # Folders
    "folder": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="folderG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#374151" />
      <stop offset="100%" stop-color="#1E1E1E" />
    </linearGradient>
    <linearGradient id="tabG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F57C00" />
      <stop offset="100%" stop-color="#D84315" />
    </linearGradient>
  </defs>
  <!-- Tab -->
  <path d="M15 28 L40 28 L48 38 L85 38 C88 38 90 40 90 43 L90 78 C90 82 87 85 83 85 L17 85 C13 85 10 82 10 78 L10 33 C10 30 12 28 15 28 Z" fill="url(#tabG)" />
  <!-- Folder Body -->
  <path d="M10 42 L90 42 L88 78 C88 82 85 85 81 85 L19 85 C15 85 12 82 12 78 Z" fill="url(#folderG)" stroke="#F57C00" stroke-width="2.5" />
  <line x1="16" y1="52" x2="84" y2="52" stroke="#6B7280" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
</svg>""",

    "folder-open": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="tabG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F57C00" />
      <stop offset="100%" stop-color="#D84315" />
    </linearGradient>
    <linearGradient id="flapG" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4B5563" />
      <stop offset="100%" stop-color="#1E1E1E" />
    </linearGradient>
  </defs>
  <!-- Back Body -->
  <path d="M15 28 L40 28 L48 38 L85 38 C88 38 90 40 90 43 L90 78 C90 82 87 85 83 85 L17 85 C13 85 10 82 10 78 L10 33 C10 30 12 28 15 28 Z" fill="url(#tabG)" />
  <!-- Interior Glow -->
  <rect x="18" y="44" width="64" height="28" fill="#FFA726" opacity="0.3" rx="2"/>
  <!-- Front Flap Angled Open -->
  <polygon points="6,85 18,48 94,48 82,85" fill="url(#flapG)" stroke="#F57C00" stroke-width="2.5" />
</svg>""",

    "folder-root": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="rootTab" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFA726" />
      <stop offset="100%" stop-color="#F57C00" />
    </linearGradient>
  </defs>
  <path d="M15 24 L42 24 L50 34 L85 34 C88 34 90 36 90 39 L90 80 C90 84 87 87 83 87 L17 87 C13 87 10 84 10 80 L10 29 C10 26 12 24 15 24 Z" fill="#1E1E1E" stroke="#F57C00" stroke-width="3" />
  <!-- StruXllence S-Emblem in center -->
  <path d="M42 48 C42 42 48 38 54 38 C60 38 64 42 62 47 C60 52 44 55 42 61 C40 67 46 72 52 72 C58 72 63 68 63 62" fill="none" stroke="url(#rootTab)" stroke-width="5" stroke-linecap="round"/>
</svg>""",

    # Default File
    "file": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="fileG" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2D3039" />
      <stop offset="100%" stop-color="#1A1B20" />
    </linearGradient>
  </defs>
  <!-- Document with folded corner -->
  <path d="M22 15 L62 15 L80 33 L80 82 C80 86 77 89 73 89 L25 89 C21 89 18 86 18 82 L18 19 C18 16 20 15 22 15 Z" fill="url(#fileG)" stroke="#4B5563" stroke-width="2.5" />
  <polygon points="62,15 62,33 80,33" fill="#6B7280" />
  <line x1="28" y1="46" x2="68" y2="46" stroke="#6B7280" stroke-width="2.5" stroke-linecap="round" />
  <line x1="28" y1="58" x2="68" y2="58" stroke="#6B7280" stroke-width="2.5" stroke-linecap="round" />
  <line x1="28" y1="70" x2="52" y2="70" stroke="#F57C00" stroke-width="2.5" stroke-linecap="round" />
</svg>""",

    # Python
    "python": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <defs>
    <linearGradient id="pyAmber" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFA726" />
      <stop offset="100%" stop-color="#F57C00" />
    </linearGradient>
    <linearGradient id="pySteel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9CA3AF" />
      <stop offset="100%" stop-color="#4B5563" />
    </linearGradient>
  </defs>
  <!-- Upper Snake (Steel) -->
  <path d="M49 14 C30 14 31 22 31 22 L31 31 L50 31 L50 34 L22 34 C14 34 8 41 8 50 C8 59 13 63 22 63 L27 63 L27 54 C27 44 36 44 36 44 L55 44 C62 44 67 39 67 32 C67 22 67 14 49 14 Z" fill="url(#pySteel)" />
  <circle cx="38" cy="22" r="3" fill="#FFFFFF" />
  <!-- Lower Snake (Innovate Orange) -->
  <path d="M51 86 C70 86 69 78 69 78 L69 69 L50 69 L50 66 L78 66 C86 66 92 59 92 50 C92 41 87 37 78 37 L73 37 L73 46 C73 56 64 56 64 56 L45 56 C38 56 33 61 33 68 C33 78 33 86 51 86 Z" fill="url(#pyAmber)" />
  <circle cx="62" cy="78" r="3" fill="#1E1E1E" />
</svg>""",

    # TypeScript
    "typescript": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="10" y="10" width="80" height="80" rx="14" fill="#1A1B20" stroke="#007ACC" stroke-width="3" />
  <text x="35" y="65" font-family="'Montserrat', sans-serif" font-weight="900" font-size="46" fill="#007ACC" text-anchor="middle">T</text>
  <text x="65" y="65" font-family="'Montserrat', sans-serif" font-weight="900" font-size="46" fill="#F57C00" text-anchor="middle">S</text>
</svg>""",

    # JavaScript
    "javascript": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="10" y="10" width="80" height="80" rx="14" fill="#1A1B20" stroke="#F57C00" stroke-width="3" />
  <text x="36" y="65" font-family="'Montserrat', sans-serif" font-weight="900" font-size="44" fill="#FFA726" text-anchor="middle">J</text>
  <text x="66" y="65" font-family="'Montserrat', sans-serif" font-weight="900" font-size="44" fill="#F57C00" text-anchor="middle">S</text>
</svg>""",

    # HTML
    "html": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <polygon points="16,14 84,14 78,78 50,88 22,78" fill="#1A1B20" stroke="#F57C00" stroke-width="3" />
  <polygon points="50,22 75,22 71,72 50,80" fill="#F57C00" opacity="0.3" />
  <text x="50" y="60" font-family="'Montserrat', sans-serif" font-weight="900" font-size="34" fill="#FFA726" text-anchor="middle">&lt;/&gt;</text>
</svg>""",

    # CSS
    "css": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <polygon points="16,14 84,14 78,78 50,88 22,78" fill="#1A1B20" stroke="#38BDF8" stroke-width="3" />
  <text x="50" y="60" font-family="'Montserrat', sans-serif" font-weight="900" font-size="32" fill="#38BDF8" text-anchor="middle">#</text>
  <circle cx="50" cy="50" r="16" fill="none" stroke="#F57C00" stroke-width="3" />
</svg>""",

    # SCSS / Sass
    "scss": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="12" y="12" width="76" height="76" rx="14" fill="#1A1B20" stroke="#EC4899" stroke-width="3" />
  <text x="50" y="62" font-family="'Montserrat', sans-serif" font-weight="900" font-size="32" fill="#EC4899" text-anchor="middle">SASS</text>
</svg>""",

    # JSON
    "json": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="12" y="12" width="76" height="76" rx="14" fill="#1A1B20" stroke="#F57C00" stroke-width="2.5" />
  <text x="50" y="64" font-family="'Montserrat', sans-serif" font-weight="900" font-size="44" fill="#FFA726" text-anchor="middle">{ }</text>
</svg>""",

    # YAML
    "yaml": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="12" y="12" width="76" height="76" rx="14" fill="#1A1B20" stroke="#A855F7" stroke-width="2.5" />
  <text x="50" y="62" font-family="'Montserrat', sans-serif" font-weight="900" font-size="28" fill="#E7E7E7" text-anchor="middle">YML</text>
</svg>""",

    # Markdown
    "markdown": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="8" y="20" width="84" height="60" rx="8" fill="#1A1B20" stroke="#E7E7E7" stroke-width="3" />
  <polyline points="20,62 20,38 32,50 44,38 44,62" fill="none" stroke="#E7E7E7" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="68" y1="38" x2="68" y2="62" stroke="#F57C00" stroke-width="4" stroke-linecap="round"/>
  <polyline points="58,52 68,62 78,52" fill="none" stroke="#F57C00" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    # C / C++ / C#
    "c": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <polygon points="50,12 85,30 85,70 50,88 15,70 15,30" fill="#1A1B20" stroke="#0284C7" stroke-width="3"/>
  <text x="50" y="64" font-family="'Montserrat', sans-serif" font-weight="900" font-size="44" fill="#0284C7" text-anchor="middle">C</text>
</svg>""",

    "cpp": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <polygon points="50,12 85,30 85,70 50,88 15,70 15,30" fill="#1A1B20" stroke="#00599C" stroke-width="3"/>
  <text x="36" y="62" font-family="'Montserrat', sans-serif" font-weight="900" font-size="38" fill="#00599C" text-anchor="middle">C</text>
  <text x="66" y="58" font-family="'Montserrat', sans-serif" font-weight="900" font-size="28" fill="#F57C00" text-anchor="middle">++</text>
</svg>""",

    "csharp": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <polygon points="50,12 85,30 85,70 50,88 15,70 15,30" fill="#1A1B20" stroke="#9333EA" stroke-width="3"/>
  <text x="36" y="62" font-family="'Montserrat', sans-serif" font-weight="900" font-size="38" fill="#9333EA" text-anchor="middle">C</text>
  <text x="66" y="58" font-family="'Montserrat', sans-serif" font-weight="900" font-size="28" fill="#F57C00" text-anchor="middle">#</text>
</svg>""",

    # Rust
    "rust": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="50" cy="50" r="32" fill="#1A1B20" stroke="#F57C00" stroke-width="4" stroke-dasharray="14 6"/>
  <circle cx="50" cy="50" r="18" fill="none" stroke="#E7E7E7" stroke-width="3"/>
  <text x="50" y="60" font-family="'Montserrat', sans-serif" font-weight="900" font-size="28" fill="#FFA726" text-anchor="middle">R</text>
</svg>""",

    # Go
    "go": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="12" y="12" width="76" height="76" rx="14" fill="#1A1B20" stroke="#00ADD8" stroke-width="3"/>
  <text x="50" y="62" font-family="'Montserrat', sans-serif" font-weight="900" font-size="36" fill="#00ADD8" text-anchor="middle">GO</text>
</svg>""",

    # Java
    "java": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="12" y="12" width="76" height="76" rx="14" fill="#1A1B20" stroke="#EA580C" stroke-width="3"/>
  <path d="M30 46 C30 62 42 66 50 66 C58 66 70 62 70 46 Z" fill="#F57C00"/>
  <path d="M70 48 C76 48 80 52 80 56 C80 60 75 62 70 62" fill="none" stroke="#F57C00" stroke-width="3"/>
  <path d="M42 38 C42 32 46 30 50 24 C54 30 58 32 58 38" fill="none" stroke="#FFA726" stroke-width="2.5"/>
</svg>""",

    # Git
    "git": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="14" y="14" width="72" height="72" rx="14" transform="rotate(45 50 50)" fill="#1A1B20" stroke="#F05032" stroke-width="3.5" />
  <circle cx="50" cy="35" r="5" fill="#F05032"/>
  <circle cx="50" cy="65" r="5" fill="#F05032"/>
  <circle cx="68" cy="50" r="5" fill="#F57C00"/>
  <line x1="50" y1="35" x2="50" y2="65" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M50 48 Q 50 50 68 50" fill="none" stroke="#FFFFFF" stroke-width="3"/>
</svg>""",

    # Docker
    "docker": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M12 55 C12 75 35 78 50 78 C75 78 88 65 92 50 C86 50 82 54 78 54 C74 42 65 42 60 42 L12 42 Z" fill="#1A1B20" stroke="#0DB7ED" stroke-width="3"/>
  <rect x="30" y="28" width="10" height="10" fill="#0DB7ED" rx="1"/>
  <rect x="44" y="28" width="10" height="10" fill="#0DB7ED" rx="1"/>
  <rect x="58" y="28" width="10" height="10" fill="#F57C00" rx="1"/>
</svg>""",

    # Database / SQL
    "database": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <ellipse cx="50" cy="28" rx="32" ry="12" fill="#1A1B20" stroke="#F57C00" stroke-width="3"/>
  <path d="M18 28 V50 C18 57 32 62 50 62 C68 62 82 57 82 50 V28" fill="#1A1B20" stroke="#F57C00" stroke-width="3"/>
  <path d="M18 50 V72 C18 79 32 84 50 84 C68 84 82 79 82 72 V50" fill="#1A1B20" stroke="#F57C00" stroke-width="3"/>
  <line x1="32" y1="50" x2="68" y2="50" stroke="#FFA726" stroke-width="2"/>
  <line x1="32" y1="72" x2="68" y2="72" stroke="#FFA726" stroke-width="2"/>
</svg>""",

    # Shell / Bash
    "shell": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="10" y="16" width="80" height="68" rx="10" fill="#1A1B20" stroke="#10B981" stroke-width="3"/>
  <polyline points="26,38 40,50 26,62" fill="none" stroke="#F57C00" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="48" y1="62" x2="72" y2="62" stroke="#10B981" stroke-width="4" stroke-linecap="round"/>
</svg>""",

    # React
    "react": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <ellipse cx="50" cy="50" rx="38" ry="14" fill="none" stroke="#61DAFB" stroke-width="2.5"/>
  <ellipse cx="50" cy="50" rx="38" ry="14" transform="rotate(60 50 50)" fill="none" stroke="#61DAFB" stroke-width="2.5"/>
  <ellipse cx="50" cy="50" rx="38" ry="14" transform="rotate(120 50 50)" fill="none" stroke="#61DAFB" stroke-width="2.5"/>
  <circle cx="50" cy="50" r="6" fill="#F57C00"/>
</svg>""",

    # Settings / Config
    "settings": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="50" cy="50" r="32" fill="#1A1B20" stroke="#6B7280" stroke-width="6" stroke-dasharray="14 6"/>
  <circle cx="50" cy="50" r="14" fill="none" stroke="#F57C00" stroke-width="4"/>
</svg>""",

    # Lock / Secret
    "lock": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M30 46 V32 C30 20 40 14 50 14 C60 14 70 20 70 32 V46" fill="none" stroke="#FFA726" stroke-width="4"/>
  <rect x="22" y="46" width="56" height="42" rx="8" fill="#1A1B20" stroke="#F57C00" stroke-width="3"/>
  <circle cx="50" cy="64" r="5" fill="#FFA726"/>
  <line x1="50" y1="69" x2="50" y2="76" stroke="#FFA726" stroke-width="3"/>
</svg>""",

    # Image
    "image": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="14" y="18" width="72" height="64" rx="8" fill="#1A1B20" stroke="#6B7280" stroke-width="3"/>
  <circle cx="34" cy="36" r="6" fill="#F57C00"/>
  <polyline points="20,72 40,48 58,66 68,56 80,72" fill="none" stroke="#E7E7E7" stroke-width="3" stroke-linejoin="round"/>
</svg>""",

    # Archive
    "archive": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M22 15 L62 15 L80 33 L80 82 C80 86 77 89 73 89 L25 89 C21 89 18 86 18 82 L18 19 Z" fill="#1A1B20" stroke="#F57C00" stroke-width="2.5" />
  <line x1="50" y1="15" x2="50" y2="89" stroke="#6B7280" stroke-width="2"/>
  <rect x="46" y="30" width="8" height="4" fill="#FFA726"/>
  <rect x="46" y="42" width="8" height="4" fill="#FFA726"/>
  <rect x="46" y="54" width="8" height="4" fill="#FFA726"/>
  <rect x="44" y="66" width="12" height="10" fill="#F57C00" rx="2"/>
</svg>""",

    # License / Legal
    "license": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M22 15 L62 15 L80 33 L80 82 C80 86 77 89 73 89 L25 89 C21 89 18 86 18 82 L18 19 Z" fill="#1A1B20" stroke="#F57C00" stroke-width="2.5" />
  <circle cx="50" cy="56" r="14" fill="none" stroke="#FFA726" stroke-width="3"/>
  <path d="M44 68 L42 82 L50 78 L58 82 L56 68" fill="#F57C00"/>
  <text x="50" y="62" font-family="'Montserrat', sans-serif" font-weight="900" font-size="14" fill="#FFA726" text-anchor="middle">&#167;</text>
</svg>"""
}

# -------------------------------------------------------------
# 2. PRODUCT ICONS SVG DEFINITIONS
# -------------------------------------------------------------
PRODUCT_SVG_DEFS = {
    "explorer": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="18" y="24" width="46" height="62" rx="4" fill="#1E1E1E" stroke="#E7E7E7" stroke-width="5"/>
  <rect x="36" y="14" width="46" height="62" rx="4" fill="#1E1E1E" stroke="#F57C00" stroke-width="5"/>
</svg>""",

    "search": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="44" cy="44" r="26" fill="none" stroke="#E7E7E7" stroke-width="6"/>
  <circle cx="44" cy="44" r="12" fill="none" stroke="#F57C00" stroke-width="3"/>
  <line x1="63" y1="63" x2="86" y2="86" stroke="#F57C00" stroke-width="8" stroke-linecap="round"/>
</svg>""",

    "scm": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="32" cy="28" r="8" fill="#F57C00"/>
  <circle cx="32" cy="72" r="8" fill="#E7E7E7"/>
  <circle cx="68" cy="48" r="8" fill="#F57C00"/>
  <line x1="32" y1="36" x2="32" y2="64" stroke="#E7E7E7" stroke-width="5"/>
  <path d="M32 48 C48 48 60 48 68 48" fill="none" stroke="#F57C00" stroke-width="5"/>
</svg>""",

    "debug": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <polygon points="50,15 82,30 82,62 50,85 18,62 18,30" fill="#1E1E1E" stroke="#E7E7E7" stroke-width="5"/>
  <polygon points="42,38 66,50 42,62" fill="#F57C00"/>
</svg>""",

    "extensions": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="18" y="18" width="28" height="28" rx="4" fill="#F57C00"/>
  <rect x="54" y="18" width="28" height="28" rx="4" fill="#6B7280"/>
  <rect x="18" y="54" width="28" height="28" rx="4" fill="#6B7280"/>
  <rect x="54" y="54" width="28" height="28" rx="4" fill="#E7E7E7"/>
</svg>""",

    "settings-gear": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="50" cy="50" r="34" fill="none" stroke="#E7E7E7" stroke-width="8" stroke-dasharray="16 8"/>
  <circle cx="50" cy="50" r="16" fill="none" stroke="#F57C00" stroke-width="6"/>
</svg>""",

    "account": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="50" cy="34" r="16" fill="none" stroke="#E7E7E7" stroke-width="5"/>
  <path d="M22 80 C22 62 34 54 50 54 C66 54 78 62 78 80" fill="none" stroke="#F57C00" stroke-width="5" stroke-linecap="round"/>
</svg>""",

    "bell": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M50 18 C38 18 30 26 30 38 V54 L22 66 H78 L70 54 V38 C70 26 62 18 50 18 Z" fill="#1E1E1E" stroke="#E7E7E7" stroke-width="5"/>
  <circle cx="50" cy="78" r="6" fill="#F57C00"/>
</svg>""",

    "terminal": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="14" y="20" width="72" height="60" rx="8" fill="#1E1E1E" stroke="#6B7280" stroke-width="5"/>
  <polyline points="28,40 40,50 28,60" fill="none" stroke="#F57C00" stroke-width="5" stroke-linecap="round"/>
  <line x1="48" y1="62" x2="68" y2="62" stroke="#E7E7E7" stroke-width="5" stroke-linecap="round"/>
</svg>""",

    "split-horizontal": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect x="16" y="20" width="68" height="60" rx="6" fill="none" stroke="#E7E7E7" stroke-width="5"/>
  <line x1="50" y1="20" x2="50" y2="80" stroke="#F57C00" stroke-width="5"/>
</svg>""",

    "close": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <line x1="25" y1="25" x2="75" y2="75" stroke="#F57C00" stroke-width="8" stroke-linecap="round"/>
  <line x1="75" y1="25" x2="25" y2="75" stroke="#E7E7E7" stroke-width="8" stroke-linecap="round"/>
</svg>"""
}

def generate_all_icons():
    print("Generating High-Definition Master Icons (512x512 PNGs and SVGs)...")

    # 1. File Icons
    for name, svg in FILE_SVG_DEFS.items():
        # Save SVG
        svg_path = os.path.join(FILE_ICONS_SVG, f"{name}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg)
            
        # Render 512x512 Master HD PNG
        png_data = resvg_py.svg_to_bytes(svg_string=svg, width=512, height=512)
        hd_path = os.path.join(FILE_ICONS_HD, f"{name}.png")
        with open(hd_path, "wb") as f:
            f.write(png_data)

    print(f"  [OK] Generated {len(FILE_SVG_DEFS)} File Icons in SVG and 512x512 PNG.")

    # 2. Product Icons
    for name, svg in PRODUCT_SVG_DEFS.items():
        svg_path = os.path.join(PRODUCT_ICONS_SVG, f"{name}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg)
            
        png_data = resvg_py.svg_to_bytes(svg_string=svg, width=512, height=512)
        hd_path = os.path.join(PRODUCT_ICONS_HD, f"{name}.png")
        with open(hd_path, "wb") as f:
            f.write(png_data)

    print(f"  [OK] Generated {len(PRODUCT_SVG_DEFS)} Product Icons in SVG and 512x512 PNG.")

    # 3. Extension Marketplace Icon (256x256)
    # Generated from authentic 3D master emblem via generate_previews.py
    from generate_previews import build_extension_icon
    build_extension_icon()

if __name__ == "__main__":
    generate_all_icons()
