import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 20
BALL_RADIUS = 15
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Ball")

# Create paddle
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create ball
ball = pygame.Rect(random.randint(0, WIDTH - BALL_RADIUS * 2), 0, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Set initial ball speed
ball_speed = 5

# Clock to control FPS
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move paddle with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(5, 0)

    # Move ball down the screen
    ball.move_ip(0, ball_speed)

    # Check if ball reaches the bottom
    if ball.bottom >= HEIGHT:
        ball.topleft = (random.randint(0, WIDTH - BALL_RADIUS * 2), 0)

    # Check for collision with paddle
    if ball.colliderect(paddle):
        ball.topleft = (random.randint(0, WIDTH - BALL_RADIUS * 2), 0)

    # Clear the screen
    screen.fill(WHITE)

    # Draw paddle and ball
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.circle(screen, BLUE, ball.center, BALL_RADIUS)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
