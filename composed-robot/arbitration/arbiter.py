class Arbiter:
    def __init__(self,update_function):
        self.behaviours = []
        self.update = update_function
        
    def add_behaviour(self,behaviour):
        self.behaviours.append(behaviour)
        self.behaviours = sorted(self.behaviours,key=lambda x: x.priority,reverse=True)
        
        
    def ask_for_control(self,behaviour_asking_for_control):
        for behaviour in self.behaviours:
            # if we encounter the behaviour that wants control before we encounter a behaviour that has control then the behaviour that wants control should be given priority
            if behaviour_asking_for_control == behaviour:
                return True
            # if we encounter a behaviour that has control before we encounter the behaviour that wants control then the behaviour that wants control should not be given priority.
            elif behaviour.has_control ==True:
                return False