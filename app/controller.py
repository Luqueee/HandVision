import json
from config import *
import math
import time
import cv2

import numpy as np


def calcular_media(lista):
    try:
        # Convertir la lista de diccionarios a un arreglo de NumPy
        np_lista = np.array([list(diccionario.values()) for diccionario in lista])

        # Calcular la suma de cada columna
        suma_columnas = np.sum(np_lista, axis=0)

        # Calcular el número de elementos en la lista
        cantidad_elementos = len(lista)

        # Calcular la media de cada columna
        media = np.round(suma_columnas / cantidad_elementos, 0)

        # Crear un diccionario con los resultados
        resultados = {
            "dedo1": media[0].tolist(),
            "dedo2": media[1].tolist(),
            "dedo3": media[2].tolist(),
            "dedo4": media[3].tolist(),
            "r1": media[4].tolist(),
            "r2": media[5].tolist()
        }

        return resultados
    except:
        return {}

def main():
    # Inicializar variables
    fps = 0
    frames = 0
    start_time = time.time()

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        canvas = np.zeros((480, 1200, 3), dtype='uint8')
        
        try:
            with open("app/data/positions.json", encoding="UTF-8") as file:
                positions = json.load(file)
            
            positions = calcular_media(positions)
            
            # Obtener las coordenadas de los puntos
            dedoX1, dedoY1 = positions['dedo1']
            dedoX2, dedoY2 = positions['dedo2']
            dedoX3, dedoY3 = positions['dedo3']
            dedoX4, dedoY4 = positions['dedo4']
            r1 = positions['r1']
            r2 = positions['r2']

            # Calcular distancias
            scrollDist = round(math.sqrt(((dedoX2-dedoX1)**2) + ((dedoY2-dedoY1)**2)), 2)
            dragDist = round(math.sqrt(((dedoX3-dedoX1)**2) + ((dedoY1-dedoY3)**2)), 2)
            clickDist = round(math.sqrt(((dedoX1-dedoX4)**2) + ((dedoY1-dedoY4)**2)), 2)
            angleHand = round(abs(r1[1]-r2[1]), 2)

            # Determinar estados
            scroll = scrollDist < MIN_VALUE
            drag = dragDist < MIN_VALUE
            click = clickDist < MIN_VALUE
            straight = angleHand < MIN_ANGLE_HAND

            # Escribir resultados en archivo
            with open("app/data/commands.json", "w", encoding="UTF-8") as file:
                json.dump({
                    'scroll': [scroll,dedoX2,dedoY2],
                    'drag': [drag,dedoX3,dedoY3],
                    'click': [click],
                    'straight': [straight]
                }, file, indent=4)

            frames += 1
            
            # Calcular FPS
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 1:  # Calcular FPS cada segundo
                fps = frames / elapsed_time
                
                start_time = time.time()  # Reiniciar el contador de tiempo
                frames = 0  # Reiniciar el contador de fotogramas
            
            cv2.putText(canvas, f"FPS: {round(fps)}", (20,30), FONT, 1, color=WHITE, thickness=4)
            cv2.putText(canvas, f'D1: x: {dedoX1} y: {dedoY1}', (20,60), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'D2: x: {dedoX2} y: {dedoY2}', (20,90), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'D3: x: {dedoX3} y: {dedoY3}', (20,120), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'D4: x: {dedoX4} y: {dedoY4}', (20,150), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'scrollDist: {scrollDist}', (20,180), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'clickDist: {clickDist}', (20,210), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'dragDist: {dragDist}', (20,240), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'DISTANCIA: {scrollDist} {scroll} | DISTANCIA MOUSE: {dragDist} {drag} DISTANCIA CLICK: {clickDist} {click}', (20,270), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'r1: {r1}', (20,300), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'r2: {r2}', (20,330), FONT, 0.6, color=WHITE, thickness=2)
            cv2.putText(canvas, f'angleHand: {angleHand} {straight}', (20,360), FONT, 0.6, color=WHITE, thickness=2)
            
            
        except Exception as error:
            #print(type(error).__name__)
            pass     
    
      
        
        cv2.imshow("MiVentana", canvas)
        cv2.moveWindow('MiVentana',800,100)
   
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()






    #print()

    '''       

    if dedoDist <= MAX_DISTANCE_dedo_VALUE and dedoDist >= MIN_DISTANCE_dedo_VALUE:
        if DistD2D3 > 20:
            if not dedo:
                
                last_distancededoY = dedoMediaY
                last_distancededoX = dedoMediaX
                dedo = True
            else:
                
                #print('distancia: ',dedoDist, dedo)
                
                dist_dedo = (dedoMediaY-last_distancededoY)/FUERZA_dedo
                #print('distance dedo: ',dist_dedo)
                
                if abs(dist_dedo) >= MIN_VALUE:
                    pyautogui.scroll(round(dist_dedo))
                
                #print('last distance: x: ',last_distancededoX, 'y: ',last_distancededoY, ' | ','distance: x: ',dedoMediaX, 'y: ',dedoMediaY)
                
                cv2.line(image, (int(last_distancededoX),int(last_distancededoY)), (int(dedoMediaX),int(dedoMediaY)), WHITE2, GLINEAS )
    else:
        dedo = False
    """
    if mouseDist <= MAX_DISTANCE_MOUSE_VALUE and mouseDist > MIN_DISTANCE_MOUSE_VALUE:
        
        await mouse(mouseMediaX, mouseMediaY, w, h)
        
        
        last_distanceDragX = mouseMediaX
        last_distanceDragY = mouseMediaY
        print(last_distanceDragY,last_distanceDragX)
    """

    if dragDist <= MAX_DISTANCE_DRAG_VALUE and dragDist >= MIN_DISTANCE_DRAG_VALUE:
        print("a")
        if DistD1D3 > 20:
            
            if not drag:
                last_distanceDragY = mouseMediaY
                last_distanceDragX = mouseMediaX
                drag = True
                
            else:
                
                #print('distancia: ',dedoDist, dedo)
                
                xx = (last_distanceDragX-mouseMediaX)/SENSIBILIDAD_MOUSE
                yy = (last_distanceDragY-mouseMediaY)/SENSIBILIDAD_MOUSE
                #print('distance dedo: ',dist_dedo)
                print(last_distanceDragX,last_distanceDragY,xx,yy)
                cv2.line(image, (int(last_distanceDragX),int(last_distanceDragY)), (int(xx),int(yy)), WHITE2, GLINEAS )

                pyautogui.moveTo(xx,yy)
                
                
    else:
        drag = False'''
        
        
        
        
        
