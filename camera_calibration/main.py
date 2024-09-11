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


while True:
    tStart = time.time()
    im = picam2.capture_array()


    frame_count+=1
    if frame_count ==30:
        cv2.imwrite('cal_image_' + str(cal_image_count) + '.jpg',im)
        cal_image_count +=1
        frame_count =0


    cv2.putText(im, str(int(fps)) + " FPS", pos, font, height, myColor, weight)
    cv2.imshow("Camera", im)
    if cv2.waitKey(1) == ord("q"):
        break
    tEnd = time.time()
    loopTime = tEnd - tStart
    fps = 0.9 * fps + 0.1 * (1 / loopTime)
cv2.destroyAllWindows()



# import cv2
# from picamera2 import Picamera2
# import time



# picam2 = Picamera2()
# dispW = 640
# dispH = 480
# picam2.preview_configuration.main.size = (dispW, dispH)
# picam2.preview_configuration.main.format = "RGB888"
# picam2.preview_configuration.controls.FrameRate = 30
# picam2.preview_configuration.align()
# picam2.configure("preview")
# picam2.start()
# fps = 0
# pos = (30, 60)
# font = cv2.FONT_HERSHEY_SIMPLEX
# height = 1.5
# weight = 3
# myColor = (0, 0, 255)

# cal_image_count = 0
# frame_count = 0


# while True:
#     tStart = time.time()
#     im = picam2.capture_array()


#     frame_count+=1
#     if frame_count ==30:
#         cv2.imwrite('cal_image_' + str(cal_image_count) + '.jpg')
#         cal_image_count +=1
#         frame_count =0


#     cv2.putText(im, str(int(fps)) + " FPS", pos, font, height, myColor, weight)
#     cv2.imshow("Camera", im)
#     if cv2.waitKey(1) == ord("q"):
#         break
#     tEnd = time.time()
#     loopTime = tEnd - tStart
#     fps = 0.9 * fps + 0.1 * (1 / loopTime)
# cv2.destroyAllWindows()
