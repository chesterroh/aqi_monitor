#!/usr/bin/python3

import threading
import time

def print_timeout(name, delay, run_event):
    while run_event.is_set():
        time.sleep(delay)
        print("%s - fucked up" % name)

def main():
    run_event = threading.Event()
    run_event.set()

    d1 = 1
    t1 = threading.Thread(target=print_timeout,args = ("Chester",d1,run_event))

    d2 = 2
    t2 = threading.Thread(target=print_timeout,args = ("SJ",d1,run_event))

    t1.start()
    time.sleep(1)
    t2.start()

    try:
        while 1:
            time.sleep(0.5)
            print("main thread working")
    except KeyboardInterrupt:
        print("Attempting the arranging the remaining thread")
        run_event.clear()
        t1.join()
        t2.join()
        print("thread successfully closed")

if __name__ == "__main__":
    main()
    
