import cv2
from picamera2 import Picamera2
import time
import pprint
import time


picam2 = Picamera2()
print("sensor_modes _________________________________")
pprint.pp(picam2.sensor_modes)

mainW = 1640
mainH = 1232
picam2.preview_configuration.main.size = (mainW, mainH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 10


# loresW = 820
# loresH = 486
# picam2.preview_configuration.enable_lores()
# picam2.preview_configuration.lores.size = (loresW, loresH)

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()
print("__________________________________________________________\n")
pprint.pp(picam2.camera_properties)
print("__________________________________________________________\n")
#picam2.controls.AeExposureMode = 1
fps = 0
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
height = 1.5
weight = 3
myColor = (0, 0, 255)

cal_image_count = 0
frame_count = 1
counter = 0
time.sleep(2)
print('go')

while True:
    tStart = time.time()
    # im = picam2.capture_array('lores')
    im = picam2.capture_array()
    # im = cv2.cvtColor(im, cv2.COLOR_YUV420p2RGB)

    frame_count += 1
    if frame_count % 10 == 0:
        counter += 1
        if counter==5:
            cal_image_count += 1
            print("saving image")
            cv2.imwrite("cal_image_" + str(cal_image_count) + ".jpg", im)
            cal_image_count += 1
            counter = 0
            
   
    #cv2.imwrite("cal_image_" + str(cal_image_count) + ".jpg", im)
    

    cv2.putText(
        im,
        str(int(fps)) + " FPS, counter:" + str(counter),
        pos,
        font,
        height,
        myColor,
        weight,
    )
    display_im = cv2.flip(im,1)
    display_im = rescale_frame(display_im,percent=50)
    cv2.imshow("Camera", display_im)
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
