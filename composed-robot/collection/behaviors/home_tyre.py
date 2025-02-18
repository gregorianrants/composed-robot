import numpy as np
import math

class HomeTyre():
    def __init__(self,robot):
        self.robot = robot
        self.priority = 100
        self.previous_translation = None
        self.previous_rotation = None
        self.count = 0
        
    def update(self,message):
        x = message['x']
        y = message['y']
        
        if not x and self.previous_rotation:
            if self.count<=5:
                print(self.count)
                self.robot.update(self,True,self.previous_translation
                                ,self.previous_rotation)
                self.count +=1
                return
            elif self.count==6:
                self.robot.update(self,False,self.previous_translation
                                ,self.previous_rotation)
                self.previous_translation = None
                self.previous_rotation = None
                return
            else:
                return
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
            self.robot.update(self,True,translation,rotation)