import os


def child_process():
    print(f'We are in the child process with PID: {os.getpid()}')


def parent():
    print(f'We are in the parent process with PID: {os.getpid()}')
    new_ref = os.fork()
    if new_ref == 0:
        child_process()
    else:
        print(f'We are in the parent process and our child process has PID: {new_ref}')


parent()
