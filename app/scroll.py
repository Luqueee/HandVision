import time
import pyautogui
from config import *
import json


scrollPoint = []
scrollv = False
dist = 0


while True:
    try:
        with open("app/data/commands.json", encoding="UTF-8") as file:
            comandos = json.load(file)
        
        scroll = comandos.get('scroll', [False, 0, 0])[0]  # El primer elemento es el booleano
        scrollx, scrolly = comandos.get('scroll', [False, 0, 0])[1:]  # Los siguientes dos son los números

       
        click = comandos.get('click', False)
        straight = comandos.get('straight', False)

        if scroll and not scrollv:
            scrollPoint = [scrollx, scrolly]
            scrollv = True
            dist = 0
        
        if not scroll and scrollv:
            scrollv = False
        
        if scroll and scrollv:
            dist = round(scrolly - scrollPoint[1])
            if abs(dist) > 10:
                pyautogui.scroll(dist)
       
            
            
            
            
        
        #print(scroll, scrollv, scrollPoint, scrollx, scrolly, dist)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    
    #time.sleep(0.1)  # Esperar 0.1 segundos antes de la próxima verificación
    