from os import path
import datetime

from ML.DBfunctions import get_active_users, get_last_user_training
from ML.get_user_training_data import get_training_data
from common import parent_directory, TRAINING_MODES, setup_logger

lg = setup_logger('training_queue_manager', 'training_queue_manager.log')


def is_sorted(x, key=lambda x: x):
    return all([key(x[i]) <= key(x[i + 1]) for i in range(len(x) - 1)])


def get_queue():
    with open(f'{parent_directory}/scripts/training_queue') as f:
        return [[int(y) for y in x.split(' ')] for x in f.read().splitlines()]


def save_queue(queue):
    try:
        with open(f'{parent_directory}/scripts/training_queue', 'w') as f:
            for item in queue:
                f.write(f'{" ".join([str(x) for x in item])}\n')
    except Exception as e:
        print('eroare', e)
        lg.error(e)


def add_to_queue(user_id, priority):
    lines = get_queue()
    users = [x[0] for x in lines]
    priority_list = [x[1] for x in lines]
    position = 0 if len(lines) == 0 else len(priority_list) if max(priority_list) <= priority else next(
        x for x, val in enumerate(priority_list) if val > priority)

    if user_id not in users:
        lines.insert(position, [user_id, priority])
        save_queue(lines)
        lg.info(f'user {user_id} added to the training queue with priority {priority}')
        return calculate_first_available_predict_day(user_id)
    else:
        lg.info(f'user {user_id} already in the list')
        return -1


def remove_from_queue(user_id):
    lines = get_queue()
    if user_id in [x[0] for x in lines]:
        lines.remove([x for x in lines if x[0] == user_id][0])
        save_queue(lines)
        lg.info(f'User {user_id} removed from training queue')
        return 0
    else:
        lg.warn(f'user {user_id} not in training queue. CAN NOT REMOVE')
        return -1


def calculate_first_available_predict_day(user):
    lines = get_queue()
    users = [x[0] for x in lines]
    priority_list = [x[1] for x in lines]
    index = users.index(user)
    minutes = 0
    for x in priority_list[:index]:
        minutes += TRAINING_MODES[x]['duration']

    return 'today'


def add_user(user_id):
    """
    1. has enough training data:
        yes - go to step 2
        no  - return, notify about inability to train
    2. has a training file:
        yes - go to step 3
        no  - add to training queue with priority 1
    3. last training more than a week ago:
        yes - add to queue with priority 2
        no  - go to step 4
    4. check under which conditions training has finished
        interrupt   - how long the training lasted ?
        test        - add to queue with priority 1
        timeout 30  - add to queue with priority 3
        timeout 60  - add to queue with priority 4
        timeout 120 - leave alone (maybe notify)
    """

    has_enough_training_data = len(get_training_data(user_id)) > 300
    if not has_enough_training_data:
        lg.warn(f'user {user_id} has not enough training data')
        add_to_queue(user_id, 0)
        return 'Nu aveti suficiente comenzi pentru a pregati un model cu o acuratete acceptabila'

    file_name = f'{parent_directory}/models/user{user_id}.pkl'
    has_trained_model = path.isfile(file_name)
    if not has_trained_model:
        return add_to_queue(user_id, 1)

    start_time, finish_reason = get_last_user_training(user_id)
    today = datetime.datetime.today()
    td = (today - start_time).days
    if td > 7:
        return add_to_queue(user_id, 2)

    if finish_reason == TRAINING_MODES['interrupt_reason'] or finish_reason == TRAINING_MODES[0]['reason']:
        return add_to_queue(user_id, 1)
    elif finish_reason == TRAINING_MODES[1]['reason'] or finish_reason == TRAINING_MODES[2]['reason']:
        return add_to_queue(user_id, 3)
    elif finish_reason == TRAINING_MODES[3]['reason']:
        return add_to_queue(user_id, 4)
    elif finish_reason == TRAINING_MODES[4]['reason'] or finish_reason == TRAINING_MODES['accuracy_reason']:
        lg.info(f'User {user_id} is already good')
        return f'User {user_id} is already good'


def check_users():
    users_list = get_active_users()

    for user in users_list:
        add_user(user)


# if __name__ == '__main__':
#     # check_users()
#     add_user(285)
