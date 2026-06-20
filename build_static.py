#!/usr/bin/env python3
"""把 site/src/content/docs 的 MD 转成纯 HTML 站点。"""
import os, re, html, shutil
from pathlib import Path

DOCS_SRC = Path("/root/lingxiao/lingxiao_cli/site/src/content/docs")
OUTPUT   = Path("/root/lingxiao/lingxiao_cli/site/static")
HOMEPAGE = Path("/root/lingxiao/lingxiao_cli/site/static/index.html")

# ===== 侧栏结构（与 astro.config.mjs 一致）=====
ZH_SIDEBAR = [
    {"label": "入门", "items": [
        ("简介", "getting-started/introduction"),
        ("安装与启动", "getting-started/install"),
        ("连接模型", "getting-started/connect-models"),
        ("第一次运行", "getting-started/first-run"),
    ]},
    {"label": "核心功能", "items": [
        ("专家团系统", "core/expert-team"),
        ("任务DAG编排", "core/task-dag"),
        ("全状态同步", "core/state-sync"),
        ("WebUI指挥中心", "core/webui"),
        ("工具内核", "core/tool-kernel"),
        ("编排验收", "core/orchestration"),
        ("MCP 与 Skills", "core/mcp-skills"),
        ("持久记忆", "core/memory"),
        ("Eternal自治模式", "core/eternal"),
        ("LLM Gateway", "core/llm-gateway"),
    ]},
    {"label": "配置与自定义", "items": [
        ("环境变量", "config/env-vars"),
        ("模型配置", "config/models"),
        ("权限系统", "config/permissions"),
        ("网络配置", "config/network"),
        ("主题", "config/theme"),
        ("自定义命令", "config/custom-commands"),
        ("MCP", "config/mcp"),
        ("Agents", "config/agents"),
        ("Skills 系统", "config/skills"),
        ("规则", "config/rules"),
    ]},
    {"label": "参考", "items": [
        ("CLI命令", "reference/cli"),
        ("Slash命令", "reference/slash-commands"),
        ("架构概览", "reference/architecture"),
        ("API契约索引", "reference/api-index"),
        ("FAQ", "reference/faq"),
        ("安全须知", "reference/security"),
        ("更新日志", "reference/changelog"),
    ]},
]

EN_SIDEBAR = [
    {"label": "Getting Started", "items": [
        ("Introduction", "en/getting-started/introduction"),
        ("Installation", "en/getting-started/install"),
        ("Connect Models", "en/getting-started/connect-models"),
        ("First Run", "en/getting-started/first-run"),
    ]},
    {"label": "Core Features", "items": [
        ("Expert Panel", "en/core/expert-team"),
        ("Task DAG", "en/core/task-dag"),
        ("State Sync", "en/core/state-sync"),
        ("WebUI Center", "en/core/webui"),
        ("Tool Kernel", "en/core/tool-kernel"),
        ("Orchestration", "en/core/orchestration"),
        ("MCP & Skills", "en/core/mcp-skills"),
        ("Memory", "en/core/memory"),
        ("Eternal Mode", "en/core/eternal"),
        ("LLM Gateway", "en/core/llm-gateway"),
    ]},
    {"label": "Configuration", "items": [
        ("Environment Variables", "en/config/env-vars"),
        ("Models", "en/config/models"),
        ("Permissions", "en/config/permissions"),
        ("Network", "en/config/network"),
        ("Theme", "en/config/theme"),
        ("Custom Commands", "en/config/custom-commands"),
        ("MCP", "en/config/mcp"),
        ("Agents", "en/config/agents"),
        ("Skills", "en/config/skills"),
        ("Rules", "en/config/rules"),
    ]},
    {"label": "Reference", "items": [
        ("CLI", "en/reference/cli"),
        ("Slash Commands", "en/reference/slash-commands"),
        ("Architecture", "en/reference/architecture"),
        ("API Index", "en/reference/api-index"),
        ("FAQ", "en/reference/faq"),
        ("Security", "en/reference/security"),
        ("Changelog", "en/reference/changelog"),
    ]},
]

