import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

const siteUrl = 'https://hexian2001.github.io';
const base = '/lingxiao_website';

function makeSidebar(prefix) {
  const isZh = prefix === 'zh';
  return [
    {
      label: isZh ? '入门' : 'Getting Started',
      items: [
        { label: isZh ? '简介' : 'Introduction', slug: `${prefix}/getting-started/introduction` },
        { label: isZh ? '安装与启动' : 'Installation', slug: `${prefix}/getting-started/install` },
        { label: isZh ? '连接模型' : 'Connect Models', slug: `${prefix}/getting-started/connect-models` },
        { label: isZh ? '第一次运行' : 'First Run', slug: `${prefix}/getting-started/first-run` },
      ],
    },
    {
      label: isZh ? '核心功能' : 'Core Features',
      items: [
        { label: isZh ? '专家团系统' : 'Expert Panel', slug: `${prefix}/core/expert-team` },
        { label: isZh ? '任务DAG编排' : 'Task DAG', slug: `${prefix}/core/task-dag` },
        { label: isZh ? '全状态同步' : 'State Sync', slug: `${prefix}/core/state-sync` },
        { label: isZh ? 'WebUI指挥中心' : 'WebUI Center', slug: `${prefix}/core/webui` },
        { label: isZh ? '工具内核' : 'Tool Kernel', slug: `${prefix}/core/tool-kernel` },
        { label: isZh ? '编排验收' : 'Orchestration', slug: `${prefix}/core/orchestration` },
        { label: isZh ? 'MCP Forge与Skills' : 'MCP Forge & Skills', slug: `${prefix}/core/mcp-skills` },
        { label: isZh ? '持久记忆' : 'Memory', slug: `${prefix}/core/memory` },
        { label: isZh ? 'Eternal自治模式' : 'Eternal Mode', slug: `${prefix}/core/eternal` },
        { label: isZh ? 'LLM Gateway' : 'LLM Gateway', slug: `${prefix}/core/llm-gateway` },
      ],
    },
    {
      label: isZh ? '配置与自定义' : 'Configuration & Customization',
      items: [
        { label: isZh ? '环境变量' : 'Environment Variables', slug: `${prefix}/config/env-vars` },
        { label: isZh ? '模型配置' : 'Models', slug: `${prefix}/config/models` },
        { label: isZh ? '权限系统' : 'Permissions', slug: `${prefix}/config/permissions` },
        { label: isZh ? '网络配置' : 'Network', slug: `${prefix}/config/network` },
        { label: isZh ? '主题' : 'Theme', slug: `${prefix}/config/theme` },
        { label: isZh ? '自定义命令' : 'Custom Commands', slug: `${prefix}/config/custom-commands` },
        { label: 'MCP', slug: `${prefix}/config/mcp` },
        { label: 'Agents', slug: `${prefix}/config/agents` },
        { label: isZh ? 'Skills 系统' : 'Skills', slug: `${prefix}/config/skills` },
        { label: isZh ? '规则' : 'Rules', slug: `${prefix}/config/rules` },
      ],
    },
    {
      label: isZh ? '参考' : 'Reference',
      items: [
        { label: isZh ? 'CLI命令' : 'CLI', slug: `${prefix}/reference/cli` },
        { label: isZh ? 'Slash命令' : 'Slash Commands', slug: `${prefix}/reference/slash-commands` },
        { label: isZh ? '架构概览' : 'Architecture', slug: `${prefix}/reference/architecture` },
        { label: isZh ? 'API契约索引' : 'API Index', slug: `${prefix}/reference/api-index` },
        { label: 'FAQ', slug: `${prefix}/reference/faq` },
        { label: isZh ? '安全须知' : 'Security', slug: `${prefix}/reference/security` },
        { label: isZh ? '更新日志' : 'Changelog', slug: `${prefix}/reference/changelog` },
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
        zh: {
          label: '简体中文',
          lang: 'zh-CN',
          slug: 'zh',
          sidebar: makeSidebar('zh'),
        },
        en: {
          label: 'English',
          lang: 'en',
          slug: 'en',
          sidebar: makeSidebar('en'),
        },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/hexian2001/lingxiao' },
      ],
      customCss: ['./src/styles/lingxiao-theme.css'],
      logo: { src: './src/assets/logo.svg', replacesTitle: false },
    }),
  ],
});
