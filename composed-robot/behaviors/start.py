from ..arbitration.behaviour import Behaviour

class Start(Behaviour):
    def __init__(self,name,arbiter,priority):
        super().__init__(name,arbiter,priority)
        self.count = 1
        

    def update(self, left_motor_data):
        if self.count < 6:
            print(f"lift off in {6-self.count}")
            self.count += 1
            return self._update(True, 0, 0)
        if self.count == 6:
            self.count +=1
            return self._update(False, 0, 0)
        return self._update(False, 0, 0)
            
