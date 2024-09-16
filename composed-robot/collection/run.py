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

from .robot import robot

from ..distance.rangers_generator import rangers_generator
from .behaviors.avoid import Avoid
from .behaviors.start import Start
from .workers import LocalWorker, Worker


def timer_generator():
    while True:
        time.sleep(1)
        yield ("timer", "local", f"hello")


load_dotenv()

PI_IP = os.getenv("PI_IP")

context = zmq.Context()

subscriber = Subscriber(
    PI_IP,
    context,
    [
        {"node": "robot", "topic": "left_motor"},
        {"node": "robot", "topic": "right_motor"},
    ],
)


q = Queue()

remote_worker = Worker(subscriber, q)
distance_worker = LocalWorker(rangers_generator, q)
timer_worker = LocalWorker(timer_generator, q)
remote_worker.start()
distance_worker.start()
timer_worker.start()


avoid = Avoid(robot)
start = Start(robot)
robot.set_initial_behavior(start)

while True:
    (topic, node, message) = q.get()
    # handlers.update(topic, node, message)
    if topic == "left_motor":
        start.update(message)
    elif topic == "distances":
        print(message)
        avoid.update(message)
