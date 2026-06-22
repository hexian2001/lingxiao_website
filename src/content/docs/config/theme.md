---
title: 主题
description: WebUI 与 TUI 主题配置及自定义
---

# 主题

凌霄支持 WebUI 和 TUI 双界面主题配置，基于凌霄剑炉配色体系。

## WebUI 主题

WebUI 支持亮色和暗色双主题，基于凌霄剑炉配色：

### 暗色主题

<div class="doc-color-swatches" role="list" aria-label="暗色主题配色">
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#0B0E11"></span>
    <strong>墨黑</strong><code>#0B0E11</code><em>背景</em>
  </div>
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#E8E4D8"></span>
    <strong>纸白</strong><code>#E8E4D8</code><em>正文文字</em>
  </div>
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#5FE0C7"></span>
    <strong>青锋</strong><code>#5FE0C7</code><em>强调色</em>
  </div>
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#C9A86A"></span>
    <strong>金箔</strong><code>#C9A86A</code><em>装饰色</em>
  </div>
</div>

### 亮色主题

<div class="doc-color-swatches" role="list" aria-label="亮色主题配色">
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#E8E4D8"></span>
    <strong>纸白</strong><code>#E8E4D8</code><em>背景</em>
  </div>
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#0B0E11"></span>
    <strong>墨黑</strong><code>#0B0E11</code><em>正文文字</em>
  </div>
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#0B8A74"></span>
    <strong>青锋</strong><code>#0B8A74</code><em>强调色</em>
  </div>
  <div class="doc-swatch" role="listitem">
    <span class="doc-swatch-chip" style="background:#9d682d"></span>
    <strong>金箔</strong><code>#9d682d</code><em>装饰色</em>
  </div>
</div>

### 主题切换

WebUI 右上角提供主题切换按钮，支持系统跟随、亮色、暗色三种模式。

## TUI 主题

TUI 终端界面支持自定义颜色方案。

## 字体

| 用途 | 字体 |
| --- | --- |
| 正文 | Inter + Noto Sans SC |
| 代码 | JetBrains Mono |

## 界面配置

`ui` 组的关键设置：

| 设置 | 说明 |
| --- | --- |
| `language` | 界面语言：`zh` / `en`（默认 `zh`） |
| `include_co_authored_by` | 是否在 Git commit 中包含 co-authored-by |
| `prompt_suggestion_enabled` | 是否启用提示建议 |

### 语言切换

```bash
# 环境变量
export LINGXIAO_LANGUAGE=en
```

```json
{
  "ui": {
    "language": "en"
  }
}
```

## 文档站主题

文档站（基于 Astro + Starlight）使用自定义 CSS 主题：

- 主题文件：`site/src/styles/lingxiao-theme.css`
- 配色变量定义在 `:root` 和 `[data-theme="dark"]` 选择器中
- 通过 `astro.config.mjs` 的 `customCss` 注入

### 自定义配色

修改 `site/src/styles/lingxiao-theme.css` 中的 CSS 变量：

```css
:root {
  --lx-bg: #0B0E11;
  --lx-text: #E8E4D8;
  --lx-accent: #5FE0C7;
  --lx-gold: #C9A86A;
}
```
