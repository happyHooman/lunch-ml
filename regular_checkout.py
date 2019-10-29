from subprocess import call

import psutil

from scripts.training_queue_manager import check_users
from common import setup_logger, parent_directory
from local_settings import PYTHON_ENV

lg = setup_logger('regular_checkout', 'regular_checkout.log')


def get_training_status():
    cmd = f'{parent_directory}/queue_trainer.py'

    for p in psutil.process_iter():
        try:
            if 'python' in p.name().lower() and len(p.cmdline()) == 2:
                if p.cmdline()[1] == cmd:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def start_trainer():
    training_is_running = get_training_status()
    if not training_is_running:
        lg.info('Training not running. Starting Trainer.')
        cmd = [PYTHON_ENV, f'{parent_directory}/queue_trainer.py']
        call(cmd)
        return


if __name__ == '__main__':
    """ Script to be run every hour """
    lg.info('Running regular checkout..')
    check_users()
    start_trainer()
