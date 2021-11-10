import time
import os
import shutil
from threading import Thread

from PIL import Image
from PIL import ImageGrab
import imagehash
import keyboard
import glob


def compare_images(image_1, image_2):
    if current_number == 1:
        return False
    hash0 = imagehash.average_hash(Image.open(image_1))
    hash1 = imagehash.average_hash(Image.open(image_2))
    cutoff = 1  # maximum bits that could be different between the hashes.
    if hash0 - hash1 < cutoff:
        return True
    else:
        return False


def get_screenshot():
    global current_number
    snapshot = ImageGrab.grab()
    snapshot.save("./src/screenshot_" + str(current_number) + ".png")


def main_thread():
    global current_number
    while True:
        if stop_sign == False:
            time.sleep(5)
            get_screenshot()

            if (
                compare_images(
                    ("./src/screenshot_" + str(current_number - 1) + ".png"),
                    ("./src/screenshot_" + str(current_number - 0) + ".png"),
                )
                == False
            ):
                shutil.copy(
                    ("./src/screenshot_" + str(current_number - 0) + ".png"),
                    ("./final_images/screenshot_" + str(current_number - 0) + ".png"),
                )
            current_number = current_number + 1

        else:
            time.sleep(5)


def stop_thread():
    global stop_sign
    global current_number
    while True:
        if keyboard.is_pressed("ctrl+y"):
            if stop_sign == False:
                stop_sign = True
                print("Paused")
            elif stop_sign == True:
                stop_sign = False
                print("Unpaused")
            time.sleep(1)
        elif keyboard.is_pressed("ctrl+x"):
            files = glob.glob("./src/*")
            for f in files:
                os.remove(f)
            files = glob.glob("./final_images/*")
            for f in files:
                os.remove(f)
            print("Files Cleared")
            current_number = 1
            time.sleep(1)


src_path = "./src"
if not os.path.exists(src_path):
    os.makedirs(src_path)

src_final_images = "./final_images"
if not os.path.exists(src_final_images):
    os.makedirs(src_final_images)

files = glob.glob("./src/*")
for f in files:
    os.remove(f)
files = glob.glob("./final_images/*")
for f in files:
    os.remove(f)
print("Prints anteriores deletados")
time.sleep(1)

current_number = 1
stop_sign = True


th_1 = Thread(target=main_thread)
th_1.start()
th_2 = Thread(target=stop_thread)
th_2.start()
