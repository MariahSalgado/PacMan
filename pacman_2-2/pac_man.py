import pygame
from bullet import Bullet  # Import the Bullet class

class PacMan:
    def __init__(self, start_x, start_y, game_objects, game_map):
        self.x = start_x
        self.y = start_y
        self.direction = 'right'
        self.last_input_direction = 'right'  # Initialize with a default value
        self.game_objects = game_objects
        self.animation_speed = 5
        self.frame_counter = 0
        self.pac_man_speed = 0.05
        self.game_map = game_map

        # Store images for each direction
        self.images = {
            'right': game_objects.pac_man_images,
            'left': [pygame.transform.flip(img, True, False) for img in game_objects.pac_man_images],  # Flip for left
            'up': [pygame.transform.rotate(img, 90) for img in game_objects.pac_man_images],  # Rotate for up
            'down': [pygame.transform.rotate(img, -90) for img in game_objects.pac_man_images],  # Rotate for down
        }
        
        self.frame = 0

    def set_direction(self, new_direction):
        # Update the last input direction when the user presses an arrow key
        if new_direction in ['left', 'right', 'up', 'down']:
            self.last_input_direction = new_direction

        # Update the direction based on user input
        self.direction = new_direction

    def move(self):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.x, self.y  # Initialize with the current position

        if keys[pygame.K_LEFT]:
            self.set_direction('left')
            new_x -= self.pac_man_speed
        elif keys[pygame.K_RIGHT]:
            self.set_direction('right')
            new_x += self.pac_man_speed
        elif keys[pygame.K_UP]:
            self.set_direction('up')
            new_y -= self.pac_man_speed
        elif keys[pygame.K_DOWN]:
            self.set_direction('down')
            new_y += self.pac_man_speed

        # If no user input, use the last input direction as the default
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction = self.last_input_direction

        if not self.game_map.check_collisions(new_x, new_y):
            # Update the position if there are no collisions
            self.x = new_x
            self.y = new_y

    def shoot_bullet(self):
        x, y = self.x, self.y
        direction = self.direction  # Get the direction Pac-Man is facing
        bullet = Bullet(x, y, direction)  # Create a bullet
        return bullet  # Return the bullet

    def check_portal_collision(self, portals):
        for portal in portals:
            if portal.collides_with_pac_man(self.x, self.y):
                self.x, self.y = portal.get_exit_position()

    def teleport_to_portal(self, collision_position, blue_portals, orange_portals):
        for portal in blue_portals + orange_portals:
            if portal.entrance_x == collision_position[0] and portal.entrance_y == collision_position[1]:
                # Teleport Pac-Man to the corresponding portal exit
                self.x = portal.exit_x
                self.y = portal.exit_y
                break

    def collides_with_portal(self, portal):
        return (self.x, self.y) == (portal.entrance_x, portal.entrance_y)

    def draw(self, screen):
        pac_man_image = self.images[self.direction][self.frame]
        screen.blit(pac_man_image, (self.x * 32, self.y * 32))

        # Control the animation speed based on elapsed time
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame = (self.frame + 1) % len(self.game_objects.pac_man_images)
            self.frame_counter = 0
