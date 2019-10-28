import os

from ML.trainer import train
from scripts.training_queue_manager import remove_from_queue
from common import parent_directory


def get_first_from_queue():
    file_name = f'{parent_directory}/scripts/training_queue'
    if os.stat(file_name).st_size != 0:
        with open(file_name, 'r') as f:
            line = [int(x) for x in f.readline().rstrip().split(' ')]
        return line
    else:
        return -1, 0


def train_queue():
    user_id, priority = get_first_from_queue()
    if user_id > 0:
        train(user_id, priority)
        remove_from_queue(user_id)
        train_queue()
    else:
        print('Training queue is empty. I\'m going to sleep now')


if __name__ == '__main__':
    train_queue()
