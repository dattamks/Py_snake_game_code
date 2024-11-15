import pygame
import time
import random
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Greedy Snake Game")

# Clock and speed
clock = pygame.time.Clock()
SPEED = 15

def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], block_size, block_size])

def message(msg, color, position):
    font = pygame.font.SysFont(None, 35)
    mesg = font.render(msg, True, color)
    screen.blit(mesg, position)

def find_closest_food(snake_position, food_positions):
    return min(food_positions, key=lambda food: abs(snake_position[0] - food[0]) + abs(snake_position[1] - food[1]))

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0

    snake_list = []
    snake_length = 1

    food_positions = [
        [random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)]
    ]

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press C to Play Again or Q to Quit", RED, [WIDTH // 6, HEIGHT // 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        # Find closest food
        closest_food = find_closest_food(snake_head, food_positions)

        if x == closest_food[0] and y == closest_food[1]:
            food_positions.remove(closest_food)
            food_positions.append([random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)])
            snake_length += 1

        screen.fill(BLACK)
        draw_snake(BLOCK_SIZE, snake_list)

        for food in food_positions:
            pygame.draw.rect(screen, BLUE, [food[0], food[1], BLOCK_SIZE, BLOCK_SIZE])

        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()
    quit()

game_loop()
