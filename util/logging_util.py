import logging


def log_helper(level):
    logger = logging.getLogger(__name__)
    if not getattr(logger, 'value_set', None):
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(levelname)s %(asctime)s %(filename)s %(module)s %(funcName)s %(lineno)d %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.value_set = True
    return logger
