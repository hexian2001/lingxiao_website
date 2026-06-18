---
title: 规则
description: 项目规则与自定义规则
---

# 规则

凌霄支持项目级规则文件，为 Agent 注入工程约束。规则是自动注入到 Agent 上下文的 Markdown 文件，无需手动引用。

## 规则文件位置

| 层级 | 目录 | 说明 |
| --- | --- | --- |
| 项目级 | `.lingxiao/rules/` | 项目特定规则 |
| 用户级 | `~/.lingxiao/rules/` | 用户全局规则 |

## 规则格式

规则文件为 Markdown 格式，自动注入到 Agent 上下文：

```markdown
# 代码规范

- 使用 TypeScript strict 模式
- 函数必须有返回类型标注
- 禁止使用 any 类型
- 所有公共 API 必须有 JSDoc 注释
```

## 规则优先级

project > global，项目级规则覆盖用户级。

## 规则注入

规则文件在 Agent 启动时自动读取并注入到系统提示词中。与 Skills 不同，规则不需要显式引用（无需 `$skill` 语法），所有规则文件内容都会被注入。

### 注入范围

| 范围 | 行为 |
| --- | --- |
| 项目级规则 | 仅当前工作区的 Agent 可见 |
| 用户级规则 | 所有 Agent 可见 |

## 常见规则示例

### 代码规范规则

```markdown
# 代码规范

- TypeScript strict 模式
- 使用 ESM import（不含 require）
- 函数返回类型必须显式标注
- 禁止 @ts-ignore
- 公共函数需 JSDoc 注释
```

### Git 规则

```markdown
# Git 规范

- 提交信息使用 conventional commits 格式
- feat: 新功能 / fix: 修复 / docs: 文档 / refactor: 重构
- 每个 commit 只包含一个逻辑变更
- PR 标题与 commit 标题保持一致
```

### 测试规则

```markdown
# 测试规范

- 新功能必须附带单元测试
- 测试覆盖率不低于 80%
- 使用 describe/it 组织测试结构
- Mock 外部依赖，不 Mock 被测模块
```

### 安全规则

```markdown
# 安全规范

- 禁止硬编码 API Key 或密码
- 环境变量必须通过 config.ts 读取
- SQL 查询必须使用参数化
- 用户输入必须经过校验和转义
```

## 与 Skills 的区别

| 特性 | 规则 | Skills |
| --- | --- | --- |
| 注入方式 | 自动注入 | 按需注入（`$skill` 或角色绑定） |
| 内容 | 约束和规范 | 流程和领域知识 |
| 格式 | 纯 Markdown | YAML frontmatter + Markdown |
| 位置 | `.lingxiao/rules/` | `.lingxiao/skills/` |
| 优先级 | project > global | 4 层（project > plugin > user > bundled） |
