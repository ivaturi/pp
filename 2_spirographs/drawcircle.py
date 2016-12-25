import math
import turtle


# Draw a circle using the turtle
def drawCircle(x, y, r):
    # move to the start of the circle
    turtle.up()
    turtle.setpos(x + r, y)
    turtle.down()

    # draw the circle
    for theta in xrange(0, 365, 5):
        a = math.radians(theta)
        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))


drawCircle(100, 100, 50)
turtle.mainloop()
