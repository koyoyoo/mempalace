# 职责: 项目任务定义文件，类似 package.json scripts
# 用法: just <任务名> [参数...]

# Windows 使用 PowerShell 作为 shell
set shell := ["powershell", "-Command"]

# 默认显示帮助
_default:
    @just --list

# 提交代码 (用法: just commit "feat: xxx")
commit msg:
    git add -A
    git commit -m "{{msg}}"
    git push origin HEAD

# 提交并打标签 (手动指定版本: just tag v1.0.0 "feat: xxx")
tag version msg:
    git add -A
    git commit -m "{{msg}}"
    git tag -a "{{version}}" -m "{{version}}: {{msg}}"
    git push origin HEAD
    git push origin "{{version}}"
    @echo "✓ 完成: {{version}}"

# 自动递增 Patch 版本 (v0.1.0 -> v0.1.1)
# 用法: just auto-tag "feat: xxx"
auto-tag msg:
    $latest = (git describe --tags --abbrev=0 2>$null) -replace 'v', ''; if (-not $latest) { $latest = '0.0.0' }; \
    $parts = $latest.Split('.'); \
    $major = [int]$parts[0]; $minor = [int]$parts[1]; $patch = [int]$parts[2] + 1; \
    $version = "v$major.$minor.$patch"; \
    git add -A; \
    git commit -m "{{msg}}"; \
    git tag -a $version -m "${version}: {{msg}}"; \
    git push origin HEAD; \
    git push origin $version; \
    Write-Host "✓ 完成: $version"

# 递增 Minor 版本 (v0.1.0 -> v0.2.0)
# 用法: just tag-minor "feat: xxx"
tag-minor msg:
    $latest = (git describe --tags --abbrev=0 2>$null) -replace 'v', ''; if (-not $latest) { $latest = '0.0.0' }; \
    $parts = $latest.Split('.'); \
    $major = [int]$parts[0]; $minor = [int]$parts[1] + 1; $patch = 0; \
    $version = "v$major.$minor.$patch"; \
    git add -A; \
    git commit -m "{{msg}}"; \
    git tag -a $version -m "${version}: {{msg}}"; \
    git push origin HEAD; \
    git push origin $version; \
    Write-Host "✓ 完成: $version"

# 递增 Major 版本 (v0.1.0 -> v1.0.0)
# 用法: just tag-major "feat: xxx"
tag-major msg:
    $latest = (git describe --tags --abbrev=0 2>$null) -replace 'v', ''; if (-not $latest) { $latest = '0.0.0' }; \
    $parts = $latest.Split('.'); \
    $major = [int]$parts[0] + 1; $minor = 0; $patch = 0; \
    $version = "v$major.$minor.$patch"; \
    git add -A; \
    git commit -m "{{msg}}"; \
    git tag -a $version -m "${version}: {{msg}}"; \
    git push origin HEAD; \
    git push origin $version; \
    Write-Host "✓ 完成: $version"

# 仅打标签 (自动递增 patch)
# 用法: just auto-tag-only "feat: xxx"
auto-tag-only msg:
    $latest = (git describe --tags --abbrev=0 2>$null) -replace 'v', ''; if (-not $latest) { $latest = '0.0.0' }; \
    $parts = $latest.Split('.'); \
    $major = [int]$parts[0]; $minor = [int]$parts[1]; $patch = [int]$parts[2] + 1; \
    $version = "v$major.$minor.$patch"; \
    git tag -a $version -m "${version}: {{msg}}"; \
    git push origin $version; \
    Write-Host "✓ 完成: $version"

# 查看日志
log:
    git log --oneline -20

# 查看标签
tags:
    git tag -l -n1

# 运行测试
test:
    cd local_graphrag_mcp && .venv\Scripts\python -m pytest tests/ -v

# 测试 MCP 协议层（真实客户端调用）
test-mcp:
    cd local_graphrag_mcp && .venv\Scripts\python test_mcp_client.py

# 运行生产环境测试（直接调用 SearchService）
test-debug:
    cd local_graphrag_mcp && .venv\Scripts\python scripts\debug_mcp.py

# 运行所有测试（单元测试 + MCP 协议层测试）
test-all:
    cd local_graphrag_mcp ; .venv\Scripts\python -m pytest tests/ -v ; .venv\Scripts\python test_mcp_client.py

# 代码检查与格式化
lint:
    cd local_graphrag_mcp && .venv\Scripts\ruff check . --fix && .venv\Scripts\ruff format .

# 类型检查
type:
    cd local_graphrag_mcp && pyright

# 安装依赖
install:
    cd local_graphrag_mcp && py -m pip install -e .

