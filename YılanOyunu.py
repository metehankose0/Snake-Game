import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import threading
import winsound

def play_sound(freq, dur):
    try:
        threading.Thread(target=winsound.Beep, args=(freq, dur), daemon=True).start()
    except:
        pass

# Kamera Ayarları
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# El Dedektörü
detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = [] 
        self.lengths = [] 
        self.currentLenght = 0
        self.allowedLenght = 150
        self.previousHead = 0, 0 

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        if self.imgFood is None:
            self.imgFood = np.zeros((50, 50, 3), np.uint8)
            print("Uyari: Donut.png bulunamadi!")
        else:
            
            self.imgFood = cv2.resize(self.imgFood, (50, 50))
            
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.bombPoint = 0, 0
        self.bombActive = False
        self.bombTimer = 0

        self.score = 0
        self.highScore = 0
        try:
            with open("highscore.txt", "r") as f:
                content = f.read().strip()
                if content:
                    self.highScore = int(content)
        except:
            pass

        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def randomBombLocation(self):
        self.bombPoint = random.randint(100, 1000), random.randint(100, 600)
        self.bombActive = True
        self.bombTimer = 100 # Bombanın ekranda kalma süresi
    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 200],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 350],
                               scale=5, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'High Score: {self.highScore}', [300, 480],
                               scale=5, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, "Yeniden oynamak icin", [150, 600],
                               scale=3, thickness=3, offset=10, colorR=(0, 0, 255))
            cvzone.putTextRect(imgMain, "parmaklarini birlestir", [150, 660],
                               scale=3, thickness=3, offset=10, colorR=(0, 0, 255))
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLenght += distance
            self.previousHead = cx, cy

            # Yılan haraket etme işleyişi
            if self.currentLenght > self.allowedLenght:
                for i, length in enumerate(self.lengths):
                    self.currentLenght -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLenght < self.allowedLenght:
                        break
            
            # Yiyecek yeme kontrolü
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
               ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                play_sound(1200, 150) # Yemek yeme sesi
                self.randomFoodLocation()
                self.allowedLenght += 50
                self.score += 1
                
            
            if not self.bombActive and random.randint(0, 100) < 2:
                self.randomBombLocation()

            # Yılanı Çizme
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, tuple(self.points[i - 1]), tuple(self.points[i]), (0, 0, 255), 20)
                cv2.circle(imgMain, tuple(self.points[-1]), 20, (0, 255, 0), cv2.FILLED)

            # Yemek Çizimi
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))

            # Bomba Çizimi ve Kontrolü
            if self.bombActive:
                self.bombTimer -= 1
                if self.bombTimer <= 0:
                    self.bombActive = False
                else:
                    bx, by = self.bombPoint
                    
                    cv2.circle(imgMain, (bx, by), 30, (0, 0, 0), cv2.FILLED)
                    cvzone.putTextRect(imgMain, "B", [bx-12, by+10], scale=2, thickness=3, colorT=(0, 0, 255), colorR=(0,0,0), offset=0)
                    
                    # Bombaya çarpma kontrolü
                    if bx - 30 < cx < bx + 30 and by - 30 < cy < by + 30:
                        print("Bombaya Carpti!")
                        play_sound(300, 800) # Patlama Sesi
                        self.gameOver = True
                        if self.score > self.highScore:
                            self.highScore = self.score
                            try:
                                with open("highscore.txt", "w") as f:
                                    f.write(str(self.highScore))
                            except:
                                pass
                        self.points = []
                        self.lengths = []
                        self.currentLenght = 0
                        self.allowedLenght = 150
                        self.previousHead = 0, 0
                        self.randomFoodLocation()
                        self.bombActive = False

            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)

            # Çarpışma Kontrolü
            if len(self.points) > 10:
                pts = np.array(self.points[:-5], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
                minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

                if -2 <= minDist <= 2: # Çarpma hassasiyeti
                    print("Carpti!")
                    play_sound(300, 600) # Yanma Sesi
                    self.gameOver = True
                    if self.score > self.highScore:
                        self.highScore = self.score
                        try:
                            with open("highscore.txt", "w") as f:
                                f.write(str(self.highScore))
                        except:
                            pass
                    self.points = []
                    self.lengths = []
                    self.currentLenght = 0
                    self.allowedLenght = 150
                    self.previousHead = 0, 0
                    self.randomFoodLocation()

        return imgMain

# Oyunu Başlat
game = SnakeGameClass("Donut.png")

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2] 
        img = game.update(img, pointIndex)
        
        if game.gameOver:
            x1, y1 = lmList[8][0:2]
            x2, y2 = lmList[4][0:2]
            dist = math.hypot(x2 - x1, y2 - y1)
            
            
            if dist < 45:
                play_sound(1500, 200) 
                game.gameOver = False
                game.score = 0
                game.bombActive = False
    
    cv2.imshow("Snake Game", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
        game.score = 0
    if key == 27: 
        break