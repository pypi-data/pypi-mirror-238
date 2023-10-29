import cv2
import json
import requests
import keyboard
import pyautogui
import numpy as np
from time import sleep

def uteis_timer(tempo:int=10, decresente:bool=False):
    if decresente == False:
        for i in range(1,tempo+1):
            print(i)
            i -= 1
            sleep(1)
    elif decresente == True:
        n = tempo 
        for i in range(tempo):
            print(n)
            n -=1
            sleep(1)

def uteis_gravadorTela(fps:float=30):
    tamanho_tela = tuple(pyautogui.size())
    codec = cv2.VideoWriter_fourcc(*"mp4h")
    video = cv2.VideoWriter("video.mp4",codec,fps,tamanho_tela)
    
    while True:
        frame = pyautogui.screenshot()
        frame = np.array(frame)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        video.write(frame)

        if keyboard.is_pressed("esc"):
            break

    video.release()
    cv2.destroyAllWindows()

