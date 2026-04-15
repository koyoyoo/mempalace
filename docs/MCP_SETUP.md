# MemPalace MCP 配置指南

本文档介绍如何将 MemPalace 配置为 MCP (Model Context Protocol) 服务器，使 AI 客户端（Claude、Cursor、Gemini CLI 等）能够调用 MemPalace 的 29 个工具。

## 前置条件

1. MemPalace 已安装:
   ```bash
   pip install mempalace
   # 或从源码安装
   pip install -e .
   ```

2. (可选) Ollama 已配置:
   ```bash
   # 如果使用 Ollama embedding，确保 ollama 服务运行中
   ollama serve
   ```

## 配置方法

### 方法一: Claude Code (推荐)

Claude Code 支持原生 MCP 插件市场安装:

```bash
# 1. 添加插件市场
claude plugin marketplace add milla-jovovich/mempalace

# 2. 安装插件
claude plugin install --scope user mempalace

# 3. 重启 Claude Code
# 4. 输入 /skills 验证 "mempalace" 出现在列表中
```

**特点:**
- 自动更新
- 集成 Claude Code 生态
- 无需手动配置 MCP JSON

---

### 方法二: 手动添加 MCP (通用)

适用于 Claude Desktop、Cursor、Windsurf 等任何支持 MCP 的客户端。

#### 步骤 1: 获取 MemPalace 路径

```bash
# 确认 mempalace 可执行
which mempalace
# 输出例如: /usr/local/bin/mempalace
# 或 Windows: C:\Python312\Scripts\mempalace.exe

# 确认 Python 模块路径
python -c "import mempalace; print(mempalace.__file__)"
# 输出例如: /home/user/.local/lib/python3.12/site-packages/mempalace/__init__.py
```

#### 步骤 2: 配置 MCP 服务器

##### Claude Desktop (claude_desktop_config.json)

文件位置:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "python",
      "args": ["-m", "mempalace.mcp_server"],
      "env": {
        "MEMPALACE_PALACE_PATH": "~/.mempalace/palace",
        "OLLAMA_BASE_URL": "http://localhost:11434"
      }
    }
  }
}
```

##### Cursor (settings.json)

文件位置:
- **VS Code 设置**: `~/.cursor/settings.json` 或 `.vscode/settings.json`

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "python",
      "args": ["-m", "mempalace.mcp_server"],
      "env": {
        "MEMPALACE_PALACE_PATH": "~/.mempalace/palace"
      }
    }
  }
}
```

##### Windsurf (config.yaml)

文件位置: `~/.windsurf/config.yaml`

```yaml
mcp_servers:
  mempalace:
    command: python
    args:
      - -m
      - mempalace.mcp_server
    env:
      MEMPALACE_PALACE_PATH: ~/.mempalace/palace
```

##### 通用 MCP 客户端

多数 MCP 客户端支持以下格式:

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "python",
      "args": ["-m", "mempalace.mcp_server"],
      "env": {
        "MEMPALACE_PALACE_PATH": "~/.mempalace/palace"
      }
    }
  }
}
```

---

### 方法三: Gemini CLI (自动集成)

MemPalace 原生支持 Gemini CLI，配置最简单:

```bash
# Gemini CLI 自动处理 MCP 配置
# 只需确保 mempalace 已安装，Gemini CLI 会自动发现

# 验证 Gemini CLI 已安装
gemini --version

# 使用 (Gemini CLI 会自动调用 mempalace MCP 工具)
gemini chat
```

**特点:**
- 自动处理服务器和保存 hooks
- 无需手动配置
- 自动记忆保存

---

## 环境变量配置

### 必需

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `MEMPALACE_PALACE_PATH` | Palace 数据目录 | `~/.mempalace/palace` |

### 可选 (Ollama)

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OLLAMA_BASE_URL` | Ollama API 地址 | `http://localhost:11434` |

### 可选 (其他)

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `MEMPALACE_CONFIG_DIR` | 配置目录覆盖 | `~/.mempalace` |
| `MEMPAL_DIR` | 自动挖掘目录 | (未设置) |

---

## 验证配置

### 1. 命令行测试

