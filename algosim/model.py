from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self):
        self._process = None

    def is_alive(self):
        return self._process.is_alive if self._process else False

    @abstractmethod
    def step(self, env, data):
        pass

    def process(self, env, *args):
        if self.is_alive():
            return self._process
        self._process = env.process(self.step(env, *args))
        return self._process
