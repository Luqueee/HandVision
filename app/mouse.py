import time
import pyautogui
from config import *
import json

mousePoint = []
mousev = False
dist = 0
mouseposx, mouseposy = pyautogui.position()
restMouseX = 0
restMouseY = 0

while True:
    try:
        with open("app/data/commands.json", encoding="UTF-8") as file:
            comandos = json.load(file)
        
        mouse = comandos.get('drag', [False, 0, 0])[0]  # El primer elemento es el booleano
        mousex, mousey = comandos.get('drag', [False, 0, 0])[1:]  # El siguiente es el número
        
        x = 1920*mousex/640
        y = 1080*mousey/480
        
        
        if mouse and not mousev:
            mousePoint = [x,y]
            mousev = True
           
            
        if not mouse and mousev:
            mousev = False
            
        if mouse and mousev:
            
            restMouseX = round((mousePoint[0]-x)/5)
            restMouseY = round((mousePoint[1]-y)/5)
            
            if abs(restMouseX) > 5 or abs(restMouseY) > 5:
                mouseposx -= restMouseX
                mouseposy -= restMouseY
                
                if mouseposx > 0 and mouseposx < 1920 and mouseposy > 0 and mouseposy < 1080: 
                    pyautogui.moveTo(mouseposx, mouseposy)
        
        mouseposx, mouseposy = pyautogui.position()
        
        #print(restMouseX,restMouseY,mousePoint, x, y,mouse,mousev,pyautogui.position(),mouseposx,mouseposy)
        
        
            
            
            
            
        
        #print(scroll, scrollv, scrollPoint, scrollx, scrolly, dist)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    
    #time.sleep(0.1)  # Esperar 0.1 segundos antes de la próxima verificación
    