#!/usr/bin/env python3
"""
MCP Server Logger - 按日期命名的日志工具

为 MCP 服务器提供日志功能，支持按日期命名日志文件，便于问题定位。
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# MCP 服务器版本号
MCP_SERVER_VERSION = "1.0.35"


def setup_mcp_logger(
    log_dir: Optional[str] = None,
    log_level: int = logging.INFO,
    log_to_console: bool = True,
) -> logging.Logger:
    """
    设置 MCP 服务器日志系统，按日期命名日志文件（每天一个文件）。

    Args:
        log_dir: 日志目录，默认为项目根目录下的 logs 文件夹
        log_level: 日志级别，默认为 INFO
        log_to_console: 是否同时输出到控制台，默认为 True

    Returns:
        配置好的 logger 实例
    """
    # 确定日志目录
    if log_dir is None:
        # 默认使用项目根目录下的 logs 文件夹
        project_root = Path(__file__).parent.parent
        log_dir = project_root / "logs"
    else:
        log_dir = Path(log_dir)

    # 创建日志目录
    log_dir.mkdir(parents=True, exist_ok=True)

    # 生成日志文件名（基于日期，而不是时间戳，避免每次启动都创建新文件）
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"mcp_server_{date_str}.log"

    # 配置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # 创建 logger
    logger = logging.getLogger("mempalace_mcp")
    logger.setLevel(log_level)

    # 清除已有的 handlers（避免重复添加）
    logger.handlers.clear()

    # 文件 handler（覆盖模式，每次启动清空日志）
    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="w")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(file_handler)

    # 控制台 handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(log_format, date_format))
        logger.addHandler(console_handler)

    logger.info(f"=" * 80)
    logger.info(f"MCP 服务器日志初始化完成。版本: {MCP_SERVER_VERSION}")
    logger.info(f"日志文件: {log_file}")
    logger.info(f"日志级别: {logging.getLevelName(log_level)}")
    logger.info(f"=" * 80)

    return logger


def get_logger(name: str = "mempalace_mcp") -> logging.Logger:
    """
    获取已配置的 logger 实例。

    Args:
        name: logger 名称，默认为 "mempalace_mcp"

    Returns:
        logger 实例
    """
    return logging.getLogger(name)


def get_version() -> str:
    """
    获取 MCP 服务器版本号。

    Returns:
        版本号字符串
    """
    return MCP_SERVER_VERSION
