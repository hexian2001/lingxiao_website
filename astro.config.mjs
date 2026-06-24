import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import { readFileSync } from 'fs';
import { visit } from 'unist-util-visit';

const pkg = JSON.parse(readFileSync('./package.json', 'utf-8'));
const VERSION = pkg.version;

function remarkVersionSubstitution() {
  return (tree) => {
    visit(tree, 'text', (node) => {
      node.value = node.value.replace(/LINGXIAO_VERSION/g, VERSION);
    });
  };
}

const siteUrl = 'https://hexian2001.github.io';
const base = '/lingxiao_website';

const sidebarTranslations = {
  '入门': { en: 'Getting Started' },
  '简介': { en: 'Introduction' },
  '安装与启动': { en: 'Install & Setup' },
  '连接模型': { en: 'Connect Models' },
  '第一次运行': { en: 'First Run' },
  '核心功能': { en: 'Core Features' },
  '专家团系统': { en: 'Expert Panel System' },
  '任务DAG编排': { en: 'Task DAG Orchestration' },
  '全状态同步': { en: 'Full State Sync' },
  'WebUI指挥中心': { en: 'WebUI Command Center' },
  '工具内核': { en: 'Tool Kernel' },
  '编排验收': { en: 'Orchestration & Verification' },
  'MCP 与 Skills': { en: 'MCP & Skills' },
  '持久记忆': { en: 'Persistent Memory' },
  'Eternal自治模式': { en: 'Eternal Mode' },
  'LLM Gateway': { en: 'LLM Gateway' },
  '配置与自定义': { en: 'Configuration & Customization' },
  '环境变量': { en: 'Environment Variables' },
  '模型配置': { en: 'Model Config' },
  '权限系统': { en: 'Permission System' },
  '网络配置': { en: 'Network Config' },
  '主题': { en: 'Theme' },
  '自定义命令': { en: 'Custom Commands' },
  'MCP': { en: 'MCP' },
  'Agents': { en: 'Agents' },
  'Skills 系统': { en: 'Skills System' },
  '规则': { en: 'Rules' },
  '参考': { en: 'Reference' },
  'CLI命令': { en: 'CLI Commands' },
  'Slash命令': { en: 'Slash Commands' },
  '架构概览': { en: 'Architecture Overview' },
  'API契约索引': { en: 'API Contract Index' },
  'FAQ': { en: 'FAQ' },
  '安全须知': { en: 'Security Notice' },
  '更新日志': { en: 'Changelog' },
};

function t(label) {
  return { label, translations: sidebarTranslations[label] || {} };
}

function sidebar() {
  return [
    {
      ...t('入门'),
      items: [
        { ...t('简介'), slug: 'getting-started/introduction' },
        { ...t('安装与启动'), slug: 'getting-started/install' },
        { ...t('连接模型'), slug: 'getting-started/connect-models' },
        { ...t('第一次运行'), slug: 'getting-started/first-run' },
      ],
    },
    {
      ...t('核心功能'),
      items: [
        { ...t('专家团系统'), slug: 'core/expert-team' },
        { ...t('任务DAG编排'), slug: 'core/task-dag' },
        { ...t('全状态同步'), slug: 'core/state-sync' },
        { ...t('WebUI指挥中心'), slug: 'core/webui' },
        { ...t('工具内核'), slug: 'core/tool-kernel' },
        { ...t('编排验收'), slug: 'core/orchestration' },
        { ...t('MCP 与 Skills'), slug: 'core/mcp-skills' },
        { ...t('持久记忆'), slug: 'core/memory' },
        { ...t('Eternal自治模式'), slug: 'core/eternal' },
        { ...t('LLM Gateway'), slug: 'core/llm-gateway' },
      ],
    },
    {
      ...t('配置与自定义'),
      items: [
        { ...t('环境变量'), slug: 'config/env-vars' },
        { ...t('模型配置'), slug: 'config/models' },
        { ...t('权限系统'), slug: 'config/permissions' },
        { ...t('网络配置'), slug: 'config/network' },
        { ...t('主题'), slug: 'config/theme' },
        { ...t('自定义命令'), slug: 'config/custom-commands' },
        { ...t('MCP'), slug: 'config/mcp' },
        { ...t('Agents'), slug: 'config/agents' },
        { ...t('Skills 系统'), slug: 'config/skills' },
        { ...t('规则'), slug: 'config/rules' },
      ],
    },
    {
      ...t('参考'),
      items: [
        { ...t('CLI命令'), slug: 'reference/cli' },
        { ...t('Slash命令'), slug: 'reference/slash-commands' },
        { ...t('架构概览'), slug: 'reference/architecture' },
        { ...t('API契约索引'), slug: 'reference/api-index' },
        { ...t('FAQ'), slug: 'reference/faq' },
        { ...t('安全须知'), slug: 'reference/security' },
        { ...t('更新日志'), slug: 'reference/changelog' },
      ],
    },
  ];
}

export default defineConfig({
  site: siteUrl,
  base,
  markdown: {
    remarkPlugins: [remarkVersionSubstitution],
  },
  integrations: [
    sitemap(),
    starlight({
      title: '凌霄剑域',
      defaultLocale: 'root',
      locales: {
        root: { label: '简体中文', lang: 'zh-CN' },
        en: { label: 'English', lang: 'en' },
      },
      sidebar: sidebar(),
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/hexian2001/lingxiao-coding' },
      ],
      customCss: ['./src/styles/lingxiao-theme.css'],
      logo: { src: './src/assets/logo.svg', replacesTitle: false },
    }),
  ],
});
