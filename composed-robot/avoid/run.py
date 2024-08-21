from dotenv import load_dotenv
import os

from robonet.Subscriber import Subscriber

import zmq
import time
from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
from .avoid import Avoid


load_dotenv()

PI_IP = os.getenv("PI_IP")

with (
    BuildHat() as buildhat,
    Motor("C", buildhat, -1) as left_motor,
    Motor("D", buildhat, 1) as right_motor,
):
    robot = Robot(left_motor, right_motor)
    avoid = Avoid(robot)

    time.sleep(1)

    context = zmq.Context()
    subscriber = Subscriber(
        PI_IP,
        context,
        [{"node": "distances", "topic": "distances"}],
    )

    subscriber.add_listener("distances", avoid.update)
    subscriber.start()
