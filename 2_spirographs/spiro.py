import turtle
import math
from fractions import gcd


# A class that draws a spirograph
class Spiro:

    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        # Initialize internal parameters
        self.t = turtle.Turtle()         # create the Turtle object
        self.t.shape('turtle')           # set the shape of the cursor
        self.step = 5                    # set the step (in degrees)
        self.drawing_complete = False    # flag to indicate drawing is complete
        # set drawing parameters
        self.setParams(xc, yc, col, R, r, l)
        # initialize the drawing
        self.restart()

    # set parameters
    def setParams(self, xc, yc, col, R, r, l):
        # assign the spirograph parameters
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        # reduce r/R - divide the numerator and denominator by their GCD
        divisor = gcd(self.r, self.R)
        self.n_rotations = self.r//divisor

        # ratio of radii
        self.k = r/float(R)

        # set the color
        self.t.color(*col)

        # current angle
        self.theta = 0

    # compute x and y
    def _compute_xy(self, theta=0.0):
        R = self.R
        k = self.k
        l = self.l
        x = R * ((1-k)*math.cos(theta) + l*k*math.cos((1-k)*theta/k))
        y = R * ((1-k)*math.sin(theta) - l*k*math.sin((1-k)*theta/k))
        return x, y

    # restart the drawing
    def restart(self):
        self.drawing_complete = False     # drawing is not complete yet
        self.t.showturtle()               # show the turtle

        # navigate to the first point
        self.t.up()
        # compute parameters
        theta = 0.0
        x, y = self._compute_xy(theta)
        # Move the turtle to the first position, computed above
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    # draw the whole thing
    def draw(self):

        for i in xrange(0, 360 * self.n_rotations + 1, self.step):
            theta = math.radians(i)
            x, y = self._compute_xy(theta)
            self.t.setpos(self.xc+x, self.yc+y)

        # drawing is now done, so hide the turtle cursor
        self.t.hideturtle()

    # update the animation, step by step
    def update(self):
        # if drawing is complete, don't do anything
        if self.drawing_complete:
            return

        # increment the angle
        self.theta += self.step

        # draw a step
        theta = math.radians(self.theta)
        x, y = self._compute_xy(theta)
        self.t.setpos(self.xc+x, self.yc+y)

        # if the drawing is complete, set the flag
        if self.theta >= 360*self.n_rotations:
            self.drawing_complete = True
            self.t.hideturtle()
