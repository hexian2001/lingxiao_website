---
title: 工具内核
description: 100+ 内置工具、ToolRegistry 统一管理与权限系统
---

# 工具内核

凌霄内置 100+ 工具，覆盖完整工程链路。所有工具通过 ToolRegistry 统一注册和管理，支持权限评估、并行执行和预检机制。

## 工具分类

### 文件系统

文件读写、目录浏览、glob 搜索、增量编辑：

- `file_read`：读取文件内容，支持行号范围
- `file_create`：创建或覆盖文件，原子写入
- `structured_patch`：增量修改，支持 search/replace、行范围替换、插入
- `list_dir`：目录树浏览
- `glob`：文件模式匹配搜索

### 代码搜索

基于 ripgrep 的高性能全文搜索：

- `code_search`：正则表达式搜索，支持文件模式过滤
- 搜索路径限定和超时控制
- 结果分页和 offset 续读

### Shell 执行

安全的命令行执行环境：

- `shell`：前台/后台执行，sandbox 隔离，网络模式控制
- 支持工作目录设置和环境变量
- 后台任务持续运行，跨工具调用保持状态

### Python 执行

内嵌 Python 代码执行：

- `python_exec`：执行 Python 代码片段，返回 stdout
- 支持超时和输出大小限制

### 浏览器自动化

完整的浏览器操作能力：

- `browser_action`：导航、点击、填写表单、等待元素、读取文本、执行 JS
- `browser_visual_verify`：页面验收，断言+截图
- `screenshot`：网页截图
- `visual_contact_sheet`：多图拼接总览
- `ocr`：本地 OCR 文字识别（tesseract.js，支持中英文）

### Office 套件

文档生成和编辑：

- `generate_pptx` / `edit_pptx` / `inspect_pptx`：PPTX 生成/编辑/检查
- `generate_docx`：DOCX 文档生成
- `generate_html_presentation` / `generate_html_document`：HTML 格式输出

### 通信

网络通信工具：

- `web_fetch`：网页抓取，自动切换 fetch/浏览器渲染
- `web_search`：搜索引擎查询，支持高级语法
- `http_request`：HTTP 请求，支持所有 HTTP 方法

### 持久记忆

- `memory`：保存、搜索、读取和删除长期记忆
- 支持 FTS5 + BM25 全文搜索

### MCP 集成

- `mcp`：统一 MCP 入口，发现和调用 MCP tools/resources/prompts

## ToolRegistry

所有工具通过 ToolRegistry 统一注册和管理：

- `find_tools`：按名称、描述、分类、tier 搜索工具
- `tool_preflight`：调用预检，验证参数 schema 和前置条件
- `parallel_read_batch`：并行只读批处理，安全工具自动并行

## 权限系统

工具调用遵循 9 层评估链：

```text
deny → allow → ask → yolo → always-allowed → network → hardened → strict → default allow
```

### 权限层级说明

| 层级 | 说明 |
| --- | --- |
| `deny` | 明确拒绝，不可覆盖 |
| `allow` | 明确允许 |
| `ask` | 询问用户确认 |
| `yolo` | 跳过所有确认（危险） |
| `always-allowed` | 永久允许 |
| `network` | 网络访问权限 |
| `hardened` | 加固模式限制 |
| `strict` | 严格模式限制 |
| `default allow` | 默认允许 |

## 工具能力层级

工具按能力分为四个层级：

| 层级 | 说明 | 示例 |
| --- | --- | --- |
| `read` | 只读工具 | file_read, code_search, list_dir |
| `write` | 写入工具 | file_create, structured_patch |
| `execute` | 执行工具 | shell, python_exec |
| `compute` | 计算工具 | node_repl, parallel_read_batch |
