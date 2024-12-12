import pygame
import sys
from game_map import GameMap
from game_objects import GameObjects
from pac_man import PacMan
from bullet import Bullet
from ghosts import Ghost
from portal import Portal

class PacManGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 650))
        pygame.display.set_caption("Pac-Man")
        self.waka_sound = pygame.mixer.Sound('audio/pacman_chomp.wav')
        pygame.mixer.music.load('audio/pacman_beginning.wav')
        self.in_title_screen = True
        self.game_objects = GameObjects()
        map_filename = "map.txt"
        self.game_map = GameMap(self.game_objects)
        self.game_map.load_map_from_file(map_filename)
        self.walls_h, self.walls_v, self.walls_g, self.dots, self.big_dots, self.corners, pac_man_start, ghost_spawn_points = self.game_map.create_game_objects()
        pac_man_start = None

        self.bullets = []  # Store bullets
        self.blue_portals = []  # List to store blue portals
        self.orange_portals = []  # List to store orange portals

        self.bullet_count = 0  # Initialize the bullet count

        # Load title image
        self.title_image = pygame.image.load('images/ghost_images/blue_run1.png')
        self.image1 = pygame.image.load('images/ghost_images/orange_run2.png')
        self.image2 = pygame.image.load('images/ghost_images/pink_run1.png')
        self.image3 = pygame.image.load('images/ghost_images/red_run2.png')

        # scale factor
        scale_factor = 3.0

        # Scale the image
        self.title_image = pygame.transform.scale(self.title_image, (
        int(self.title_image.get_width() * scale_factor),
        int(self.title_image.get_height() * scale_factor)
        ))
        self.image1 = pygame.transform.scale(self.image1, (
        int(self.image1.get_width() * scale_factor),
        int(self.image1.get_height() * scale_factor)
        ))
        self.image2 = pygame.transform.scale(self.image2, (
        int(self.image2.get_width() * scale_factor),
        int(self.image2.get_height() * scale_factor)
        ))
        self.image3 = pygame.transform.scale(self.image3, (
        int(self.image3.get_width() * scale_factor),
        int(self.image3.get_height() * scale_factor)
        ))


        self.lives = 3
        original_pacman_life = pygame.image.load('images/player_images/1.png')
        pacman_life_width = 20
        pacman_life_height = int(
            pacman_life_width * original_pacman_life.get_height() / original_pacman_life.get_width())
        self.pacman_life_image = pygame.transform.scale(original_pacman_life, (pacman_life_width, pacman_life_height))

        for y, row in enumerate(self.game_map.game_map):
            for x, char in enumerate(row):
                if char == 'P':
                    pac_man_start = (x, y)
                    break
        if pac_man_start is not None:
            self.pac_man = PacMan(pac_man_start[0], pac_man_start[1], self.game_objects, self.game_map)
        else:
            raise Exception("Pac-Man's initial position was not found in the map.")
        
        ghost_box = pygame.Rect(288, 224, 96, 96)

        # Create different sets of images for each ghost
        blue_ghost_images = [
            pygame.image.load("images/ghost_images/blue_run1.png"),
            pygame.image.load("images/ghost_images/blue_run2.png")
        ]

        red_ghost_images = [
            pygame.image.load("images/ghost_images/red_run1.png"),
            pygame.image.load("images/ghost_images/red_run2.png")
        ]

        orange_ghost_images = [
            pygame.image.load("images/ghost_images/orange_run1.png"),
            pygame.image.load("images/ghost_images/orange_run2.png")
        ]

        pink_ghost_images = [
            pygame.image.load("images/ghost_images/pink_run1.png"),
            pygame.image.load("images/ghost_images/pink_run2.png")
        ]

                # Adjust the initial position of the blue ghost inside the ghost box
        blue_ghost_start_x = 324  # Adjust the X coordinate as needed
        blue_ghost_start_y = 260  # Adjust the Y coordinate as needed

        # Adjust the initial position of the red ghost outside the ghost box
        red_ghost_start_x = 30 # Adjust the X coordinate as needed
        red_ghost_start_y = 15 # Adjust the Y coordinate as needed

        orange_ghost_start_x = 310  # Adjust the X coordinate as needed
        orange_ghost_start_y = 250  # Adjust the Y coordinate as needed

        pink_ghost_start_x = 315  # Adjust the X coordinate as needed
        pink_ghost_start_y = 240  # Adjust the Y coordinate as needed

        # Create the blue ghost and set its initial position inside the ghost box
        blue_ghost = Ghost(blue_ghost_images, blue_ghost_start_x, blue_ghost_start_y, ghost_box)
        red_ghost = Ghost(red_ghost_images, red_ghost_start_x, red_ghost_start_y, None)
        pink_ghost = Ghost(pink_ghost_images, pink_ghost_start_x, pink_ghost_start_y, ghost_box)
        orange_ghost = Ghost(orange_ghost_images, orange_ghost_start_x, orange_ghost_start_y, ghost_box)

        # Store the ghosts in a list
        self.ghosts = [red_ghost, blue_ghost, pink_ghost, orange_ghost]

        self.FPS = 32
        self.clock = pygame.time.Clock()
        self.pac_man_speed = 0.1
        self.score = 0  # Initialize the score

        # Create a list to store bullet hit positions
        self.bullet_hits = []

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.in_title_screen and event.key == pygame.K_SPACE:
                        self.in_title_screen = False
                    elif not self.in_title_screen and event.key == pygame.K_SPACE:
                        while len(self.bullets) >= 2:
                            self.bullets.pop(0)
                        bullet = Bullet(self.pac_man.x, self.pac_man.y, self.pac_man.direction, self.game_map)
                        self.bullets.append(bullet)
                        self.bullet_count += 1  # Increment the bullet count

            self.screen.fill((0, 0, 0))

            if self.in_title_screen:
                title_font = pygame.font.Font(None, 94)
                title_text = title_font.render("PAC-MAN", True, (255, 255, 0))
            

                #More images on the title screen
                image1 = pygame.image.load('images/ghost_images/orange_run1.png')
                image2 = pygame.image.load('images/ghost_images/pink_run1.png')
                image3 = pygame.image.load('images/ghost_images/red_run1.png')
                image4 = pygame.image.load('images/player_images/1.png')
                image5 = pygame.image.load('images/big_dot.png')
                image6 = pygame.image.load('images/dot.png')
                image7 = pygame.image.load('images/big_dot.png')
                image8 = pygame.image.load('images/dot.png')
                image9 = pygame.image.load('images/big_dot.png')
                image10 = pygame.image.load('images/dot.png')
                image11 = pygame.image.load('images/big_dot.png')
                image12 = pygame.image.load('images/dot.png')
                border = pygame.image.load('images/border_pacman.png')
                
                # Blit images
                self.screen.blit(image4, (5, 100))
                self.screen.blit(image5, (630, 310))
                self.screen.blit(image6, (650, 310))
                self.screen.blit(image7, (670, 310))
                self.screen.blit(image8, (690, 310))
                self.screen.blit(image9, (710, 310))
                self.screen.blit(image10, (730, 310))
                self.screen.blit(image11, (750, 310))
                self.screen.blit(image12, (770, 310))
                self.screen.blit(border, (290, 185))
                
                # Blit other images in the corners
                image1_top_left = (10, 10)
                self.screen.blit(self.image1, image1_top_left)

                image2_top_right = (self.screen.get_width() - self.image2.get_width() - 10, 10)
                self.screen.blit(self.image2, image2_top_right)

                image3_bottom_left = (10, self.screen.get_height() - self.image3.get_height() - 10)
                self.screen.blit(self.image3, image3_bottom_left)

                title_bottom_right_x = self.screen.get_width() - self.title_image.get_width() - 10
                title_bottom_right_y = self.screen.get_height() - self.title_image.get_height() - 10
                self.screen.blit(self.title_image, (title_bottom_right_x, title_bottom_right_y))


                # Set the title in center
                title_x = (self.screen.get_width() - title_text.get_width()) // 2
                title_y = (self.screen.get_height() - title_text.get_height()) // 2
    
               
                instructions_font = pygame.font.Font(None, 32)
                instructions_text_1 = instructions_font.render("Press", True, (255, 0, 0))  # Red
                instructions_text_2 = instructions_font.render("SPACE", True, (255, 192, 203))  # Pink
                instructions_text_3 = instructions_font.render("to", True, (173, 216, 230))  # Blue
                instructions_text_4 = instructions_font.render("start", True, (255, 165, 0))  # 0range

                self.screen.blit(title_text, (300, 300))

                # Position text
                press_space_x = (self.screen.get_width() - instructions_text_1.get_width()) // 2
                press_space_y = title_y + title_text.get_height() + 20


                # Position text title
                word_spacing = 10
                total_width = (instructions_text_1.get_width() + word_spacing +
                                instructions_text_2.get_width() + word_spacing +
                                instructions_text_3.get_width() + word_spacing +
                                instructions_text_4.get_width())

                start_x = (self.screen.get_width() - total_width) // 1.8
                start_y = title_y + title_text.get_height() + 20
                # Blit each word at calculated positions
                self.screen.blit(instructions_text_1, (start_x, start_y))
                start_x += instructions_text_1.get_width() + word_spacing

                self.screen.blit(instructions_text_2, (start_x, start_y))
                start_x += instructions_text_2.get_width() + word_spacing

                self.screen.blit(instructions_text_3, (start_x, start_y))
                start_x += instructions_text_3.get_width() + word_spacing

                self.screen.blit(instructions_text_4, (start_x, start_y))

                # Update the display
                pygame.display.update()
            else:
                for wall_x, wall_y in self.walls_h:
                    self.screen.blit(self.game_objects.wall_image_h, (wall_x * 32, wall_y * 32))
                for wall_x, wall_y in self.walls_v:
                    self.screen.blit(self.game_objects.wall_image_v, (wall_x * 32, wall_y * 32))
                for wall_g_x, wall_g_y in self.walls_g:
                    self.screen.blit(self.game_objects.ghost_wall_image, (wall_g_x * 32, wall_g_y * 32))

                # Iterate over dots and draw them
                for dot_x, dot_y, collected in self.dots:
                    if not collected:  # Only draw if the dot has not been collected
                        self.screen.blit(self.game_objects.dot_image, (dot_x * 32, dot_y * 32))
                for big_dot_x, big_dot_y in self.big_dots:
                    if not self.in_title_screen:
                        if int(self.pac_man.x) == big_dot_x and int(self.pac_man.y) == big_dot_y:
                            self.big_dots.remove((big_dot_x, big_dot_y))
                            self.score += 20  # Increase the score
                            self.waka_sound.play()  # Play the waka sound

                for big_dot_x, big_dot_y in self.big_dots:
                    self.screen.blit(self.game_objects.big_dot_image, (big_dot_x * 32 + 2, big_dot_y * 32 - 2))
                for corner_x, corner_y, corner_image in self.corners:
                    self.screen.blit(corner_image, (corner_x * 32, corner_y * 32))

                for ghost in self.ghosts:
                    ghost.move()
                    ghost.draw(self.screen)
                # Check for bullet-wall collisions and generate portals
                self.check_bullet_wall_collisions()

                self.pac_man.move()
                self.pac_man.check_portal_collision(self.blue_portals)
                self.pac_man.check_portal_collision(self.orange_portals)
                self.pac_man.draw(self.screen)

                # Check for collisions with dots
                for dot_x, dot_y, collected in self.dots:
                    if not collected and int(self.pac_man.x) == dot_x and int(self.pac_man.y) == dot_y:
                        self.dots.remove((dot_x, dot_y, False))  # Remove the collected dot
                        self.score += 10  # Increase the score
                        self.waka_sound.play()  # Play the waka sound

                # Draw the score on the screen
                self.draw_score(self.screen)

            # Update and draw bullets
            self.update_bullets()
            self.draw_bullets(self.screen)

            self.draw_portals(self.screen)

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def draw_score(self, screen):
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        for i in range(self.lives):
            screen.blit(self.pacman_life_image, (
            self.screen.get_width() - (i + 1) * (self.pacman_life_image.get_width() + 10),
            self.screen.get_height() - self.pacman_life_image.get_height() - 10))

    def check_bullet_wall_collisions(self):
        # Iterate over bullets to check for collisions with walls
        for bullet in self.bullets:
            collision_position = bullet.move()  # Capture the collision position
            if collision_position is not None:
                self.spawn_portals(collision_position)

    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw_portals(self, screen):
        for portal in self.blue_portals:
            portal.draw(screen)
        for portal in self.orange_portals:
            portal.draw(screen)

    def update_bullets(self):
        new_bullets = []
        for bullet in self.bullets:
            bullet.move()
            # Update the cooldown timer for the bullet
            if bullet.timer > 0:
                bullet.timer -= 1
            new_bullets.append(bullet)
        # Limit the number of bullets to two
        self.bullets = new_bullets

    def spawn_portals(self, collision_position):
        print(f"Spawning portals at position {collision_position}")
        entrance_x, entrance_y = collision_position
        exit_x, exit_y = collision_position

        # Determine the portal color based on the bullet count
        if self.bullet_count % 2 == 0:
            portal_color = 'blue'
            portals_list = self.blue_portals
        else:
            portal_color = 'orange'
            portals_list = self.orange_portals

        portal = Portal(entrance_x, entrance_y, exit_x, exit_y, portal_color)
        portal.load_images()

        if len(portals_list) >= 1:
            portals_list.pop()  # Remove the existing portal (if any)
        portals_list.append(portal)


if __name__ == "__main__":
    game = PacManGame()
    game.run()
