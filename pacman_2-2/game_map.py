import pygame

class GameMap:
    def __init__(self, game_objects):
        self.game_objects = game_objects
        self.walls_h = []
        self.walls_v = []
        self.walls_g = []
        self.corners = []
        self.ghost_spawn_points = []

    def load_map_from_file(self, filename):
        with open(filename, 'r') as file:
            map_data = [line.strip() for line in file.readlines()]

        self.game_map = []
        for line in map_data:
            row = list(line)
            self.game_map.append(row)

    def create_game_objects(self):
        dots = []
        big_dots = []
        pac_man_start = None

        for y, row in enumerate(self.game_map):
            for x, char in enumerate(row):
                if char == '#':
                    self.walls_v.append((x, y))
                elif char == '=':
                    self.walls_h.append((x, y))
                elif char == '+':
                    self.walls_g.append((x, y))
                elif char == '.':
                    dots.append((x, y, False))  # Initialize all dots as not collected
                elif char == '!':
                    big_dots.append((x, y))
                elif char == 'P':
                    pac_man_start = (x, y)
                elif char == 'x':
                    self.ghost_spawn_points.append((x, y))
                elif char == '1':
                    self.corners.append((x, y, self.game_objects.corner_image_1))
                elif char == '2':
                    self.corners.append((x, y, self.game_objects.corner_image_2))
                elif char == '3':
                    self.corners.append((x, y, self.game_objects.corner_image_3))
                elif char == '4':
                    self.corners.append((x, y, self.game_objects.corner_image_4))

        return self.walls_h, self.walls_v, self.walls_g, dots, big_dots, self.corners, pac_man_start, self.ghost_spawn_points

    def check_collisions(self, x, y):
        pac_man_rect = pygame.Rect(x * 32, y * 32 - 5, 20, 15)

        for wall_x, wall_y in self.walls_h:
            wall_rect = pygame.Rect(wall_x * 32 + 2, wall_y * 32 + 2, 25, 25)
            if pac_man_rect.colliderect(wall_rect):
                return True

        for wall_x, wall_y in self.walls_v:
            wall_rect = pygame.Rect(wall_x * 32 + 2, wall_y * 32 + 2, 25, 25)
            if pac_man_rect.colliderect(wall_rect):
                return True

        for corner_x, corner_y, _ in self.corners:
            corner_rect = pygame.Rect(corner_x * 32 + 2, corner_y * 32 + 2, 25, 25)
            if pac_man_rect.colliderect(corner_rect):
                return True

        for wall_g_x, wall_g_y in self.walls_g:
            wall_g_rect = pygame.Rect(wall_g_x * 32, wall_g_y * 32, 4, 4)
            if pac_man_rect.colliderect(wall_g_rect):
                return True

        return False

    def check_bullet_collisions(self, bullet_x, bullet_y):
        bullet_rect = pygame.Rect(bullet_x * 32, bullet_y * 32, 4, 4)  # Define the dimensions of your bullet
        
        for wall_x, wall_y in self.walls_h:
            wall_rect = pygame.Rect(wall_x * 32 + 2, wall_y * 32 + 2, 20, 25)  # Adjust the dimensions for horizontal walls
            if bullet_rect.colliderect(wall_rect):
                return True

        for wall_x, wall_y in self.walls_v:
            wall_rect = pygame.Rect(wall_x * 32 + 2, wall_y * 32 + 2, 25, 20)  # Adjust the dimensions for vertical walls
            if bullet_rect.colliderect(wall_rect):
                return True

        for corner_x, corner_y, _ in self.corners:
            corner_rect = pygame.Rect(corner_x * 32 + 2, corner_y * 32 + 2, 25, 25)  # Adjust the dimensions for corners
            if bullet_rect.colliderect(corner_rect):
                return True

        return False
