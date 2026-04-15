#!/usr/bin/env python3
"""Unit tests for config.py functions."""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from mempalace.config import sanitize_content


def test_sanitize_content_normal():
    """Test normal content sanitization."""
    content = "This is normal content"
    result = sanitize_content(content)
    assert result == content
    logger.info("✅ test_sanitize_content_normal passed")


def test_sanitize_content_empty():
    """Test empty content raises ValueError."""
    try:
        sanitize_content("")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "non-empty string" in str(e)
        logger.info("✅ test_sanitize_content_empty passed")


def test_sanitize_content_whitespace():
    """Test whitespace-only content raises ValueError."""
    try:
        sanitize_content("   ")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "non-empty string" in str(e)
        logger.info("✅ test_sanitize_content_whitespace passed")


def test_sanitize_content_too_long():
    """Test content exceeding max length raises ValueError."""
    content = "x" * 100001
    try:
        sanitize_content(content)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "maximum length" in str(e)
        logger.info("✅ test_sanitize_content_too_long passed")


def test_sanitize_content_null_bytes():
    """Test content with null bytes raises ValueError."""
    content = "test\x00content"
    try:
        sanitize_content(content)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "null bytes" in str(e)
        logger.info("✅ test_sanitize_content_null_bytes passed")


def test_sanitize_content_unicode():
    """Test Unicode content works correctly."""
    content = "Test with unicode: 你好世界 🌍"
    result = sanitize_content(content)
    assert result == content
    logger.info("✅ test_sanitize_content_unicode passed")


def test_sanitize_content_long_unicode():
    """Test long Unicode content works correctly."""
    content = "Test with unicode: 你好世界 🌍" * 1000
    result = sanitize_content(content)
    assert result == content
    logger.info("✅ test_sanitize_content_long_unicode passed")


if __name__ == "__main__":
    logger.info("Running unit tests for config.py...")
    logger.info("=" * 60)

    test_sanitize_content_normal()
    test_sanitize_content_empty()
    test_sanitize_content_whitespace()
    test_sanitize_content_too_long()
    test_sanitize_content_null_bytes()
    test_sanitize_content_unicode()
    test_sanitize_content_long_unicode()

    logger.info("=" * 60)
    logger.info("All tests passed! ✅")
