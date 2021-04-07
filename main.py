import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("TkAgg")


class ParticleBox:
    """Orbits class

    init_state is an [N x 4] array, where N is the number of particles:
       [[x1, y1, vx1, vy1],
        [x2, y2, vx2, vy2],
        ...               ]
    """

    def __init__(self,
                 init_state=None,
                 size=0.04):
        # Defaults to 3 particles with these positions/velocities if none are specified upon the initialization of a
        # ParticleBox instance.
        if init_state is None:
            init_state = [[1, 0, 0, -1],
                          [-0.5, 0.5, 0.5, 0.5],
                          [-0.5, -0.5, -0.5, 0.5]]
        self.init_state = np.asarray(init_state, dtype=float)
        self.size = size
        self.state = self.init_state.copy()  # A list of all particle's positions and velocities.
        self.time_elapsed = 0
        self.bounds = [-2, 2, -2, 2]  # Size of the box. Should be formatted as [xmin, xmax, ymin, ymax]

    def step(self, dt):
        """step once by dt seconds"""
        self.time_elapsed += dt

        # Update positions by adding the particle's velocity to their position.
        self.state[:, :2] += dt * self.state[:, 2:]

        # Check for crossing boundary and create four arrays with boolean values for each particle that signify if a
        # particle has crossed a boundary.
        crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
        crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
        crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
        crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

        # Sets the position of all particles that are over a given boundary to just inside the boundary.
        self.state[crossed_x1, 0] = self.bounds[0] + self.size
        self.state[crossed_x2, 0] = self.bounds[1] - self.size
        self.state[crossed_y1, 1] = self.bounds[2] + self.size
        self.state[crossed_y2, 1] = self.bounds[3] - self.size

        # Reverses the velocity of all particles that are over a given boundary.
        self.state[crossed_x1 | crossed_x2, 2] *= -1
        self.state[crossed_y1 | crossed_y2, 3] *= -1


# Set up the initial state.

np.random.seed(5)
# A 50 X 4 array filled with random numbers from -0.5 to 0.5. This
# represents 50 particles with starting positions and velocities as 4 values generated randomly.
init_state = -0.5 + np.random.random((50, 4))
init_state[:, :2] *= 3.9  # Multiply the positions of the particles by 4 so they're evenly spread through the box.

box = ParticleBox(init_state, size=0.04)
dt = 1. / 30  # 30fps

# Set up figure. Basically just makes the window and visual scaling properties.
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-3.2, 3.2), ylim=(-3.2, 3.2))

# The particles variable holds the locations of the particles.
# The 'bo' parameter is the color and type of marker. This one means the particles will be represented as blue circles.
# The ms parameter is the marker size.
particles, = ax.plot([], [], 'bo', ms=6)

# rect is the box edge
rect = plt.Rectangle(box.bounds[::2],
                     box.bounds[1] - box.bounds[0],
                     box.bounds[3] - box.bounds[2],
                     ec='none', lw=2, fc='none')
ax.add_patch(rect)


def init():
    """initialize animation"""
    global box, rect
    particles.set_data([], [])
    rect.set_edgecolor('none')
    return particles, rect


def animate(i):
    """perform animation step"""
    global box, rect, dt, ax, fig
    box.step(dt)

    ms = int(fig.dpi * 2 * box.size * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])

    # update pieces of the animation
    rect.set_edgecolor('k')
    particles.set_data(box.state[:, 0], box.state[:, 1])
    particles.set_markersize(ms)
    return particles, rect


ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)
plt.show()
