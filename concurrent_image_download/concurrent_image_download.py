import threading
import urllib.request
import time


NUMBER_OF_THREADS = 10


def download_image(image_path, file_name):
    print(f'Downloading image from: {image_path}')
    urllib.request.urlretrieve(image_path, file_name)
    print('Completed Download')


def execute_thread(thread_number):
    image_name = f'temp/image-{thread_number}.jpg'
    download_image('https://picsum.photos/400/200', image_name)


def main():
    start = time.time()
    # create an array to store references to our threads
    threads = []

    # create the threads first and append them to the array to have their references
    for i in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=execute_thread, kwargs={'thread_number': i})
        threads.append(thread)
        # This starts each thread
        thread.start()
        # Although it is tempting to put join() here as it looks like the loop below is redundant we must understand
        # that the join() blocks until thread completes which means that each iteration of the loop would stop and wait
        # for each thread to complete instead of starting them all at once - there would be no benefit to using
        # threading with such an approach.

    for thread in threads:
        # calling join() on the thread blocks until it completes. Doing this in a loop makes sure that we stop execution
        # of the further part of the code until all threads have completed their execution first.
        thread.join()

    stop = time.time()
    total_time = stop - start
    print(f'Total execution time: {total_time}')


if __name__ == '__main__':
    main()
