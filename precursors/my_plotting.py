import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Acceleration due to gravity, m.s-2.
g = 9.81
# The maximum x-range of ball's trajectory to plot.
XMAX = 5
# The maximum y-range of ball's trajectory to plot.
YMAX = 4
# The coefficient of restitution for bounces (-v_up/v_down).
cor = 0.85
# The time step for the animation.
dt = 100

# Initial position and velocity vectors.
x0, y0 = 0, 4
vx0, vy0 = 1, 0

def sum_forces(x, y, mass):
    force_grav = list(map(lambda x: mass * x, g))
    summed_forces =

def get_pos(t=0):
    """A generator yielding the ball's position at time t."""
    x, y, vx, vy = x0, y0, vx0, vy0
    while True:
        f = m * g;
        t += dt
        x += vx * dt
        y += vy * dt
        vy -= g * dt

        # adjusting y in case of collision
        if y < 0:
            y = 0
            vy = -vy * cor
        elif y > YMAX:
            y = YMAX
            vy = -vy * cor

        # adjusting x in case of collision
        if x < 0:
            x = 0
            vx = -vx * cor
        elif x > XMAX:
            x = XMAX
            vx = -vx * cor
        yield x, y
        

def init():
    """Initialize the animation figure."""
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, YMAX)
    ax.set_xlabel('$x$ /m')
    ax.set_ylabel('$y$ /m')
    line.set_data(xdata, ydata)
    ball.set_center((x0, y0))
    height_text.set_text(f'Height: {y0:.1f} m')
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
ball = plt.Circle((x0, y0), 0.08)
height_text = ax.text(XMAX*0.5, y0*0.8, f'Height: {y0:.1f} m')
ax.add_patch(ball)
xdata, ydata = [], []

interval = 1000*dt
ani = animation.FuncAnimation(fig, animate, get_pos, blit=True,
                      interval=interval, repeat=False, init_func=init)
plt.show()
