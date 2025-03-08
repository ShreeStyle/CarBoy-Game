import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
display_width = 800
display_height = 600
pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Simple 3D Car and Boy Game')

# Set up the OpenGL environment
glViewport(0, 0, display_width, display_height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (display_width / display_height), 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)

# Define colors
RED = (1, 0, 0)
DARK_RED = (0.8, 0, 0)
BLUE = (0, 0, 1)
GREEN = (0, 0.5, 0)
ROAD_GRAY = (0.2, 0.2, 0.2)
SKY_BLUE = (0.53, 0.81, 0.92)
BROWN = (0.55, 0.27, 0.07)
BLACK = (0, 0, 0)
SKIN_COLOR = (0.96, 0.75, 0.6)
DARK_BLUE = (0, 0, 0.5)
TREE_GREEN = (0, 0.39, 0)
WHITE = (1, 1, 1)

# Game variables
car_x = 0
car_speed = 0.5
road_z = 0
score = 0
game_over = False

# Obstacles
obstacles = []
obstacle_timer = 0

# Trees
trees = []

# Font for rendering text
font = pygame.font.Font(None, 36)

# Function to draw a cube
def draw_cube(width, height, depth):
    w, h, d = width/2, height/2, depth/2
    vertices = [
        # Front face
        [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d],
        # Back face
        [-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d]
    ]
    
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
        (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
    ]
    
    faces = [
        (0, 1, 2, 3),  # Front face
        (4, 5, 6, 7),  # Back face
        (0, 3, 7, 4),  # Left face
        (1, 2, 6, 5),  # Right face
        (3, 2, 6, 7),  # Top face
        (0, 1, 5, 4)   # Bottom face
    ]
    
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to draw a cylinder
def draw_cylinder(radius, height, slices):
    # Draw the cylinder walls
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        angle = 2.0 * math.pi * i / slices
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, -height/2)
        glVertex3f(x, y, height/2)
    glEnd()
    
    # Draw the top and bottom caps
    for j in range(2):
        if j == 0:
            z = -height/2
        else:
            z = height/2
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, z)
        for i in range(slices + 1):
            angle = 2.0 * math.pi * i / slices
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, z)
        glEnd()

# Function to draw a sphere
def draw_sphere(radius, slices, stacks):
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + (i / stacks))
        z0 = math.sin(lat0) * radius
        zr0 = math.cos(lat0) * radius
        
        lat1 = math.pi * (-0.5 + ((i + 1) / stacks))
        z1 = math.sin(lat1) * radius
        zr1 = math.cos(lat1) * radius
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * (j / slices)
            x = math.cos(lng)
            y = math.sin(lng)
            
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

# Function to draw a cone
def draw_cone(base_radius, height, slices):
    # Draw the cone walls
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, height)  # Apex
    for i in range(slices + 1):
        angle = 2.0 * math.pi * i / slices
        x = base_radius * math.cos(angle)
        y = base_radius * math.sin(angle)
        glVertex3f(x, y, 0)
    glEnd()
    
    # Draw the base
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)  # Center
    for i in range(slices + 1):
        angle = 2.0 * math.pi * i / slices
        x = base_radius * math.cos(angle)
        y = base_radius * math.sin(angle)
        glVertex3f(x, y, 0)
    glEnd()

# Function to draw the car
def draw_car(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Car body (red box)
    glColor3f(*RED)
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    draw_cube(1.5, 1, 3)
    glPopMatrix()
    
    # Car top (darker red box)
    glColor3f(*DARK_RED)
    glPushMatrix()
    glTranslatef(0, 1.1, -0.2)
    draw_cube(1.3, 0.7, 1.5)
    glPopMatrix()
    
    # Wheels (black cylinders)
    glColor3f(*BLACK)
    # Front left wheel
    glPushMatrix()
    glTranslatef(-0.8, 0, -1)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.4, 0.3, 16)
    glPopMatrix()
    
    # Front right wheel
    glPushMatrix()
    glTranslatef(0.8, 0, -1)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.4, 0.3, 16)
    glPopMatrix()
    
    # Rear left wheel
    glPushMatrix()
    glTranslatef(-0.8, 0, 1)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.4, 0.3, 16)
    glPopMatrix()
    
    # Rear right wheel
    glPushMatrix()
    glTranslatef(0.8, 0, 1)
    glRotatef(90, 0, 1, 0)
    draw_cylinder(0.4, 0.3, 16)
    glPopMatrix()
    
    glPopMatrix()

