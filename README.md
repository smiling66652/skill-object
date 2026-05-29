# task-orchestrator

> AI Agent Task Orchestrator — 智能任务编排器 Skill  
> 专为 WorkBuddy/CodeBuddy 设计的跨工具任务协调引擎

## 🔧 是什么

**task-orchestrator** 是一个 WorkBuddy Skill，能让 AI Agent 自动将复杂任务拆解为子任务、为每个子任务匹配最佳工具、定义降级方案、并记录错误日志。

### 核心能力

| 能力 | 说明 |
|------|------|
| 🧩 任务拆解 | 将复杂请求分解为独立子任务，标注依赖关系 |
| 🔀 工具分配 | 优先级：MCP → Skill → CLI → 直接编码 |
| ⬇️ 三层降级 | 每个子任务至少一个 Plan B，失败自动降级 |
| 📊 并行执行 | 自动识别无依赖子任务，并发执行 |
| 📝 错误记录 | 所有失败生成 .log 文件 + 手动修复方案 |
| ✅ 确认机制 | 展示计划 → 用户确认 → 自动执行 |

## 📂 文件结构

```
task-orchestrator/
├── SKILL.md                         # 核心编排逻辑 + 8个预设场景
├── references/
│   ├── tool-discovery.md            # 工具发现与能力映射
│   ├── orchestration-rules.md       # 编排规则（拆解/并行/提示词）
│   └── error-handling.md            # 错误处理与降级策略
└── scripts/
    └── log_error.py                 # 错误日志生成器
```

## 🎯 8个预设使用场景

| # | 场景 | 触发词 | 工具链 |
|---|------|--------|--------|
| 1 | 课程设计自动化 | 课程设计、斯特林、建模 | WebSearch → docx → pdfkit-py → pptx → solidworks |
| 2 | 校园信息监控 | 监控、公告、抓取 | web-scraper → wechat-search → api-gateway |
| 3 | 考研备考助手 | 考研、真题、错题 | WebSearch → education → pdfkit-py |
| 4 | BuddyOS开发发布 | 开发、调试、发布 | Edit → test → github MCP → release |
| 5 | SolidWorks建模+文档 | 建模、装配、工程图 | com-automation → agent-browser → docx → pdfkit-py |
| 6 | 非遗传媒文创 | 非遗、文化、内容 | WebSearch → docx → ImageGen → pptx |
| 7 | 数据采集+分析 | 数据、爬取、图表 | web-scraper → pandas → matplotlib → docx |
| 8 | 通用文档处理 | 文档、转换、格式 | docx → xlsx → pptx → pdfkit-py |

## 🚀 快速开始

### 安装

1. 将 `task-orchestrator/` 目录放入 `~/.workbuddy/skills/`（用户级）或 `.workbuddy/skills/`（项目级）
2. 重启 WorkBuddy 或发送任意消息以触发 Skills 刷新

### 触发方式

- **自动触发**：任务涉及 3+ 步骤或跨多个工具类别时自动激活
- **显式调用**：说 `编排`、`拆解`、`多步骤`、`/orchestrate`
- **关键词匹配**：匹配到预设场景的关键词时自动加载对应模板

### 使用示例

```
用户：帮我完成斯特林发动机课程设计

→ task-orchestrator 自动触发
→ 匹配「课程设计自动化」预设
→ 展示 7 步计划，等待确认
→ 确认后自动执行：搜索资料 → 写说明书 → 建模 → 生成PPT → 导出PDF
```

## 🔄 工作流程

```
用户请求
  │
  ├─ Phase 1: 分析 & 规划
  │   ├─ 解析需求
  │   ├─ 发现可用工具
  │   ├─ 拆解子任务
  │   ├─ 匹配预设场景
  │   └─ 展示计划表
  │
  ├─ Phase 2: 执行（用户确认后）
  │   ├─ 串行执行依赖步骤
  │   ├─ 并行执行独立步骤
  │   ├─ 失败 → Plan B → Plan C
  │   └─ 记录所有结果
  │
  └─ Phase 3: 报告
      ├─ 汇总成功/失败表
      ├─ 失败: 写入 .log 文件 + 手动方案
      └─ 交付最终产物
```

## 📋 降级策略

| 错误类型 | Plan A | Plan B | Plan C |
|---------|--------|--------|--------|
| 依赖缺失 | 自动安装 | 完整路径 | 手动安装指南 |
| 权限拒绝 | 换目录 | --user 安装 | 申请权限 |
| 服务未运行 | 检查+启动 | 备用工具 | 手动启动指南 |
| 认证失败 | 检查环境变量 | 备用认证 | 手动认证指南 |

## 🛠️ 依赖技能（推荐安装）

- `pdfkit-py` — PDF 处理（50个命令）
- `docx` — Word 文档处理
- `minimax-xlsx` — Excel 高级功能
- `pptx` — 演示文稿创建
- `agent-browser-core` — 浏览器自动化
- `web-scraper` — 网页抓取
- `solidworks-com-automation` — SW 2024 COM 自动化
- `education` — 教育学习工具
- `github` — GitHub 集成

## 📊 项目背景

### 为什么创建

用户拥有 120+ Skills 但面临：
- **选择困难**：功能重叠（如 4 个 PDF 技能）
- **流程断裂**：多步任务需要手动串联工具
- **无降级**：工具失败后不知道下一步怎么办
- **无记录**：失败原因无法追溯

### 解决思路

1. 全面审计 120+ Skills，识别功能重叠
2. 激进合并（N合一），删除 8 个冗余技能
3. 构建编排引擎，自动化工具选择和降级
4. 设计 8 个预设场景，覆盖常见工作流

### 达到的效果

- 技能从 120+ 精简到核心可用，避免 AI 决策瘫痪
- 复杂任务从"手动串联 6 步"变成"一次确认，自动完成"
- 每个步骤都有降级方案，不会因单一工具失败而中断
- 完整错误日志，可追溯可手动修复

## 📦 完整项目产物

| 文件 | 说明 |
|------|------|
| `skills/task-orchestrator/SKILL.md` | 核心编排技能 |
| `skills/task-orchestrator/references/*.md` | 3 个参考文件 |
| `skills/task-orchestrator/scripts/log_error.py` | 错误日志脚本 |
| `docs/Skills功能重叠分析与优化方案.docx` | 完整 Word 说明书（9章） |
| `docs/functional-overlap-analysis.md` | 功能重叠分析报告 |
| `docs/browser-automation-test-results.md` | 浏览器自动化测试详情 |

## 📄 License

MIT

---

_为 WorkBuddy 生态构建 — 让 AI Agent 真正学会协同工作_
