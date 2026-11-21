# Change Log

All notable changes to the **StruXllence Themes** extension suite will be documented in this file.

## [1.0.3] - 2026-11-21

### Added
- Explicit semantic styles for all 23 standard token types, read-only variables/properties and deprecated symbols in both themes. Existing TextMate highlighting remains the fallback.
- Theme-specific diff line/text fills, diff gutter/overview colours and coordinated Git, minimap and editor gutter markers.
- Terminal cursor, selection and search colours, plus matched coverage and calculated contrast regression tests for the dark/light pair.

### Improved
- Refined the existing 16-slot ANSI palettes, particularly bright and neutral text on the light terminal background.
- Deepened light-theme syntax colours and lifted dark comments, keeping semantic and TextMate categories aligned over the diff fills.
- Made terminal, semantic-provider and diff coverage explicit in the Marketplace README, including override and true-colour limitations.
- Replaced unverified universal readability/eye-fatigue claims with the specific scope of the checks performed. Historical release notes below retain their original wording.

This is a theme-only update. It adds no activation code, telemetry, terminal shell integration or external service. The VSIX is prepared for owner publication; packaging does not upload it to Marketplace.

## [1.0.2] - 2026-11-10

### Fixed & Enhanced
- **Official GitHub Repository Integration**: Connected to [`StruXllence/struxllence-themes`](https://github.com/StruXllence/struxllence-themes).
- **Asset CDN Resolution**: Hosted all high-definition banners, theme previews, and icon showcases via GitHub's CDN to ensure immediate, crystal-clear rendering across both the VS Code Marketplace and in-editor extension details view.
- **Authentic Metrics**: Removed static placeholder mock badges in favor of verified store analytics and direct 1-click installation links.

---

## [1.0.1] - 2026-11-10

### Enhanced
- **Marketplace SEO & Discoverability**: Expanded search keywords with high-intent developer discovery queries (eye strain, aesthetic, high contrast, clean, modern, developer tools).
- **1-Click Web Installer**: Added direct `vscode:extension` URI badge for instant browser-to-editor installation.
- **Store Category Compliance**: Standardized gallery classification to `Themes` for seamless Marketplace upload and validation.
- **Documentation Overhaul**: Added comprehensive activation instructions for Color Themes, File Icons, and Product Icons, as well as recommended font ligature pairings and community issue links.

---

## [1.0.0] - 2026-11-01

### Added
- **StruXllence Dark Color Theme**:
  - Deep graphite (`#1E1E1E`) and obsidian (`#111215`) canvas with molten Innovate Orange (`#F57C00`) accents.
  - Accessible, WCAG AAA high-contrast syntax highlighting for Python, TypeScript, Rust, Go, C++, HTML, CSS, JSON, and Markdown.
  - Refined editor UI including subtle line highlighting, git gutters, bracket match borders, and amber search markers.
- **StruXllence Light Color Theme**:
  - Architectural drafting paper and clean concrete aesthetic (`#F8F9FA` / `#FFFFFF`).
  - Warm industrial copper and amber highlights (`#D96B00`) with graphite text (`#1E1E1E`).
- **StruXllence File Icon Themes (Dark & Light)**:
  - Custom 512×512 high-definition master PNG and SVG file icons.
  - Complete coverage for all major programming languages, frameworks (React, Vue, Svelte), configurations, databases, archives, and documents.
- **StruXllence Product Icon Themes (Dark & Light)**:
  - Custom UI icon font (`struxllence-product-icons.woff` / `.ttf`).
  - Styled Activity Bar, Status Bar, Explorer, Terminal, and View glyphs.
- **SEO & Marketplace Publishing Suite**:
  - High-resolution marketplace banners, badges, and documentation.
