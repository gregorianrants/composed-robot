from ..behaviors import avoid,drive_free,home_tyre
from .arbiter import Arbiter

def update_function(translation,rotation):
    #print(translation,rotation)
    pass

arbiter = Arbiter(update_function)



home_tyre = home_tyre.HomeTyre('home_tyre',arbiter,priority=50)
avoid = avoid.Avoid('avoid',arbiter,priority=20)
drive_free = drive_free.DriveFree('drive_free',arbiter,priority=10)

dont_avoid = [100,100,100,100,100]
do_avoid = [20,20,20,20,20]
tyre_seen = {'x': 20, 'y': 20}
tyre_not_seen = {'x': False, 'y': False}

print('_____________')
avoid.update(dont_avoid)
drive_free.update(dont_avoid)

print('_____________')
avoid.update(do_avoid)
drive_free.update(do_avoid)

print('_____________')
avoid.update(dont_avoid)
drive_free.update(dont_avoid)

home_tyre.update(tyre_seen)
avoid.update(do_avoid)
drive_free.update(do_avoid)




home_tyre.update(tyre_seen)
home_tyre.update(tyre_not_seen)
home_tyre.update(tyre_not_seen)
home_tyre.update(tyre_not_seen)
home_tyre.update(tyre_not_seen)
home_tyre.update(tyre_not_seen)
home_tyre.update(tyre_not_seen)
home_tyre.update(tyre_not_seen)


avoid.update(do_avoid)
drive_free.update(do_avoid)

