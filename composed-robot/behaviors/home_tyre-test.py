from .home_tyre import HomeTyre
from .drive_free import DriveFree



class Robot:
    def __init__(self):
        pass
    
    def update(self,new_behavior, active, translation, rotation):
        print(new_behavior, active, translation, rotation)

home_tyre = HomeTyre(Robot())
drive_free = DriveFree(Robot())




home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 10,'y': 90})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
drive_free.update('distances')
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 10,'y': 90})
home_tyre.update({'x': 10,'y': 90})
home_tyre.update({'x': 10,'y': 90})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})
home_tyre.update({'x': 0,'y': 0})

