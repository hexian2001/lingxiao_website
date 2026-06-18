---
title: 安装与启动
description: 从零搭建凌霄运行环境
---

# 安装与启动

## 前置条件

| 依赖 | 要求 |
| --- | --- |
| Node.js | `>=24.0.0` |
| npm | 随 Node 24 配套版本 |
| Git | 推荐安装 |
| 操作系统 | Linux / macOS / Windows / WSL |

## 安装步骤

```bash
git clone https://github.com/hexian2001/lingxiao.git
cd lingxiao
npm install
npm run build
npm link
```

安装完成后，`lingxiao` 命令将全局可用。

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

## 从源码开发

```bash
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
