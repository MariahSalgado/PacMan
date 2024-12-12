import pygame

class Portal:
    def __init__(self, entrance_x, entrance_y, exit_x, exit_y, color):
        self.entrance_x = entrance_x
        self.entrance_y = entrance_y
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.color = color
        self.load_images()

    def load_images(self):
        if self.color == 'blue':
            self.portal_image = pygame.image.load("pacman_2/images/blue_portal2.png")
        elif self.color == 'orange':
            self.portal_image = pygame.image.load("pacman_2/images/orange_portal2.png")

    def collides_with_pac_man(self, x, y):
        return self.entrance_x == int(x) and self.entrance_y == int(y)

    def get_exit_position(self):
        return self.exit_x, self.exit_y

    def draw(self, screen):
        screen.blit(self.portal_image, (self.entrance_x * 32, self.entrance_y * 32))
        screen.blit(self.portal_image, (self.exit_x * 32, self.exit_y * 32))
