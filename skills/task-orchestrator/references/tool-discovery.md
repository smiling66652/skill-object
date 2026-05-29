# 工具发现与能力映射

## 可用工具类别

task-orchestrator 需要了解三类可用工具：

### 1. Skills
路径：`~/.workbuddy/skills/` 和 `.workbuddy/skills/`（插件）
查找方式：遍历所有 SKILL.md 文件，解析 YAML frontmatter 中的 name 和 description

### 2. CLI 工具
- `which` 检查 PATH 中的命令
- `npm list -g` 检查全局 Node.js 包
- `pip list` 检查 Python 包
- 常见 CLI：gh, npx, python, node, git, docker, etc.

### 3. MCP 服务器
配置文件：`~/.workbuddy/mcp.json`
检查 mcpServers 字段获取所有已配置的 MCP 服务器

## 能力分类

| 领域 | 技能 | CLI | MCP |
|------|------|-----|-----|
| PDF处理 | pdfkit-py | - | - |
| DOCX处理 | docx | - | - |
| XLSX处理 | minimax-xlsx | - | - |
| PPTX处理 | pptx | - | - |
| 浏览器自动化 | agent-browser-core, playwright-browser-automation | npx agent-browser, npx playwright | Playwright MCP |
| GitHub | github | gh | GitHub MCP |
| SolidWorks | solidworks-com-automation | - | - |
| API网关 | api-gateway | maton | - |

## 工具选择优先级

1. **MCP 优先**：如果功能有 MCP 实现，优先使用 MCP（更标准化、错误处理更好）
2. **Skill 其次**：如果功能有 skill 封装，使用 skill（带上下文和文档）
3. **CLI 作为降级**：当 skill/MCP 不可用时，降级到原始 CLI
4. **直接编码**：最后手段，用 Python/Node.js 直接实现
