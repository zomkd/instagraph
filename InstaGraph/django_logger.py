"""Initilize Django logger """
import os
import logging

from .settings import BASE_DIR


log = logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom_formatter': {
            'format': '{levelname} {asctime} {module} {process:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs.log'),
            'formatter': 'custom_formatter',
        },
    },
    'loggers': {
        'backend': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propatage': True,
        },
    },
}
