import time
import random
from multiprocessing import Process

NUMBER_OF_PROCESSES = 10
BATCH_SIZE = 1000


def calculate_prime_factors(n):
    prime_factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            prime_factors.append(d)
            n //= d
        d += 1

    if n > 1:
        prime_factors.append(n)

    return prime_factors


# Split the total number of factorizations (batching) so that each batch can be processed in parallel.
def batch_factorization(batch_size):
    for i in range(batch_size):
        number_to_factor = random.randint(20000, 100000000)
        print(calculate_prime_factors(number_to_factor))


def main():
    print('Starting factorization')
    start = time.time()

    processes = []

    for i in range(NUMBER_OF_PROCESSES):
        process = Process(target=batch_factorization, kwargs={'batch_size': BATCH_SIZE})
        processes.append(process)
        process.start()

    # Similarly to threading, we have to block here until all processes terminated by calling join() on each of them.
    for process in processes:
        process.join()

    stop = time.time()
    total_time = stop - start

    print(f'Execution time: {total_time}')


if __name__ == '__main__':
    main()
