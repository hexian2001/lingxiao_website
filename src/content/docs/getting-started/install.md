---
title: 安装与启动
description: 从源码安装凌霄剑域
---

# 安装与启动

## 前置要求

| 依赖 | 要求 |
| --- | --- |
| 操作系统 | Linux / macOS / Windows / WSL |
| Node.js | >= 24.0.0 |
| Git | 推荐 |

## 安装

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
npm install
npm run build
npm link
```

安装完成后直接运行：

```bash
lingxiao
```

首次运行会引导配置模型和 API 密钥。配置文件位于 `~/.lingxiao/settings.json`。

> `npm link` 会将 `lingxiao` 命令注册到全局 PATH，之后可在任意目录使用。

## 验证安装

```bash
lingxiao --version
```

## 升级

```bash
lingxiao upgrade
```

或手动执行：

```bash
cd lingxiao-coding
git pull
npm install
npm run build
```

## 从源码开发

```bash
git clone https://github.com/hexian2001/lingxiao-coding.git
cd lingxiao-coding
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

## 许可协议

本项目采用 **AGPL v3 + 商业双授权** 模式。详见 [LICENSE](https://github.com/hexian2001/lingxiao-coding/blob/main/LICENSE)。

## 下一步

- [连接模型](connect-models) — 配置 LLM 提供商
- [第一次运行](first-run) — 启动你的第一个专家团
