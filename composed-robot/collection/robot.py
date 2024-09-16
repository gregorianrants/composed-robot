from dotenv import load_dotenv
import os
import zmq
from robonet.Publisher import Publisher
import time

PI_IP = os.getenv("PI_IP")

context = zmq.Context()

publisher = Publisher(
    PI_IP, context, f"tcp://{PI_IP}", "collection", topics=["robot-command"]
)


class Robot:
    def __init__(self, publisher):
        self.publisher = publisher
        self.current_behavior = None
        self.latched = None

    def set_initial_behavior(self, behavior):
        self.current_behavior = behavior
        self.latched = True

    def update(self, behavior, active, translation, rotation):
        if behavior is self.current_behavior:
            if active:
                return self.set_velocities(translation, rotation)
            else:
                self.latched = False
        elif active:
            if behavior.priority > self.current_behavior.priority:
                self.current_behavior = behavior
                self.latched = True
            if behavior.priority < self.current_behavior.priority and not self.latched:
                print("hellolooowowo")
                self.current_behavior = behavior
                self.latched = True

    def set_velocities(self, translation, rotation):
        self.publisher.send_json(
            "robot-command", {"translation": translation, "rotation": rotation}
        )


robot = Robot(publisher)
