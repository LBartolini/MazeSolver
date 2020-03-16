import time as t

def MainLoop(func):
    def wrapper():
        while True:
            t.sleep(0.01)
            func()

    return wrapper