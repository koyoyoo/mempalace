#!/usr/bin/env python3
"""Test script to find the exact length threshold where MCP add_drawer fails."""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('length_threshold_test.log'),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent))
from mempalace.mcp_server import tool_add_drawer

# Test different content lengths to find the threshold
test_lengths = [
    100,      # Very short
    500,      # Short
    1000,     # Medium
    2000,     # Medium-long
    3000,     # Long
    4000,     # Very long
    4500,     # Full document size
    5000,     # Extra long
]

logger.info("=" * 80)
logger.info("Testing content length thresholds")
logger.info("=" * 80)

for length in test_lengths:
    # Generate content of specific length
    content = "x" * length
    logger.info(f"\n--- Testing length: {length} characters ---")
    
    try:
        result = tool_add_drawer(
            wing='test',
            room='threshold',
            content=content,
            source_file=f'test_{length}.txt'
        )
        logger.info(f"✅ SUCCESS: {result.get('success', False)}")
        logger.info(f"   Drawer ID: {result.get('drawer_id', 'N/A')}")
    except Exception as e:
        logger.error(f"❌ EXCEPTION: {type(e).__name__}: {e}")
        logger.exception("Full exception:")

logger.info("=" * 80)
logger.info("Threshold test completed")
logger.info("=" * 80)
