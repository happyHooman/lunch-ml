import pickle
import sys


def inspect_model(user):
    file_name = f'models/user{user}.pkl'
    try:
        with open(file_name, 'rb') as inp:
            model = pickle.load(inp)
    except FileNotFoundError:
        return f'no training file for user {user}'
    model.inspect()


if __name__ == '__main__':
    user_id = sys.argv[1] or 268
    inspect_model(user_id)
