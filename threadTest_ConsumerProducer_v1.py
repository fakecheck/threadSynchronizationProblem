import threading
import random
from time import sleep
import datetime


class Consumer(threading.Thread):
    def __init__(self, lock, event, buffer, targetNum):
        super().__init__()
        self.lock = lock
        self.event = event
        self.buffer = buffer
        self.targetNum = targetNum

    def consumeItem(self):
        self.lock.acquire()
        self.targetNum -= 1
        item = self.buffer.pop()
        print("{} Consumer: taking out item: {}".format(datetime.datetime.now(), item))
        self.lock.release()

    def run(self):
        while self.targetNum:

            # comment out this line below, consumer will consume instantly
            sleep(random.randint(1, 3))

            if len(self.buffer) > 0:
                self.consumeItem()
            else:
                print("{} Consumer: NO item in buffer, waiting".format(datetime.datetime.now()))
                self.event.wait()
                self.event.clear()


class Producer(threading.Thread):
    def __init__(self, lock, event, buffer, targetNum):
        super().__init__()
        self.lock = lock
        self.event = event
        self.buffer = buffer
        self.targetNum = targetNum

    def produceItem(self):
        self.lock.acquire()
        self.targetNum -= 1
        item = random.randint(0, 10)
        self.buffer.append(item)
        print("{} Producer: pushing in item: {}".format(datetime.datetime.now(), item))
        self.lock.release()

    def run(self):
        while self.targetNum:
            sleep(random.randint(1, 3))
            self.produceItem()
            if len(self.buffer) == 1:
                self.event.set()


if __name__ == "__main__":
    lock = threading.Lock()
    event = threading.Event()
    buffer = []

    consumer = Consumer(lock, event, buffer, 5)
    producer = Producer(lock, event, buffer, 5)
    consumer.start()
    producer.start()

    consumer.join()
    producer.join()
