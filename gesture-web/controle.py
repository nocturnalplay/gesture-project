import sys
import cv2
import mediapipe as mp
import time
import asyncio
from websockets import serve


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


async def handler(websocket):
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
            if li:
                tx, ty = li[4][0], li[4][1]
                sx, sy = li[8][0], li[8][1]
                rx, ry = li[12][0], li[12][1]
                # circle shape x and y axis point
                cv2.circle(img, (tx, ty), 8, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (sx, sy), 8, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (rx, ry), 8, (0, 255, 0), cv2.FILLED)
                print("x:", tx, "y:", ty, "::", "x:", sx,
                      "y:", sy, "::", "x:", rx, "y:", ry)
                await websocket.send("{\"tx\":"+str((tx - 0) * 100 / (0 - 600))+",\"ty\":"+str((ty - 0) * 100 / (0 - 350))+",\
\"sx\":"+str((sx - 0) * 100 / (0 - 600))+",\"sy\":"+str((sy - 0) * 100 / (0 - 350))+",\
\"rx\":"+str((rx - 0) * 100 / (0 - 600))+",\"ry\":"+str((ry - 0) * 100 / (0 - 350))+"}")
            cv2.imshow("Images", img)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print("\nExit...")


async def main():
    print("server created on 3333 port")
    async with serve(handler, "127.0.0.1", 3333):
        await asyncio.Future()  # run forever

asyncio.run(main())
