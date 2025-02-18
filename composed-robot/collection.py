from dotenv import load_dotenv
import os
from queue import Queue
import time
import zmq


from robonet.Subscriber import Subscriber
from robonet.Publisher import Publisher
from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot

from .robot import Robot

from .distance.rangers_generator import rangers_generator, rg
from .behaviors.avoid import Avoid
from .behaviors.start import Start
from .workers import LocalWorker, Worker
from .odometry import Odometry
from .behaviors.drive_free import DriveFree
from .behaviors.home_tyre import HomeTyre
from .arbitration.arbiter import Arbiter




def timer_generator():
    while True:
        time.sleep(0.5)
        yield ("timer", "local", f"hello")


load_dotenv()

PI_IP = os.getenv("PI_IP")

context = zmq.Context()

subscriber = Subscriber(
    PI_IP,
    [
        {"node": "robot", "topic": "left_motor"},
        {"node": "robot", "topic": "right_motor"},
        {"node": "aruco-location", "topic": "aruco-location"},
        {"node": "object_locator", "topic": "object_position"},
    ],
)

publisher = Publisher(
    PI_IP, f"tcp://{PI_IP}", "collection", topics=["robot-command", "robot-position"]
)



q = Queue()

remote_worker = Worker(subscriber, q)
distance_worker = LocalWorker(rangers_generator, q)
timer_worker = LocalWorker(timer_generator, q)
remote_worker.start()
distance_worker.start()
timer_worker.start()


def set_velocities(translation, rotation):
        publisher.send_json(
            "robot-command", {"translation": translation, "rotation": rotation}
        )

arbiter = Arbiter(update_function=set_velocities)

start = Start('start',arbiter,priority=100)
start.has_control = True

home_tyre = HomeTyre('home_tyre',arbiter,priority=50)
avoid = Avoid('avoid',arbiter,priority=20)
drive_free = DriveFree('drive_free',arbiter,priority=10)


odometry = Odometry()


count = 0
while True:
    (topic, node, message) = q.get()
    count+=1
    # if count%15==0:
    #         print(message)
    
    #handlers.update(topic, node, message)
    if topic == "left_motor":
        start.update(message)
        odometry.updateLeft(message["pos"])
    if topic == "right_motor":
        odometry.updateRight(message["pos"])
    if topic == "distances":
        avoid.update(message)
        drive_free.update(message)
    if topic == 'object_position':
        #print('hey homie',message)
        home_tyre.update(message)
    if topic == "aruco-location":
        # print("aruco", message)
        odometry.updateAbsolutePosition(message["x"], message["y"], message["theta"])
    if topic == "timer":
        publisher.send_json(
            "robot-position",
            {"x": odometry.x, "y": odometry.y, "theta": odometry.theta},
        )
            #print(rg.readings)
