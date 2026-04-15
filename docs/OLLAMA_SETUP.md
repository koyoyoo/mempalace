# MemPalace + Ollama 本地 Embedding 配置指南

MemPalace 支持使用 Ollama 本地运行的 embedding 模型（如 qwen3-embedding），
替代默认的 ChromaDB ONNX 模型。

## 优势

- **完全本地**: 无需下载 ChromaDB 默认的 ONNX 模型 (~50MB)
- **中文优化**: Qwen3-embedding 对中文语义理解更好
- **灵活切换**: 可随时切换不同 embedding 模型进行对比测试

## 前置要求

1. 安装并启动 Ollama: https://ollama.com
2. 拉取 embedding 模型:
   ```bash
   ollama pull qwen3-embedding  # 或其他模型如 nomic-embed-text
   ```

## 配置方法

### 方法一: 修改配置文件

编辑 `~/.mempalace/config.json`:

```json
{
  "palace_path": "~/.mempalace/palace",
  "collection_name": "mempalace_drawers",
  "embedding_provider": "ollama",
  "ollama_model": "qwen3-embedding",
  "ollama_base_url": "http://localhost:11434"
}
```

### 方法二: 环境变量 (推荐)

```bash
# Windows PowerShell
$env:OLLAMA_BASE_URL = "http://localhost:11434"

# Windows CMD
set OLLAMA_BASE_URL=http://localhost:11434

# Linux/macOS
export OLLAMA_BASE_URL=http://localhost:11434
```

## 使用说明

### 验证 Ollama 服务

```bash
# 测试 Ollama 是否运行
curl http://localhost:11434/api/tags

# 测试 embedding 接口
curl -X POST http://localhost:11434/api/embed \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3-embedding", "input": ["hello world"]}'
```

### 初始化 palace

配置完成后，正常使用 mempalace 命令：

```bash
# 初始化 (会自动使用配置的 embedding provider)
mempalace init ~/my-project

# 挖掘数据
mempalace mine ~/my-project

# 搜索 (embedding 查询会通过 Ollama 处理)
mempalace search "查询内容"
```

### 切换回默认 embedding

将 `embedding_provider` 改为 `"default"` 或删除配置项即可。

## 支持的 Ollama Embedding 模型

| 模型 | 维度 | 特点 |
|------|------|------|
| qwen3-embedding | 1024 | 中文优化，多语言支持 |
| nomic-embed-text | 768 | 通用文本，性能好 |
| mxbai-embed-large | 1024 | 高质量，多语言 |
| snowflake-arctic-embed | 1024 | 轻量高效 |

## 故障排除

### 连接失败

```
Ollama embedding request failed: Connection refused
```

**解决**: 确认 Ollama 服务已启动

```bash
ollama serve  # 启动服务
```

### 模型不存在

```
model 'qwen3-embedding' not found
```

**解决**: 拉取模型

```bash
ollama pull qwen3-embedding
```

### 维度不匹配 (已有数据)

如果 palace 中已有使用不同 embedding 模型的数据，
需要创建新的 palace 或清空旧数据：

```bash
# 备份并重建
rm -rf ~/.mempalace/palace
mempalace init ~/my-project
mempalace mine ~/my-project
```

## 注意事项

1. **首次切换需重建**: 已有 palace 切换 embedding 模型后，原有数据与新查询的向量维度可能不匹配
2. **性能**: Ollama embedding 依赖本地 GPU/CPU 性能，可能比 ONNX 稍慢
3. **兼容性**: Qwen3-embedding 是 1024 维，确保与 palace 其他数据兼容

## 技术实现

- `mempalace.embeddings.OllamaEmbeddingFunction`: ChromaDB 兼容的 embedding 函数
- `ChromaBackend`: 支持注入自定义 embedding function
- 配置通过 `MempalaceConfig` 自动读取

## 相关代码

```python
from mempalace.embeddings import OllamaEmbeddingFunction
from mempalace.config import MempalaceConfig

# 手动使用
config = MempalaceConfig()
ef = OllamaEmbeddingFunction(
    model=config.ollama_model,
    base_url=config.ollama_base_url,
)

# 生成 embedding
embeddings = ef(["hello", "world"])
```
