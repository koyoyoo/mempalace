#!/usr/bin/env python3
"""单元测试：验证 drawer_id 生成中的代理字符问题"""

import sys
import logging
import hashlib
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_drawer_id_generation_with_surrogate():
    """测试包含代理字符的内容生成 drawer_id"""
    logger.info("=" * 60)
    logger.info("测试 drawer_id 生成中的代理字符问题")
    logger.info("=" * 60)

    # 正常内容
    normal_content = "测试短内容"
    wing = "mempalace"
    room = "documentation"

    try:
        drawer_id = f"drawer_{wing}_{room}_{hashlib.sha256((wing + room + normal_content).encode()).hexdigest()[:24]}"
        logger.info(f"✅ 正常内容生成 drawer_id 成功: {drawer_id}")
    except Exception as e:
        logger.error(f"❌ 正常内容生成 drawer_id 失败: {e}")

    # 包含代理字符的内容（从日志中看到的实际内容）
    # 日志显示：'content': '娴嬭瘯鐭\udcad鍐呭\udcae\udcb9'
    surrogate_content = "娴嬭瘯鐭\udcad鍐呭\udcae\udcb9"

    logger.info(f"\n测试包含代理字符的内容: {repr(surrogate_content)}")
    logger.info(f"内容长度: {len(surrogate_content)}")

    try:
        drawer_id = f"drawer_{wing}_{room}_{hashlib.sha256((wing + room + surrogate_content).encode()).hexdigest()[:24]}"
        logger.info(f"✅ 包含代理字符的内容生成 drawer_id 成功: {drawer_id}")
    except UnicodeEncodeError as e:
        logger.error(f"❌ 包含代理字符的内容生成 drawer_id 失败: {e}")
        logger.error(f"   错误类型: {type(e).__name__}")
        return False
    except Exception as e:
        logger.error(f"❌ 包含代理字符的内容生成 drawer_id 失败: {e}")
        logger.error(f"   错误类型: {type(e).__name__}")
        return False

    logger.info("=" * 60)
    logger.info("测试完成")
    logger.info("=" * 60)
    return True


def test_drawer_id_generation_with_surrogate_fix():
    """测试修复后的 drawer_id 生成方法"""
    logger.info("=" * 60)
    logger.info("测试修复后的 drawer_id 生成方法")
    logger.info("=" * 60)

    # 包含代理字符的内容
    surrogate_content = "娴嬭瘯鐭\udcad鍐呭\udcae\udcb9"
    wing = "mempalace"
    room = "documentation"

    logger.info(f"\n测试包含代理字符的内容: {repr(surrogate_content)}")

    # 修复方法：先清理代理字符，再编码
    def sanitize_for_id(content: str) -> str:
        """清理代理字符，用于生成 drawer_id"""
        # 移除代理字符（范围 U+D800 到 U+DFFF）
        return ''.join(char for char in content if not (0xD800 <= ord(char) <= 0xDFFF))

    try:
        cleaned_content = sanitize_for_id(surrogate_content)
        logger.info(f"清理后的内容: {repr(cleaned_content)}")
        logger.info(f"清理后内容长度: {len(cleaned_content)}")

        drawer_id = f"drawer_{wing}_{room}_{hashlib.sha256((wing + room + cleaned_content).encode()).hexdigest()[:24]}"
        logger.info(f"✅ 修复后的方法生成 drawer_id 成功: {drawer_id}")
        return True
    except Exception as e:
        logger.error(f"❌ 修复后的方法仍然失败: {e}")
        logger.error(f"   错误类型: {type(e).__name__}")
        return False

    logger.info("=" * 60)
    logger.info("测试完成")
    logger.info("=" * 60)


if __name__ == "__main__":
    logger.info("开始单元测试...")
    
    # 测试当前方法
    test_drawer_id_generation_with_surrogate()
    
    # 测试修复方法
    test_drawer_id_generation_with_surrogate_fix()
