import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Acceleration due to gravity, m.s-2.
g = [0.0, -9.81]
# The maximum x-range of ball's trajectory to plot.
XMAX = 5
# The maximum y-range of ball's trajectory to plot.
YMAX = 5
# The coefficient of restitution for bounces (-v_up/v_down).
cor = 0.65
# The time step for the animation.
dt = 0.005

# Initial position, velocity, and acceleration vectors.
init_pos = [0, 4]
init_vel = [1, 0]
init_acc = [0, 0]

mass = 1

def mul_s2v(scalar, vec):
    return [scalar * e for e in vec]

def add_vecs(vec1, vec2):
    return [x + y for x, y in zip(vec1, vec2)]

def get_bounce(pos, m):
    acc = 100

    if pos[0] < 0:
        return [m * acc, 0.0]
    elif pos[0] > XMAX:
        return [-m * acc, 0.0]

    if pos[1] < 0:
        return [0.0, m * acc]
    elif pos[1] > YMAX:
        return [0.0, -m * acc]

    return [0, 0]

def get_force(pos, m):
    gravity = mul_s2v(m, g)
    bounce = get_bounce(pos, m)
    return add_vecs(gravity, bounce)

def get_acc(pos, m):
    return mul_s2v(1/m, get_force(pos, m))

def get_pos(t=0):
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

        yield pos

def init():
    """Initialize the animation figure."""
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, YMAX)
    ax.set_xlabel('$x$ /m')
    ax.set_ylabel('$y$ /m')
    line.set_data(xdata, ydata)
    ball.set_center((init_pos[0], init_pos[1]))
    height_text.set_text(f'Height: {init_pos[1]:.1f} m')
    return line, ball, height_text

def animate(pos):
    """For each frame, advance the animation to the new position, pos."""
    x, y = pos
    xdata.append(x)
    ydata.append(y)
    line.set_data(xdata, ydata)
    ball.set_center((x, y))
    height_text.set_text(f'Height: {y:.1f} m')
    return line, ball, height_text

# Set up a new Figure, with equal aspect ratio so the ball appears round.
fig, ax = plt.subplots()
ax.set_aspect('equal')

# These are the objects we need to keep track of.
line, = ax.plot([], [], lw=2)
ball = plt.Circle((init_pos[0], init_pos[1]), 0.08)
height_text = ax.text(XMAX*0.5, init_pos[1]*0.8, f'Height: {init_pos[1]:.1f} m')
ax.add_patch(ball)
xdata, ydata = [], []

interval = 1000*dt
ani = animation.FuncAnimation(fig, animate, get_pos, blit=True,
                      interval=interval, repeat=False, init_func=init, cache_frame_data=False)
plt.show()
