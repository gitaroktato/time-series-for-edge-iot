from collections.abc import Callable

class Downsampler:
    def __init__(self, period: int) -> None:
        self.__period = period
        self.__counter = 0

    def print(self, text: str) -> None:
        self.__counter += 1
        if (self.__counter % self.__period == 0):
            print(text)
            self.__counter = 0

    def call(self, callback: Callable[[None], None]) -> None:
        self.__counter += 1
        if (self.__counter % self.__period == 0):
            callback()
            self.__counter = 0