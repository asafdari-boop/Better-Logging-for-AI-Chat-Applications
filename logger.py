from collections.abc import MutableMapping
from typing import Any, Dict, Optional
import structlog
import logging.config
from starlette_context import context
from starlette_context.middleware import RawContextMiddleware
from starlette_context.plugins import Plugin
from starlette.middleware import Middleware
import json
import copy


class ChatIdPlugin(Plugin):
    """
    Plugin to extract request arguments and add them to the context.
    """
    key = "chat_id"

    async def process_request(self, request):
        # Extract chat_id from path
        path = request.scope["path"]
        chat_id = None
        if path:
            # Get everything after the last /
            chat_id = path.split("/")[-1]
        return chat_id


class CustomFormatter(logging.Formatter):
    """
    Custom formatter to format logs as level:[chat_id]:location:message
    """
    def format(self, record):
        # Make a copy of the record to avoid modifying the original
        record = copy.copy(record)

        # Try to get chat_id from starlette context first, then fallback to record
        chat_id = None
        if context.exists():
            chat_id = context.get("chat_id")
        if not chat_id:
            chat_id = getattr(record, 'chat_id', None)

        # Format the message
        original_msg = record.msg
        if chat_id:
            record.msg = f"{record.levelname}:{chat_id}:{record.name}:{original_msg}"
        else:
            record.msg = f"{record.levelname}:{record.name}:{original_msg}"

        # Store original levelname and temporarily clear it
        original_levelname = record.levelname
        record.levelname = ""

        # Format the record
        formatted = super().format(record)

        # Restore original values
        record.levelname = original_levelname
        record.msg = original_msg

        return formatted


def get_context_middleware():
    """
    Get the starlette-context middleware with our plugins.
    """
    return Middleware(RawContextMiddleware, plugins=[
        ChatIdPlugin(),
    ])


def setup_logging():
    """
    Configure logging to use CustomFormatter globally.
    """
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "custom": {
                "()": CustomFormatter,
                "format": "%(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "custom",
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(logging_config)

