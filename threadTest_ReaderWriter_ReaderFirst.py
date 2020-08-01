import threading
import datetime
import random
from time import sleep
import pprint


class Reader(threading.Thread):
    isReading = False
    id = 0
    readerNum = 0
    readComplete = threading.Event()
    readerWaitingList = []

    def __init__(self, lock):
        super().__init__()
        self.id = Reader.id

        Reader.id += 1
        Reader.readerNum += 1
        self.logMutex = lock

    def run(self) -> None:
        waited = False

        if not Reader.isReading and not Writer.isWriting:
            Reader.isReading = True

        if not Reader.isReading:
            self.logMutex.acquire()
            print("{} Reader {}: there are writer writing, waiting".format(datetime.datetime.now(), self.id))
            pprint.pprint(Reader.readerWaitingList)
            pprint.pprint(Writer.writerWaitingList)
            self.logMutex.release()

            Reader.readerWaitingList.append(self.id)
            Writer.writeComplete.wait()
            Writer.writeComplete.clear()
            Reader.isReading = True
            waited = True

        if waited:
            Reader.readerWaitingList.remove(self.id)

        self.logMutex.acquire()
        print("{} Reader {}: reading stuff".format(datetime.datetime.now(), self.id))
        pprint.pprint(Reader.readerWaitingList)
        pprint.pprint(Writer.writerWaitingList)
        self.logMutex.release()

        sleep(random.randint(1, 3))

        self.logMutex.acquire()
        print("{} Reader {}: reading complete".format(datetime.datetime.now(), self.id))
        pprint.pprint(Reader.readerWaitingList)
        pprint.pprint(Writer.writerWaitingList)
        self.logMutex.release()

        Reader.readerNum -= 1

        if Reader.readerNum == 0:
            Reader.isReading = False
            Reader.readComplete.set()


class Writer(threading.Thread):
    isWriting = False
    id = 0
    writerNum = 0
    writeComplete = threading.Event()
    writerWaitingList = []

    def __init__(self, lock):
        super().__init__()
        self.id = Writer.id
        self.logMutex = lock

        Writer.id += 1
        Writer.writerNum += 1

    def run(self) -> None:
        waited = False

        if not Reader.isReading and not Writer.isWriting:
            Writer.isWriting = True

        if Writer.isWriting or Reader.isReading:
            self.logMutex.acquire()
            print("{} Writer {}: there are writer writing/reader reading, waiting".format(datetime.datetime.now(), self.id))
            pprint.pprint(Reader.readerWaitingList)
            pprint.pprint(Writer.writerWaitingList)
            self.logMutex.release()

            Writer.writerWaitingList.append(self.id)
            if Reader.isReading:
                Reader.readComplete.wait()
                Reader.readComplete.clear()
                Writer.isWriting = True
            elif Writer.isWriting:
                if Reader.readerNum:
                    Reader.readComplete.wait()
                    Reader.readComplete.clear()
                    Writer.isWriting = True

            waited = True

        if waited:
            Writer.writerWaitingList.remove(self.id)

        self.logMutex.acquire()
        print("{} Writer {}: writing stuff".format(datetime.datetime.now(), self.id))
        pprint.pprint(Reader.readerWaitingList)
        pprint.pprint(Writer.writerWaitingList)
        self.logMutex.release()

        sleep(random.randint(1, 3))

        self.logMutex.acquire()
        print("{} Writer {}: writing complete".format(datetime.datetime.now(), self.id))
        pprint.pprint(Reader.readerWaitingList)
        pprint.pprint(Writer.writerWaitingList)
        self.logMutex.release()

        Writer.writerNum -= 1

        if len(Reader.readerWaitingList):
            Writer.isWriting = False
            Writer.writeComplete.set()


if __name__ == '__main__':
    idx = 0
    mutex = threading.Lock()
    for i in range(10):
        reader = Reader(mutex)
        reader.start()
        idx += 1
        if idx % 3 == 0:
            writer = Writer(mutex)
            writer.start()
