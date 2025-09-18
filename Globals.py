import pygame
import random

# Initialize Pygame
pygame.init()


WIDTH, HEIGHT = 1024, 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

RACES = ["Human",
         "Elf",
         "Orc"]

# global player_health, player_experience, player_mana

# Create window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Radiant Crystal')


ABILITY_SCORE_COST_TABLE = {
    8: 0,
    9: 1,
    10: 2,
    11: 3,
    12: 4,
    13: 5,
    14: 7,
    15: 9
}


