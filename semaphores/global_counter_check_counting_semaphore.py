import random
import threading
import time
from datetime import datetime

FUZZ = True

counter = 0
total_number_of_workers = 4
number_of_concurrent_workers = 2
batch_size = 5
total_number_of_items = total_number_of_workers * batch_size

semaphore = threading.Semaphore(number_of_concurrent_workers)
counter_lock = threading.Lock()

use_counter_lock = False


def fuzz():
    if FUZZ:
        time.sleep(random.random())


def increase_count_in_batch(batch_size: int):
    global counter

    print(f'Thread {threading.current_thread().getName()} trying to acquire semaphore\n')
    semaphore.acquire()
    print(f'Thread {threading.current_thread().getName()} acquired semaphore\n')

    if use_counter_lock:
        print(f'Thread {threading.current_thread().getName()} trying to acquire counter lock\n')
        counter_lock.acquire()
        print(f'Thread {threading.current_thread().getName()} acquired counter lock\n')

    for _ in range(batch_size):
        fuzz()
        old_counter = counter
        fuzz()
        counter = old_counter + 1
        fuzz()
        print(f'The counter is: {counter}, increased by 1 by thread: {threading.current_thread().getName()}\n')

    if use_counter_lock:
        counter_lock.release()
        print(f'Thread {threading.current_thread().getName()} released counter lock\n')
    semaphore.release()
    print(f'Thread {threading.current_thread().getName()} releasing semaphore\n')


start_time = datetime.now()
print('Starting\n')
fuzz()
workers = []
for i in range(total_number_of_workers):
    worker = threading.Thread(target=increase_count_in_batch, kwargs={'batch_size': batch_size})
    fuzz()
    workers.append(worker)
    fuzz()
    worker.start()
    fuzz()


for worker in workers:
    worker.join()

finish_time = datetime.now()
print('Finished')
print(f'Final counter: {counter}')
print(f'Difference: {total_number_of_items - counter}')
print(f'Time taken for operation: {(finish_time - start_time).total_seconds()}')
fuzz()
