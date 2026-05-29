---
name: task-orchestrator
description: |
  Intelligent task orchestrator that decomposes complex multi-step tasks into subtasks,
  assigns appropriate tools (Skills/CLI/MCP) to each, manages fallback strategies (Plan B),
  and generates error logs with manual resolution steps when automated solutions fail.
  This skill should be used when the user's request involves 3+ distinct steps, requires
  coordination between multiple tools, or when the user explicitly asks for orchestration.
  Trigger keywords: orchestrate, 编排, 拆解, 多步骤, 复杂任务, /orchestrate.
  Auto-triggers when a task clearly exceeds the complexity of a single tool call.
agent_created: true
---

# Task Orchestrator

## Purpose

Orchestrate complex multi-step tasks by:
1. Decomposing user requests into independent subtasks
2. Mapping each subtask to the best tool (Skill → CLI → MCP → direct code)
3. Defining Plan B fallback strategies for each subtask
4. Executing the plan autonomously after user confirmation
5. Logging errors with manual resolution steps when all automated strategies fail

## When to Use

**Auto-trigger**: When user request has 3+ distinct steps or spans multiple tool categories.

**Explicit trigger**: When user says "orchestrate", "编排", "拆解", "多步骤", or "/orchestrate".

**Skip**: For simple single-tool tasks (e.g., "read this file", "search for X").

## Core Workflow

### Phase 1: Analyze & Plan

1. **Parse the user request** to extract:
   - Core goal (what must be achieved)
   - Constraints (environment, permissions, preferences)
   - Implicit prerequisites (things needed before the main task)

2. **Discover available tools** by scanning:
   - Skills: list `~/.workbuddy/skills/` and `.workbuddy/skills/`
   - CLI: check available commands (gh, npx, python, etc.)
   - MCP: read `~/.workbuddy/mcp.json` for configured servers
   - See `references/tool-discovery.md` for discovery patterns

3. **Decompose into subtasks** following `references/orchestration-rules.md`:
   - Each subtask = one tool call
   - Mark dependencies (parallel vs serial)
   - Define primary tool + Plan B fallback

4. **Present the plan** as a table for user confirmation:

```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | xxx    | skill:pdf   | CLI   | -    | -     |
| 2 | xxx    | mcp:github  | gh    | 1    | -     |
```

### Phase 2: Execute (after confirmation)

1. **Execute subtasks in order** respecting dependencies
2. **Run parallel subtasks concurrently** when possible
3. **On failure → try Plan B → Plan C → log error**
4. **Record results** for each subtask (success/failure/output)

### Phase 3: Report

1. Summarize results in a table
2. List any failures with manual resolution steps
3. Write error logs to `C:/Users/Mypc/.workbuddy/logs/task-errors/{task_id}.log`

## Fallback Strategy

For each subtask, always have at least one Plan B. Follow `references/error-handling.md`:

| Error Type | Plan A | Plan B | Plan C |
|-----------|--------|--------|--------|
| Missing dependency | Auto-install | Use full path | Manual install guide |
| Permission denied | Alt directory | --user install | Request permission |
| Service not running | Check & start | Alternative tool | Manual startup guide |
| Auth required | Check env vars | Alt auth method | Manual auth guide |

## Prompt Construction for Subtask Agents

When dispatching a subtask to an agent, construct prompts containing:
1. **Role**: What this subtask is in the overall plan
2. **Input**: Specific data/files needed
3. **Output**: Exact format required
4. **Context**: Results from previous steps
5. **Fallback**: "If this fails, try..."

### Example prompt template:
```
[子任务 2/5] 从PDF中提取表格数据
上下文：前一步已生成 input.pdf
输入：C:/path/to/input.pdf
输出：JSON 格式的表格数据
工具：pdfkit-py extract_table
降级：如果 extract_table 失败，尝试 pymupdf_edit + exec_python
```

## Error Logging Format

When all fallbacks exhausted, write to log file:
```
[ERROR] 2025-XX-XX HH:MM:SS - task-{id} - {subtask}
  Plan A: {tool} → {error}
  Plan B: {tool} → {error}
  Plan C: {tool} → {error}
  操作指导: {manual steps to resolve}
```

## Use Case Presets

When the user's request matches one of these patterns, use the preset plan as a starting point, then adapt to specifics.

### 课程设计自动化 (Course Design Automation)
**触发词**: 课程设计、斯特林、建模、说明书、图纸
**场景**: 机械工程课程设计全流程
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 收集设计资料 | WebSearch | web-scraper skill | - | ✅ |
| 2 | 整理知识点 | 直接整理 | education skill | 1 | - |
| 3 | 撰写设计说明书 | docx skill | python-docx | 2 | - |
| 4 | 生成机构运动简图 | pdfkit-py pdf_create | reportlab | 2 | ✅ |
| 5 | 创建3D模型 | solidworks-com-automation | 手动建模指南 | 2 | ✅ |
| 6 | 生成展示PPT | pptx skill | pptxgenjs | 3 | - |
| 7 | 导出PDF终稿 | pdfkit-py convert | soffice | 3,4,5 | - |
```

### 校园信息监控与推送 (Campus Info Monitor)
**触发词**: 监控、公告、抓取、通知、学校官网
**场景**: 自动抓取多个信息源，筛选推送
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 抓取学校官网 | web-scraper skill | WebFetch | - | ✅ |
| 2 | 抓取微信公众号 | wechat-article-search | WebSearch | - | ✅ |
| 3 | 解析关键公告 | 直接分析 | AI 摘要 | 1,2 | - |
| 4 | 生成摘要报告 | docx skill | Markdown | 3 | - |
| 5 | 推送通知 | api-gateway (QQ/微信) | buddy-secretary | 3 | - |
```

