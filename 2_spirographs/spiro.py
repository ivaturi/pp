import argparse
import math
import random
import turtle
from fractions import gcd


# A class that draws a spirograph
class Spiro:

    # constructor
    def __init__(self, xc, yc, col, R, r, l):
        """
        Spiro constructor  - initializes parameters and drawing
        """
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

    def clear(self):
        # clear everything
        self.t.clear()


# a class for animating spirographs
class SpiroAnimator:
    """
    The SpiroAnimator class lets us draw random spiros simultaneously.
    This class uses a timer to draw the curves one segment at a time; this
    technique updates the graphics periodically and lets the program process
    UI events.
    """
    # constructor
    def __init__(self, N):
        # set the time value (in milliseconds)
        self.delta_t = 10

        # get the dimensions of the window
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        # create the spiro objects, to draw with
        self.spiros = []
        for i in xrange(N):

            # Generate random parameters
            r_params = self.genRandomParams()
            spiro = Spiro(*r_params)
            self.spiros.append(spiro)

            # call the timer
            turtle.ontimer(self.update, self.delta_t)

    def genRandomParams(self):
        """
        Generate random parameters to initialize Spiros with
        """
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)

    def restart(self):
        """
        Restart the spiro drawing
        """
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro.setParams(*rparams)
            # restart drawing
            spiro.restart()

    def update(self):
        """
        Method called by the timer to update all spiros
        that are used in the animation
        """
        n_complete = 0
        # loop through the spiros and update each one
        for spiro in self.spiros:
            spiro.update()
            # count the number of completed spiros
            if spiro.drawing_complete:
                n_complete += 1
        # restart the drawing if all spiros are complete
        if n_complete == len(self.spiros):
            self.restart()
        # call the timer
        turtle.ontimer(self.update, self. delta_t)

    def toggleTurtles(self):
        """
        Toggle turles on and off.
        Toggling them off makes the drawing go faster
        """
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


def main():
    """
    The main entry point
    """
    print("Generating spirograph...")
    # create a parser
    descr = """This program draws Spirographs using the Turtle module.
When run with no arguments, this program draws random spirographs.

Terminology:

R - radius of the outer circle
r - radius of the inner circle
l - ration of hole distance to r
"""
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument('--sparams',
                        nargs=3,
                        required=False,
                        help="The three arguments in sparams: R, r, l.")

    # parse args
    args = parser.parse_args()

    # Basic turtle setup
    turtle.setup(width=0.5)
    turtle.shape('turtle')
    turtle.title("Spirographs!")
    turtle.listen()

    turtle.hideturtle()

    # check for any arguments sent to --sparams
    if args.sparams:
        params = map(float, args.sparams)
        # draw with the given params
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create the animator object
        spiro_anim = SpiroAnimator(4)
        # add a key handler to toggle the turtle cursor
        turtle.onkey(spiro_anim.toggleTurtles, "t")
        # add a key handler to restart the animation
        turtle.onkey(spiro_anim.restart, "space")

    # start the main loop
    turtle.mainloop()


# call main
if __name__ == "__main__":
    main()
