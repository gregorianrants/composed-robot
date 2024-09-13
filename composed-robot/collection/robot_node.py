from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
from robonet.Subscriber import Subscriber
from dotenv import load_dotenv
from robonet.Publisher import Publisher
import os

import zmq

load_dotenv()

PI_IP = os.getenv("PI_IP")


with (
    BuildHat() as buildhat,
    Motor("C", buildhat, -1, 1) as left_motor,
    Motor("D", buildhat, 1, 1) as right_motor,
):
    robot = Robot(left_motor, right_motor)

    context = zmq.Context()

    publisher = Publisher(
        PI_IP, context, f"tcp://{PI_IP}", "robot", topics=["left_motor", "right_motor"]
    )

    def send_left(data):
        publisher.send_json("left_motor", data)

    def send_right(data):
        publisher.send_json("right_motor", data)

    left_motor.add_listener(send_left)
    right_motor.add_listener(send_right)

    subscriber = Subscriber(
        PI_IP,
        context,
        [{"node": "collection", "topic": "robot-command"}],
    )

    # subscriber.add_listener("distances", avoid.update)
    subscriber.start()

    for topic, node, message in subscriber.json_stream():
        # print(topic, node, message)
        if topic == "robot-command":
            robot.set_velocities(message["translation"], message["rotation"])
