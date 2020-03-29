import time
import random


NUMBER_OF_FACTORIZATIONS = 100000


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


def main():
    print('Starting factorization')
    start = time.time()

    for i in range(NUMBER_OF_FACTORIZATIONS):
        number_to_factor = random.randint(20000, 100000000)
        print(calculate_prime_factors(number_to_factor))

    stop = time.time()
    total_time = stop - start

    print(f'Execution time: {total_time}')


if __name__ == '__main__':
    main()