```bash
# 直接启动 MCP 服务器 (前台运行，用于测试)
python -m mempalace.mcp_server

# 带自定义 palace 路径
python -m mempalace.mcp_server --palace /path/to/palace
```

成功启动后，服务器会等待 stdin 的 JSON-RPC 消息。

### 2. 客户端验证

配置完成后，重启客户端并检查:

**Claude Code:**
```
/tools  # 查看可用工具列表，应包含 mempalace_ 开头的工具
```

**Claude Desktop:**
查看 Settings > Developer > MCP Servers，应显示 mempalace 为绿色状态。

**Cursor:**
使用 Command Palette (Ctrl+Shift+P) > "MCP: List Servers"

### 3. 功能测试

向 AI 提问验证 MCP 工具调用:

> "使用 mempalace_status 查看我的 palace 状态"

预期响应:
```
I'll check your palace status using the mempalace MCP tool.

[调用 mempalace_status]

Your palace contains:
- 1,234 drawers across 5 wings
- Wings: project-a, project-b, personal, work, diary
```

---

## 可用工具列表

配置成功后，AI 客户端可调用以下 29 个工具:

### Palace 读取
- `mempalace_status` - Palace 概览
- `mempalace_list_wings` - 列出所有 wings
- `mempalace_list_rooms` - 列出 wing 中的 rooms
- `mempalace_get_taxonomy` - 完整层级结构
- `mempalace_search` - 语义搜索
- `mempalace_check_duplicate` - 重复检测

### Palace 写入
- `mempalace_add_drawer` - 添加内容
- `mempalace_delete_drawer` - 删除内容
- `mempalace_update_drawer` - 更新内容

### 知识图谱
- `mempalace_kg_query` - 查询实体关系
- `mempalace_kg_add` - 添加事实
- `mempalace_kg_timeline` - 实体时间线

### 导航
- `mempalace_traverse` - 遍历图
- `mempalace_find_tunnels` - 发现连接
- `mempalace_create_tunnel` - 创建连接

### 抽屉管理
- `mempalace_get_drawer` - 获取单个抽屉
- `mempalace_list_drawers` - 列出抽屉

### 代理日记
- `mempalace_diary_write` - 写入日记
- `mempalace_diary_read` - 读取日记

---

## 故障排除

### MCP 服务器未启动

**现象:** 客户端显示 "mempalace server disconnected"

**解决:**
```bash
# 检查 Python 路径
which python
python -c "import mempalace; print('OK')"

# 测试直接启动
python -m mempalace.mcp_server --palace ~/.mempalace/palace
```

### 工具不显示

**现象:** 客户端工具列表没有 mempalace_ 工具

**解决:**
1. 确认配置文件路径正确
2. 重启客户端
3. 检查客户端 MCP 日志

### Ollama 连接失败

**现象:** 搜索/添加时出现 embedding 错误

**解决:**
```bash
# 检查 Ollama 状态
curl http://localhost:11434/api/tags

# 确认模型已下载
ollama list
```

### Palace 路径错误

**现象:** "No palace found" 错误

**解决:**
```bash
# 确认 palace 存在
ls ~/.mempalace/palace/chroma.sqlite3

# 或创建新 palace
mempalace init ~/my-project
mempalace mine ~/my-project
```

---

## 高级配置

### 多 Palace 切换

为不同项目配置不同的 palace:

```json
{
  "mcpServers": {
    "mempalace-work": {
      "command": "python",
      "args": ["-m", "mempalace.mcp_server", "--palace", "~/work-palace"]
    },
    "mempalace-personal": {
      "command": "python",
      "args": ["-m", "mempalace.mcp_server", "--palace", "~/personal-palace"]
    }
  }
}
```

### Docker 部署

```json
{
  "mcpServers": {
    "mempalace": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "~/.mempalace:/data",
        "-e", "MEMPALACE_PALACE_PATH=/data/palace",
        "mempalace:latest"
      ]
    }
  }
}
```

---

## 参考

- [MCP 协议文档](https://modelcontextprotocol.io/)
- [MemPalace README](https://github.com/milla-jovovich/mempalace#mcp-server)
- [Ollama 配置](./OLLAMA_SETUP.md)
