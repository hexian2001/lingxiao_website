---
title: 主题
description: WebUI 与 TUI 主题配置及自定义
---

# 主题

凌霄支持 WebUI 和 TUI 双界面主题配置，基于凌霄剑炉配色体系。

## WebUI 主题

WebUI 支持亮色和暗色双主题，基于凌霄剑炉配色：

### 暗色主题

| 色彩 | 色值 | 用途 |
| --- | --- | --- |
| 墨黑 | `#0B0E11` | 背景 |
| 纸白 | `#E8E4D8` | 正文文字 |
| 青锋 | `#5FE0C7` | 强调色 |
| 金箔 | `#C9A86A` | 装饰色 |

### 亮色主题

| 色彩 | 色值 | 用途 |
| --- | --- | --- |
| 纸白 | `#E8E4D8` | 背景 |
| 墨黑 | `#0B0E11` | 正文文字 |
| 青锋 | `#0B8A74` | 强调色 |
| 金箔 | `#9d682d` | 装饰色 |

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
