import cv2
import numpy as np
import mediapipe as mp
import time
import math
import autopy
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

class HandController:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        
        # Initialize volume control
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.volRange = self.volume.GetVolumeRange()
        self.minVol, self.maxVol = self.volRange[0], self.volRange[1]
        
        # Initialize screen dimensions
        self.wScr, self.hScr = autopy.screen.size()
        
        # Mouse control parameters
        self.frameR = 100
        self.smoothening = 7
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                            (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        if len(self.lmList) != 0:
            # Thumb
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

    def controlVolume(self, length, img, draw=True):
        # Convert length to volume
        vol = np.interp(length, [50, 200], [self.minVol, self.maxVol])
        volBar = np.interp(length, [50, 200], [400, 150])
        volPercentage = np.interp(length, [50, 200], [0, 100])
        
        # Set volume
        self.volume.SetMasterVolumeLevel(vol, None)
        
        if draw:
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPercentage)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                       1, (255, 0, 0), 3)
        
        return volPercentage

    def controlMouse(self, img, fingers):
        if len(self.lmList) != 0:
            x1, y1 = self.lmList[8][1:]
            x2, y2 = self.lmList[12][1:]
            
            # Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (self.frameR, 640 - self.frameR), (0, self.wScr))
                y3 = np.interp(y1, (self.frameR, 480 - self.frameR), (0, self.hScr))
                
                self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
                self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening
                
                autopy.mouse.move(self.wScr - self.clocX, self.clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                self.plocX, self.plocY = self.clocX, self.clocY
            
            # Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = self.findDistance(8, 12, img)
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()

def main():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    # Initialize hand controller
    controller = HandController(maxHands=1)
    
    pTime = 0
    cTime = 0
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Mirror image
        
        # Find hands
        img = controller.findHands(img)
        lmList, bbox = controller.findPosition(img)
        
        if len(lmList) != 0:
            fingers = controller.fingersUp()
            
            # Control volume with thumb and index finger
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:
                length, img, lineInfo = controller.findDistance(4, 8, img)
                controller.controlVolume(length, img)
            
            # Control mouse with index and middle fingers
            controller.controlMouse(img, fingers)
        
        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        
        # Display image
        cv2.imshow("Hand Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 