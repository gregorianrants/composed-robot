from dotenv import load_dotenv
import os

from robonet.Subscriber import Subscriber
from robonet.Publisher import Publisher
from queue import Queue

import zmq
import time
from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
from .avoid import Avoid
from .robot import robot
from threading import Thread

from ..distance.local_publisher import rangers_generator


load_dotenv()

PI_IP = os.getenv("PI_IP")

context = zmq.Context()

subscriber = Subscriber(
    PI_IP,
    context,
    [
        # {"node": "distances", "topic": "distances"},
        {"node": "robot", "topic": "left_motor"},
        {"node": "robot", "topic": "right_motor"},
    ],
)


class Worker(Thread):
    def __init__(self, subscriber, queue):
        super().__init__()
        self.subscriber = subscriber
        self.queue = queue

    def run(self):
        self.subscriber.start()
        for topic, node, message in self.subscriber.json_stream():
            self.queue.put((topic, node, message))


class LocalWorker(Thread):
    def __init__(self, event_generator, queue):
        super().__init__()
        self.event_generator = event_generator
        self.queue = queue

    def run(self):
        for topic, node, message in self.event_generator():
            self.queue.put((topic, node, message))


count = 0


def timer_generator():
    while True:
        time.sleep(1)
        yield ("timer", "local", f"hello{count}")


q = Queue()

avoid = Avoid(robot)
remote_worker = Worker(subscriber, q)
distance_worker = LocalWorker(rangers_generator, q)
timer_worker = LocalWorker(timer_generator, q)
remote_worker.start()
distance_worker.start()
timer_worker.start()


start = False

while True:
    (topic, node, message) = q.get()
    if topic == "timer":
        print(message)
    if topic == "left_motor" and count < 5:
        count += 1
    if topic == "distances" and count == 5:
        avoid.update(message)
        if count % 10 == 0:
            print(message)
            count += 1
