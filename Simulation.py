import pygame
import math
from colors import WHITE, RED, BLUE, YELLOW, GREY, ORANGE

pygame.init()

WIDTH, HEIGHT = 1280, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")
FONT = pygame.font.SysFont("comicsans", 16)


class Planet:

    AU = 149.6e6 * 1000  # Astronomical Unit
    G = 6.67408e-11  # Gravitational Constant
    SCALE = 250/AU  # To convert it to pixels i.e: 1AU = 100 pixels
    TIMESTEP = 3600*24  # One day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun/1000, 1)} km", 1, WHITE)
            win.blit(distance_text, (x-distance_text.get_width() /
                     2, y-distance_text.get_height()/2))

    def force_of_attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.force_of_attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))


# Event Loop


def main():
    run = True
    clock = pygame.time.Clock()  # To set the FPS

    sun = Planet(0, 0, 30, YELLOW, 1.98892*10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16,  BLUE, 5.9742*10**24)
    earth.y_vel = 29.8 * 1000

    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_vel = 24.1 * 1000

    mercury = Planet(0.387*Planet.AU, 0, 8, GREY, 3.30*10**23)
    mercury.y_vel = -47.9 * 1000

    venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    venus.y_vel = -35.0 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WINDOW.fill((0, 0, 0))
        # pygame.display.update()  # Mention this to update the backgroud
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


main()
