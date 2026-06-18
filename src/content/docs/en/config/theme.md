---
title: Theme
description: WebUI and TUI theme configuration and customization
---

# Theme

LingXiao supports dual-interface theme configuration for WebUI and TUI, based on the LingXiao Sword Forge color system.

## WebUI Theme

WebUI supports light and dark dual themes, based on the LingXiao Sword Forge palette:

### Dark Theme

| Color | Hex | Usage |
| --- | --- | --- |
| Ink Black | `#0B0E11` | Background |
| Paper White | `#E8E4D8` | Body text |
| Cyan Edge | `#5FE0C7` | Accent |
| Gold Foil | `#C9A86A` | Decoration |

### Light Theme

| Color | Hex | Usage |
| --- | --- | --- |
| Paper White | `#E8E4D8` | Background |
| Ink Black | `#0B0E11` | Body text |
| Cyan Edge | `#0B8A74` | Accent |
| Gold Foil | `#9d682d` | Decoration |

### Theme Switching

The WebUI provides a theme toggle button in the top-right corner, supporting system follow, light, and dark modes.

## TUI Theme

The TUI terminal interface supports custom color schemes.

## Fonts

| Usage | Font |
| --- | --- |
| Body | Inter + Noto Sans SC |
| Code | JetBrains Mono |

## UI Config

Key settings in the `ui` group:

| Setting | Description |
| --- | --- |
| `language` | UI language: `zh` / `en` (default `zh`) |
| `include_co_authored_by` | Include co-authored-by in Git commits |
| `prompt_suggestion_enabled` | Enable prompt suggestions |

### Language Switching

```bash
# Environment variable
export LINGXIAO_LANGUAGE=en
```

```json
{
  "ui": {
    "language": "en"
  }
}
```

## Documentation Site Theme

The documentation site (based on Astro + Starlight) uses a custom CSS theme:

- Theme file: `site/src/styles/lingxiao-theme.css`
- Color variables defined in `:root` and `[data-theme="dark"]` selectors
- Injected via `astro.config.mjs` `customCss`

### Custom Colors

Modify CSS variables in `site/src/styles/lingxiao-theme.css`:

```css
:root {
  --lx-bg: #0B0E11;
  --lx-text: #E8E4D8;
  --lx-accent: #5FE0C7;
  --lx-gold: #C9A86A;
}
```
