import logging
from pythonjsonlogger import jsonlogger

from .consts import (
    SERVICE_NAME,
    DEFAULT_LOG_FILE,
    AUDIT_LOG_FILE,
    ERROR_LOG_FILE,
    ACCESS_LOG_FILE,
)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # Add custom fields or modify the log record here
        log_record["service"] = SERVICE_NAME


def get_log_config():
    return {
        "version": 1,
        "formatters": {
            "default_formatter": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "json_formatter": {
                "()": CustomJsonFormatter,
                "format": "[ %(asctime)s ] %(levelname)s %(message)s",
            },
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json_formatter",
            },
            "default_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": DEFAULT_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "json_formatter",
            },
            "error_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": ERROR_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "json_formatter",
            },
            "access_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": ACCESS_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "json_formatter",
            },
            "audit_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": AUDIT_LOG_FILE,
                "maxBytes": 1024 * 1024,
                "backupCount": 10,
                "formatter": "json_formatter",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console_handler"]},
        "loggers": {
            "werkzeug": {
                "handlers": ["access_handler"],
                "level": "INFO",
                "propagate": False,
            },
            "default": {
                "handlers": ["default_handler"],
                "level": "INFO",
            },
            "error": {
                "handlers": ["error_handler"],
                "level": "ERROR",
            },
            "access": {
                "handlers": ["access_handler"],
                "level": "INFO",
            },
            "audit": {
                "handlers": ["audit_handler"],
                "level": "INFO",
            },
        },
    }


def default_logger():
    return logging.getLogger("default")


def error_logger():
    return logging.getLogger("error")


def access_logger():
    return logging.getLogger("access")


def audit_logger():
    return logging.getLogger("audit")
