import threading
import time


def thread_worker():
    # Only when the thread starts executing it switches from Runnable state to Running.
    print("Thread in 'RUNNING' state")

    # sleep causes thread to go into not-runnable state. We cannot do any more work in here.
    time.sleep(10)
    # the thread completes and terminates
    print('The thread is terminating')


# here we only have the definition of the object, the thread itself has not started, it is not initiated.
thread = threading.Thread(target=thread_worker)

# When .start() is called on the thread, Python allocates resources required to it and calls .run() on the thread and it
# executes. We switch from 'STARTING' to 'RUNNABLE' state. Now we will have to wait for OS scheduler to allow the thread
# to execute on the CPU and then it is in 'RUNNING' state.
thread.start()

# Once the OS scheduled the thread to execute it may also tell it to yield interrupting it and putting it back in 'RUNNABLE' state waiting for
# it's next round of execution (round robin scheduling).

# When we join() on the thread we are waiting for it to finish execution after which it goes into 'DEAD' state. Its
# resources are released and object is garbage collected by python.
thread.join()
print('The thread is in dead state')

