import threading
import time
a = 0
def t1():
    while(1):
        print(a)
        time.sleep(2)
class myThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        t1()
if __name__ == "__main__":
    thr = myThread(1)
    thr.start()
    while(1):
        a = input("input:")
