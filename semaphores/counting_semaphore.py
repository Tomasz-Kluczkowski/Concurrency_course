# Semaphore is a synchronisation primitive with a counter.
# The counter represents the number of acquisitions.
# We are allowing acquisitions until the counter drops below zero.

# So if we start with counter = 2, we allow 2 threads to acquire the semaphore and then we stop it from happening.
# This allows setting how many threads at once can hold access some data at the same time.

# When threads release the semaphore, the counter is increased by 1 for each thread releasing it.
# When the counter goes above zero again, threads may acquire the semaphore again, dropping it by 1 for each aquisition
# again until it goes below zero and stops.


# CODE EXAMPLE
# TICKETING SYSTEM -
# NOTE THAT THIS IS INCORRECT!!! THE GLOBAL tickets_available IS NOT PROTECTED BY THE SEMAPHORE!
# we allow 4 threads to try and sell the tickets.
# Since in reality users can take random time when buying, each 'buy' operation will have random delay added to it.
# This will allow for our threads to attempt to acquire the semaphore and sell the tickets.
# Each thread will try to sell as many tickets as possible
# Until they are sold out.
import copy
import threading
import time
import random


class TicketSeller(threading.Thread):
    def __init__(self, semaphore, name: str = None):
        super().__init__(name=name)
        self.semaphore = semaphore
        self.tickets_sold = 0
        print(f'Ticket Seller {name} started work\n')

    def run(self):
        global tickets_available
        running = True

        while running:
            self.random_delay()
            self.semaphore.acquire()

            if tickets_available <= 0:
                running = False
            else:
                self.tickets_sold += 1
                tickets_available -= 1
                print(f'{self.getName()} sold one ticket, ({tickets_available} left)\n')
            self.semaphore.release()
        print(f'{self.getName()} sold {self.tickets_sold} tickets in total\n')

    @staticmethod
    def random_delay():
        time.sleep(random.randint(0, 4) / 4)


semaphore = threading.Semaphore()

tickets_available = 2000
# tickets_available_total = copy.deepcopy(tickets_available)

number_of_sellers = 2000

sellers = []
for i in range(number_of_sellers):
    seller = TicketSeller(semaphore=semaphore, name=f'seller {i+1}')
    seller.start()
    sellers.append(seller)


for seller in sellers:
    seller.join()

tickets_sold = sum([seller.tickets_sold for seller in sellers])

print(f'total number of tickets sold is: {tickets_sold}')
# assert tickets_sold == tickets_available_total
