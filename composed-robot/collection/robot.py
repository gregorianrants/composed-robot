from dotenv import load_dotenv
import os
import zmq
from robonet.Publisher import Publisher

PI_IP = os.getenv("PI_IP")

context = zmq.Context()

publisher = Publisher(
    PI_IP, context, f"tcp://{PI_IP}", "collection", topics=["robot-command"]
)


class Robot:
    def __init__(self, publisher):
        self.publisher = publisher

    def set_velocities(self, translation, rotation):
        self.publisher.send_json(
            "robot-command", {"translation": translation, "rotation": rotation}
        )


robot = Robot(publisher)