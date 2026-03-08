import logging
from pathlib import Path


def get_logger(name: str, log_file: str = 'app.log') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    log_path = (
        Path('/app/logs') / log_file if Path('/app/logs').is_dir() else Path(log_file)
    )
    try:
        file = logging.FileHandler(log_path, encoding='utf-8')
        file.setFormatter(fmt)
        logger.addHandler(file)
    except OSError:
        pass

    return logger


logger = get_logger('App')
