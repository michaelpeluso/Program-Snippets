# Particle Simulation with OpenGL and GLFW

This Python script simulates particles moving and colliding within a window using basic physics principles. It utilizes OpenGL for rendering and GLFW for window management.

## Description

The simulation initializes a number of particles with random positions and velocities. Particles are affected by gravity, friction, and collisions with other particles and the window boundaries. The simulation is optimized using a spatial hash to efficiently handle collisions between particles.

## Features

- **Particle Movement**: Physics-based acceleration and velocity.
- **Collision Detection**: Efficient handling of particle collisions.
- **Boundary Conditions**: Options to bounce off walls or pass through.
- **Forces**: Gravity and friction effects.
- **Optimization**: Spatial hashing for improved performance.
- **Configurable Parameters**: Adjust simulation settings easily.

## Installation

### Prerequisites

Make sure you have the following libraries installed:

- `glfw`
- `PyOpenGL`

Install them using pip:

``pip install glfw PyOpenGL``

### Clone the Repository

Clone this repository to your local machine:

``git clone https://github.com/yourusername/your-repo-name.git``

## Usage

Run the script using Python 3:

``python your_script_name.py``

Press the `ESC` key to close the simulation window.

## Configuration

Adjust the following parameters in the script to change the simulation behavior:

- `window_size`: Size of the simulation window (default: `500`).
- `cell_size`: Cell size for spatial hashing (default: `10`).
- `timestep`: Time step for simulation updates (default: `0.025`).
- `particleCount`: Number of particles in the simulation (default: `300`).
- `particle_radius`: Radius of each particle (default: `4`).
- `gravity_constant`: Strength of gravity (default: `9.81`).
- `friction_coefficient`: Friction applied to particles (default: `0.5`).
- `bounce_constant`: Elasticity of particle collisions (default: `1`).
- `optimize`: Enable spatial hashing optimization (default: `True`).
- `pass_through`: Particles pass through walls if `True` (default: `False`).
- `use_gravity`: Enable gravity effect if `True` (default: `True`).

## Code Overview

### Particle Class

Defines the properties and behaviors of particles in the simulation.

```python
class Particle:
    def __init__(self, coords, radius=particle_radius, edges=25):
        # Initialization code

    def draw(self):
        # Drawing code

    def apply_force(self, force):
        # Apply force to particle

    def update_position(self):
        # Update particle position and handle boundary conditions

    def apply_friction(self):
        # Apply friction to particle

    def apply_gravity(self):
        # Apply gravity to particle
```

## Spatial_Hash Class

Optimizes collision detection by dividing the space into a grid.
```python
class Spatial_Hash:
    def __init__(self, cell_size):
        # Initialization code

    def clear_buckets(self):
        # Clear spatial hash buckets

    def add_particle(self, p):
        # Add particle to spatial hash

    def get_nearby_particles(self, p):
        # Retrieve nearby particles for collision detection
```

## Main Loop
The main loop initializes particles, updates their positions, handles collisions, and renders them to the window.

```python
def main():
    # Initialization code

    while not glfw.window_should_close(window):
        # Clear window

        # Update particles

        # Handle collisions

        # Draw particles

        # Swap buffers and poll events

```
