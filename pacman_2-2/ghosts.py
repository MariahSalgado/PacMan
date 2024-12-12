import pygame
import random

class Ghost:
    def __init__(self, images, start_x, start_y, ghost_box):
        self.images = images
        self.image_index = 0
        self.x = start_x
        self.y = start_y
        self.direction = 'up'
        self.ghost_box = ghost_box

    def set_position(self, x, y):
        if self.ghost_box is None or (
                self.ghost_box.left <= x <= self.ghost_box.right and self.ghost_box.top <= y <= self.ghost_box.bottom):
            self.x = x
            self.y = y

    def move(self):
        # Implement ghost movement logic here
        # For example, move the ghost horizontally within the box
        self.x += 1  # Move the ghost one unit to the right

        # Check if the ghost is outside the ghost box boundaries
        if self.ghost_box and self.x < self.ghost_box.left:
            self.x = self.ghost_box.left
        elif self.ghost_box and self.x > self.ghost_box.right:
            self.x = self.ghost_box.right

    def roam(self):
        # Implement logic to restrict movement within the ghost box
        if self.ghost_box:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            dx, dy = random.choice(directions)

            # Calculate the new position
            new_x = self.x + dx
            new_y = self.y + dy

            # Check if the new position is within the ghost box boundaries
            if self.ghost_box.collidepoint(new_x, new_y):
                self.x = new_x
                self.y = new_y

    def draw(self, screen):
        # Draw the ghost on the screen within the ghost box
        screen.blit(self.images[self.image_index], (self.x, self.y))

        # Update the current image for animation (if you have multiple images)
        self.image_index = (self.image_index + 1) % len(self.images)
