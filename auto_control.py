import socket
import docker
import requests
import threading
import time
from redis import Redis
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO


redis = Redis(host='localhost', port=6379)

class auto_control():

    def __init__(self):
        self.client = docker.from_env()
        self.high_threshold = 1.2
        self.low_threshold = 0.3
        self.times = []
        self.high_count = 0
        self.low_count = 0
        self.size = 1
        services = self.client.services.list()
        for i in services:
            if(i.name == 'my_app_web'):
                self.web_service = i
                break
        self.web_service.scale(1)

    def monitor(self):
        count = 0
        s = 0
        while(1):
            count += 1
            try:
                r = requests.post('http://10.2.10.38:8000/')
            except:
                time.sleep(1)
                r = requests.post('http://10.2.10.38:8000/')

            s += r.elapsed.total_seconds()
            if(count == 5):
                print(f'{s/5}-----{self.high_count}------{self.low_count}')
                self.auto_scale(s/5)
                s = 0
                count = 0
            time.sleep(1)

    def auto_scale(self, t):
        s = self.check_threshold(t)
        if (s == 1):
            self.size += 1
            self.web_service.reload()
            self.web_service.scale(self.size)
            time.sleep(2)
        elif (s == 2 and self.size > 1):
            self.size -= 1
            self.web_service.reload()
            self.web_service.scale(self.size)
            time.sleep(2)


    def check_threshold(self, t):
        self.times.append(t)
        if(t > self.high_threshold):
            self.high_count += 1
        elif(t < self.low_threshold):
            self.low_count += 1
        if(len(self.times) > 5):
            temp = self.times.pop(0)
            if(temp > self.high_threshold):
                self.high_count -= 1
            elif(temp < self.low_threshold):
                self.low_count -= 1
        if(self.high_count >= 3):
            self.high_count = 0
            self.low_count = 0
            self.times = []
            return 1
        elif(self.low_count >= 3):
            self.high_count = 0
            self.low_count = 0
            self.times = []
            return 2
        return 0

def count():
    while(1):
        c0 = int(redis.get('hits'))
        t0 = time.time()
        time.sleep(10)
        c1 = int(redis.get('hits'))
        t1 = time.time()
        print("hits/second:", round((c1-c0)/(t1-t0), 1))


class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        if(self.threadID == 1):
            a = auto_control()
            a.monitor()
        elif(self.threadID == 2):
            count()


if __name__ == "__main__":
    thread1 = myThread(1)
    thread2 = myThread(2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    #a = auto_control()
    #a.monitor()

        
  