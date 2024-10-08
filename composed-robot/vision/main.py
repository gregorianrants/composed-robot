from robonet.Publisher import Publisher
import zmq
from dotenv import load_dotenv
import os
import time
import pprint

import cv2
from picamera2 import Picamera2
import time


picam2 = Picamera2()

print("sensor_modes _________________________________")
pprint.pp(picam2.sensor_modes)

mainW = 1640
mainH = 1232
picam2.preview_configuration.main.size = (mainW, mainH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 10


loresW = 820
loresH = 486
picam2.preview_configuration.enable_lores()
picam2.preview_configuration.lores.size = (loresW, loresH)


picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
print("__________________________________________________________\n")
pprint.pp(picam2.camera_properties)
print("__________________________________________________________\n")
picam2.controls.AeExposureMode = 1
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

publisher = Publisher(
    hub_ip=PI_IP,
    address=f"tcp://{PI_IP}",
    node="vision",
    topics=["frame"],
)

count = 0
while True:
    tStart = time.time()
    im = picam2.capture_array("lores")
    im = cv2.cvtColor(im, cv2.COLOR_YUV420p2RGB)
    if count == 0:
        print(im.shape)
        count += 1
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
