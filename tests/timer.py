from threading import Thread
from collections.abc import Callable, Iterable, Mapping
from typing import Any
import time
from asyncio.exceptions import CancelledError
import sys

class Timer(Thread):
    def __init__(self, time_, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._time = time_
        self._done = False
        self.exc = None


    def _timer(self):
        was_set_to = self._time
        while not self._done:
            time.sleep(1)
            self._time -= 1
            # print(f'timer: {self._time}')
            if (self._time == 0) and (not self._done):
                raise TimeoutError(f'timer was set to {was_set_to}s.')


    def run(self) -> None:
        try:
            self._timer()
        except Exception as ex:
            self.exc = ex

    
    def join(self):
        Thread.join(self)
        if self.exc:
            raise self.exc
        

    def done(self):
        self._done = True

