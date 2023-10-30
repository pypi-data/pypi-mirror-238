import logging

from pathier import Pathier, Pathish

from loggi import models

root = Pathier(__file__).parent


def getLogger(name: str, path: Pathish = Pathier.cwd()) -> logging.Logger:
    """Get a configured `logging.Logger` instance for `name` with a file handler.

    The log file will be located in `path`.

    Default level is `INFO`.

    Logs are in the format: `{levelname}|-|{asctime}|-|{message}

    asctime is formatted as `%x %X`"""
    path = Pathier(path)
    logger = logging.getLogger(name)
    # TODO: Add option for a stream handler
    handler = logging.FileHandler((path / name).with_suffix(".log"), encoding="utf-8")
    handler.setFormatter(
        logging.Formatter(
            "{levelname}|-|{asctime}|-|{message}",
            style="{",
            datefmt="%x %X",
        )
    )
    if handler.baseFilename not in [
        existing_handler.baseFilename
        for existing_handler in logger.handlers
        if isinstance(existing_handler, logging.FileHandler)
    ]:
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def load_log(logpath: Pathish) -> models.Log:
    """Return a `Log` object for the log file at `logpath`."""
    return models.Log.load_log(Pathier(logpath))
