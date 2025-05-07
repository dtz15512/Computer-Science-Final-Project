import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 20
GRID_SIZE = 25
WIDTH = HEIGHT = GRID_SIZE * TILE_SIZE

# Speed of the snake
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (200, 0, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLOOD = (138, 3, 3)
NAVY = (15, 15, 40)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - CSC221 Final Project SP2025")

# Fonts
font = pygame.font.SysFont(None, 36)

# Sounds
pygame.mixer.init()
background_music = "Oogway Ascends.mp3"
death_sound = pygame.mixer.Sound("scream.mp3")


def draw_text(text, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def random_food_position(snake):
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if (x, y) not in snake:
            return (x, y)


def game():
    clock = pygame.time.Clock()
    snake = [(5, 5)]
    direction = (1, 0)
    current_direction = direction  # To prevent 180-degree turns
    food = random_food_position(snake)
    score = 0
    running = True
    paused = False

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_UP and current_direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and current_direction != (0, -1):
                        direction = (0, 1)
                    elif event.key == pygame.K_LEFT and current_direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and current_direction != (-1, 0):
                        direction = (1, 0)

        if paused:
            screen.fill(NAVY)
            draw_text("Paused - Press P to Resume", WHITE, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            continue

        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        current_direction = direction  # Lock in direction once move begins

        # Check collisions
        if (new_head in snake or
            new_head[0] < 0 or new_head[0] >= GRID_SIZE or
            new_head[1] < 0 or new_head[1] >= GRID_SIZE):
            pygame.mixer.music.stop()
            death_sound.play()
            pygame.time.delay(2000)
            return score

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = random_food_position(snake)
        else:
            snake.pop()

        # Draw everything
        screen.fill(NAVY)
        for segment in snake:
            pygame.draw.rect(screen, PURPLE, (segment[0]*TILE_SIZE, segment[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, WHITE, (food[0]*TILE_SIZE, food[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        draw_text(f"Score: {score}", WHITE, WIDTH // 2, 20)
        pygame.display.flip()


def main():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)

    while True:
        score = game()
        screen.fill(BLOOD)
        draw_text("Don't quit your day job just yet", BLUE, WIDTH // 2, HEIGHT // 2 - 30)
        draw_text(f"Final Score: {score}", WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press R to Restart or Q to Quit", WHITE, WIDTH // 2, HEIGHT // 2 + 30)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.load(background_music)
                        pygame.mixer.music.play(-1)
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


if __name__ == '__main__':
    main()
