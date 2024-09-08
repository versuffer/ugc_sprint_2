"""logger settings"""

import logging
from logging.config import dictConfig

from app.fastapi_app.settings.config import settings

logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s[%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'json': {
            '()': 'app.fastapi_app.settings.logging_utils.JSONFormatter',
            'fmt_keys': {
                'level': 'levelname',
                'timestamp': 'timestamp',
                'message': 'message',
                'module': 'module',
                'function': 'funcName',
                'line': 'lineno',
            },
        },
    },
    'handlers': {
        'console': {
            'level': settings.LOG_LEVEL,
            'formatter': 'json' if settings.JSON_LOGS is True else 'default',
            'class': 'app.fastapi_app.settings.logging_utils.RequestIdStreamHandler',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        'root': {
            'level': settings.LOG_LEVEL,
            'handlers': ['console'],
        },
    },
}

# Initiate logger config
dictConfig(logger_config)
logger = logging.getLogger('root')
