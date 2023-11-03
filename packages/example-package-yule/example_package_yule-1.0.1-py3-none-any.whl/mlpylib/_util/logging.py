import logging

# Common logger.
_logger = None

_FORMAT = "%(asctime)s | %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s"


def get_logger():
    """ Get logger 
    Returns:
        Logger instance.
    """
    global _logger

    if _logger is None:
        # create a logger
        _logger = logging.getLogger()
        _logger.setLevel(logging.INFO)

        # remove old loghandlers
        for hdlr in _logger.handlers:
            _logger.removeHandler(hdlr)

        # disable logger propagate
        _logger.propagate = False

        # create formatters
        formatter = logging.Formatter(_FORMAT)

        # create a console handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(formatter)

        # add console handler
        _logger.addHandler(consoleHandler)

    return _logger