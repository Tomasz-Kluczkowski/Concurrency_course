import random
import threading
import time
from datetime import datetime

# Should we add random delays everywhere to allow system scheduler to switch threads and expose race conditions?
FUZZ = True

# Global variable that the threads will try to update concurrently
counter = 0


total_number_of_threads = 5
maximum_number_of_concurrent_threads = 2
batch_size = 2
total_number_of_items = total_number_of_threads * batch_size

# We will restrict number of threads that can work on the problem using this counting semaphore.
# We can easily prove that the semaphore itself does not protect against race condition at all!
semaphore = threading.Semaphore(maximum_number_of_concurrent_threads)

# Only if using a mutex to guard the counter variable we can make sure that it is updated to the correct final state!
counter_lock = threading.Lock()

# We can disable guarding of the counter variable and observe how the multiple threads fight for it and how the final
# count will not be as expected.
use_counter_lock = True


def fuzz():
    """
    Add some random time to expose race conditions in multi threading.
    """
    if FUZZ:
        time.sleep(random.random())


def increase_count_in_batch(batch_size: int):
    global counter

    print(f'{threading.current_thread().getName()} trying to acquire semaphore\n')
    semaphore.acquire()
    print(f'{threading.current_thread().getName()} acquired semaphore\n')

    if use_counter_lock:
        print(f'{threading.current_thread().getName()} trying to acquire counter lock\n')
        counter_lock.acquire()
        print(f'{threading.current_thread().getName()} acquired counter lock\n')

    for _ in range(batch_size):
        fuzz()
        old_counter = counter
        fuzz()
        counter = old_counter + 1
        fuzz()
        print(f'The counter is: {counter}, increased by 1 by: {threading.current_thread().getName()}\n')

    if use_counter_lock:
        counter_lock.release()
        print(f'{threading.current_thread().getName()} released counter lock\n')
    semaphore.release()
    print(f'{threading.current_thread().getName()} released semaphore\n')


start_time = datetime.now()
print('Starting\n')
fuzz()
workers = []
for i in range(total_number_of_threads):
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
difference = total_number_of_items - counter
print(f'Time taken for operation: {(finish_time - start_time).total_seconds()}')
if difference:
    print(f'Difference in counting: {difference}')
else:
    print('No difference in counting')
fuzz()
