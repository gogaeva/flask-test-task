import array
import threading
from time import sleep

class MemoryConsumer:
    def __init__(self):
        self.buffer = array.array('b')
        self.lock = threading.Lock()

    def alloc(self, megabytes):
        with self.lock:
            self.buffer.extend([0] * megabytes * 1024 * 1024)

    def free(self):
        with self.lock:
            del self.buffer[:]

    def run(self):
        while True:
            self.alloc(50)
            sleep(1)