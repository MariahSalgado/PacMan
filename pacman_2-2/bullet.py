import pygame

class Bullet:
    def __init__(self, x, y, direction, game_map):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 1.0
        self.bounds = (0, 0, 800, 650)  # Define the bounds for the bullet
        self.cooldown = 10  # Cooldown for shooting (in frames)
        self.timer = 0  # Timer to keep track of the cooldown
        self.bullet_image = pygame.image.load("pacman_2/images/bullet.png")

        self.images = {
            'right': self.bullet_image,
            'left': pygame.transform.flip(self.bullet_image, True, False),
            'up': pygame.transform.rotate(self.bullet_image, 90),
            'down': pygame.transform.rotate(self.bullet_image, -90),
        }
        self.collision_position = None
        self.collision_rect = self.bullet_image.get_rect()  # Initialize the collision rect
        self.game_map = game_map

    def move(self):
        if self.direction == 'right':
            new_x = self.x + self.speed
            new_y = self.y
        elif self.direction == 'left':
            new_x = self.x - self.speed
            new_y = self.y
        elif self.direction == 'up':
            new_x = self.x
            new_y = self.y - self.speed
        elif self.direction == 'down':
            new_x = self.x
            new_y = self.y + self.speed

        # Check for collisions using GameMap
        if not self.game_map.check_bullet_collisions(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            # Store the collision position
            self.collision_position = (int(self.x), int(self.y))

        # Update the cooldown timer
        if self.timer > 0:
            self.timer -= 1

        return self.collision_position

    def can_shoot(self):
        return self.timer <= 0

    def shoot(self, x, y, direction):
        if self.can_shoot():
            self.x = x
            self.y = y
            self.direction = direction
            self.timer = self.cooldown

    def is_within_bounds(self):
        return self.bounds[0] <= self.x <= self.bounds[2] and self.bounds[1] <= self.y <= self.bounds[3]

    def draw(self, screen):
        if self.is_within_bounds():
            bullet_image = self.images[self.direction]
            screen.blit(bullet_image, (self.x * 32, self.y * 32))
