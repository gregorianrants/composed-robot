from ..behaviors import avoid,drive_free,home_tyre
from .arbiter import Arbiter

def update_function(translation,rotation):
    print(translation,rotation)

arbiter = Arbiter(update_function)



home_tyre = home_tyre.HomeTyre('home_tyre',arbiter,priority=50)
avoid = avoid.Avoid('avoid',arbiter,priority=20)
drive_free = drive_free.DriveFree('drive_free',arbiter,priority=10)

dont_avoid = [20,20,20,20,20]
do_avoid = [100,100,20,20,20]
tyre_seen = {'x': 20, 'y': 20}

drive_free.update([20,20,20,20,20])
print(arbiter.get_priority_behaviours())
avoid.update([100,100,20,20,20])
print(arbiter.get_priority_behaviours())
avoid.update([20,20,20,20,20])
drive_free.update([20,20,20,20,20])
print(arbiter.get_priority_behaviours())