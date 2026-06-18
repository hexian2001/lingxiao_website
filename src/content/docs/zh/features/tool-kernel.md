---
title: 工具内核
description: 100+ 内置工具与 ToolRegistry
---

# 工具内核

凌霄内置 100+ 工具，覆盖完整工程链路。

## 工具分类

### 文件系统
文件读写、目录浏览、glob 搜索、增量编辑（structured_patch）

### 代码搜索
ripgrep 全文搜索、正则匹配、文件模式过滤

### Shell 执行
前台/后台、sandbox 隔离、网络模式控制

### 浏览器自动化
页面导航、截图、点击、表单填写、JS 执行、OCR

### Office 套件
PPTX 生成/编辑/检查、DOCX 生成、XLSX 生成、PDF 生成

### Workflow 画布
可视化工作流编辑和执行引擎

### 通信
网页抓取、搜索、HTTP 请求、邮件

## ToolRegistry

所有工具通过 ToolRegistry 统一注册和管理：

- 工具发现和搜索（find_tools）
- 调用预检（tool_preflight）
- 并行只读批处理（parallel_read_batch）
- 权限层级评估

## 权限系统

工具调用遵循 9 层评估链：

```text
deny → allow → ask → yolo → always-allowed → network → hardened → strict → default allow
```
