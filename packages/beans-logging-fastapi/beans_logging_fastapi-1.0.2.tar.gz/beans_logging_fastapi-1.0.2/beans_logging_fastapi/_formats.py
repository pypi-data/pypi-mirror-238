# -*- coding: utf-8 -*-

from typing import Dict, Any


def http_file_format(
    record: dict,
    msg_format: str = '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" {status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}',
) -> str:
    """Http access log file format.

    Args:
        record (dict): Log record as dictionary.

    Returns:
        str: Format for http access log record.
    """

    if "http_info" not in record["extra"]:
        return ""

    if "http_message" not in record:
        _http_info: Dict[str, Any] = record["extra"]["http_info"]
        if "datetime" not in _http_info:
            _http_info["datetime"] = record["time"].isoformat(timespec="milliseconds")

        if "content_length" not in _http_info:
            _http_info["content_length"] = 0

        if "h_referer" not in _http_info:
            _http_info["h_referer"] = "-"

        if "h_user_agent" not in _http_info:
            _http_info["h_user_agent"] = "-"

        if "response_time" not in _http_info:
            _http_info["response_time"] = 0

        record["extra"]["http_info"] = _http_info

        _msg = msg_format.format(**_http_info)
        record["http_message"] = _msg

    return "{http_message}\n"


def http_file_json_format(record: dict) -> str:
    """Http access json log file format.

    Args:
        record (dict): Log record as dictionary.

    Returns:
        str: Format for http access json log record.
    """

    if "http_info" not in record["extra"]:
        return ""

    _http_info: Dict[str, Any] = record["extra"]["http_info"]
    if "datetime" not in _http_info:
        _http_info["datetime"] = record["time"].isoformat(timespec="milliseconds")
        record["extra"]["http_info"] = _http_info

    return "{extra[http_info]}\n"


__all__ = ["http_file_format", "http_file_json_format"]
