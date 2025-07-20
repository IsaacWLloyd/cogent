"""
Logging configuration for COGENT backend.
Structured logging with correlation ID support.
"""

import logging
import logging.config
import sys
from typing import Dict, Any

from app.core.config import get_settings


class CorrelationFilter(logging.Filter):
    """Filter to add correlation ID to log records"""
    
    def filter(self, record):
        # Import here to avoid circular imports
        from app.main import request_context
        
        # Add correlation ID if available
        correlation_id = request_context.get("correlation_id", "no-request")
        record.correlation_id = correlation_id
        
        return True


def setup_logging():
    """Configure application logging"""
    settings = get_settings()
    
    # Logging configuration
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": (
                    "%(asctime)s [%(correlation_id)s] %(levelname)s "
                    "%(name)s:%(lineno)d - %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(levelname)s - %(message)s",
            },
        },
        "filters": {
            "correlation": {
                "()": CorrelationFilter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "detailed" if settings.is_development else "simple",
                "filters": ["correlation"],
            },
        },
        "loggers": {
            # Application loggers
            "app": {
                "level": settings.log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            # FastAPI and uvicorn
            "fastapi": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            # SQLAlchemy
            "sqlalchemy.engine": {
                "level": "INFO" if settings.is_development else "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.pool": {
                "level": "INFO" if settings.is_development else "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["console"],
        },
    }
    
    logging.config.dictConfig(config)
    
    # Set the correlation filter on the root logger too
    root_logger = logging.getLogger()
    root_logger.addFilter(CorrelationFilter())