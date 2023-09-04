# Building withpygame
# Importing libraries
import pygame
import sys

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 25
GRID_COLOR_WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 128, 255)
OBSTACLES = (128, 128, 128)
ITEMS = (255, 0, 0)
FINISHING_CELL_COLOR = (0, 255, 0)

class Grid_Game:

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        #  Initialising the Constants
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.GRID_SIZE = GRID_SIZE
        self.GRID_WIDTH = self.WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.GRID_SIZE
        self.WHITE = GRID_COLOR_WHITE
        self.PLAYER_COLOR = PLAYER_COLOR
        self.OBSTACLE_COLOR = OBSTACLES
        self.ITEM_COLOR = ITEMS
        self.FINISH_COLOR = FINISHING_CELL_COLOR
        self.FONT = pygame.font.Font(None, 36)

        # Create the window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Grid Game")

        # Initialize game state
        self.player_x, self.player_y = 0, 0
        self.obstacles = [(3, 3), (6, 6), (8, 5), (10, 8), (12, 12), (15, 15), (17, 17), (8, 3),
                          (12, 5), (77, 4), (42, 9), (4, 8), (12, 14), (50, 66)]  # obstacle positions
        self.items = [(2, 2), (7, 4), (9, 9), (10, 9), (43, 7)]  # item positions
        self.finish_line = (self.GRID_WIDTH - 1, self.GRID_HEIGHT - 1)  # Finish line at the right bottom of grid
        self.player_has_finished = False
        self.rules_displayed = False

    def make_grid(self):
        # Clear the screen
        self.screen.fill(self.WHITE)

        # Draw the grid
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.WIDTH, y))

    def display_rules(self):
        self.screen.fill(self.WHITE)
        text1 = self.FONT.render("Welcome to the Grid Game!", True, (0, 0, 0))
        text2 = self.FONT.render("Use arrow keys to navigate.", True, (0, 0, 0))
        text3 = self.FONT.render("Collect red items.", True, (0, 0, 0))
        text4 = self.FONT.render("Avoid grey cells.", True, (0, 0, 0))
        text5 = self.FONT.render("Reach the green cell to win!", True, (0, 0, 0))
        text6 = self.FONT.render("Press any key to start...", True, (0, 0, 0))
        self.screen.blit(text1, (20, 50))
        self.screen.blit(text2, (20, 100))
        self.screen.blit(text3, (20, 150))
        self.screen.blit(text4, (20, 200))
        self.screen.blit(text5, (20, 250))
        self.screen.blit(text6, (20, 300))
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.event.clear()
        pygame.event.wait()

    def events_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Move the player based on arrow key input
                if not self.player_has_finished:
                    if event.key == pygame.K_LEFT and self.player_x > 0:
                        self.player_x -= 1
                    elif event.key == pygame.K_RIGHT and self.player_x < self.GRID_WIDTH - 1:
                        self.player_x += 1
                    elif event.key == pygame.K_UP and self.player_y > 0:
                        self.player_y -= 1
                    elif event.key == pygame.K_DOWN and self.player_y < self.GRID_HEIGHT - 1:
                        self.player_y += 1

    def make_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, self.OBSTACLE_COLOR, (
                obstacle[0] * self.GRID_SIZE, obstacle[1] * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))

    def make_items(self):
        for item in self.items:
            pygame.draw.rect(self.screen, self.ITEM_COLOR,
                             (item[0] * self.GRID_SIZE, item[1] * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))

    def set_finish_line(self):
        pygame.draw.rect(self.screen, self.FINISH_COLOR,
                         (self.finish_line[0] * self.GRID_SIZE, self.finish_line[1] * self.GRID_SIZE, self.GRID_SIZE,
                          self.GRID_SIZE))

    def check_collision(self):
        # Check if the player collides with an obstacle
        player_rect = pygame.Rect(self.player_x * self.GRID_SIZE, self.player_y * self.GRID_SIZE, self.GRID_SIZE,
                                  self.GRID_SIZE)
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle[0] * self.GRID_SIZE, obstacle[1] * self.GRID_SIZE, self.GRID_SIZE,
                                        self.GRID_SIZE)
            if player_rect.colliderect(obstacle_rect):
                return True

        # Check if the player collects an item
        for item in self.items[:]:
            item_rect = pygame.Rect(item[0] * self.GRID_SIZE, item[1] * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE)
            if player_rect.colliderect(item_rect):
                self.items.remove(item)  # Remove the collected item

        # Check if the player has reached the finish line
        if (self.player_x, self.player_y) == self.finish_line:
            self.player_has_finished = True

        return False

    def run(self):

        if not self.rules_displayed:
            self.display_rules()
            self.rules_displayed = True

        # Game loop
        while True:
            self.events_handler()
            self.make_grid()
            self.make_obstacles()
            self.make_items()
            self.set_finish_line()
            pygame.draw.rect(self.screen, self.PLAYER_COLOR, (
                self.player_x * self.GRID_SIZE, self.player_y * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE))

            if self.check_collision():
                # Handle collision (e.g., game over)
                if not self.player_has_finished:
                    font = pygame.font.Font(None, 36)
                    text = font.render("Game Over!", True, (0, 0, 0))
                    self.screen.blit(text, (150, self.HEIGHT // 2 - 18))
                    pygame.display.flip()
                    pygame.time.wait(1000)  # Wait for a second before restarting
                    self.__init__()  # Restart the game
                else:
                    self.player_has_finished = False  # Reset the flag
                    self.player_x, self.player_y = 0, 0  # Reset player position

            if self.player_has_finished:
                # Display a message upon finishing
                font = pygame.font.Font(None, 36)
                text = font.render("Congratulations! You finished!", True, (0, 0, 0))
                self.screen.blit(text, (50, self.HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(1000)  # Wait for a second before restarting
                self.__init__()  # Restart the game

            pygame.display.flip()


if __name__ == "__main__":
    game = Grid_Game()
    game.run()
