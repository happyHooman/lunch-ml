from scripts.training_queue_manager import add_user, remove_from_queue
from common import setup_logger

lg = setup_logger('modify_option', 'modify_option.log')


def modify_option(user, auto_order_option):
    if auto_order_option:
        lg.info(f'User {user} turned auto_order ON')
        print(f'User {user} turned auto_order ON')
        result = add_user(user)
        lg.info(result)
        return result
    else:
        lg.info(f'User {user} turned auto_order OFF')
        print(f'User {user} turned auto_order OFF')
        remove_from_queue(user)
        return 'removed from queue'


if __name__ == '__main__':
    import sys

    user_id = int(sys.argv[1])
    option = bool(sys.argv[2] == "True")
    print(modify_option(user_id, option))
