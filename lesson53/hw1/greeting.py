import os


def greet():
    to_greet = os.environ.get('TO_GREET', 'World')
    print(f'Hello, {to_greet}!')


if __name__ == '__main__':
    greet()