### 考研备考助手 (Exam Prep Assistant)
**触发词**: 考研、真题、错题、复习计划、刷题
**场景**: 收集真题→整理错题→生成复习计划→定期推送
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 搜索历年真题 | WebSearch | wechat-article-search | - | ✅ |
| 2 | 整理知识点框架 | education skill | 直接整理 | 1 | - |
| 3 | 生成刷题计划 | 直接生成 | arxiv-reader skill | 2 | - |
| 4 | 分析错题规律 | 数据分析 | education skill | 1 | - |
| 5 | 导出复习资料 | pdfkit-py pdf_create | docx skill | 2,3,4 | - |
```

### BuddyOS 开发发布流水线 (Development Pipeline)
**触发词**: 开发、调试、发布、Release、提交
**场景**: 代码修改→本地测试→提交GitHub→生成Release Note
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 修改/新增代码 | 直接编辑 | 写脚本 | - | - |
| 2 | 本地运行测试 | python 脚本 | Bash 检查 | 1 | - |
| 3 | 更新版本号 | Edit (version) | 手动记录 | 2 | - |
| 4 | 生成提交信息 | 直接生成 | gh CLI | 3 | - |
| 5 | 提交+推送 | github MCP | gh CLI | 4 | - |
| 6 | 生成Release Note | 直接生成 | markitdown skill | 5 | - |
```

### SolidWorks 建模+文档自动化 (CAD + Docs Automation)
**触发词**: SolidWorks、建模、模型、装配、工程图
**场景**: 参数设计→COM建模→截图→插入说明书
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 计算设计参数 | python 脚本 | 手动计算 | - | - |
| 2 | 创建零件模型 | solidworks-com-automation | 手动建模 | 1 | - |
| 3 | 创建装配体 | solidworks-com-automation | 手动装配 | 2 | - |
| 4 | 导出模型截图 | agent-browser (截图) | SW 截图 | 3 | - |
| 5 | 插入说明书 | docx skill (插入图片) | python-docx | 4 | - |
| 6 | 生成最终PDF | pdfkit-py convert | soffice | 5 | - |
```

### 非遗传媒文创内容创作 (Cultural Heritage Content)
**触发词**: 非遗、文化、文创、内容创作、文章
**场景**: 搜索非遗资料→整理内容→生成文章→设计封面→发布
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 搜索非遗资料 | WebSearch | wechat-article-search | - | - |
| 2 | 整理文化背景 | 直接整理 | deep-research skill | 1 | - |
| 3 | 撰写文章正文 | docx skill | Markdown | 2 | - |
| 4 | 设计封面图片 | ImageGen | canvas-design skill | 2 | ✅ |
| 5 | 生成发布用PPTX | pptx skill | pptxgenjs | 3 | ✅ |
| 6 | 导出PDF存档 | pdfkit-py convert | soffice | 3,4,5 | - |
```

### 数据采集+分析+可视化 (Data Pipeline)
**触发词**: 数据、爬取、分析、图表、可视化、报告
**场景**: 多源数据采集→清洗→分析→可视化→报告
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 采集网页数据 | web-scraper skill | playwright-browser | - | - |
| 2 | 清洗数据 | python pandas | minimax-xlsx | 1 | - |
| 3 | 数据分析 | python pandas | minimax-xlsx | 2 | - |
| 4 | 生成图表 | python matplotlib | minimax-xlsx chart | 3 | - |
| 5 | 生成分析报告 | docx skill | Markdown | 4 | - |
| 6 | 导出PDF终稿 | pdfkit-py convert | soffice | 5 | - |
```

### 通用文档处理流水线 (Document Processing Pipeline)
**触发词**: 文档、转换、整理、格式、PDF、Word、Excel、PPT
**场景**: 任意格式→处理→多格式输出
```
| # | 子任务 | 工具 (Plan A) | Plan B | 依赖 | 并行? |
|---|--------|-------------|--------|------|-------|
| 1 | 读取源文档 | skill (对应格式) | pandas/pandoc | - | - |
| 2 | 内容分析/清洗 | python 脚本 | skill 内置功能 | 1 | - |
| 3 | 生成表格/数据 | minimax-xlsx | python openpyxl | 2 | ✅ |
| 4 | 生成文档 | docx skill | python-docx | 2 | ✅ |
| 5 | 生成演示文稿 | pptx skill | pptxgenjs | 2 | ✅ |
| 6 | 生成PDF | pdfkit-py convert | soffice | 3,4,5 | - |
```

## Important Rules

1. **Never skip the confirmation step** unless the user explicitly requests full autonomy
2. **Always define Plan B** before executing any subtask
3. **Log ALL failures** with actionable manual resolution steps
4. **Respect tool priority**: MCP > Skill > CLI > Direct code
5. **Max 25 subtasks per orchestration** to keep plans manageable
6. **Prefer parallel execution** when subtasks are independent
7. **Use presets above** as templates when user's request matches a known pattern. Adapt presets to specifics rather than starting from scratch.
