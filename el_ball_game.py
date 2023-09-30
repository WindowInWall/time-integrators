# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

g = [0.0, 9.81]

# Initial position, velocity, and acceleration vectors.
init_pos = [0, 4]
init_vel = [300, 100]
init_acc = [0, 0]
charge_mouse = 0.1
charge_ball = 0.1

mass = 30

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
    return 9.0 * 10**9 * charge_ball * charge_mouse / ((mouse_pos[0] - pos[0])**2 + (mouse_pos[1] - pos[1])**2)

def get_el_force(mouse_pos, pos):
    mag = get_el_force_mag(mouse_pos, pos)
    vecvec = add_vecs(pos, mul_s2v(-1, mouse_pos))
    dist = ((mouse_pos[0] - pos[0])**2 + (mouse_pos[1] - pos[1])**2) ** (1/2)
    
    vec_norm = mul_s2v(1.0 / dist, vecvec)
    return mul_s2v(mag, vec_norm)
    

def get_force(pos, m):
    gravity = mul_s2v(m, g)
    bounce = get_bounce(pos, m)
    el = get_el_force(list(pygame.mouse.get_pos()), pos)
    return add_vecs(add_vecs(gravity, bounce), el)
    #return add_vecs(gravity, bounce)


def get_acc(pos, m):
    return mul_s2v(1/m, get_force(pos, m))

def get_pos():
    """A generator yielding the ball's position at time t."""
    pos = init_pos
    vel = init_vel
    acc = init_acc
    while True:
        half_new_vel = add_vecs(vel, mul_s2v(0.5 * dt, acc))
        new_pos = add_vecs(pos, mul_s2v(dt, half_new_vel))
        new_acc = get_acc(new_pos, mass)
        new_vel = add_vecs(half_new_vel, mul_s2v(0.5 * dt, new_acc))

        pos = new_pos
        vel = new_vel
        acc = new_acc
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

    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.circle(screen, "blue", particle_pos, 40)

    (x, y) = pygame.mouse.get_pos()
    player_pos.x = x
    player_pos.y = y
    
    (pp_x, pp_y) = next(gen)
    particle_pos.x = pp_x
    particle_pos.y = pp_y
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    """

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()