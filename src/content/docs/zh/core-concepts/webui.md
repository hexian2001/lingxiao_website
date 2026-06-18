---
title: WebUI指挥中心
description: 可视化指挥控制台
---

# WebUI 指挥中心

WebUI 是凌霄的可视化指挥控制台，提供完整的运行态可视化。

## 核心面板

### 任务面板

- DAG 可视化展示
- 任务状态流转
- 依赖关系图谱
- 阻塞和错误提示

### Agent 面板

- 各 Worker 的角色和身份
- 实时进度和输出
- 工具调用历史
- 运行状态监控

### 工具调用

- 每次工具的参数、权限和结果
- 调用链路追踪
- 耗时和性能分析

### 代码变更

- 文件 diff 对比
- Git 操作记录
- 分支和合并管理

## 启动方式

```bash
lingxiao
```

启动后终端打印 WebUI 地址，默认端口信息写入 `~/.lingxiao/port`。

## 开发模式

```bash
LINGXIAO_WEB_PORT=8787 npm run cli
cd web
LINGXIAO_WEB_PROXY_TARGET=http://127.0.0.1:8787 npm run dev
```