# Function to draw the boy character
def draw_boy(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Boy body (blue box)
    glColor3f(*BLUE)
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    draw_cube(0.6, 1, 0.3)
    glPopMatrix()
    
    # Boy head (skin-colored sphere)
    glColor3f(*SKIN_COLOR)
    glPushMatrix()
    glTranslatef(0, 1.2, 0)
    draw_sphere(0.3, 16, 16)
    glPopMatrix()
    
    # Boy legs (dark blue boxes)
    glColor3f(*DARK_BLUE)
    # Left leg
    glPushMatrix()
    glTranslatef(-0.2, -0.05, 0)
    draw_cube(0.2, 0.6, 0.2)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(0.2, -0.05, 0)
    draw_cube(0.2, 0.6, 0.2)
    glPopMatrix()
    
    glPopMatrix()

# Function to draw a tree
def draw_tree(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Trunk (brown cylinder)
    glColor3f(*BROWN)
    glPushMatrix()
    glTranslatef(0, 1, 0)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.2, 2, 8)
    glPopMatrix()
    
    # Leaves (green cone)
    glColor3f(*TREE_GREEN)
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    glRotatef(-90, 1, 0, 0)
    draw_cone(1, 2, 8)
    glPopMatrix()
    
    glPopMatrix()

# Function to draw the ground
def draw_ground(z_offset):
    # Ground (green)
    glColor3f(*GREEN)
    glPushMatrix()
    glTranslatef(0, 0, z_offset)
    glBegin(GL_QUADS)
    glVertex3f(-25, 0, -500)
    glVertex3f(25, 0, -500)
    glVertex3f(25, 0, 100)
    glVertex3f(-25, 0, 100)
    glEnd()
    glPopMatrix()
    
    # Road (gray)
    glColor3f(*ROAD_GRAY)
    glPushMatrix()
    glTranslatef(0, 0.01, z_offset)  # Slightly above ground to prevent z-fighting
    glBegin(GL_QUADS)
    glVertex3f(-5, 0, -500)
    glVertex3f(5, 0, -500)
    glVertex3f(5, 0, 100)
    glVertex3f(-5, 0, 100)
    glEnd()
    glPopMatrix()

# Function to draw an obstacle
def draw_obstacle(x, y, z, size):
    glColor3f(*BROWN)
    glPushMatrix()
    glTranslatef(x, y, z)
    draw_cube(size, size, size)
    glPopMatrix()

# Function to add a new obstacle
def add_obstacle():
    size = random.uniform(0.5, 1.0)
    x = random.uniform(-4, 4)
    obstacles.append({
        'x': x,
        'y': size/2,
        'z': -100,
        'size': size
    })

# Function to add a new tree
def add_tree(z_pos=None):
    side = random.choice([-1, 1])
    x = (10 + random.uniform(0, 5)) * side
    z = z_pos if z_pos is not None else random.uniform(-500, -20)
    trees.append({
        'x': x,
        'y': 0,
        'z': z
    })

# Initialize trees
for i in range(30):
    add_tree(z_pos=-i * 30 - 20)

# Initialize boy position
boy_pos = {
    'x': 3,
    'y': 0,
    'z': 0
}

# Function to reset the game
def reset_game():
    global car_x, car_speed, road_z, score, game_over, obstacles, obstacle_timer
    car_x = 0
    car_speed = 0.5
    road_z = 0
    score = 0
    game_over = False
    obstacles = []
    obstacle_timer = 0

# Render text function
def render_text(text, position):
    # This is a workaround to render text in OpenGL with Pygame
    text_surface = font.render(text, True, WHITE)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    text_width, text_height = text_surface.get_size()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glWindowPos2d(position[0], position[1])
    glDrawPixels(text_width, text_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    glDisable(GL_BLEND)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
    
    # Clear the screen
    glClearColor(*SKY_BLUE, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set up camera view
    glLoadIdentity()
    if not game_over:
        gluLookAt(car_x * 0.3, 3, 15, car_x * 0.3, 0, 0, 0, 1, 0)
    else:
        gluLookAt(0, 3, 15, 0, 0, 0, 0, 1, 0)
    
    # Handle input
    keys = pygame.key.get_pressed()
    if not game_over:
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and car_x > -4:
            car_x -= 0.1
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and car_x < 4:
            car_x += 0.1
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and car_speed < 0.8:
            car_speed += 0.005
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and car_speed > 0.2:
            car_speed -= 0.005
    
    # Update game state if not game over
    if not game_over:
        # Move ground
        road_z += car_speed
        if road_z > 100:
            road_z = 0
        
        # Add new obstacles
        obstacle_timer += 1
        if obstacle_timer > 100 / car_speed:
            add_obstacle()
            obstacle_timer = 0
        
        # Update obstacles and check collisions
        for obstacle in obstacles[:]:
            obstacle['z'] += car_speed
            
            # Remove obstacles that are behind the camera
            if obstacle['z'] > 20:
                obstacles.remove(obstacle)
                score += 1
            
            # Check for collision with car
            if abs(obstacle['x'] - car_x) < (obstacle['size']/2 + 0.75) and \
               obstacle['z'] > 3.5 and obstacle['z'] < 6.5:
                game_over = True
        
        # Update boy position
        boy_pos['z'] += car_speed * 0.2
        if boy_pos['z'] > 20:
            boy_pos['z'] = -40
            boy_pos['x'] = random.uniform(-4, 4)
        
        # Update trees
        for tree in trees:
            tree['z'] += car_speed
            if tree['z'] > 30:
                tree['z'] -= 600
    
    # Draw everything
    draw_ground(road_z)
    
    # Draw trees
    for tree in trees:
        draw_tree(tree['x'], tree['y'], tree['z'])
    
    # Draw obstacles
    for obstacle in obstacles:
        draw_obstacle(obstacle['x'], obstacle['y'], obstacle['z'], obstacle['size'])
    
    # Draw boy
    draw_boy(boy_pos['x'], boy_pos['y'], boy_pos['z'])
    
    # Draw car
    draw_car(car_x, 0, 5)
    
    # Render UI text
    if game_over:
        render_text(f"Game Over! Score: {score}", (300, 400))
        render_text("Press R to restart", (320, 350))
    else:
        render_text(f"Score: {score}", (10, 570))
        render_text(f"Speed: {car_speed:.2f}", (10, 540))
        render_text("Use WASD or Arrow Keys to control the car", (200, 570))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
