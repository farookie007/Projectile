#projectile.py
"""projectile.py
Provides a simple class for modeling the
flight of projectiles."""

from math import sin, cos, radians


class Projectile:
    """Simulates the flight of simple projectile near the earth's
    surface ignoring wind resistance. Tracking is done in two
    dimensions, height (y) and distance (x)."""

    def __init__(self, angle, velocity, height):
        """Create a projectile with given launch angle, initial
        velocity and height."""
        self.xpos = 0.0
        self.ypos = height
        theta = radians(angle)
        self.xvel = velocity * cos(theta)
        self.yvel = velocity * sin(theta)

    def update(self, time):
        """Update the state of this projectile to move it time seconds
        farther into its flight."""
        self.xpos += (time*self.xvel)
        yvel1 = self.yvel - (9.8 * time)
        self.ypos += (time * (self.yvel+yvel1) / 2.0)
        self.yvel = yvel1

    def getY(self):
        "Returns the y position (height) of this projectile."
        return self.ypos

    def getX(self):
        "Returns the x position (distance) of this projectile."
        return self.xpos

    def maxHeight(self):
        "Returns the maximum height of the projectile."
        maxHeight = 0
        time = 1
        while self.ypos > 0:
            self.update(time)
            if float(self.ypos) >= self.ypos:
                maxHeight = float(self.ypos)
            time += .01
        return maxHeight
