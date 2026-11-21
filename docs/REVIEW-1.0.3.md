# Theme coverage review — 21 Nov 2026

The extension is developed in `C:\Users\srini\Desktop\On Screen\StruXllence\vs-themes`, in the existing `StruXllence/struxllence-themes` Git repository. Its two colour themes are under `themes/`. File and product icon definitions remain under `icons/`.

## Finding in published 1.0.2

The Marketplace VSIX downloaded during review reports version 1.0.2. Both its bundled theme JSONs explicitly define all 16 ANSI colours and terminal foreground/background. Both set `semanticHighlighting: true`, but neither defines `semanticTokenColors` or contributes new semantic token scopes. VS Code uses its fallback semantic-to-TextMate mapping. Git/editor gutter colours are defined; diff line and changed-text backgrounds are not.

The member's question is in [reply 2, post 7 of the theme thread](https://forum.struxllence.com/showthread.php?tid=3&pid=7#pid7), by `nathantaylor`. A proposed response is saved in [FORUM-REPLY-1.0.3.txt](FORUM-REPLY-1.0.3.txt). It has not been posted.

## Prepared changes

- Matched key/selector coverage in dark and light themes. There are 26 explicit semantic selectors: 23 standard types, read-only variables/properties and a deprecated-symbol modifier. Standard types are styled; the extension does not implement a semantic token provider or invent language classifications.
- Explicit translucent diff line and changed-text fills, diff gutter/overview colours, editor and minimap markers, plus Git resource decorations. Plain diff TextMate additions/removals/changes are also defined.
- Revised 16-slot ANSI palettes, cursor, selection and terminal search colours. Light ANSI whites are readable dark neutrals on the pale background; dark ANSI black remains deliberately dark for programs using that slot as a background.
- Coordinated TextMate and semantic foregrounds, deeper light colours and clearer dark comments. The broader workbench and icon designs remain intact.
- Updated Marketplace text and real VS Code previews. Unverified universal eye-fatigue/accessibility claims were replaced by the particular checks performed. Historical change notes are labelled as historical.

## Verification and limits

Eight regression tests cover dark/light key parity, 23 standard semantic types, semantic/TextMate correspondence, translucent diff overlays, contributed resources and lack of runtime entry points. Every defined syntax and semantic foreground is checked at 4.5:1 or more against the base editor background and inserted/removed line, text and combined diff fills. ANSI foregrounds are checked against the terminal's default background, with the documented dark ANSI-black exception. This is a bounded numerical check, not a certification of all application states, arbitrary ANSI foreground/background combinations or personal comfort.

The actual themes were loaded in isolated Windows profiles in VS Code **1.147.0** and Insiders **1.148.0-insider**. For each application, six views cover dark/light semantic source, the real diff editor and the real integrated terminal. Checks read registered colour variables, actual TypeScript span colours and actual rendered xterm colours for all 16 ANSI slots. The TypeScript provider returned 29 tokens covering class, interface, enum, enum member, method, parameter, property and variable, including read-only modifiers. No provider coverage is claimed for untested languages.

Terminal minimum-contrast adjustment was set to 1 during rendering checks to expose the supplied palette directly. Normal user defaults may adjust terminal text. The existing `^1.74.0` manifest remains; VS Code 1.74 was not runtime-tested. Current versions ignore colour identifiers they do not use. User theme/token overrides, language-provider differences and 256-colour/true-colour terminal programs remain outside the palette guarantee.

No user VS Code profile was changed. The extension continues to have no runtime activation code, telemetry, network service or shell integration. Test harnesses, development dependencies, private isolated profiles and review notes are excluded from the VSIX. Only static themes, icon resources and listing materials are distributed.

The pinned packaging tool uses an override to patched `minimatch` 11.0.1 for [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249). Packaging and archive-resource checks were rerun with that override; no packaging dependency is distributed as extension runtime code.

## Build and publish

Use Node.js 22 or later for the pinned `@vscode/vsce` development tool:

```powershell
npm ci --ignore-scripts
npm test
npm run package
```

The owner uploads `struxllence-themes-1.0.3.vsix` through the existing StruXllence publisher's **Update** action. Packaging and source control do not publish to Marketplace. The reply must retain its prepared/unpublished wording until the store update is actually visible.

## Primary references

- [VS Code semantic highlight guide: explicit rules and fallback behaviour](https://code.visualstudio.com/api/language-extensions/semantic-highlight-guide)
- [VS Code theme colour reference: terminal and diff identifiers](https://code.visualstudio.com/api/references/theme-color)
- [VS Code built-in commands: semantic tokens and diff editor](https://code.visualstudio.com/api/references/commands)
- [VS Code publishing guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
