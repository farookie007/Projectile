#file: animation.py
from graphics import *
from button import Button
from projectile import Projectile
from math import sin, cos, radians, degrees
from random import randint


class ShotTracker:
    def __init__(self, win, angle, velocity, height):
        """win is the GraphWin to display the shot. angle, velocity,
        and height are initial projectile parameters."""

        self.proj = Projectile(angle, velocity, height)
        self.marker = Circle(Point(0,height), 3)
        self.marker.setFill('green2')
        self.marker.setOutline('green2')
        self.marker.draw(win)

    def update(self, dt):
        """ Move the shot dt seconds farther along its flight."""

        # update the projectile
        self.proj.update(dt)

        # move the circle to the new projectile location
        center = self.marker.getCenter()
        dx = self.proj.getX() - center.getX()
        dy = self.proj.getY() - center.getY()
        self.marker.move(dx,dy)

    def getX(self):
        "Return the current x coordinate of the shot's center."
        return self.proj.getX()

    def getY(self):
        "Return the current y coordinate of the shot's center."
        return self.proj.getY()

    def undraw(self):
        "Undraw the shot."
        self.marker.undraw()

class InputDialog:
    """A custom window for getting simulation values (angle, velocity,
    and height) from the user."""

    def __init__(self, angle, vel, height):
        "Build and display the input window"

        self.win = win = GraphWin("Initial Values", 200, 300)
        win.setCoords(0,4.5, 4,.5)

        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))

        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))

        Text(Point(1,3), "Height").draw(win)
        self.height = Entry(Point(3,3), 5).draw(win)
        self.height.setText(str(height))

        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()

        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()
    def interact(self):
        """ Wait for user to click Quit or Fire button
        Returns a string indicating which button was clicked"""

        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        "Return input values"
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        h = float(self.height.getText())
        return a, v, h

    def close(self):
        "Close the input window."
        self.win.close()


class Launcher:

    def __init__(self, win):
        # draw the base shot of the launcher
        self.base = Circle(Point(0,0), 3)
        self.base.setFill("red")
        self.base.setOutline("red")
        self.base.draw(win)

        # save the window and create initial angle and velocity
        self.win = win
        self.angle = radians(45.0)
        self.vel = 40.0
        self.height = 0.0

        # create initial "dummy" arrow (needed by redraw)
        self.arrow = Line(Point(0,0), Point(0,0)).draw(win)

        # create initial target to shoot at
        self.center = Point(200, 10)
        self.target = Button(self.win, self.center, 10, 20, '')
        self.target.activate()

        # replace it with the correct arrow
        self.redraw()

    def adjAngle(self, amt):
        """Change launch angle by amt degrees."""

        self.angle += radians(amt)
        self.redraw()

    def adjVel(self, amt):
        """Change launch velocity by amt."""

        self.vel += amt
        self.redraw()

    def adjHeight(self, amt):
        """Change launch height by amt."""

        self.height += amt
        self.redraw()

    def drawTarget(self):
        """Erases and redraw a Target on the graphical window."""
        self.target.undraw()
        self.center = Point(randint(100,200), randint(0,145))
        self.target = Button(self.win, self.center, 10, 20, '')
        self.target.activate()


    def redraw(self):
        """Redraw the arrow to show current angle and velocity and also adjust the height of the ball."""

        self.arrow.undraw()
        self.base.undraw()
        pt2 = Point(self.vel*cos(self.angle),
            (self.vel*sin(self.angle)+self.height))
        self.arrow = Line(Point(0,self.height), pt2).draw(self.win)
        self.arrow.setArrow('last')
        self.arrow.setWidth(4)
        self.base = Circle(Point(0,self.height),3)
        self.base.setFill("red")
        self.base.setOutline("red")
        self.base.draw(self.win)



    def fire(self):
        """Returns a ShotTracker object for the projectile."""
        return ShotTracker(self.win, degrees(self.angle), self.vel, self.height)

class ProjectileApp:

    def __init__(self):
        #create graphics window with a scale line at the bottom
        self.win = GraphWin("Projectile", 640, 480)
        self.win.setCoords(-10, -10, 210, 155)
        Line(Point(-10,0), Point(210,0).draw(self.win))
        for x in range(0, 210, 50):
            Text(Point(x,-7), str(x)).draw(self.win)
            Line(Point(x,0), Point(x,2)).draw(self.win)

        #add the launcher to the window
        self.launcher = Launcher(self.win)

        #start withh an empty list of "live" shots
        self.shots = []

    def hit(self):
        for shot in self.shots:
            pt = Point(shot.getX(), shot.getY())
            if self.launcher.target.clicked(pt):
                shot.undraw()
                return True


    def run(self):

        # main event/animation loop
        while True:
            self.updateShots(1/30)

            key = self.win.checkKey()
            if key in ["q", "Q"]:
                break

            if key == "Up":
                self.launcher.adjAngle(5)
            elif key == "Down":
                self.launcher.adjAngle(-5)
            elif key == "Right":
                self.launcher.adjVel(5)
            elif key == "Left":
                self.launcher.adjVel(-5)
            elif key == "equal":
                self.launcher.adjHeight(+5)
            elif key == "minus":
                self.launcher.adjHeight(-5)
            elif key in ["f", "F"]:
                self.shots.append(self.launcher.fire())

            if self.hit():
                self.launcher.target.deactivate()
                self.launcher.target.undraw()
                self.launcher.drawTarget()





            update(30)

        self.win.close()

    def updateShots(self, dt):
        alive = []
        for shot in self.shots:
            shot.update(dt)
            if shot.getY() >= 0 and -10 < shot.getX() <210:
                alive.append(shot)
            else:
                shot.undraw()
        self.shots = alive
