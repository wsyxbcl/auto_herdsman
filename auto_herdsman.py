import sys
import subprocess
import random
import time
import datetime

import pytesseract
from PIL import Image

from common.auto_adb import auto_adb

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
adb = auto_adb()

def wakeup_unlock():
    """
    Wake up and unlock the device
    """
    adb.run('shell input keyevent 26')
    time.sleep(2)
    # Since the unlock process is not universal, a simple swipe up is used here.
    adb.run('shell input swipe 540 800 540 100')

def pull_screenshot(filename='room.png'):
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')
    f = open(filename, 'wb')
    f.write(screenshot)
    f.close()

def get_time():
    touch(int(0.31 * w), int(0.22 * h))
    print("Taking a look of the first egg...")
    pull_screenshot(filename='monster_condition.png')
    print("Getting time remaining...")

    screenshot = Image.open('./monster_condition.png')
    box =  (671, 711, 816, 750)
    time_img = screenshot.crop(box)
    time_remain = pytesseract.image_to_string(time_img)
    h_min_sec = [3600, 60, 1]
    time_sec = sum([a * b for a, b in zip(h_min_sec, map(int, time_remain.split(':')))])
    print("Time remaining: "+time_remain+'({}s)'.format(time_sec))

    touch(int(0.31 * w), int(0.22 * h))
    print("Got it.")
    return time_sec

def incubate():
    # Loading monster eggs
    touch(int(0.12 * w), int(0.96 * h))
    print("Loading monster eggs...")

    # Selecting priority
    touch(int(0.13 * w), int(0.7 * h))
    print("Priority: Shortest time")

def collect():
    # Easy to implement but due to the limited space, a feed function may also be needed
    pass

def sell():
    # Selling all monsters
    touch(int(0.51 * w), int(0.96 * h))
    print("Selling all monsters...")

    touch(int(0.33 * w), int(0.61 * h))
    print("Confirmed")

def touch(left, top):
    left = int(random.uniform(left - 5, left + 5))
    top = int(random.uniform(top - 5, top + 5))
    after_top = int(random.uniform(top - 5, top + 5))
    after_left = int(random.uniform(left - 5, left + 5))
    swipe_x1, swipe_y1, swipe_x2, swipe_y2 = left, top, after_left, after_top
    cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=swipe_x1,
        y1=swipe_y1,
        x2=swipe_x2,
        y2=swipe_y2,
        duration=200
    )
    print(cmd)
    adb.run(cmd)
    time.sleep(3)

if __name__ == "__main__":
    # Get screen size
    pull_screenshot()
    screen = Image.open('./room.png')
    w, h = screen.size

    while True:
        incubate()
        time_remain = get_time() - 3
        print(datetime.datetime.now())
        for i in range(time_remain):
            sys.stdout.write("\rWill be back in {} seconds".format(time_remain - i))
            sys.stdout.flush()
            time.sleep(1)
        sell()