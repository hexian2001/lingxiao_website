---
title: 安装与启动
description: 一行命令安装凌霄剑域
---

# 安装与启动

## 一行安装

### macOS / Linux / WSL

```bash
curl -fsSL https://raw.githubusercontent.com/hexian2001/lingxiao-coding/main/scripts/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/hexian2001/lingxiao-coding/main/scripts/install.ps1 | iex
```

安装完成后运行：

```bash
lingxiao doctor
```

脚本会自动检测平台和架构，下载对应的便携版二进制包，解压并配置命令链接。无需预装 Node.js。

> **指定版本**：macOS/Linux 追加 `-- --version v1.0.0`，Windows 使用 `-Version "v1.0.0"` 参数。

## 前置条件

| 依赖 | 要求 |
| --- | --- |
| 操作系统 | Linux / macOS / Windows / WSL |
| Node.js | 便携版无需；从源码开发需 `>=24.0.0` |
| Git | 推荐安装 |

## 首次配置

```bash
lingxiao init
```

该命令会引导你完成初始配置。配置文件位于：

```text
~/.lingxiao/settings.json
```

## 验证安装

```bash
lingxiao doctor
```

环境诊断命令会检查 Node.js 版本、Git、配置文件、LLM key 等。

## 升级

```bash
lingxiao upgrade
```

自动检查 GitHub 最新 release，下载对应平台便携包并替换安装。也可以先检查是否有新版本：

```bash
lingxiao upgrade --check
```

> npm 全局安装的用户请使用 `npm update -g lingxiao_cli` 升级。

## 从源码开发

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao
npm install
npm run build
npm run cli
```

Web 前端开发：

```bash
cd web
npm install
npm run dev
npm run build
```

Vite 开发代理示例：

```bash
LINGXIAO_WEB_PORT=8787 npm run cli
cd web
LINGXIAO_WEB_PROXY_TARGET=http://127.0.0.1:8787 npm run dev
```

## 测试

```bash
npx tsc -p tsconfig.cli.json --noEmit
npx tsc -p web/tsconfig.json --noEmit
npm run test:architecture
npm run build
npm test
```

## 下一步

- [连接模型](./connect-models) — 配置 LLM 提供商
- [第一次运行](./first-run) — 启动你的第一个专家团
