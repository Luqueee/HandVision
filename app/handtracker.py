import mediapipe as mp
import cv2
from config import *

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
        
    
    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    
    def positionFinder(self,image, handNo=0, draw=True, positions = True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            #print(self.results.multi_hand_landmarks)
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = float(lm.x*w), float(lm.y*h)
                
                #cx,cy = int(lm.x), int(lm.y)
                lmlist.append([id,cx,cy])
                
                cx = round(cx)
                cy = round(cy)
                #print(f'{id} , {lm}')
        
                
                if DIBUJARCIRCULOS:
                    cv2.circle(image, (cx,cy), RCIRCULO, WHITE2, GLINEAS, TIPOLINEA)
                    #cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)
                
                if positions:
                    cv2.putText(image, f"{id} \n x: {cx} \n y: {cy}", (cx,cy), FONT, FONTSCALE, color=RED)

                
        list_positions = {}
        try:
            list_positions['0'] = [lmlist[0]]
            list_positions['1'] = lmlist[1:5]
            list_positions['2'] = lmlist[6:9]
            list_positions['3'] = lmlist[10:13]
            list_positions['4'] = lmlist[14:17]
            list_positions['5'] = lmlist[18:21]
        except IndexError:
            pass
                 
        return list_positions
