from handGesture import hand
import cv2

cam = cv2.VideoCapture(0)
Wcam = 640
Hcam = 480
cam.set(3, Wcam)
cam.set(4, Hcam)

hands = hand.Hand(max_hands=2)

while 1:
    success, img = cam.read()
    hand.DetectHands(img, hands)
