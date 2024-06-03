from threading import Thread, Event
from time import sleep
import time

event = Event()
print(time.time())


def modify_variable(var):
    while True:
        event.wait()
        for i in range(len(var)):
            var[i] += 1
        event.clear()
    print("Stop printing")


my_var = [1, 2, 3]
t1 = Thread(target=modify_variable, args=(my_var,))
t1.start()
t2 = Thread(target=modify_variable, args=(my_var,))
t2.start()
while True:
    try:
        print(my_var)
        sleep(1)
    except KeyboardInterrupt:
        event.set()
        continue
t1.join()
t2.join()
print(my_var)
