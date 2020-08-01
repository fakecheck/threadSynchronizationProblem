import threading


class CrossPrinter(threading.Thread):
    def __init__(self, event1, event2, buffer, id):
        super().__init__()
        self.id = id
        self.Finished1 = event1
        self.Finished2 = event2
        self.buffer = buffer
        self.idx = 0

    def printArr1(self):
        while True:
            print(self.buffer[self.idx], end="")
            self.idx += 1
            self.idx %= len(self.buffer)
            self.Finished1.set()
            self.Finished2.wait()
            self.Finished2.clear()

    def printArr2(self):
        while True:
            self.Finished1.wait()
            self.Finished1.clear()

            print(self.buffer[self.idx], end="")
            self.idx += 1
            self.idx %= len(self.buffer)
            self.Finished2.set()

    def run(self):
        if self.id == 1:
            self.printArr1()
        elif self.id == 2:
            self.printArr2()


a = ['a', 'b', 'c']
b = [1, 2, 3, 4, 5]

event1 = threading.Event()
event2 = threading.Event()

crossPrinter1 = CrossPrinter(event1, event2, a, 1)
crossPrinter2 = CrossPrinter(event1, event2, b, 2)

crossPrinter1.start()
crossPrinter2.start()
crossPrinter1.join()
crossPrinter2.join()



