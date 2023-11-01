# -*- coding: utf-8 -*-

from typing import Dict, Any

from pydantic import validate_arguments
from fastapi import Request
from fastapi.concurrency import run_in_threadpool

from beans_logging import logger, Logger


@validate_arguments(config=dict(arbitrary_types_allowed=True))
async def async_log_http_error(
    request: Request,
    status_code: int,
    msg_format: str = '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" <n>{status_code}</n>',
):
    """Log HTTP error for unhandled Exception.

    Args:
        request     (Request, required): Request instance.
        status_code (int    , required): HTTP status code.
        msg_format  (str    , optional): Message format. Defaults to '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" <n>{status_code}</n>'.
    """

    _http_info: Dict[str, Any] = {"request_id": request.state.request_id}
    if hasattr(request.state, "http_info") and isinstance(
        request.state.http_info, dict
    ):
        _http_info: Dict[str, Any] = request.state.http_info
    _http_info["status_code"] = status_code

    _msg = msg_format.format(**_http_info)
    _logger: Logger = logger.opt(colors=True, record=True).bind(http_info=_http_info)
    await run_in_threadpool(_logger.error, _msg)


@validate_arguments
async def async_log_trace(message: str):
    """Log trace message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.trace, message)


@validate_arguments
async def async_log_debug(message: str):
    """Log debug message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.debug, message)


@validate_arguments
async def async_log_info(message: str):
    """Log info message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.info, message)


@validate_arguments
async def async_log_success(message: str):
    """Log success message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.success, message)


@validate_arguments
async def async_log_warning(message: str):
    """Log warning message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.warning, message)


@validate_arguments
async def async_log_error(message: str):
    """Log error message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.error, message)


@validate_arguments
async def async_log_critical(message: str):
    """Log critical message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.critical, message)


@validate_arguments
async def async_log_level(level: str, message: str):
    """Log level message.

    Args:
        level   (str, required): Log level.
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.log, level, message)


__all__ = [
    "async_log_http_error",
    "async_log_trace",
    "async_log_debug",
    "async_log_info",
    "async_log_success",
    "async_log_warning",
    "async_log_error",
    "async_log_critical",
    "async_log_level",
]
