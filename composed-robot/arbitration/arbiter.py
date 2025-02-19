class Arbiter:
    def __init__(self,update_function):
        self.behaviours = []
        self.update = update_function
        self.previous_priority_behaviour = None
        
    def add_behaviour(self,behaviour):
        self.behaviours.append(behaviour)
        self.behaviours = sorted(self.behaviours,key=lambda x: x.priority,reverse=True)
        
    def get_behaviours_wanting_control(self):
        return [b.name for b in self.behaviours if b.wants_control == True]
    
    def log_behaviour_taking_control(self,behaviour_asking_for_control,behaviour):
        if (behaviour_asking_for_control != self.previous_priority_behaviour):
                    print('behaviour: ',behaviour_asking_for_control.name,' taking control')
            
    def ask_for_control(self,behaviour_asking_for_control):
        for behaviour in self.behaviours:
            # if we encounter the behaviour that wants control before we encounter a behaviour that has control then the behaviour that wants control should be given priority
            if behaviour_asking_for_control == behaviour:
                self.log_behaviour_taking_control(behaviour_asking_for_control,behaviour)
                self.previous_priority_behaviour = behaviour_asking_for_control
                return True
            # if we encounter a behaviour that has control before we encounter the behaviour that wants control then the behaviour that wants control should not be given priority.
            elif behaviour.wants_control ==True:
                return False