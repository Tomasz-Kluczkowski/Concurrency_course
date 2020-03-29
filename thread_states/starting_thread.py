import threading
import time
import random


def execute_thread(thread_number):
    print(f'Thread {thread_number} started\n')
    sleep_time = random.randint(1, 10)
    time.sleep(sleep_time)
    print(f'Thread {thread_number} finished executing\n')


for i in range(10):
    thread = threading.Thread(target=execute_thread, kwargs={'thread_number': i})
    thread.start()

    print(f'Active threads: {threading.enumerate()}')
