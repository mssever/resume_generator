'''
Handles logging for this program.
'''

import logging
from logging import debug, info, warning, error, exception, critical
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

def init_logging(level):
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')
    debug(repr((
        ('DEBUG', DEBUG),
        ('INFO', INFO),
        ('WARNING', WARNING),
        ('ERROR', ERROR),
        ('CRITICAL', CRITICAL)
    )))

