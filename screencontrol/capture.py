import time
from threading import Thread

import cv2
import mss
import numpy as np

from WebTop import settings


class Capture(Thread):
    def __init__(self, master):
        super(Capture, self).__init__()
        self.master = master
        self.stop = False
        self.pause = False
        self.img = self.proc()

    def pause_check(self):
        if self.master.last_update + 3 < time.time():
            self.pause = True

    def get_img(self):
        self.pause = False
        return self.img

    def proc(self):
        mon = {"top": 0, "left": 0, "width": settings.SCREEN_WIDTH, "height": settings.SCREEN_HEIGHT}
        with mss.mss() as sct:
            return np.array(sct.grab(mon))

    def run(self):
        while not self.stop:
            if not self.pause:
                # start_time = time.time()
                self.img = self.proc()
                self.pause_check()
            # print("thread capture:", 1.0 / ((time.time() - start_time)+0.0001))
            else:
                time.sleep(1)


class Process(Thread):
    def __init__(self, master, capture):
        super(Process, self).__init__()
        self.master = master
        self.capture = capture
        self.stop = False
        self.pause = False
        self.img = self.proc()

    def pause_check(self):
        if self.master.last_update + 3 < time.time():
            self.pause = True

    def get_img(self):
        self.pause = False
        return self.img

    def proc(self):
        img = cv2.resize(np.array(self.capture.get_img()), (settings.TARGET_WIDTH, settings.TARGET_HEIGHT),
                         interpolation=cv2.INTER_AREA)
        ret, img = cv2.imencode('.jpg', img)
        return img.tobytes()

    def run(self):
        while not self.stop:
            if not self.pause:
                self.pause_check()
                # start_time = time.time()
                self.img = self.proc()
            # print("thread process:", 1.0 / ((time.time() - start_time)+0.0001))
            else:
                time.sleep(1)


class VideoFeed(object):
    def __init__(self):
        self.last_update = time.time()
        self.capture = Capture(self)
        self.process = Process(self, self.capture)
        self.capture.start()
        self.process.start()

    def __del__(self):
        self.capture.stop = True
        self.capture.join()
        self.process.stop = True
        self.process.join()

    def get_frame(self):
        self.last_update = time.time()
        return self.process.get_img()
