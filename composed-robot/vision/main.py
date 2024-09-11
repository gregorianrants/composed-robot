from robonet.Publisher import Publisher
import zmq
from dotenv import load_dotenv
import os
import time


import cv2
from picamera2 import Picamera2
import time


picam2 = Picamera2()
dispW = 640
dispH = 480
picam2.preview_configuration.main.size = (dispW, dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
fps = 0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
height = 1.5
weight = 3
myColor = (0, 0, 255)

cal_image_count = 0
frame_count = 0

PI_IP = os.getenv("PI_IP")
DESKTOP_IP = os.getenv("DESKTOP_IP")

context = zmq.Context()
publisher = Publisher(
    hub_ip=DESKTOP_IP,
    context=context,
    address=f"tcp://{PI_IP}",
    node="camera-calibration",
    topics=["frame"],
)


while True:
    tStart = time.time()
    im = picam2.capture_array()
    cv2.putText(im, str(int(fps)) + " FPS", pos, font, height, myColor, weight)
    res, jpeg = cv2.imencode(".jpg", im)
    publisher.send_bytes("frame", jpeg)
    if cv2.waitKey(1) == ord("q"):
        break
    tEnd = time.time()
    loopTime = tEnd - tStart
    fps = 0.9 * fps + 0.1 * (1 / loopTime)
cv2.destroyAllWindows()


for i in range(10):

    time.sleep(1)
