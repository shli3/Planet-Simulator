import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation") #Window name

#Colours
BLACK = (0, 0, 0)
SUN_YELLOW = (254, 217, 54)
EARTH_BLUE = (8, 23, 57)
MERCURY_GRAY = (141, 152, 181)
VENUS = (196, 163, 105)
MARS = (209, 128, 53)
JUPITER = (219, 206, 178)
# INNER_SATURN = (194, 182, 121)
# OUTER_SATURN = (43, 41, 29)
# URANUS_SOFT_BLUE = (209, 247, 250)
# NEPTUNE_DEEP_BLUE = (66, 118, 253)
# BROWN_PLUTO = (200, 155, 125)

# For simplicity sake, will include the sun as a planet even though it's a star
class Planet:
    AU = 149.6e6 * 1000 #Astronomical Unit (distance from Earth to Sun approximately) converted to metres
    G = 6.67428e-11
    SCALE = 62.5 / AU #1AU = 75 pixels
    TIMESTEP = 3600 * 24 #1 day

    def __init__(self, x, y, r, colour, mass):
        self.x = x
        self.y = y
        self.r = r #radius of the planet
        self.colour = colour
        self.mass = mass

        self.orbit = []
        self.sun = False #draw orbit if not sun
        self.SunDistance = 0

        self.xVelo = 0
        self.yVelo = 0

    def draw(self, TargetWindow):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(TargetWindow, self.colour, False, updated_points, 2)

        pygame.draw.circle(TargetWindow, self.colour, (x, y), self.r)

    def attraction(self, OtherPlanet):
        otherx, othery = OtherPlanet.x, OtherPlanet.y
        Xdistance = otherx - self.x
        Ydistance = othery - self.y
        distance = math.sqrt(Xdistance ** 2 + Ydistance ** 2)

        if OtherPlanet.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * OtherPlanet.mass / distance ** 2 # F = G(m1)(m2)/distance^2
        theta = math.atan2(Ydistance, Xdistance) 
        Xforce = math.cos(theta) * force
        Yforce = math.sin(theta) * force
        return Xforce, Yforce

    def update_pos(self, planets):
        TotalXforce = TotalYforce = 0

        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            TotalXforce += fx
            TotalYforce += fy

        self.xVelo += TotalXforce / self.mass * self.TIMESTEP
        self.yVelo += TotalYforce / self.mass * self.TIMESTEP

        self.x += self.xVelo * self.TIMESTEP
        self.y += self.yVelo * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    running = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 20, SUN_YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(1 * Planet.AU, 0, 10, EARTH_BLUE, 5.9724 * 10**24)
    mercury = Planet(-0.4 * Planet.AU, 0, 4, MERCURY_GRAY, 3.285 * 10**23)
    venus = Planet(-0.7 * Planet.AU, 0, 9.5, VENUS, 4.867 * 10**24)
    mars = Planet(-1.5 * Planet.AU, 0, 5, MARS, 6.39 * 10**23)
    jupiter = Planet(5.2 * Planet.AU, 0, 15, JUPITER, 1.898 * 10**27)

    earth.yVelo = -29.783 * 1000
    mercury.yVelo = 47.4 * 1000
    venus.yVelo = 35.02 * 1000
    mars.yVelo = 24.077 * 1000
    jupiter.yVelo = -13.06 * 1000
    # multiply by 1000 to get m/s


    # CUT PLANETS (DIDNT FIT IN THE SCALE) #
    # saturn = Planet(9.5 * Planet.AU, 0, 19, INNER_SATURN, 5.683 * 10**26)
    # SaturnRing = Planet(9.5 * Planet.AU, 0, 24, OUTER_SATURN, 5.683 * 10**26)
    # uranus = Planet(19.8 * Planet.AU, 0, 15, URANUS_SOFT_BLUE, 8.681 * 10**25)
    # neptune = Planet(30 * Planet.AU, 0, 14, NEPTUNE_DEEP_BLUE, 1.024 * 10**26)
    # pluto = Planet(39 * Planet.AU, 0 , 2, BROWN_PLUTO, 1.30900 * 10**22) #they did Pluto dirty
    # CUT PLANETS (DIDNT FIT IN THE SCALE) #

    planets = [sun, earth, mercury, venus, mars, jupiter] 
    while running:                  #Equivalent to Update() in C# Unity
        clock.tick(60)              #60FPS
        Window.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(Window)

        pygame.display.update()

    pygame.quit()

main()