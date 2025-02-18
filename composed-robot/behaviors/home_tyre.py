import numpy as np
import math
from ..arbitration.behaviour import Behaviour


class HomeTyre(Behaviour):
    def __init__(self,name,arbiter,priority):
        super().__init__(name,arbiter,priority)
        self.previous_translation = None
        self.previous_rotation = None
        self.count = 0
        
    def _update(self,message):
        x = message['x']
        y = message['y']
        
        if not x and self.previous_rotation:
            if self.count<=5:
                print(self.count)
                
                self.count +=1
                return (True,self.previous_translation,self.previous_rotation)
                return
            elif self.count==6:
                result = (False,self.previous_translation,self.previous_rotation)
                self.previous_translation = None
                self.previous_rotation = None
                return result
        if (not x) and (not self.previous_rotation):
                return (False,self.previous_translation,self.previous_rotation)
        if x:
            self.count = 0

            #this converts from being w.r.t aruco marker to w.r.t robot frame
            #TODO not sure this is the best place to do this but i am hacking right now
            y = abs(y)+307
            theta = math.atan(x/y)
            v = np.array([x,y])
            distance = np.linalg.norm(v)
            
            max_rotation = 0.5
            translation = 200
            rotation = -(theta/(math.pi/2))
            self.previous_translation = translation
            self.previous_rotation = rotation
            return (True,translation,rotation)