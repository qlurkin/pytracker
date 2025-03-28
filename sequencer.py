from time import perf_counter as time


class Sequencer:
    def __init__(self):
        self.__tempo = 128
        self.__last_tick_time = time()
        self.step_count = 0
        self.__groove = [6]
        self.__groove_index = 0
        self.__remaining_ticks_before_next_step = self.__groove[self.__groove_index]

    def get_tempo(self):
        return self.__tempo

    def tick_time(self):
        return 60 / (self.__tempo * 24)

    def step(self):
        self.step_count += 1

    def tick(self):
        self.__remaining_ticks_before_next_step -= 1
        if self.__remaining_ticks_before_next_step == 0:
            self.step()
            self.__groove_index = (self.__groove_index + 1) % len(self.__groove)
            self.__remaining_ticks_before_next_step = self.__groove[self.__groove_index]

    def update(self):
        tick_time = self.tick_time()
        if time() - self.__last_tick_time >= tick_time:
            self.__last_tick_time += tick_time
            self.tick()
