# 错误处理与降级策略

## 降级层级

每个子任务按以下层级降级：
```
Plan A (首选) → Plan B (备用) → Plan C (兜底) → 记录错误 + 手动方案
```

## 常见错误类型与降级策略

### 依赖缺失
- 症状：ModuleNotFoundError, command not found
- Plan A：自动安装（pip install / npm install）
- Plan B：检查 PATH，用完整路径
- Plan C：手动安装说明

### 权限错误
- 症状：Permission denied, EACCES
- Plan A：换到允许的目录
- Plan B：用 --user 或本地安装
- Plan C：向用户申请权限

### 环境缺失
- 症状：COM未注册、服务未启动
- Plan A：检查服务状态，尝试启动
- Plan B：用备用工具替代
- Plan C：记录需要手动启动的服务

### API/认证错误
- 症状：401, 403, not authenticated
- Plan A：检查环境变量
- Plan B：尝试其他认证方式（token vs OAuth）
- Plan C：提示用户手动认证

## 错误日志格式

当所有降级方案都失败时，生成以下格式的错误日志：
```
[ERROR] {timestamp} - {task_id} - {subtask_name}
 工具链：{tool_chain_tried}
 错误信息：{original_error}
 操作指导：{manual_fix_instructions}
 文件路径：C:/Users/Mypc/.workbuddy/logs/task-errors/{task_id}.log
```

## 恢复策略

- 每次子任务失败时，检查是否可以跳过继续
- 如果可以跳过，记录跳过原因，继续后续步骤
- 如果不可跳过（关键路径），标记整个任务失败
