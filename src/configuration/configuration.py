import os


class Configuration:

    def __init__(self):
        self.config = {}
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def get(self):
        CONFIG_PATH = os.path.join(self.ROOT_DIR, 'Proteus.conf')
        print(f'AAAAAAAAAAAAAAAAAAAAAAAAAAAAA _______________!!!!!!!!!!!!!!!!!! {CONFIG_PATH}')
        exec(open(CONFIG_PATH).read(), self.config)
