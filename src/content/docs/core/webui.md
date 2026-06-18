---
title: WebUI 指挥中心
description: Chat/Tasks/Agents/Review/Git/Blackboard/Terminal/Settings 八大面板
---

# WebUI 指挥中心

凌霄的 WebUI 不是一个简单的聊天界面，而是一个完整的工程指挥中心。它把任务图、Agent 面板、代码审查、Git 操作、终端、设置等工程能力整合到一个实时同步的界面中。

## 八大功能面板

### Chat（对话）

主对话面板，与 Leader 直接交互：

- 发送目标和需求
- 接收 Leader 的拆解方案和确认请求
- 实时查看 Worker 的执行进展
- 支持文件附件和截图

### Tasks（任务图）

可视化展示任务 DAG：

- 任务节点和依赖关系图形化显示
- 实时状态更新（pending/in_progress/completed/failed/blocked）
- 点击任务查看详情：owner、描述、写入范围、结果、证据
- 支持任务过滤和搜索

### Agents（Agent 面板）

实时监控每个 Worker 的运行状态：

- 角色身份和当前任务
- 工具调用记录（参数、权限评估、输出、耗时）
- 运行日志和实时输出
- 结果回执和验证证据
- 心跳状态和进程信息

### Review（审查中心）

代码审查和验收面板：

- 查看 Worker 提交的代码变更（diff）
- Review verdict（PASS/FAIL/BLOCKED）和证据
- 审查建议和改进意见
- 支持多轮审查和修复

### Git（Git 操作）

Git 仓库管理面板：

- 分支管理和切换
- 提交历史和 diff 查看
- Worktree 创建和管理
- 合并和冲突解决

### Blackboard（黑板）

共享知识图谱面板：

- 查看 Facts、Intents、Contracts、Design Docs
- 知识节点的关系图谱
- 跨 Agent 的公共记忆
- 契约版本和变更历史

### Terminal（终端）

内嵌终端面板：

- 直接在浏览器中执行 shell 命令
- 与 Worker 的 shell 调用共享工作目录
- 支持前台和后台命令
- 命令历史和输出记录

### Settings（设置）

配置管理面板：

- 模型配置（Leader/Worker 模型选择）
- Provider 配置（OpenAI/Anthropic/兼容服务）
- 工具权限策略
- 主题和界面偏好
- LLM Gateway 虚拟密钥管理

## 实时同步

WebUI 通过 SSE 事件流与后端实时同步，所有状态变更无需刷新即可看到：

<div class="doc-flow" role="img" aria-label="WebUI 实时同步：Leader 和 Workers 更新 SessionManager，经 SseBridge 和 SSE 推送到 WebUI。">
  <span>Leader / Workers</span><i>→</i><span>SessionManager</span><i>→</i><span>SseBridge</span><i>→</i><span>SSE</span><i>→</i><strong>WebUI</strong>
</div>

## 访问方式

启动凌霄后，终端会打印 WebUI 地址：

```bash
lingxiao
# 输出: WebUI: http://127.0.0.1:3780
```

默认端口信息写入 `~/.lingxiao/port`。WebUI 受 Server Token 保护，开发模式下通过注入 `window.__LINGXIAO_TOKEN__` 自动鉴权。
