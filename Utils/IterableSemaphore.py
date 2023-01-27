import logging
from threading import BoundedSemaphore, Semaphore


class ISemaphore(Semaphore):

    def __init__(self, value=1, name="default"):
        super().__init__(value=value)
        self.name = name

    def acquire(self, n: int = 1, blocking: bool = True, timeout: float = None) -> bool:
        r = True
        for i in range(n):
            r = r and super().acquire(blocking=blocking, timeout=timeout)
        return r

    def release(self, n: int = 1) -> None:
        for i in range(n):
            super().release()


class IBoundedSemaphore(BoundedSemaphore):

    def __init__(self, value=1, name="default"):
        super().__init__(value=value)
        self.name = name

    def update_size(self, size:int=2, update_value:bool=False)->None:
        if size<1:
            raise ValueError("semaphore initial value must be >= 1")
        s = self._value
        ##if self._value > size:
         #   self._value = size - 1
        self._initial_value = size
        if update_value:
            self._value = size

    def acquire(self, n: int = 1, blocking: bool = True, timeout: float = None) -> bool:
        r = True
        for i in range(n):
            r = r and super().acquire(blocking=blocking, timeout=timeout)
        return r

    def release(self, n: int = 1) -> None:
        try:
            for i in range(n):
                super().release()
        except ValueError:
            logging.log(logging.WARN, "Value Error: Semaphore {} released too many times ({}/{})".format(self.name, n, self._initial_value))