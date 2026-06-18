---
title: Skills 系统
description: 4层优先级、YAML frontmatter、阶段加载与自动注入
---

# Skills 系统

凌霄的 Skill 系统是 Agent 的**执行知识面**。Skill 是结构化的 Markdown 文档（YAML frontmatter + body），运行时注入到 Worker 的任务提示词中作为 `<skill>` 块，为 LLM 提供上下文流程、领域约束和质量门。

Skill **不是**运行时工具，也**不是**插件清单。它们是声明式知识包，按来源分级和版本化。

## 4 层优先级

Skill 按来源优先级加载（高优先级覆盖低优先级）：

| 优先级 | 来源 | 目录 |
| --- | --- | --- |
| 1（最高） | 项目级 | `.lingxiao/skills/` |
| 2 | 插件贡献 | 插件目录 |
| 3 | 用户级 | `~/.lingxiao/skills/` |
| 4（最低） | 内置 | 包内 bundled |

## Skill 定义格式

磁盘格式为 **YAML frontmatter + Markdown body**：

```markdown
---
name: my-skill
description: 一行简短描述
---
<markdown body — 流程、质量门、参考>
```

### 必填字段

| 字段 | 规则 | 说明 |
| --- | --- | --- |
| `name` | kebab-case，由 `validateSkillName` 校验 | 技能名称 |
| `description` | 非空，单行 | 技能描述 |

### 可选字段

| 字段 | 说明 |
| --- | --- |
| `triggers` | 触发条件（保留扩展点） |
| `content` | 内容引用（保留扩展点） |

### 验证规则

- `description` 和 `body` 在写入时均为**必填**
- `validateSkillName` 强制 kebab-case；无效名称写入时抛出，读取时跳过
- 缺少 `description` 且 body 为空的文件在读取时被静默丢弃

## 阶段加载与质量门

Skill 目录可包含 `phases/` 子目录，每个 `*.md` 文件成为一个 `SkillPhase`：

```ts
interface SkillPhase { name: string; path: string; content: string; }
interface QualityGate { checks: string[]; skipConditions: string[]; }
```

`loadSkillPhases(skillDir)` 返回有序的阶段列表，每个阶段可包含质量门检查和跳过条件。

## 自动注入机制

### 注入点

| 注入点 | 场景 | 预算 |
| --- | --- | --- |
| Worker 任务提示词 | `BaseAgentRuntime.buildTaskPrompt` | 总计 18,000 字符，单技能 7,500 字符 |
| TUI 消息 | `SessionManagerRuntime` | 按需注入 |

### 技能名称来源

三个来源合并去重后注入：

| 来源 | 起源 | 应用时机 |
| --- | --- | --- |
| `skillNames` | 角色能力（`RoleCapabilityModel`） | 基于角色，始终生效 |
| `explicitSkills` | 任务描述和系统提示词中的 `$skill` 引用 | 用户/角色通过语法选择 |
| `officeSkill` | `OFFICE_MODE_ACTIVE` 会话状态 | 会话级 office 模式 |

### `$skill` 引用语法

在任务描述或系统提示词中使用 `$skill-name` 引用技能：

```
$debug-frontend-backend-contract
$office_suite
$explore_implement_verify
```

正则匹配：`/ \$([a-zA-Z0-9_][a-zA-Z0-9_-]*) /g`，去重后注入。

### 注入预算

| 限制 | 值 | 超限效果 |
| --- | --- | --- |
| `maxTotalChars` | 18,000 | 后续技能按到达顺序丢弃 |
| `maxPerSkillChars` | 7,500 | 每个技能 body 截断到此长度 |
| 可见性 | `truncated: true` | 调用方可读取 `descriptor.path` 获取完整内容 |

## 内置技能包

凌霄内置 14 个技能包：

| 技能 | 说明 |
| --- | --- |
| `code-quality` | 代码质量检查 |
| `commit-message` | Git 提交信息规范 |
| `doc-coauthoring` | 文档协同 |
| `docx` | Word 文档生成 |
| `frontend-design` | 前端设计 |
| `office-suite` | Office 套件 |
| `pdf` | PDF 生成 |
| `pptx` | PPT 生成 |
| `skill-creator` | 技能创建器 |
| `slidev` | Slidev 演示 |
| `theme-factory` | 主题工厂 |
| `web-artifacts-builder` | Web 产物构建 |
| `xlsx` | Excel 生成 |
| `design-market` | 设计素材市场 |

## 自定义技能

### 通过 skill-creator 创建

使用 `skill-creator` 技能包自动创建自定义技能。

### 手动创建

在项目级或用户级目录中编写：

```bash
# 项目级
mkdir -p .lingxiao/skills/my-skill
cat > .lingxiao/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: 我的自定义技能
---

# 我的技能

## 流程
1. 步骤一
2. 步骤二

## 质量门
- 检查项一
- 检查项二
EOF
```

### HTTP API

通过 `/api/v1/skills` 路由管理技能：

| 端点 | 方法 | 说明 |
| --- | --- | --- |
| `/api/v1/skills` | GET | 列出技能 |
| `/api/v1/skills` | POST | 创建技能 |
| `/api/v1/skills/:name` | PUT | 更新技能 |
| `/api/v1/skills/:name` | DELETE | 删除技能 |

## 选择策略

`SkillSelectionPolicy.digestGuidance` 定义了 5 条选择规则，这些规则会出现在 Leader 的摘要提示词中，指导技能的自动选择和禁用。
