class Eratosthenes():

    def __init__(self, num, window, tick=0.1):
        self.num = num
        self.sieve = [True] * self.num
        self.base = 0
        self.window = window
        self.tick = tick
        self.coroutines = []
        self.done = False
        self.nursery = None

    async def start(self):
        async with trio.open_nursery() as self.nursery:
            self.nursery.start_soon(self.update_text)
            while self.base <= self.num / 2:
                await trio.sleep(self.tick)
                self.nursery.start_soon(self.mark_number, self.base + 1)
            while sum(self.coroutines) > 0:
                await trio.sleep(self.tick)
            self.done = True

    async def mark_number(self, base):
        id = len(self.coroutines)
        self.coroutines.append(1)
        for i in range(2 * base, self.num + 1, base):
                self.window.set_num.emit(i, color)
            await trio.sleep(self.tick)
        self.coroutines[id] = 0

    async def update_text(self):
        while not self.done:
            await trio.sleep(self.tick)
            if int(trio.lowlevel.current_clock().current_time() + self.tick) % 2:
                text = "⚙️ ...Calculating prime numbers... ⚙️"
            else:
                text = "👩‍💻 ...Hacking the universe... 👩‍💻"
            self.window.widget_outer_text.setText(text)

        self.window.widget_outer_text.setText(
            "🥳 Congratulations! You found all the prime numbers and solved mathematics. 🥳"
        )
        

