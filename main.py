from handGesture import hand
import cv2
import math
import socket
import json
import sys
# ----------------------------------------------------------------
# car gesture arch
# ----------------------------------------------------------------

# find the actual percentage for the inbetween values


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


cam = cv2.VideoCapture(0)
Wcam = 640
Hcam = 480
cam.set(3, Wcam)
cam.set(4, Hcam)

hands = hand.Hand(max_hands=2)
host = ""
port = int(sys.argv[1])
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print("waiting for connection...")
        client, addr = s.accept()
        with client:
            # when client connects to the server videocapture start
            print(f"Connection established: {addr}")
            print(f"{client.recv(1024).decode()}")
            while 1:
                success, img = cam.read()
                res = hand.DetectHands(img, hands)
                if not res['status']:
                    break
                img = res["image"]
                left = res["data"]["left"]
                right = res["data"]["right"]
                enddata = {}
                if right:
                    # circle shape x and y axis point
                    cv2.circle(img, (right[4][0], right[4][1]),
                               8, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, (right[8][0], right[8][1]),
                               8, (0, 255, 0), cv2.FILLED)

                    # data for the car
                    enddata["acspeed"] = findPercents(math.hypot(
                        right[4][0]-right[8][0], right[4][1]-right[8][1]), 20, 100, 0)
                    if enddata["acspeed"] > 0:
                        if right[12][1] < right[11][1]:
                            enddata["diraction"] = "backward"
                            # lines for the eache shape in rgb
                            cv2.line(img, (right[4][0], right[4][1]),
                                     (right[8][0], right[8][1]), (0, 0, 0), 2)
                        else:
                            enddata["diraction"] = "forward"
                            # lines for the eache shape in rgb
                            cv2.line(img, (right[4][0], right[4][1]),
                                     (right[8][0], right[8][1]), (255, 255, 255), 2)
                    else:
                        enddata["diraction"] = "neutral"

                if left:
                    # circle shape x and y axis point
                    cv2.circle(img, (left[4][0], left[4][1]),
                               8, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, (left[8][0], left[8][1]),
                               8, (0, 255, 0), cv2.FILLED)
                    # data for the car
                    enddata["rospeed"] = findPercents(math.hypot(
                        left[4][0]-left[8][0], left[4][1]-left[8][1]), 30, 100, 0)
                    if enddata["rospeed"] > 0:
                        if left[4][0] < left[8][0]:
                            enddata["diraction"] = "left"
                            # lines for the eache shape in rgb
                            cv2.line(img, (left[4][0], left[4][1]),
                                     (left[8][0], left[8][1]), (0, 0, 0), 2)
                        elif left[4][0] > left[8][0]:
                            enddata["diraction"] = "right"
                            # lines for the eache shape in rgb
                            cv2.line(img, (left[4][0], left[4][1]),
                                     (left[8][0], left[8][1]), (255, 255, 255), 2)
                if enddata:
                    d = json.dumps(enddata)
                    client.send(d.encode())
                cv2.imshow("Images", img)
                cv2.waitKey(1)

except KeyboardInterrupt:
    cam.release()
    cv2.destroyAllWindows()

cam.release()
cv2.destroyAllWindows()