def get_flat_list(sidebar):
    """把侧栏拍平成有序列表，用于上下页导航。"""
    flat = []
    for group in sidebar:
        for label, slug in group["items"]:
            flat.append((label, slug))
    return flat

def get_prev_next(slug, sidebar):
    flat = get_flat_list(sidebar)
    for i, (label, s) in enumerate(flat):
        if s == slug:
            prev = flat[i-1] if i > 0 else None
            nxt  = flat[i+1] if i < len(flat)-1 else None
            return prev, nxt
    return None, None

def is_ascii_art(text):
    """检测是否是 ASCII 架构图。"""
    indicators = ["──→", "──>", "┌", "└", "├", "│", "▼", "◄", "►", "┼"]
    return any(ind in text for ind in indicators)

def md_to_html(md_text):
    """简易 Markdown → HTML 转换，去掉 ASCII 架构图。"""
    lines = md_text.split("\n")
    result = []
    in_code = False
    code_lang = ""
    code_lines = []
    in_table = False
    table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # 代码块
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_lang = line.strip()[3:]
                code_lines = []
            else:
                in_code = False
                code_content = "\n".join(code_lines)
                # 跳过 ASCII 架构图
                if is_ascii_art(code_content):
                    result.append('<div class="ascii-art-removed"><em>（架构图已省略，详见 <a href="/docs/reference/architecture/">架构概览</a>）</em></div>')
                else:
                    escaped = html.escape(code_content)
                    lang_class = f' class="lang-{code_lang}"' if code_lang else ""
                    result.append(f'<pre><code{lang_class}>{escaped}</code></pre>')
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # 表格
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            # 跳过分隔行
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()):
                i += 1
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table and table_rows:
                # 输出表格
                result.append('<div class="table-wrap"><table>')
                if table_rows:
                    result.append("<thead><tr>")
                    for cell in table_rows[0]:
                        result.append(f"<th>{inline_md(cell)}</th>")
                    result.append("</tr></thead><tbody>")
                    for row in table_rows[1:]:
                        result.append("<tr>")
                        for cell in row:
                            result.append(f"<td>{inline_md(cell)}</td>")
                        result.append("</tr>")
                    result.append("</tbody></table></div>")
                in_table = False
                table_rows = []

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = inline_md(m.group(2))
            result.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # 引用块
        if line.strip().startswith(">"):
            quote_text = inline_md(line.strip()[1:].strip())
            result.append(f"<blockquote>{quote_text}</blockquote>")
            i += 1
            continue

        # 列表
        if re.match(r'^[\s]*[-*]\s', line):
            result.append("<ul>")
            while i < len(lines) and re.match(r'^[\s]*[-*]\s', lines[i]):
                item_text = inline_md(re.sub(r'^[\s]*[-*]\s+', '', lines[i]))
                result.append(f"<li>{item_text}</li>")
                i += 1
            result.append("</ul>")
            continue

        # 有序列表
        if re.match(r'^[\s]*\d+\.\s', line):
            result.append("<ol>")
            while i < len(lines) and re.match(r'^[\s]*\d+\.\s', lines[i]):
                item_text = inline_md(re.sub(r'^[\s]*\d+\.\s+', '', lines[i]))
                result.append(f"<li>{item_text}</li>")
                i += 1
            result.append("</ol>")
            continue

        # 水平线
        if line.strip() in ("---", "***", "___"):
            result.append("<hr>")
            i += 1
            continue

        # 空行
        if not line.strip():
            i += 1
            continue

        # 普通段落
        para = inline_md(line.strip())
        result.append(f"<p>{para}</p>")
        i += 1

    # 收尾表格
    if in_table and table_rows:
        result.append('<div class="table-wrap"><table>')
        if table_rows:
            result.append("<thead><tr>")
            for cell in table_rows[0]:
                result.append(f"<th>{inline_md(cell)}</th>")
            result.append("</tr></thead><tbody>")
            for row in table_rows[1:]:
                result.append("<tr>")
                for cell in row:
                    result.append(f"<td>{inline_md(cell)}</td>")
                result.append("</tr>")
            result.append("</tbody></table></div>")

    return "\n".join(result)

