from os import path
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
parent_directory = path.abspath(path.dirname(__file__))


def setup_logger(name, log_file, level=logging.INFO):
    """Setup as many loggers as you want"""
    log_file_path = f'{parent_directory}/logs/{log_file}'
    handler = logging.FileHandler(log_file_path)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


TRAINING_MODES = {
    0: {'name': 'TEST Training', 'duration': 5, 'reason': 4},
    1: {'name': 'First Time Training', 'duration': 30, 'reason': 5},
    2: {'name': 'Regular Training', 'duration': 30, 'reason': 5},
    3: {'name': 'Improvement 1', 'duration': 60, 'reason': 6},
    4: {'name': 'Improvement 2', 'duration': 120, 'reason': 7},
    'accuracy_reason': 3,
    'interrupt_reason': 1
}
