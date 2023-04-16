import asyncio
import time



class Timer:
    def __init__(self, time_) -> None:
        self._time = time_
        self._done = False

    async def _timer(self):
        was_set_to = self._time
        while not self._done:
            await asyncio.sleep(1)
            self._time -= 1
            if (self._time == 0) and (not self._done):
                raise TimeoutError(f'Timeout, timer was set to {was_set_to}s.')
            
    def start(self):
        asyncio.run(self._timer())

    def done(self):
        self._done = True