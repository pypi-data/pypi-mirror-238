import sys
from types import FunctionType, ModuleType


def main(func: FunctionType):
    class Main(ModuleType):
        def __init__(self):
            super().__init__(__name__)
            self.__dict__.update(sys.modules[__name__].__dict__)

        def __call__(self):
            return func(" ".join(sys.argv[1:]))

    sys.modules[func.__module__] = Main()
