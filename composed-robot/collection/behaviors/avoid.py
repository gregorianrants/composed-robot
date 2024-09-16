from .state import State


# class Avoid:
#     def __init__(self, robot):
#         self.state = State()
#         self.robot = robot

#     def update(self, distances):
#         self.state.update_state(distances)
#         translation, rotation = self.state.get_velocities(distances)
#         self.robot.update(translation, rotation)


class Avoid:
    def __init__(self, robot):
        self.state = State()
        self.robot = robot
        self.priority = 90

    def update(self, distances):
        self.state.update_state(distances)
        translation, rotation = self.state.get_velocities(distances)
        self.robot.update(self, True, translation, rotation)
