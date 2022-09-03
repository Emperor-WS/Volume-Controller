`````import cv2
import mediapipe as mp
import time



class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity = 1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon  
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity,
                                        self.detectionCon, self.trackCon,)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self, img, draw = True ):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        #checking if there is a hand in the window
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:      
                if draw:                                                       
                    #showing dots and connections of hands (21 land mark)
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                
        return img  
    def findPostion(self,img, handNo = 0, draw = True):
         
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo] 
            #Getting x,y cordination for each landmark on hand
            for id, lm in enumerate(myHand.landmark):
                h , w , c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)               
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED) 
                    
                    
        return lmList
        
                
def main():
    #opening the webcam
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector()
    while True:
        success,img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPostion(img)
        
        if len(lmList) !=0:            
            print(lmList[4])
        
        #calculating our fps
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        
        
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (255 , 0 , 255), 3)
        
        cv2.imshow("Image", img)
        #closing the window by using q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

 

if __name__ == "__main__":
    main()











