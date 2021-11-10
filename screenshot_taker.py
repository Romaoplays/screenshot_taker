import time
import os
import shutil
from threading import Thread
import random

from PIL import Image
from PIL import ImageGrab
import imagehash
import keyboard
import glob
import img2pdf


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
            if current_number > 10:
                os.remove("./src/screenshot_" + str(current_number - 10) + ".png")
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
                print("Pausado")
            elif stop_sign == True:
                stop_sign = False
                print("Despausado")
            time.sleep(1)
        elif keyboard.is_pressed("ctrl+x"):
            files = glob.glob("./src/*")
            for f in files:
                os.remove(f)
            files = glob.glob("./final_images/*")
            for f in files:
                os.remove(f)
            stop_sign = True
            current_number = 1
            print("Resetado e pausado")
            time.sleep(1)
        elif keyboard.is_pressed("ctrl+s"):
            print("Convertendo (1%) ...")
            stop_sign = True
            time.sleep(5)
            with open(
                "resultado_" + str(random.randint(1000, 9999)) + ".pdf", "wb"
            ) as f:
                f.write(img2pdf.convert(glob.glob("./final_images/*")))
            print("Convertendo (50%) ...")
            time.sleep(5)
            files = glob.glob("./src/*")
            for f in files:
                os.remove(f)
            files = glob.glob("./final_images/*")
            for f in files:
                os.remove(f)
            print("Convertendo (100%)")
            print("\nFotos convertidas para PDF\n1 = Fechar programa")
            resposta = input()
            exit()


src_path = "./src"
if not os.path.exists(src_path):
    os.makedirs(src_path)

src_final_images = "./final_images"
if not os.path.exists(src_final_images):
    os.makedirs(src_final_images)


current_number = 1
stop_sign = True

print(
    "\n!!Aperte Ctrl + Y para iniciar!!\n\nInstruções:\nCtrl + y - Pausar/Despausar\nCtrl + s - Salvar e converter pra PDF depois de finalizado (OBS: Se fechar sem dar control S -> NÃO VAI SALVAR)\nCtrl + x - Resetar Programa (Necessário se fechou sem dar ctrl + S)"
)

th_1 = Thread(target=main_thread)
th_1.start()
th_2 = Thread(target=stop_thread)
th_2.start()
