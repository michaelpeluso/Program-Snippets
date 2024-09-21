# import libraries
import glfw
from OpenGL.GL import *
import math
import random
import time


# init global variables
window = None
window_size = 500
cell_size = 10
timestep = 0.025

particles = []
particleCount = 300
particle_radius = 4

gravity_constant = 9.81
friction_coefficient = 0.5  # 0 = no friction
bounce_constant = 1  # 1 = no speed lost on bounce; 0 = lose all velocity

optimize = True # used spacial hash
pass_through = False  # pass through walls
use_gravity = True # turn on/off gravity

def key_callback(window, key, scancode, action, mods) :
    if action == glfw.PRESS :
        if key == glfw.KEY_ESCAPE :
            glfw.set_window_should_close(window, True)


if not glfw.init() :
    exit()


window = glfw.create_window(window_size, window_size, "mq72 - HW3, Question 1", None, None)
if not window :
    glfw.terminate()
    exit()

glfw.make_context_current(window)
glfw.set_key_callback(window, key_callback)


def normalize(x) :
    global window_size
    x = x / window_size * 2
    return x


def random_direction() :
    angle = random.uniform(0, 2 * math.pi)
    x = math.cos(angle)
    y = math.sin(angle)
    return x, y


def get_distance(coords1, coords2) :
    return math.sqrt((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2)


class Particle :
    def __init__(self, coords : tuple[int, int], radius=particle_radius, edges=25) :
        self.coords = (normalize(coords[0]) - 1, 1 - normalize(coords[1]))
        self.radius = normalize(radius)
        self.edges = edges
        self.bgColor = (0.807, 0.0, 0.0)
        self.borderColor = (0.0, 0.0, 0.0)
        self.velocity = (0, 0)
        self.acceleration = (0, 0)
        self.mass = 1


    def draw(self) :
        if self.bgColor :
            glBegin(GL_POLYGON)
            self.trace_particle(self.bgColor)
            glEnd()

        if self.borderColor :
            glBegin(GL_LINE_LOOP)
            self.trace_particle(self.borderColor)
            glEnd()


    def trace_particle(self, color) :
        glColor3f(*color)
        for i in range(self.edges) :
            currX, currY = self.coords
            theta = 2.0 * math.pi * i / self.edges
            x = self.radius * math.cos(theta) + currX
            y = self.radius * math.sin(theta) + currY
            glVertex2f(x, y)


    def apply_force(self, force : tuple[float, float]) :
        self.acceleration = (self.acceleration[0] + force[0] / self.mass, self.acceleration[1] + force[1] / self.mass)


    def update_position(self) :
        self.velocity = (self.velocity[0] + self.acceleration[0] * timestep, self.velocity[1] + self.acceleration[1] * timestep)
        self.coords = (self.coords[0] + self.velocity[0] * timestep, self.coords[1] + self.velocity[1] * timestep)
        self.acceleration = (0, 0)

        # Boundary conditions
        global pass_through
        if pass_through :
            # pass through to other side
            if self.coords[1] > 1 :
                self.coords = (self.coords[0], -1)
            elif self.coords[1] < -1 :
                self.coords = (self.coords[0], 1)

            if self.coords[0] > 1 :
                self.coords = (-1, self.coords[1])
            elif self.coords[0] < -1 :
                self.coords = (1, self.coords[1])
        else :
            # bounce off walls
            if self.coords[1] + self.radius > 1 :
                self.coords = (self.coords[0], 1 - self.radius)
                self.velocity = (self.velocity[0], -self.velocity[1] * bounce_constant)
            elif self.coords[1] - self.radius < -1 :
                self.coords = (self.coords[0], self.radius - 1)
                self.velocity = (self.velocity[0], -self.velocity[1] * bounce_constant)
                
            if self.coords[0] - self.radius < -1 :
                self.coords = (self.radius - 1, self.coords[1])
                self.velocity = (-self.velocity[0] * bounce_constant, self.velocity[1])
            elif self.coords[0] + self.radius > 1 :
                self.coords = (1 - self.radius, self.coords[1])
                self.velocity = (-self.velocity[0] * bounce_constant, self.velocity[1])


    def apply_friction(self) :
        friction = (self.velocity[0] * -friction_coefficient, self.velocity[1] * -friction_coefficient)
        self.apply_force(friction)


    def apply_gravity(self) :
        gravity = (0, -gravity_constant * self.mass)
        self.apply_force(gravity)

# end of Particle class
        

def handle_collision(p : Particle, q : Particle) :
        # check if identicle
        if (p == q) :
            return

        # Calculate particle distance
        distance = math.sqrt((q.coords[0] - p.coords[0]) ** 2 + (q.coords[1] - p.coords[1]) ** 2)
        combined_radius = p.radius + q.radius
        
        # Check for collision
        if distance < combined_radius :
            overlap = combined_radius - distance
            
            if overlap > 0 and distance != 0 :
                # calculate collision vectors
                dx = (q.coords[0] - p.coords[0]) / distance
                dy = (q.coords[1] - p.coords[1]) / distance
                    
                # calculate collision velocities
                dvx = q.velocity[0] - p.velocity[0]
                dvy = q.velocity[1] - p.velocity[1]
                    
                # calculate collision impulse
                impulse = 2 * (dvx * dx + dvy * dy) / (p.mass + q.mass)
                    
                # update velocities
                p.velocity = (p.velocity[0] + impulse * q.mass * dx, p.velocity[1] + impulse * q.mass * dy)
                q.velocity = (q.velocity[0] - impulse * p.mass * dx, q.velocity[1] - impulse * p.mass * dy)
                    
                # move ps out of collision
                move_out = overlap / 2
                p.coords = (p.coords[0] - move_out * dx, p.coords[1] - move_out * dy)
                q.coords = (q.coords[0] + move_out * dx, q.coords[1] + move_out * dy)

                # apply bounce constant
                p.velocity = (p.velocity[0] * bounce_constant, p.velocity[1] * bounce_constant)
                q.velocity = (q.velocity[0] * bounce_constant, q.velocity[1] * bounce_constant)


class Spatial_Hash :

    def __init__(self, cell_size : int) : 
        global window_size
        self.scene_width = window_size
        self.scene_height = window_size
        self.cols = self.scene_width // cell_size
        self.rows = self.scene_height // cell_size
        self.cell_size = cell_size

        # Assign each bucket an empty list
        self.buckets = {}
        for i in range(self.cols * self.rows):
            self.buckets[i] = []


    def clear_buckets(self) :
        for bucket in self.buckets:
            self.buckets[bucket] = []

    def add_particle(self, p: Particle):
        cell_ids = self.get_particle_id(p)
        for cell_id in cell_ids:
            if cell_id in self.buckets:
                self.buckets[cell_id].append(p)
            else:
                self.buckets[cell_id] = [p]



    def get_nearby_particles(self, p : Particle) :
        nearby_particles = []
        bucket_ids = self.get_particle_id(p)
        
        for id in bucket_ids :
            nearby_particles.extend(self.buckets[id])

        return nearby_particles


    def get_particle_id(self, p : Particle) :
    # get bucket ids for a given particle
        buckets_particle_is_in = []

        min_x = p.coords[0] - p.radius
        min_y = p.coords[1] - p.radius
        max_x = p.coords[0] + p.radius
        max_y = p.coords[1] + p.radius

        # search each corner
        self.add_bucket((min_x, min_y), buckets_particle_is_in)
        self.add_bucket((max_x, min_y), buckets_particle_is_in)
        self.add_bucket((max_x, max_y), buckets_particle_is_in)
        self.add_bucket((min_x, max_y), buckets_particle_is_in)

        return buckets_particle_is_in


    def add_bucket(self, vector : tuple[float, float], curr_buckets : list[int]) :
    # add bucket to the list of buckets the particle is in
        cell_position = int((vector[0] // self.cell_size) + (vector[1] // self.cell_size) * self.cols)

        if cell_position not in curr_buckets :
            curr_buckets.append(cell_position)

# end of Spatial_Hash


def main() :

    # init variables
    global window_size
    global particles
    global particleCount
    lastUpdated = time.time()
    frame_count = 0
    last_time = time.time()

    # init spacial hash
    shash = Spatial_Hash(cell_size)

    # init particles
    for i in range(particleCount) :
        coords = (random.randint(0, window_size), random.randint(0, window_size))
        p = Particle(coords)
        p.acceleration = (random.randint(-10, 10), random.randint(-10, 10))
        particles.append(p)
        shash.add_particle(p)

    # for each particle
    while not glfw.window_should_close(window) :

        # clear window
        glClearColor(0.870, 0.905, 0.937, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # clear spatail hash
        shash.clear_buckets()
        
        # timstep
        timerFlag = False
        currTime = time.time()
        elapsed = currTime - lastUpdated

        if elapsed >= timestep :
            lastUpdated = currTime
            timerFlag = True

        # particle movement
        for p in particles :
            if timerFlag :

                # add particles to hash
                shash.add_particle(p)
                
                if optimize :
                    for q in shash.get_nearby_particles(p) :
                        handle_collision(p, q)
                else :
                    for q in particles :
                        handle_collision(p, q)

                if use_gravity :
                    p.apply_gravity()
                
                p.apply_friction()
                p.update_position()

            p.draw()

        # display frame rate
        frame_count += 1
        current_time = time.time()
        if current_time - last_time >= 0.25 :
            fps = frame_count / (current_time - last_time)
            fps = str(round(fps * 10) / 10)
            print("\rFPS :", fps, end="")
            print(" " * (len("FPS : " + fps)), end="", flush=True)
            frame_count = 0
            last_time = current_time

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

main()

glfw.terminate()
print()
