from .state import State,DriveFree
from ..arbitration.behaviour import Behaviour


class Avoid(Behaviour):
    def __init__(self,name,arbiter,priority):
        super().__init__(name,arbiter,priority)
        self.state = State()

    def _update(self, distances):
        self.state.update_state(distances)
        translation, rotation = self.state.get_velocities(distances)
        if isinstance(self.state.state,DriveFree):
            return False,translation,rotation
        return True,translation,rotation
            
        
