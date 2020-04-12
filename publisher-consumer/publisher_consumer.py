import threading
import random
import time

# This is not really a publisher / consumer that we are used to as whichever thread aquires the condition receives the
# integer but it is a good example on how condition notifies threads.


class Publisher(threading.Thread):
    def __init__(self, integers, condition):
        self.condition = condition
        self.integers = integers
        super().__init__()

    def run(self):
        while True:
            integer = random.randint(0, 1000)
            self.condition.acquire()
            print(f'Condition acquired by publisher: {self.name}')
            self.integers.append(integer)
            print(f'Publisher {self.name} appending to array: {integer}')
            self.condition.notify()
            print(f'Condition released by publisher: {self.name}')
            self.condition.release()
            time.sleep(1)


class Subscriber(threading.Thread):
    def __init__(self, integers, condition):
        self.integers = integers
        self.condition = condition
        super().__init__()

    def run(self):
        while True:
            self.condition.acquire()
            print(f'Condition acquired by consumer: {self.name}')
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print(f'{integer} popped from list by consumer {self.name}')
                    break
                print(f'Condition wait by {self.name}')
                self.condition.wait()
            print(f'Consumer {self.name} releasing condition')
            self.condition.release()


def main():
    integers = []
    condition = threading.Condition()

    #     publisher
    publisher = Publisher(integers, condition)
    publisher.start()

    #     Subscribers
    subsriber_1 = Subscriber(integers, condition)
    subsriber_2 = Subscriber(integers, condition)
    subsriber_1.start()
    subsriber_2.start()

    publisher.join()
    subsriber_1.join()
    subsriber_2.join()


if __name__ == '__main__':
    main()
