


class DriveFree:
    def __init__(self, robot):
        self.robot = robot
        self.priority = 10

    def update(self, distances):
        self.robot.update(self,True,200, 0)