import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

const siteUrl = 'https://hexian2001.github.io';
const base = '/lingxiao';

function makeSidebar(prefix) {
  return [
    {
      label: prefix === 'zh' ? '入门' : 'Getting Started',
      translations: prefix === 'zh' ? { en: 'Getting Started' } : undefined,
      items: [
        { label: prefix === 'zh' ? '简介' : 'Introduction', slug: `${prefix}/getting-started/introduction` },
        { label: prefix === 'zh' ? '安装与启动' : 'Installation', slug: `${prefix}/getting-started/install` },
        { label: prefix === 'zh' ? '连接模型' : 'Connect Models', slug: `${prefix}/getting-started/connect-models` },
        { label: prefix === 'zh' ? '第一次运行' : 'First Run', slug: `${prefix}/getting-started/first-run` },
      ],
    },
    {
      label: prefix === 'zh' ? '核心功能' : 'Core Features',
      items: [
        { label: prefix === 'zh' ? '专家团系统' : 'Expert Panel', slug: `${prefix}/core/expert-team` },
        { label: prefix === 'zh' ? '任务DAG编排' : 'Task DAG', slug: `${prefix}/core/task-dag` },
        { label: prefix === 'zh' ? '全状态同步' : 'State Sync', slug: `${prefix}/core/state-sync` },
        { label: prefix === 'zh' ? 'WebUI指挥中心' : 'WebUI Center', slug: `${prefix}/core/webui` },
        { label: prefix === 'zh' ? '工具内核' : 'Tool Kernel', slug: `${prefix}/core/tool-kernel` },
        { label: prefix === 'zh' ? '编排验收' : 'Orchestration', slug: `${prefix}/core/orchestration` },
        { label: prefix === 'zh' ? 'MCP Forge与Skills' : 'MCP Forge & Skills', slug: `${prefix}/core/mcp-skills` },
        { label: prefix === 'zh' ? '持久记忆' : 'Memory', slug: `${prefix}/core/memory` },
        { label: prefix === 'zh' ? 'Eternal自治模式' : 'Eternal Mode', slug: `${prefix}/core/eternal` },
        { label: prefix === 'zh' ? 'LLM Gateway' : 'LLM Gateway', slug: `${prefix}/core/llm-gateway` },
      ],
    },
    {
      label: prefix === 'zh' ? '配置与自定义' : 'Configuration & Customization',
      items: [
        { label: prefix === 'zh' ? '环境变量' : 'Environment Variables', slug: `${prefix}/config/env-vars` },
        { label: prefix === 'zh' ? '模型配置' : 'Models', slug: `${prefix}/config/models` },
        { label: prefix === 'zh' ? '权限系统' : 'Permissions', slug: `${prefix}/config/permissions` },
        { label: prefix === 'zh' ? '网络配置' : 'Network', slug: `${prefix}/config/network` },
        { label: prefix === 'zh' ? '主题' : 'Theme', slug: `${prefix}/config/theme` },
        { label: prefix === 'zh' ? '自定义命令' : 'Custom Commands', slug: `${prefix}/config/custom-commands` },
        { label: 'MCP', slug: `${prefix}/config/mcp` },
        { label: 'Agents', slug: `${prefix}/config/agents` },
        { label: prefix === 'zh' ? 'Skills 系统' : 'Skills', slug: `${prefix}/config/skills` },
        { label: prefix === 'zh' ? '规则' : 'Rules', slug: `${prefix}/config/rules` },
      ],
    },
    {
      label: prefix === 'zh' ? '参考' : 'Reference',
      items: [
        { label: prefix === 'zh' ? 'CLI命令' : 'CLI', slug: `${prefix}/reference/cli` },
        { label: prefix === 'zh' ? 'Slash命令' : 'Slash Commands', slug: `${prefix}/reference/slash-commands` },
        { label: prefix === 'zh' ? '架构概览' : 'Architecture', slug: `${prefix}/reference/architecture` },
        { label: prefix === 'zh' ? 'API契约索引' : 'API Index', slug: `${prefix}/reference/api-index` },
        { label: 'FAQ', slug: `${prefix}/reference/faq` },
        { label: prefix === 'zh' ? '安全须知' : 'Security', slug: `${prefix}/reference/security` },
        { label: prefix === 'zh' ? '更新日志' : 'Changelog', slug: `${prefix}/reference/changelog` },
      ],
    },
  ];
}

export default defineConfig({
  site: siteUrl,
  base,
  integrations: [
    sitemap(),
    starlight({
      title: '凌霄剑域',
      defaultLocale: 'zh',
      locales: {
        zh: { label: '简体中文', lang: 'zh-CN' },
        en: { label: 'English', lang: 'en' },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/hexian2001/lingxiao' },
      ],
      sidebar: makeSidebar('zh'),
      customCss: ['./src/styles/lingxiao-theme.css'],
      logo: { src: './src/assets/logo.svg', replacesTitle: false },
    }),
  ],
});
