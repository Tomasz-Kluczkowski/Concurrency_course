import threading
import time


def standard_thread_execution():
    print('starting standard thread')
    time.sleep(20)
    print('ending standard thread')


def daemon_thread_execution():
    while True:
        print('sending out a heartbeat signal')
        time.sleep(2)


if __name__ == '__main__':
    standard_thread = threading.Thread(target=standard_thread_execution)
    # The daemon thread will run until the rest of our program stops executing. Then it also stops.
    # This is useful when we need a service to run in the background.
    daemon_thread = threading.Thread(target=daemon_thread_execution)
    daemon_thread.setDaemon(True)
    daemon_thread.start()
    standard_thread.start()
