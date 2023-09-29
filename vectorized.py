import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Acceleration due to gravity, m.s-2.
g = [0.0, -9.81]
# The maximum x-range of ball's trajectory to plot.
XMAX = 5
# The coefficient of restitution for bounces (-v_up/v_down).
cor = 0.65
# The time step for the animation.
dt = 0.005

# Initial position and velocity vectors.
init_pos = [0, 4]
init_vel = [1, 0]

def mul_s2v(scalar, vec):
    return [scalar * e for e in vec]

def add_vecs(vec1, vec2):
    return [x + y for x, y in zip(vec1, vec2)]

def get_pos(t=0):
    """A generator yielding the ball's position at time t."""
    pos = init_pos
    vel = init_vel
    while pos[0] < XMAX:
        pos = add_vecs(pos, mul_s2v(dt, vel))
        vel = add_vecs(vel, mul_s2v(dt, g))
        if pos[1] < 0:
            # bounce!
            pos[1] = 0
            vel[1] = -vel[1] * cor 
        yield pos

def init():
    """Initialize the animation figure."""
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, init_pos[1])
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
