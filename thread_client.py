#!/usr/bin/python3

import threading
import urllib.request
import urllib.parse
import time

aqi_request = {}
aqi_request['aqi01']=81
aqi_request['aqi25']=88
aqi_request['aqi10']=100
aqi_request['voc']=11

def log_aqi(delay,run_event):
    while run_event.is_set():
        time.sleep(delay)
        log_server_http()

def log_server_http():
    host = "http://localhost:8000"
    uri = "/polls/logaqi?aqi01=%s&aqi25=%s&aqi10=%s&voc=%s" % ( aqi_request['aqi01'], aqi_request['aqi25'], aqi_request['aqi10'], aqi_request['voc'] )
    
    f = urllib.request.urlopen(host+uri)
    print(f.read().decode('utf-8'))
    f.close()

def main():
    run_event = threading.Event()
    run_event.set()

    log_thread = threading.Thread(target=log_aqi,args = (5,run_event))

    log_thread.start()


    try:
        while 1:
            aqi_request['aqi01'] += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("keyboard interrupt caught")
        run_event.clear()
        log_thread.join()
        print("exiting...")

if __name__ == "__main__":
    main()
    

