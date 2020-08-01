import threading
import datetime
import random
from time import sleep
import pprint


class Reader(threading.Thread):
    isReading = False
    id = 0
    readerNum = 0  # number of working readers
    readComplete = threading.Event()
    readerWaitingList = []

    def __init__(self, lock):
        super().__init__()
        self.id = Reader.id

        Reader.id += 1
        self.logMutex = lock

    def run(self) -> None:
        waited = False

        if not Reader.isReading and not Writer.isWriting:
            Reader.isReading = True

        # Writer First: No reader comes in until there are no writers(waiting/working)
        if len(Writer.writerWaitingList):
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

        Reader.readerNum += 1
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

        # Writer First: finishes when all working reader finish
        if Reader.readerNum == 0:
            Reader.isReading = False
            Reader.readComplete.set()


class Writer(threading.Thread):
    isWriting = False
    id = 0
    writerNum = 0
    writeComplete = threading.Event()
    _writeLock = threading.Lock()
    writerWaitingList = []

    def __init__(self, lock):
        super().__init__()
        self.id = Writer.id
        self.logMutex = lock

        Writer.id += 1

    def run(self) -> None:
        waited = False
        isFirst = False

        if not Reader.isReading and not Writer.isWriting:
            Writer.isWriting = True
            isFirst = True

        # Writer First: wait until all working reader finishes or there is already a writer
        if not isFirst:
            self.logMutex.acquire()
            print("{} Writer {}: there are writer writing/reader reading, waiting".format(datetime.datetime.now(),
                                                                                          self.id))
            pprint.pprint(Reader.readerWaitingList)
            pprint.pprint(Writer.writerWaitingList)
            self.logMutex.release()

            Writer.writerWaitingList.append(self.id)
            Writer._writeLock.acquire()

            # wait for working readers to complete
            if len(Writer.writerWaitingList) == 1 and Reader.isReading:
                Reader.readComplete.wait()
                Reader.readComplete.clear()
                Writer.isWriting = True


            waited = True

        if waited:
            Writer.writerWaitingList.remove(self.id)

        Writer.writerNum += 1
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

        if len(Writer.writerWaitingList) == 0:
            Writer.isWriting = False
            Writer.writeComplete.set()
        Writer._writeLock.release()


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
