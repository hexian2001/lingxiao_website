import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

const siteUrl = 'https://hexian2001.github.io';
const base = '/lingxiao_website';

function zhSidebar() {
  return [
    {
      label: '入门',
      items: [
        { label: '简介', slug: 'getting-started/introduction' },
        { label: '安装与启动', slug: 'getting-started/install' },
        { label: '连接模型', slug: 'getting-started/connect-models' },
        { label: '第一次运行', slug: 'getting-started/first-run' },
      ],
    },
    {
      label: '核心功能',
      items: [
        { label: '专家团系统', slug: 'core/expert-team' },
        { label: '任务DAG编排', slug: 'core/task-dag' },
        { label: '全状态同步', slug: 'core/state-sync' },
        { label: 'WebUI指挥中心', slug: 'core/webui' },
        { label: '工具内核', slug: 'core/tool-kernel' },
        { label: '编排验收', slug: 'core/orchestration' },
        { label: 'MCP Forge与Skills', slug: 'core/mcp-skills' },
        { label: '持久记忆', slug: 'core/memory' },
        { label: 'Eternal自治模式', slug: 'core/eternal' },
        { label: 'LLM Gateway', slug: 'core/llm-gateway' },
      ],
    },
    {
      label: '配置与自定义',
      items: [
        { label: '环境变量', slug: 'config/env-vars' },
        { label: '模型配置', slug: 'config/models' },
        { label: '权限系统', slug: 'config/permissions' },
        { label: '网络配置', slug: 'config/network' },
        { label: '主题', slug: 'config/theme' },
        { label: '自定义命令', slug: 'config/custom-commands' },
        { label: 'MCP', slug: 'config/mcp' },
        { label: 'Agents', slug: 'config/agents' },
        { label: 'Skills 系统', slug: 'config/skills' },
        { label: '规则', slug: 'config/rules' },
      ],
    },
    {
      label: '参考',
      items: [
        { label: 'CLI命令', slug: 'reference/cli' },
        { label: 'Slash命令', slug: 'reference/slash-commands' },
        { label: '架构概览', slug: 'reference/architecture' },
        { label: 'API契约索引', slug: 'reference/api-index' },
        { label: 'FAQ', slug: 'reference/faq' },
        { label: '安全须知', slug: 'reference/security' },
        { label: '更新日志', slug: 'reference/changelog' },
      ],
    },
  ];
}

function enSidebar() {
  return [
    {
      label: 'Getting Started',
      items: [
        { label: 'Introduction', slug: 'en/getting-started/introduction' },
        { label: 'Installation', slug: 'en/getting-started/install' },
        { label: 'Connect Models', slug: 'en/getting-started/connect-models' },
        { label: 'First Run', slug: 'en/getting-started/first-run' },
      ],
    },
    {
      label: 'Core Features',
      items: [
        { label: 'Expert Panel', slug: 'en/core/expert-team' },
        { label: 'Task DAG', slug: 'en/core/task-dag' },
        { label: 'State Sync', slug: 'en/core/state-sync' },
        { label: 'WebUI Center', slug: 'en/core/webui' },
        { label: 'Tool Kernel', slug: 'en/core/tool-kernel' },
        { label: 'Orchestration', slug: 'en/core/orchestration' },
        { label: 'MCP Forge & Skills', slug: 'en/core/mcp-skills' },
        { label: 'Memory', slug: 'en/core/memory' },
        { label: 'Eternal Mode', slug: 'en/core/eternal' },
        { label: 'LLM Gateway', slug: 'en/core/llm-gateway' },
      ],
    },
    {
      label: 'Configuration & Customization',
      items: [
        { label: 'Environment Variables', slug: 'en/config/env-vars' },
        { label: 'Models', slug: 'en/config/models' },
        { label: 'Permissions', slug: 'en/config/permissions' },
        { label: 'Network', slug: 'en/config/network' },
        { label: 'Theme', slug: 'en/config/theme' },
        { label: 'Custom Commands', slug: 'en/config/custom-commands' },
        { label: 'MCP', slug: 'en/config/mcp' },
        { label: 'Agents', slug: 'en/config/agents' },
        { label: 'Skills', slug: 'en/config/skills' },
        { label: 'Rules', slug: 'en/config/rules' },
      ],
    },
    {
      label: 'Reference',
      items: [
        { label: 'CLI', slug: 'en/reference/cli' },
        { label: 'Slash Commands', slug: 'en/reference/slash-commands' },
        { label: 'Architecture', slug: 'en/reference/architecture' },
        { label: 'API Index', slug: 'en/reference/api-index' },
        { label: 'FAQ', slug: 'en/reference/faq' },
        { label: 'Security', slug: 'en/reference/security' },
        { label: 'Changelog', slug: 'en/reference/changelog' },
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
      defaultLocale: 'root',
      locales: {
        root: { label: '简体中文', lang: 'zh-CN' },
        en: { label: 'English', lang: 'en' },
      },
      sidebar: zhSidebar(),
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/hexian2001/lingxiao-coding' },
      ],
      customCss: ['./src/styles/lingxiao-theme.css'],
      logo: { src: './src/assets/logo.svg', replacesTitle: false },
    }),
  ],
});
