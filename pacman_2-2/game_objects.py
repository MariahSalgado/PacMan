import pygame

class GameObjects:
    def __init__(self):
        # Load images
        print("Loading all images...")
        self.wall_image_h = pygame.image.load("images/wall_h.png")
        self.wall_image_v = pygame.image.load("images/wall_v.png")
        self.ghost_wall_image = pygame.image.load("images/wall_ghost.png")
        self.dot_image = pygame.image.load("images/dot.png")
        self.big_dot_image = pygame.image.load("images/big_dot.png")
        self.corner_image_1 = pygame.image.load("images/1.png")
        self.corner_image_2 = pygame.image.load("images/2.png")
        self.corner_image_3 = pygame.image.load("images/3.png")
        self.corner_image_4 = pygame.image.load("images/4.png")

        # Load Pac-Man images and scale them
        self.player_size = (32, 32)
        self.pac_man_images = []
        for i in range(1, 5):
            self.pac_man_images.append(pygame.transform.scale(
                pygame.image.load(f'images/player_images/{i}.png'),
                self.player_size))

        # Load portal animation frames
        self.portal_size = (64, 32)
        self.portal_animation_images = {
            'orange': [],
            'blue': [],
        }
        for i in range(1, 3):
            orange_portal_frame = pygame.transform.scale(
                pygame.image.load(f'images/orange_portal{i}.png'),
                self.portal_size
            )
            self.portal_animation_images['orange'].append(orange_portal_frame)
            blue_portal_frame = pygame.transform.scale(
                pygame.image.load(f'images/blue_portal{i}.png'),
                self.portal_size
            )
            self.portal_animation_images['blue'].append(blue_portal_frame)


        #load ghost images and scale them
        self.ghost_size = (32, 32)
        self.blue_ghost_images = []
        self.red_ghost_images = []
        self.orange_ghost_images = []
        self.pink_ghost_images = []

        for i in range(1, 3):
            self.blue_ghost_images.append(pygame.transform.scale(
                pygame.image.load(f'images/ghost_images/blue_run{i}.png'),
                self.ghost_size
            ))
            self.red_ghost_images.append(pygame.transform.scale(
                pygame.image.load(f'images/ghost_images/red_run{i}.png'),
                self.ghost_size
            ))
            self.orange_ghost_images.append(pygame.transform.scale(
                pygame.image.load(f'images/ghost_images/orange_run{i}.png'),
                self.ghost_size
            ))
            self.pink_ghost_images.append(pygame.transform.scale(
                pygame.image.load(f'images/ghost_images/pink_run{i}.png'),
                self.ghost_size
            ))


