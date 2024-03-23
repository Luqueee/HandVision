import cv2
import math
import os
import pyautogui
import json
import asyncio
import time
import numpy as np
from config import *
from handtracker import handTracker


async def main():
    
    # Captura
    cap = cv2.VideoCapture(0)
    tracker = handTracker()
    fps = 0
    
    # Captura frames
    start_time = time.time()
    frames = 0
    
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        success, image = cap.read()
        image = cv2.flip(image, 1)
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        frames += 1
        
        # Calcular FPS
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > 1:  # Calcular FPS cada segundo
            fps = frames / elapsed_time
            
            start_time = time.time()  # Reiniciar el contador de tiempo
            frames = 0  # Reiniciar el contador de fotogramas
        
        cv2.putText(image, f"FPS: {round(fps)}", (20,30), FONT, 1, color=WHITE, thickness=4)

        try:
            positions = lmList
            
            if len(positions['1'][-1]):
                dedoX1, dedoY1 = (positions['1'][-1])[1:]
                dedoX2, dedoY2 = (positions['2'][-1])[1:]
                dedoX3, dedoY3 = (positions['3'][-1])[1:]
                dedoX4, dedoY4 = (positions['4'][-1])[1:] 
                r1 = lmList['1'][0][1:]
                r2 = lmList['2'][0][1:]
                
                with open("app/data/positions.json", encoding="UTF-8") as file:
                    pos = json.load(file)

                if len(pos) < MEDIA:
                
                    pos.append(
                        {
                            'dedo1': [dedoX1,dedoY1],
                            'dedo2': [dedoX2,dedoY2],
                            'dedo3': [dedoX3,dedoY3],
                            'dedo4': [dedoX4,dedoY4],
                            'r1': r1,
                            'r2': r2
                        }
                    )
                    
                    
                else:
                    pos.pop(-1)
                    pos.insert(0,{
                            'dedo1': [dedoX1,dedoY1],
                            'dedo2': [dedoX2,dedoY2],
                            'dedo3': [dedoX3,dedoY3],
                            'dedo4': [dedoX4,dedoY4],
                            'r1': r1,
                            'r2': r2
                        })
                    
                with open("app/data/positions.json", "w", encoding="UTF-8") as file:
                    json.dump(pos, file, indent=4)
        except Exception as error:
            #print(type(error).__name__)
            pass
        
        cv2.imshow("MiVentana", image)
        
        # Obtener la posición de la ventana y mostrarla
        cv2.moveWindow('MiVentana',100,100)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
