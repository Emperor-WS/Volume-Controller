import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
#pycaw usuage volume library import
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
##############################################################
#pycaw usuage volume library 

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
##############################################################
#opening the webcam
cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0
detector = htm.handDetector(detectionCon = 0.7)


while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPostion(img, draw=False)
    if len(lmList) !=0:
        # print(lmList)
        
        #getting the x and y for the index and the thumb
        x1, y1 = lmList[4][1], lmList[4][2] 
        x2, y2 = lmList[8][1], lmList[8][2] 
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        # putting circle on the index and the thumb
        cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED) 
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED) 
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)    
        length = math.hypot(x2 - x1, y2 - y1)
        #changing the lenght from index to thumb to our volume and setting our volume to it
        vol = np.interp(length, [20, 250], [minVol, maxVol])
        volBar = np.interp(length, [30, 250], [400, 150])
        volPer = np.interp(length, [30, 250], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
    cv2.rectangle(img,(50, 150), (85, 400), (255,0,0), 3)
    cv2.rectangle(img,(50, int(volBar)), (85, 400), (255,0,0), cv2.FILLED)
    cv2.putText(img, str(int(volPer)) + "%", (45,450), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 2)
    #calculating our fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (0 , 255 , 0), 3)
    cv2.imshow("Image", img)
    #closing the window by using q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