def inline_md(text):
    """处理行内 Markdown。"""
    # 链接
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # 粗体
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # 行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def parse_frontmatter(md_text):
    """解析 YAML frontmatter，返回 (meta, body)。"""
    if md_text.startswith("---"):
        end = md_text.find("---", 3)
        if end > 0:
            fm = md_text[3:end].strip()
            body = md_text[end+3:].strip()
            meta = {}
            for line in fm.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            return meta, body
    return {}, md_text

def build_sidebar_html(current_slug, sidebar, is_en):
    """生成侧栏 HTML。"""
    parts = []
    for group in sidebar:
        parts.append(f'<div class="sidebar-group">')
        parts.append(f'<div class="sidebar-group-label">{html.escape(group["label"])}</div>')
        for label, slug in group["items"]:
            active = " active" if slug == current_slug else ""
            href = f"/docs/{slug}/"
            parts.append(f'<a href="{href}" class="sidebar-link{active}">{html.escape(label)}</a>')
        parts.append('</div>')
    return "\n".join(parts)

def build_prev_next(prev, nxt, is_en):
    """生成上下页导航 HTML。"""
    parts = ['<div class="prev-next">']
    if prev:
        label, slug = prev
        parts.append(f'<a href="/docs/{slug}/" class="prev-page"><span class="pn-label">← { "Previous" if is_en else "上一页"}</span><span class="pn-title">{html.escape(label)}</span></a>')
    else:
        parts.append('<span></span>')
    if nxt:
        label, slug = nxt
        parts.append(f'<a href="/docs/{slug}/" class="next-page"><span class="pn-label">{ "Next" if is_en else "下一页"} →</span><span class="pn-title">{html.escape(label)}</span></a>')
    else:
        parts.append('<span></span>')
    parts.append('</div>')
    return "\n".join(parts)

