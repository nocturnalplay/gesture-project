import cv2
import mediapipe as mp
import time
import math

# find the percentage of the inbetween value of min and max values


def findPercents(inp, mi, ma, v):
    va = (inp - mi) * 100 / (ma - mi)
    if v == 100:
        va = v - va
    if va > 100:
        return 100
    elif va < 0:
        return 0
    else:
        return int(va)


# videocapture initialization
Wcam, Hcam = 640, 480
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
mpHande = mp.solutions.hands
hands = mpHande.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

cap.set(3, Wcam)
cap.set(4, Hcam)

# first try to initialization the socket server
try:
    while 1:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        li = []
        # find the hand and position with its 20 points
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    # Id, x, y axis of the point
                    li.append([cx, cy])
                # this below line for the 21 dots and connection between them
                # mpDraw.draw_landmarks(
                #     img, handLms, mpHande.HAND_CONNECTIONS)
        rgb = [0]
        Rlen = [0, 0]
        if li:

            # rgb x and y axis point
            rx, ry = li[4][0], li[4][1]
            gx, gy = li[8][0], li[8][1]
            print(rx, "-", ry, ":", gx, "-", gy)

            # circle shape x and y axis point
            cv2.circle(img, (rx, ry), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (gx, gy), 8, (0, 255, 0), cv2.FILLED)

            # lines for the eache shape in rgb
            cv2.line(img, (gx, gy), (rx, ry), (255, 255, 255), 2)

            # canculate the length between the bottom to the each point
            Rlen = [findPercents(math.hypot(rx - gx, ry - gy), 30, 200, 0),
                    findPercents(math.hypot(rx - gx, ry - gy), 30, 200, 100)]
            print("[value]:", Rlen)

            # add the rgb percent values to the list
            rgb = [Rlen[0]]
            
            print(rgb)
        # FPS count of the image
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (400, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Images", img)
        cv2.waitKey(1)

except KeyboardInterrupt:
    print("\nExit...")
