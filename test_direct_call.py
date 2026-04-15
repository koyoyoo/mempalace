#!/usr/bin/env python3
"""直接调用 tool_add_drawer 测试功能，绕过 MCP 协议"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from mempalace.mcp_server import tool_add_drawer

def test_add_drawer_direct():
    """直接调用 tool_add_drawer 测试"""
    logger.info("=" * 60)
    logger.info("直接调用 tool_add_drawer 测试")
    logger.info("=" * 60)

    # 测试1: 正常内容
    logger.info("\n测试1: 正常内容")
    try:
        result = tool_add_drawer(
            wing='mempalace',
            room='documentation',
            content='测试正常内容'
        )
        logger.info(f"✅ 测试1成功: {result}")
    except Exception as e:
        logger.error(f"❌ 测试1失败: {e}")
        logger.exception("详细异常:")

    # 测试2: 包含代理字符的内容
    logger.info("\n测试2: 包含代理字符的内容")
    surrogate_content = "娴嬭瘯鐭\udcad鍐呭\udcae\udcb9"
    try:
        result = tool_add_drawer(
            wing='mempalace',
            room='documentation',
            content=surrogate_content
        )
        logger.info(f"✅ 测试2成功: {result}")
    except Exception as e:
        logger.error(f"❌ 测试2失败: {e}")
        logger.exception("详细异常:")

    # 测试3: 长内容
    logger.info("\n测试3: 长内容")
    long_content = "测试长内容 " * 100
    try:
        result = tool_add_drawer(
            wing='mempalace',
            room='documentation',
            content=long_content
        )
        logger.info(f"✅ 测试3成功: {result}")
    except Exception as e:
        logger.error(f"❌ 测试3失败: {e}")
        logger.exception("详细异常:")

    logger.info("=" * 60)
    logger.info("测试完成")
    logger.info("=" * 60)

if __name__ == "__main__":
    test_add_drawer_direct()
