from .state import State,DriveFree
# we are importing the state class drive free dont mix it up with the behaviour drive free

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
        #this is different from the stand alone version of avoid as the stand alone behaviour gives velocities this version leaves it to a another behaviour 
        if isinstance(self.state.state,DriveFree):
            self.robot.update(self, False, translation, rotation)
            return
        self.robot.update(self, True, translation, rotation)
            
        
