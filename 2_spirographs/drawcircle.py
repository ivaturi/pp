import argparse
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


def main():
    # create a parser
    descr = "This program draws a circle using turtle"
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument(type=int, nargs=3, dest='params')

    args = parser.parse_args()
    print args
    drawCircle(args.params[0], args.params[1], args.params[2])
    turtle.mainloop()


if __name__ == "__main__":
    main()