def build_page(title, content_html, sidebar_html, prev_next_html, is_en):
    """组装完整 HTML 页面。"""
    lang = "en" if is_en else "zh-CN"
    nav_docs = "/docs/en/getting-started/introduction/" if is_en else "/docs/getting-started/introduction/"
    
    return f'''<!DOCTYPE html>
<html lang="{lang}" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} | 凌霄剑域</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E5%89%91%3C/text%3E%3C/svg%3E">
<style>
:root {{
  --ink-bg:#0a0c10;--ink-deep:#06080c;--ink-mid:#12151b;
  --ink-card:rgba(18,21,27,0.85);--ink-border:rgba(200,211,213,0.12);
  --ink-border-strong:rgba(200,211,213,0.22);
  --cloud-white:#EAE8E2;--cloud-gray:#C8D3D5;
  --gold:#D4AF37;--gold-soft:#b89968;--gold-dim:rgba(212,175,55,0.15);
  --jade:#5ba897;--fg:#e8e6e1;--fg-muted:#9a9a95;--fg-dim:#555b64;
  --font-sans:'Inter','Noto Sans SC',system-ui,sans-serif;
  --font-serif:'Noto Serif SC','Songti SC',serif;
  --font-mono:'JetBrains Mono','Fira Code',monospace;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-sans);background:var(--ink-deep);color:var(--fg);-webkit-font-smoothing:antialiased;overflow-x:hidden}}

/* 水墨背景 */
.ink-bg{{position:fixed;inset:0;z-index:0;pointer-events:none;opacity:0.06;
  background:
    radial-gradient(ellipse 80% 50% at 20% 0%,var(--cloud-gray) 0%,transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 100%,var(--cloud-white) 0%,transparent 50%),
    linear-gradient(180deg,var(--ink-deep) 0%,var(--ink-bg) 50%,var(--ink-deep) 100%)}}

/* 导航 */
.nav{{position:fixed;top:0;left:0;right:0;z-index:100;backdrop-filter:blur(20px) saturate(140%);-webkit-backdrop-filter:blur(20px) saturate(140%);background:rgba(6,8,12,0.7);border-bottom:1px solid var(--ink-border)}}
.nav-inner{{max-width:1400px;margin:0 auto;padding:0.75rem 1.5rem;display:flex;align-items:center;justify-content:space-between}}
.nav-brand{{display:flex;align-items:center;gap:0.625rem;font-weight:700;font-size:1.05rem;color:var(--fg);text-decoration:none}}
.nav-brand .brand-mark{{width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,var(--gold),var(--gold-soft));display:flex;align-items:center;justify-content:center;font-family:var(--font-serif);font-size:1.1rem;color:var(--ink-deep);font-weight:900}}
.nav-brand .brand-sub{{font-size:0.7rem;font-weight:500;color:var(--fg-muted);letter-spacing:0.05em}}
.nav-links{{display:flex;align-items:center;gap:1.5rem}}
.nav-links a{{font-size:0.875rem;color:var(--fg-muted);text-decoration:none;transition:color 0.2s}}
.nav-links a:hover{{color:var(--gold)}}

/* 文档布局 */
.doc-layout{{position:relative;z-index:1;display:flex;max-width:1400px;margin:0 auto;padding-top:64px;min-height:100vh}}

/* 侧栏 */
.doc-sidebar{{position:sticky;top:64px;width:260px;height:calc(100vh - 64px);overflow-y:auto;padding:1.5rem 0.75rem;border-right:1px solid var(--ink-border);flex-shrink:0}}
.sidebar-group{{margin-bottom:1.5rem}}
.sidebar-group-label{{font-size:0.7rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--fg-dim);padding:0 0.875rem 0.5rem}}
.sidebar-link{{display:block;padding:0.4rem 0.875rem;border-radius:6px;font-size:0.82rem;color:var(--fg-muted);text-decoration:none;transition:all 0.15s;line-height:1.5}}
.sidebar-link:hover{{background:rgba(200,211,213,0.06);color:var(--fg)}}
.sidebar-link.active{{background:var(--gold-dim);color:var(--gold);font-weight:500}}

/* 主内容 */
.doc-main{{flex:1;padding:2rem 3rem;max-width:900px;min-width:0}}
.doc-content h1{{font-family:var(--font-serif);font-size:2.2rem;font-weight:700;margin-bottom:1.5rem;color:var(--fg);letter-spacing:-0.01em}}
.doc-content h2{{font-family:var(--font-serif);font-size:1.5rem;font-weight:600;margin:2rem 0 1rem;color:var(--fg);border-bottom:1px solid var(--ink-border);padding-bottom:0.5rem}}
.doc-content h3{{font-size:1.15rem;font-weight:600;margin:1.5rem 0 0.75rem;color:var(--fg)}}
.doc-content p{{font-size:0.9rem;line-height:1.8;color:var(--fg-muted);margin-bottom:1rem}}
.doc-content strong{{color:var(--gold);font-weight:600}}
.doc-content a{{color:var(--jade);text-decoration:none;transition:color 0.2s}}
.doc-content a:hover{{color:var(--gold)}}
.doc-content ul,.doc-content ol{{margin:0.5rem 0 1rem 1.5rem}}
.doc-content li{{font-size:0.9rem;line-height:1.8;color:var(--fg-muted);margin-bottom:0.25rem}}
.doc-content blockquote{{border-left:3px solid var(--gold-soft);padding:0.5rem 1rem;margin:1rem 0;background:rgba(212,175,55,0.05);border-radius:0 6px 6px 0;color:var(--fg-muted);font-size:0.875rem;font-style:italic}}
.doc-content code{{font-family:var(--font-mono);font-size:0.82rem;background:rgba(200,211,213,0.08);padding:0.15rem 0.4rem;border-radius:4px;color:var(--cloud-gray)}}
.doc-content pre{{background:var(--ink-deep);border:1px solid var(--ink-border);border-radius:8px;padding:1rem;overflow-x:auto;margin:1rem 0}}
.doc-content pre code{{background:none;padding:0;font-size:0.8rem;color:var(--cloud-white);line-height:1.6}}
.doc-content hr{{border:none;border-top:1px solid var(--ink-border);margin:2rem 0}}
.doc-content .table-wrap{{overflow-x:auto;margin:1rem 0}}
.doc-content table{{width:100%;border-collapse:collapse;font-size:0.85rem}}
.doc-content th{{padding:0.625rem 0.875rem;text-align:left;border-bottom:2px solid var(--ink-border-strong);color:var(--fg);font-weight:600}}
.doc-content td{{padding:0.5rem 0.875rem;border-bottom:1px solid var(--ink-border);color:var(--fg-muted)}}
.doc-content .ascii-art-removed{{padding:0.75rem 1rem;border:1px dashed var(--ink-border);border-radius:6px;color:var(--fg-dim);font-size:0.8rem;margin:1rem 0;text-align:center}}

/* 上下页导航 */
.prev-next{{display:flex;justify-content:space-between;margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--ink-border);gap:1rem}}
.prev-next a{{display:flex;flex-direction:column;gap:0.25rem;padding:0.75rem 1rem;border:1px solid var(--ink-border);border-radius:8px;text-decoration:none;transition:all 0.2s;max-width:48%}}
.prev-next a:hover{{border-color:var(--gold-soft);background:var(--gold-dim)}}
.prev-next .pn-label{{font-size:0.72rem;color:var(--fg-dim)}}
.prev-next .pn-title{{font-size:0.85rem;color:var(--fg);font-weight:500}}
.prev-next .next-page{{text-align:right;margin-left:auto}}
.prev-page .pn-title{{text-align:left}}

/* 响应式 */
@media(max-width:900px){{
  .doc-sidebar{{display:none}}
  .doc-main{{padding:1.5rem 1rem}}
  .nav-links a:not(.nav-cta){{display:none}}
}}
</style>
</head>
<body>
<div class="ink-bg"></div>
<nav class="nav"><div class="nav-inner">
  <a href="/" class="nav-brand"><span class="brand-mark">剑</span><span>凌霄剑域</span><span class="brand-sub">LingXiao</span></a>
  <div class="nav-links">
    <a href="{nav_docs}">文档</a>
    <a href="https://github.com/hexian2001/lingxiao-coding" target="_blank" rel="noopener">GitHub</a>
    <a href="{nav_docs}" class="nav-cta" style="padding:0.4rem 1rem;border-radius:8px;background:var(--gold-dim);color:var(--gold);font-weight:600;font-size:0.8rem;border:1px solid rgba(212,175,55,0.3)">快速上手</a>
  </div>
</div></nav>
<div class="doc-layout">
  <aside class="doc-sidebar">
{sidebar_html}
  </aside>
  <main class="doc-main">
    <div class="doc-content">
{content_html}
    </div>
{prev_next_html}
  </main>
</div>
</body>
</html>'''

