import threading
from time import sleep
import random
import datetime


class Philosopher(threading.Thread):

    id = 0
    takeChopstick = threading.Lock()
    logMutex = threading.Lock()

    def __init__(self, lock1, lock2, solutionId):
        super().__init__()
        self.id = Philosopher.id
        Philosopher.id += 1
        self.leftChopstick = lock1
        self.rightChopstick = lock2
        self.solutionId = solutionId

    def takeUpChopsticks(self):
        if self.leftChopstick.acquire():
            if self.rightChopstick.acquire():
                return True
            self.leftChopstick.release()
            return False
        else:
            return False

    def putDownChopsticks(self):
        self.leftChopstick.release()
        self.rightChopstick.release()

    def eat(self):
        self.logMutex.acquire()
        print("{} Philosopher {} is eating".format(datetime.datetime.now(), self.id))
        self.logMutex.release()

        sleep(random.randint(1, 3))

        self.logMutex.acquire()
        print("{} Philosopher {} finished".format(datetime.datetime.now(), self.id))
        self.logMutex.release()

    def think(self):
        self.logMutex.acquire()
        print("{} Philosopher {} is thinking".format(datetime.datetime.now(), self.id))
        self.logMutex.release()

        sleep(random.randint(1, 3))

        self.logMutex.acquire()
        print("{} Philosopher {} is hungry".format(datetime.datetime.now(), self.id))
        self.logMutex.release()

    def solution1(self):
        while True:
            Philosopher.takeChopstick.acquire()
            if self.takeUpChopsticks():
                Philosopher.takeChopstick.release()
                self.eat()
                self.putDownChopsticks()
                self.think()

    def solution2(self):
        """
        asymmetric solution

        :return:
        """
        pass

    def solution3(self):
        pass

    def run(self) -> None:
        if self.solutionId == 1:
            self.solution1()
        elif self.solutionId == 2:
            self.solution2()
        elif self.solutionId == 3:
            self.solution3()


if __name__ == '__main__':
    locks = [threading.Lock() for _ in range(5)]
    philosophers = []

    pre = 0
    cur = 1

    solution = 1

    for i in range(5):
        philosophers.append(Philosopher(locks[pre], locks[cur], solution))
        pre = (pre + 1) % 5
        cur = (cur + 1) % 5

    for philosopher in philosophers:
        philosopher.start()
