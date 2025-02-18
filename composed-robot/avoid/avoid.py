from .state import State,DriveFree
class Avoid:
    def __init__(self, robot):
        self.state = State()
        self.robot = robot

    def update(self, distances):
        self.state.update_state(distances)
        translation, rotation = self.state.get_velocities(distances)
        self.robot.set_velocities(translation, rotation)
        

        
