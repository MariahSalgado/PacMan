import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((600, 650))
pygame.display.set_caption("Pac-Man")

# Load images
wall_image_h = pygame.image.load("pacman_2/images/wall_h.png")
wall_image_v = pygame.image.load("pacman_2/images/wall_v.png")
dot_image = pygame.image.load("pacman_2/images/dot.png")
corner_image_1 = pygame.image.load("pacman_2/images/1.png")
corner_image_2 = pygame.image.load("pacman_2/images/2.png")
corner_image_3 = pygame.image.load("pacman_2/images/3.png")
corner_image_4 = pygame.image.load("pacman_2/images/4.png")

pac_man_images = []

# Load Pac-Man images and scale them
player_size = (25, 25)
for i in range(1, 5):
    pac_man_images.append(pygame.transform.scale(pygame.image.load(f'pacman_2/images/player_images/{i}.png'), player_size))

# Read the map from a text file
def load_map_from_file(filename):
    with open(filename, 'r') as file:
        map_data = [line.strip() for line in file.readlines()]

    game_map = []
    for line in map_data:
        row = list(line)
        game_map.append(row)

    return game_map

# Create game objects
def create_game_objects(game_map):
    walls_h = []
    walls_v = []
    dots = []
    corners = []
    pac_man_start = None

    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if char == '#':
                walls_v.append((x, y))
            elif char == '=':
                walls_h.append((x, y))
            elif char == '.':
                dots.append((x, y))
            elif char == 'P':
                pac_man_start = (x, y)
            elif char == '1':
                corners.append((x, y, corner_image_1))
            elif char == '2':
                corners.append((x, y, corner_image_2))
            elif char == '3':
                corners.append((x, y, corner_image_3))
            elif char == '4':
                corners.append((x, y, corner_image_4))

    return walls_h, walls_v, dots, corners, pac_man_start

map_filename = "pacman_2/map.txt"
game_map = load_map_from_file(map_filename)
walls_h, walls_v, dots, corners, pac_man_start = create_game_objects(game_map)

# Initialize Pac-Man's position and direction
pac_man_x, pac_man_y = pac_man_start
pac_man_direction = 'right'
pac_man_frame = 0  # Animation frame for Pac-Man

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Pac-Man movement and animation here (you can implement Pac-Man controls)
    
    # Update Pac-Man animation frame (this can be done in response to game logic)
    pac_man_frame = (pac_man_frame + 1) % len(pac_man_images)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the game objects based on their positions
    for wall_pos in walls_h:
        screen.blit(wall_image_h, (wall_pos[0] * 32, wall_pos[1] * 32))
    for wall_pos in walls_v:
        screen.blit(wall_image_v, (wall_pos[0] * 32, wall_pos[1] * 32))
    for dot_pos in dots:
        screen.blit(dot_image, (dot_pos[0] * 32, dot_pos[1] * 32))
    for corner_pos in corners:
        x, y, corner_image = corner_pos
        screen.blit(corner_image, (x * 32, y * 32))
    # Display Pac-Man image based on the animation frame and direction
    if pac_man_direction == 'right':
        screen.blit(pac_man_images[pac_man_frame], (pac_man_x * 32, pac_man_y * 32))
    # You can add similar blocks for other directions (up, down, left)

    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
