class Behaviour:
    def __init__(self,name,arbiter,priority):
        self.name = name
        self.wants_control = False
        self.priority = priority
        self.arbiter = arbiter
        arbiter.add_behaviour(self)
    
        
    def update(self,message):
        wants_control,translation,rotation = self._update(message)
        if not wants_control:
            self.wants_control = False
            return
        if self.arbiter.ask_for_control(self):
            if(not self.wants_control): print(self.name,'taking control')
            self.wants_control = True
            self.arbiter.update(translation,rotation)
            
class Behaviour:
    def __init__(self,name,arbiter,priority):
        self.name = name
        self.wants_control = False
        self.priority = priority
        self.arbiter = arbiter
        arbiter.add_behaviour(self)
    
        
    def _update(self,wants_control,translation,rotation):
        if not wants_control:
            self.wants_control = False
            return
        if self.arbiter.ask_for_control(self):
            if(not self.wants_control): print(self.name,'taking control')
            self.wants_control = True
            self.arbiter.update(translation,rotation)