#!/usr/bin/env python3
"""测试sanitize_chinese_text函数"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from mempalace.config import sanitize_chinese_text

# 测试包含代理字符的内容
test_cases = [
    "娴嬭瘯鐭\udcad鍐呭\udcae\udcb9",
    "这是一个测试内容，包含中文字符",
    "Test with surrogates\ud800\udc00",
    "Normal text without surrogates",
]

print("=" * 60)
print("测试 sanitize_chinese_text 函数")
print("=" * 60)

for i, test_case in enumerate(test_cases, 1):
    print(f"\n测试 {i}: {repr(test_case)}")
    print(f"原始长度: {len(test_case)}")
    
    cleaned = sanitize_chinese_text(test_case, method="remove_surrogates")
    print(f"清理后: {repr(cleaned)}")
    print(f"清理后长度: {len(cleaned)}")
    print(f"是否移除了字符: {len(test_case) != len(cleaned)}")
    
    # 检查是否还有代理字符
    has_surrogates = any(0xD800 <= ord(char) <= 0xDFFF for char in cleaned)
    print(f"是否仍有代理字符: {has_surrogates}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
