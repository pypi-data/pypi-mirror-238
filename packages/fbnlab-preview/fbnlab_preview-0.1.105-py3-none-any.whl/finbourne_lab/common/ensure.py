from abc import ABC, abstractmethod
from termcolor import colored


class BaseData(ABC):

    def __init__(self, quiet):
        self.label = type(self).__name__
        self.quiet = quiet

    def log(self, txt):
        if not self.quiet:
            print(colored(f'[{self.label}]: ', 'blue') + txt)

    @abstractmethod
    def check_data(self, **kwargs):
        pass

    @abstractmethod
    def ensure(self, **kwargs):
        pass
