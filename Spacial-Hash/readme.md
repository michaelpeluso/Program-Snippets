# Spacial Hashing a Particle Simulation

This Python script simulates particles moving and colliding within a window using basic physics principles. It utilizes OpenGL for rendering and GLFW for window management. The simulation employs spatial hashing to optimize collision detection between particles, significantly improving performance in scenarios with a large number of particles.

## Introduction

The simulation initializes a number of particles with random positions and velocities. Particles are affected by gravity, friction, and collisions with other particles and the window boundaries. To handle collisions efficiently, especially as the number of particles increases, the simulation implements a **spatial hash**.

## Spatial Hashing Optimization

### What is Spatial Hashing?

Spatial hashing is a technique used to partition space into a grid of cells (or buckets) to efficiently query spatial data. In the context of this simulation, it divides the simulation space into a grid, where each cell contains references to the particles located within it.

### Why Use Spatial Hashing?

Collision detection between particles is computationally intensive, especially when the number of particles is large. Without optimization, the simulation would need to check for collisions between every pair of particles, resulting in **O(n²)** complexity.

Spatial hashing reduces the number of collision checks by only considering particles that are within the same or neighboring cells. This reduces the complexity significantly, leading to better performance and higher frame rates.

### How Does It Work in This Simulation?

1. **Grid Division**: The simulation window is divided into a grid based on the specified `cell_size`.

2. **Hashing Particles**: Each particle is assigned to one or more cells based on its position and radius. This accounts for particles that span multiple cells.

3. **Collision Detection**: When checking for collisions, the simulation only considers particles within the same cells as a given particle, rather than all particles.

4. **Dynamic Updates**: The spatial hash grid is updated each simulation step to account for particle movement.

### Implementation Details

- **Cell Identification**: Each cell in the grid is assigned a unique identifier based on its position in the grid.

- **Particle Assignment**: Particles are assigned to cells by calculating which cells their bounding boxes (defined by their positions and radii) intersect.

- **Neighbor Retrieval**: When checking for collisions, the simulation retrieves particles from the same cells that a particle occupies.

- **Handling Edge Cases**: Particles that are near the boundaries of the grid or span multiple cells are correctly handled to ensure accurate collision detection.

## Features

- **Efficient Collision Detection**: Uses spatial hashing to optimize collision checks.
- **Physics-Based Movement**: Particles move according to physics principles, including acceleration, velocity, and forces.
- **Configurable Forces**: Gravity and friction can be toggled and configured.
- **Boundary Conditions**: Supports both bouncing off walls and passing through to the opposite side.
- **Customizable Parameters**: Simulation settings can be easily adjusted for different scenarios.
- **Performance Metrics**: Displays frame rate to monitor performance.
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
        # Initialize the spatial hash grid based on the cell size

    def clear_buckets(self):
        # Clear the contents of all buckets (cells) in the grid

    def add_particle(self, p):
        # Assign a particle to the appropriate cells based on its position and radius

    def get_nearby_particles(self, p):
        # Retrieve particles that are in the same cells as the given particle

    def get_particle_id(self, p):
        # Calculate the cell IDs that a particle occupies

    def add_bucket(self, vector, curr_buckets):
        # Add a cell ID to the list if it's not already included
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
