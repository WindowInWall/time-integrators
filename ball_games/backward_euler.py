# Example file showing a circle moving on screen
import pygame
import math
import numpy as np

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = clock.tick(60) / 1000
g = [0, 9.81]

# Initial position, velocity, and acceleration vectors.
init_pos = [screen.get_width() / 2, 0]
init_vel = [0, 0]
init_acc = [0, 0]
d = 0
w = 10
init_x = np.array([500, 0])
A = np.array([[0, 1],
              [-w**2, -2 * d * w]])
print(A.shape)

# in milliCoulombs
charge_mouse = 0.1
charge_ball = 0.1

mass = 30
k = 1
d = 2
radius = 40
player_radius = 40

def get_pos():
    """A generator yielding the ball's position at time t."""
    print('should be zero:')
    x = init_x
    while True:
        x = np.linalg.pinv(np.eye(2) - A.dot(dt)).dot(x)
        yield x[0]

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
particle_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 2)

gen = get_pos()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, player_radius)
    pygame.draw.circle(screen, "blue", particle_pos, radius)

    player_pos.x, player_pos.y = pygame.mouse.get_pos()
    particle_pos.x = next(gen) + screen.get_width() / 2
    particle_pos.y = screen.get_height() / 2

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
