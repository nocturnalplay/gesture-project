from handGesture import hand
import cv2

cam = cv2.VideoCapture(0)
Wcam = 640
Hcam = 480
cam.set(3, Wcam)
cam.set(4, Hcam)

hands = hand.Hand(max_hands=2)

try:
    while 1:
        success, img = cam.read()
        val = hand.DetectHands(img, hands)
        print(val)
except KeyboardInterrupt:
    cam.release()
    cv2.destroyAllWindows()
cam.release()
cv2.destroyAllWindows()