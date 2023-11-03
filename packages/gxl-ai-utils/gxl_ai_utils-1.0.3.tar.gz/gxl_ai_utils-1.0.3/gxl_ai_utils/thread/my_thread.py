import threading


class MyThreadPool:
    def __init__(self, ):
        self._threads = []

    def add_thread(self, func: callable, fun_args: list):
        thread = threading.Thread(target=func, args=fun_args)
        self._threads.append(thread)

    def start(self):
        for thread in self._threads:
            thread.start()
        self._join()

    def _join(self):
        for thread in self._threads:
            thread.join()