def main():
    # 清理输出目录（保留 index.html）
    docs_out = OUTPUT / "docs"
    if docs_out.exists():
        shutil.rmtree(docs_out)
    docs_out.mkdir(parents=True)

    # 处理中文文档
    process_locale(DOCS_SRC, docs_out, ZH_SIDEBAR, is_en=False)
    # 处理英文文档
    process_locale(DOCS_SRC, docs_out, EN_SIDEBAR, is_en=True)

    print(f"✓ 文档生成完成: {docs_out}")

def process_locale(src_base, out_base, sidebar, is_en):
    locale_prefix = "en/" if is_en else ""
    for group in sidebar:
        for label, slug in group["items"]:
            md_path = src_base / f"{slug}.md"
            if not md_path.exists():
                print(f"  ⚠ 缺少: {md_path}")
                continue

            md_text = md_path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(md_text)
            title = meta.get("title", label)
            content_html = md_to_html(body)
            sidebar_html = build_sidebar_html(slug, sidebar, is_en)
            prev, nxt = get_prev_next(slug, sidebar)
            prev_next_html = build_prev_next(prev, nxt, is_en)

            page_html = build_page(title, content_html, sidebar_html, prev_next_html, is_en)

            out_dir = out_base / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(page_html, encoding="utf-8")
            print(f"  ✓ {slug}/index.html")

if __name__ == "__main__":
    main()
