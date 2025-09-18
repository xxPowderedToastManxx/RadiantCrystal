import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BRICK_COLORS = [RED, BLUE, (0, 255, 0), (255, 255, 0), (255, 0, 255)]

# Game variables
score = 0
lives = 3
level = 1

# Function to reset the game state for a new level
def reset_level():
    global score, lives, level
    score = 0
    lives = 3
    level += 1
    return create_bricks()

# Function to create bricks for the current level
def create_bricks():
    bricks = []
    for row in range(min(5, level + 2)):
        for col in range(WIDTH // BRICK_WIDTH):
            brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append(brick)
    return bricks

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Create paddle
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [5, -5]

# Create bricks for the current level
bricks = create_bricks()

# Clock to control FPS
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

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

    # Move ball
    ball.move_ip(ball_speed)

    # Check for collisions with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1

    # Check for collisions with paddle
    if ball.colliderect(paddle):
        ball_speed[1] *= -1

    # Check for collisions with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] *= -1
            score += 10

    # Check if all bricks are cleared for the current level
    if not bricks:
        bricks = create_bricks()

    # Check if the ball reaches the bottom
    if ball.top >= HEIGHT:
        lives -= 1
        if lives <= 0:
            # Game over, reset for a new level
            bricks = reset_level()

        # Reset the ball to the center
        ball.topleft = (WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS)
        ball_speed = [5, -5]

    # Clear the screen
    screen.fill(WHITE)

    # Draw paddle, ball, and bricks
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.circle(screen, BLUE, ball.center, BALL_RADIUS)
    for brick in bricks:
        pygame.draw.rect(screen, random.choice(BRICK_COLORS), brick)

    # Display score, lives, and level
    score_text = font.render(f"Score: {score}", True, BLUE)
    lives_text = font.render(f"Lives: {lives}", True, BLUE)
    level_text = font.render(f"Level: {level}", True, BLUE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(level_text, (WIDTH - 150, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
