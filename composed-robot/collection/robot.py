from dotenv import load_dotenv
import os
import zmq
from robonet.Publisher import Publisher
import time
from .behaviors.home_tyre import HomeTyre

# PI_IP = os.getenv("PI_IP")


# publisher = Publisher(
#     PI_IP, f"tcp://{PI_IP}", "collection", topics=["robot-command"]
# )


# class Robot:
#     def __init__(self, publisher):
#         self.publisher = publisher
#         self.current_behavior = None
#         self.latched = None

#     def set_initial_behavior(self, behavior):
#         self.current_behavior = behavior
#         self.latched = True

#     def update(self, behavior, active, translation, rotation):
#         if behavior is self.current_behavior:
#             # new behavior is current behavior and new behavior is active
#             if active:
#                 return self.set_velocities(translation, rotation)
#             # new behavior is current behavior and new behavior is not active
#             else:
#                 self.latched = False
#                 self.set_velocities(translation, rotation)
#         elif active:
#              # new behavior is not current behavior and 
#              # new behavior is active
#              # and new behavior has higher priority than current behavior
#              #doesnt matter if latched or not because it has higher priority
#             if behavior.priority > self.current_behavior.priority:
#                 self.current_behavior = behavior
#                 print('changing behaviour to',behavior)
#                 self.latched = True
#                 self.set_velocities(translation, rotation)
#             if behavior.priority < self.current_behavior.priority and not self.latched:
#                 print('changing behaviour to', behavior)
#                 self.current_behavior = behavior
#                 self.latched = True
#                 self.set_velocities(translation, rotation)
                

#     def set_velocities(self, translation, rotation):
#         self.publisher.send_json(
#             "robot-command", {"translation": translation, "rotation": rotation}
#         )
        
        
class Unlatched:
    def __init__(self):
        self.priority = 0
    
class Robot:
    def __init__(self, publisher):
        self.publisher = publisher
        self.latched_behavior = Unlatched()
        
    def set_initial_behavior(self, behavior):
        self.latched_behavior = behavior
        
    def is_latched(self,new_behavior):
        return self.latched_behavior == new_behavior
    
        
    def update(self,new_behavior, active, translation, rotation):
        # if isinstance(new_behavior,HomeTyre):
        #     print(' we are homing now')
        #     print(new_behavior,new_behavior.priority,self.latched_behavior,self.latched_behavior.priority)
        if new_behavior.priority < self.latched_behavior.priority:
            #1
            return
        #notice we use early return making the bellow equivalent to
        # new_behavior.priority >= self.latched_behavior.priority
        if  (active):
            #3
            #priority greater than OR EQUAL TO previous behavior
            # and can be either latched or not latched
            # and is active
            if self.latched_behavior != new_behavior:
                print('latching',new_behavior)
                self.latched_behavior = new_behavior
            self.set_velocities(translation,rotation)
        if (not active and self.is_latched(new_behavior)):
            #2
            #priority greater than OR EQUAL TO previous behavior
            # and is latched
            # and is not active
            print('unlatching',new_behavior)
            self.latched_behavior=Unlatched()
            #should previous behavior set a velocity
            return
        
    def set_velocities(self, translation, rotation):
        self.publisher.send_json(
            "robot-command", {"translation": translation, "rotation": rotation}
        )
        
            
        


# robot = Robot(publisher)
