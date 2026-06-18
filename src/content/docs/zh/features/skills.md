---
title: Skills系统
description: 4层优先级技能注入体系
---

# Skills 系统

凌霄的技能系统为 Agent 注入执行知识、流程和领域约束。

## 4 层来源优先级

```text
project（项目级）> plugin（插件贡献）> global（用户级）> builtin（内置）
```

- **项目级**：`.lingxiao/skills/`
- **用户级**：`~/.lingxiao/skills/`
- **插件/内置**：由插件和市场贡献

## 技能定义

YAML frontmatter + Markdown 内容：

- 阶段加载（phases/*.md）
- Quality Gate 质量门控
- 按角色和任务自动注入 worker prompt

## 内置技能包（14 个）

| 技能 | 用途 |
| --- | --- |
| algorithmic-art | 算法艺术生成 |
| canvas-design | 画布设计 |
| design-market | 设计素材市场 |
| doc-coauthoring | 文档协同 |
| docx | Word 文档生成 |
| frontend-design | 前端设计 |
| office-suite | Office 套件 |
| pdf | PDF 生成 |
| pptx | PPT 生成 |
| skill-creator | 技能创建器 |
| slidev | Slidev 演示 |
| theme-factory | 主题工厂 |
| web-artifacts-builder | Web 产物构建 |
| xlsx | Excel 生成 |

## 自定义技能

通过 `skill-creator` 技能包创建自定义技能，或手动在项目/用户级目录编写。
