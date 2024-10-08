import math


class Odometry:
    def __init__(self):
        self.lastLeftPosition = None
        self.lastRightPosition = None
        self.x = 0
        self.y = 0
        self.theta = 0
        self.dl = None
        self.dr = None
        self.DISTANCE_BETWEEN_WHEELS = 176  # mm

    def updateAbsolutePosition(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def updatePosition(self):
        dTheta = (self.dr - self.dl) / self.DISTANCE_BETWEEN_WHEELS
        self.theta = self.theta + dTheta
        dc = (self.dl + self.dr) / 2
        self.x = self.x - dc * math.sin(self.theta)
        self.y = self.y + dc * math.cos(self.theta)

    def updateLeft(self, pos):
        pos = (pos / 360) * 276.401 * -1  # convert to mm
        if not self.lastLeftPosition:
            self.lastLeftPosition = pos
            return
        self.dl = pos - self.lastLeftPosition
        self.lastLeftPosition = pos
        self.dr = 0
        self.updatePosition()

    def updateRight(self, pos):
        pos = (pos / 360) * 276.401
        if not self.lastRightPosition:
            self.lastRightPosition = pos
            return
        self.dr = pos - self.lastRightPosition
        self.lastRightPosition = pos
        self.dl = 0
        self.updatePosition()
