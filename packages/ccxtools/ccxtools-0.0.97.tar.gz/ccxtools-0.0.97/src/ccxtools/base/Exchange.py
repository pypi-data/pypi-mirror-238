from abc import ABCMeta, abstractmethod


class Exchange(metaclass=ABCMeta):

    def __init__(self, env_vars):
        self.env_vars = env_vars

    @abstractmethod
    def get_balance(self, ticker):
        raise NotImplementedError
