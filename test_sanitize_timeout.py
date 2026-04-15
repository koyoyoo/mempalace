#!/usr/bin/env python3
"""Test script with timeout to debug sanitize functions."""

import sys
import logging
import threading
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from mempalace.config import sanitize_name, sanitize_content


def test_with_timeout(func, *args, timeout=5, **kwargs):
    """Test a function with a timeout using threading."""
    result = None
    exception = None

    def worker():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout=timeout)

    if thread.is_alive():
        # Thread is still running, timeout occurred
        return None, TimeoutError("Function call timed out")
    else:
        # Thread completed
        if exception:
            return None, exception
        return result, None


logger.info("=" * 60)
logger.info("Testing sanitize functions with 5 second timeout")
logger.info("=" * 60)

# Test sanitize_name
logger.info("\n1. Testing sanitize_name...")
result, error = test_with_timeout(sanitize_name, "mempalace", "wing", timeout=5)
if error:
    if isinstance(error, TimeoutError):
        logger.error("❌ sanitize_name timed out after 5 seconds")
    else:
        logger.error(f"❌ sanitize_name failed: {error}")
else:
    logger.info(f"✅ sanitize_name('mempalace', 'wing') = {result}")

# Test sanitize_content
logger.info("\n2. Testing sanitize_content...")
result, error = test_with_timeout(sanitize_content, "Test short content", timeout=5)
if error:
    if isinstance(error, TimeoutError):
        logger.error("❌ sanitize_content timed out after 5 seconds")
    else:
        logger.error(f"❌ sanitize_content failed: {error}")
else:
    logger.info(f"✅ sanitize_content('Test short content') = {result}")

# Test sanitize_content with longer content
logger.info("\n3. Testing sanitize_content with longer content...")
long_content = "Test content " * 100
result, error = test_with_timeout(sanitize_content, long_content, timeout=5)
if error:
    if isinstance(error, TimeoutError):
        logger.error("❌ sanitize_content timed out after 5 seconds")
    else:
        logger.error(f"❌ sanitize_content failed: {error}")
else:
    logger.info(f"✅ sanitize_content(long_content) = success (length: {len(result)})")

# Test sanitize_content with unicode
logger.info("\n4. Testing sanitize_content with unicode...")
unicode_content = "Test with unicode: 你好世界 🌍"
result, error = test_with_timeout(sanitize_content, unicode_content, timeout=5)
if error:
    if isinstance(error, TimeoutError):
        logger.error("❌ sanitize_content timed out after 5 seconds")
    else:
        logger.error(f"❌ sanitize_content failed: {error}")
else:
    logger.info(f"✅ sanitize_content(unicode_content) = {result}")

logger.info("\n" + "=" * 60)
logger.info("Testing completed")
logger.info("=" * 60)
