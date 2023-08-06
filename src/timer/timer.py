import logging
import time
import keyboard


class Timer:
    def __init__(self, logger=logging):
        self.logger = logger
        self.hotkey_pressed = False
        self.show_elapsed_time = False

    def __start_timer(self, seconds):
        self.elapsed_time = 0
        while self.elapsed_time < seconds:
            time.sleep(1)
            self.elapsed_time += 1

            if self.show_elapsed_time:
                self.logger.info(f'Elapsed time: {self.elapsed_time}')
            if self.hotkey_pressed:
                break

    def __toggle_elapsed_time(self):
        self.show_elapsed_time = not self.show_elapsed_time

    def __terminate_timer(self):
        self.hotkey_pressed = True

    def start_timer(self, seconds):
        terminate_hotkey = 'alt+t'
        elapsed_time_hotkey = 'ctrl'

        self.logger.info(f'The timer is now running. The operations are paused for {seconds} seconds...')
        self.logger.info(f'Press {elapsed_time_hotkey} to get time info or {terminate_hotkey} to terminate the job')

        keyboard.add_hotkey(terminate_hotkey, self.__terminate_timer)
        keyboard.add_hotkey(elapsed_time_hotkey, self.__toggle_elapsed_time)

        self.__start_timer(seconds)

        self.logger.info(f'Job is finished, resuming the operations...')
