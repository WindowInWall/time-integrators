# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

g = [0, 9.81]

# Initial position, velocity, and acceleration vectors.
init_pos = [screen.get_width() / 2, 0]
init_vel = [0, 0]
init_acc = [0, 0]

# in milliCoulombs
charge_mouse = 0.1
charge_ball = 0.1

mass = 30
k = 1
d = 2
radius = 40
player_radius = 40

def mul_s2v(scalar, vec):
    return [scalar * e for e in vec]

def add_vecs(vec1, vec2):
    return [x + y for x, y in zip(vec1, vec2)]

def get_bounce(pos, m):
    acc = 10000
    
    XMAX, YMAX = pygame.display.get_surface().get_size()
    
    vec = [0, 0]

    if pos[0] < 0:
        vec = add_vecs(vec, [m * acc, 0.0])
    elif pos[0] > XMAX:
        vec = add_vecs(vec, [-m * acc, 0.0])

    if pos[1] < 0:
        vec = add_vecs(vec, [0.0, m * acc])
    elif pos[1] > YMAX:
        vec = add_vecs(vec, [0.0, -m * acc])

    return vec

def get_el_force_mag(mouse_pos, pos):
    return 9.0 * 10.0 ** 9.0 * charge_ball * charge_mouse / ((mouse_pos[0] - pos[0])**2 + (mouse_pos[1] - pos[1])**2)

def get_el_force(mouse_pos, pos):
    mag = get_el_force_mag(mouse_pos, pos)
    vecvec = add_vecs(pos, mul_s2v(-1, mouse_pos))
    dist = ((mouse_pos[0] - pos[0])**2 + (mouse_pos[1] - pos[1])**2) ** (1/2)
    
    vec_norm = mul_s2v(1.0 / dist, vecvec)
    return mul_s2v(mag, vec_norm)
    
def get_drag(vel):
    op_vel = mul_s2v(-1, vel)
    vel_mag = (op_vel[0] * op_vel[0] + op_vel[1] * op_vel[1]) ** (1 / 2)
    norm_op_vel = mul_s2v(1 / vel_mag, op_vel)

    # honey
    dyn_viscosity = 0.05
    drag_mag = 6 * math.pi * dyn_viscosity * radius * vel_mag
    return mul_s2v(drag_mag, norm_op_vel)

def get_force(pos, vel, m):
    gravity = mul_s2v(m, g)
    bounce = get_bounce(pos, m)
    el = get_el_force(list(pygame.mouse.get_pos()), pos)
    drag = get_drag(vel)
    return add_vecs(add_vecs(add_vecs(gravity, bounce), el), drag)
    #return add_vecs(add_vecs(gravity, bounce), el)

def get_acc(pos, vel, m):
    return mul_s2v(1/m, get_force(pos, vel, m))

def getNewVel(pos,vel, m):
    vec = mul_s2v(1 - ((k/m) * (dt**2)) + ((d/m) * dt), add_vecs(add_vecs(vel, mul_s2v(dt, g)), mul_s2v(k/m * dt, pos)))
    vec[0] = 0
    return vec

def get_pos():
    """A generator yielding the ball's position at time t."""
    pos = init_pos
    vel = init_vel
    #acc = init_acc
    while True:
        print(vel[1])
        new_vel = add_vecs(vel, getNewVel(pos, vel, mass))
        print(vel[0])
        new_pos = add_vecs(pos, mul_s2v(dt, vel))
        #new_acc = get_acc(new_pos, new_vel, mass)

        pos = new_pos
        vel = new_vel
        #acc = new_acc

        yield (pos[0], pos[1])

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
    particle_pos.x, particle_pos.y = next(gen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
