import socket
import docker
import requests
import threading
import time

import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO



class auto_control():

    def __init__(self):
        self.client = docker.from_env()
        self.high_threshold = 1.1
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

if __name__ == "__main__":
    a = auto_control()
    a.monitor()
