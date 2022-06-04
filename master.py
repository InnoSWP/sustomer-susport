from time import sleep, time
from typing import Callable


class Bot:
    isAlive: bool = True
    _notifications: int = 0

    def __init__(self, name) -> None:
        self.name = name

    # our super callback function
    def send_site_dead_message(self):
        print("kill", self.name)
        print(self.name, self._notifications)
        print(id(self))
        self.isAlive = False

    def send_support_message(self, msg: str) -> None:
        self._notifications += 1
        print("bot received message:", msg, self.name)

    # infinite loop, imagine that there is real bot execution logic
    def polling(self):
        i = 0
        while self._notifications < 20:
            if not self.isAlive:
                print("site killed", self.name)
                break
            i += 1
            self._notifications += 2
            print(self._notifications, i)
            sleep(1)
        print(f'{self.name} is dead')
        print(id(self))

    def run(self):
        self.polling()


class FlaskApp:
    _callbacks: list[Callable] = list()
    _dead_callbacks: list[Callable] = list()
    # here add all callbacks for sevices

    def add_callback(
        self, callback: Callable): self._callbacks.append(callback)

    def add_dead_callback(
        self, callback: Callable): self._dead_callbacks.append(callback)

    # imagine that here is something good
    def trigger_callbacks(self, msg: str):
        for callback in self._callbacks:
            callback(f'site triggered {msg} bot at {time()}')

    def run(self):
        from random import randint
        for _ in range(2):
            self.trigger_callbacks(str(randint(1, 10000)))
            sleep(0.5)
        print("site is killing bots")
        for dead in self._dead_callbacks:
            dead()
        print("site is dead")


def thread_run():
    import threading

    bot = Bot("biba")
    bot2 = Bot("boba")
    site = FlaskApp()
    site.add_callback(bot.send_support_message)
    site.add_callback(bot2.send_support_message)

    site.add_dead_callback(bot.send_site_dead_message)
    site.add_dead_callback(bot2.send_site_dead_message)

    bot_thread = threading.Thread(target=bot.polling)
    bot2_thread = threading.Thread(target=bot2.polling)
    flask_thread = threading.Thread(target=site.run)

    print("ready to launch")
    bot_thread.start()
    bot2_thread.start()
    flask_thread.start()


    print("started")
    bot_thread.join()
    bot2_thread.join()
    print("bot joined")
    flask_thread.join()
    print("flask joined")


def process_run():
    from multiprocessing import Process
    bot = Bot("biba")
    bot2 = Bot("boba")
    site = FlaskApp()
    site.add_callback(bot.send_support_message)
    site.add_callback(bot2.send_support_message)

    site.add_dead_callback(bot.send_site_dead_message)
    site.add_dead_callback(bot2.send_site_dead_message)

    bot1_process = Process(target=bot.polling)
    bot2_process = Process(target=bot2.polling)
    flask_process = Process(target=site.run)

    print("ready to launch")
    bot1_process.start()
    bot2_process.start()
    flask_process.start()

    print("started")

    bot1_process.join()
    print("bot1 joined")
    bot2_process.join()
    print("bot2 joined")
    flask_process.join()
    print("flask joined")


if __name__ == "__main__":
    thread_run()
    # process_run()
