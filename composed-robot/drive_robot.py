from buildhat_alternative.buildhat import BuildHat
from buildhat_alternative.motor import Motor
from buildhat_alternative.robot import Robot
import time
import signal
import sys
from sshkeyboard import listen_keyboard

print("dont press anything yet we will let you know when we are ready to rock.....")

with (
    BuildHat() as buildhat,
    Motor("C", buildhat, -1) as left_motor,
    Motor("D", buildhat, 1) as right_motor,
):
    try:
        left_motor.add_listener(print)
        robot = Robot(left_motor, right_motor)

        print("ready to rock")
        print("keys are:")
        print("k=forward m=back z=left x=right")
        print("press SPACE TO STOP")

        def press(key):
            print(f"'{key}' pressed")
            if key == "k":
                robot.forward(200)
            if key == "m":
                robot.back()
            if key == "z":
                robot.left(220)
            if key == "x":
                robot.right(220)
            if key == "space":
                robot.pause()

        def release(key):
            print(f"'{key}' released")

        listen_keyboard(
            on_press=press,
            on_release=release,
        )
    except KeyboardInterrupt:
        print("you pressed control c")
