from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
from robonet.Subscriber import Subscriber
from dotenv import load_dotenv
import os
import zmq
import numpy as np
import math

load_dotenv()

PI_IP = os.getenv("PI_IP")

context = zmq.Context()

subscriber = Subscriber(
    PI_IP,
    [
        {"node": "object_locator", "topic": "object_position"},
    ],
)

subscriber.start()

count = 0

    

        



with (
    BuildHat() as buildhat,
    Motor("C", buildhat, -1) as left_motor,
    Motor("D", buildhat, 1) as right_motor,
):
    try:
        #left_motor.add_listener(print)
        robot = Robot(left_motor, right_motor)
        print('after robot')
        
        for topic, node, message in subscriber.json_stream():
            print(message)
            count+=1
            x = message['x']
            y = message['y']
            #this converts from being w.r.t aruco marker to w.r.t robot frame
            #TODO not sure this is the best place to do this but i am hacking right now
            y = abs(y)+307
            theta = math.atan(x/y)
            v = np.array([x,y])
            distance = np.linalg.norm(v)
            
            max_rotation = 0.5
            translation = 200
            rotation = -(theta/(math.pi/2))
            #robot.set_velocities(translation,rotation)
        
            if count%15==0:
                print(x,y,theta,distance)
    

        
    except KeyboardInterrupt:
        print("you pressed control c")