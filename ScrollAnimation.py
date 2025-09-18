import pygame
import sys
import pygame_gui

class ScrollAnimation:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rectangle = pygame.Rect((screen_width - 20) // 2, (screen_height - 400) // 2, 20, 400)
        self.animation_speed = 2
        self.actions = {
            'expand': self.expand,
            'shrink': self.shrink,
            # Add more actions as needed
        }

    def expand(self):
        self.rectangle.width += self.animation_speed
        if self.rectangle.width >= self.screen_width:
            self.rectangle.width = self.screen_width

    def shrink(self):
        self.rectangle.width -= self.animation_speed
        if self.rectangle.width <= 0:
            self.rectangle.width = 0

# Initialize Pygame and Pygame GUI
pygame.init()
# pygame_gui.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scroll Animation")

# Create the ScrollAnimation instance
scroll_animation = ScrollAnimation(screen_width, screen_height)

# Set up Pygame GUI
ui_manager = pygame_gui.UIManager((screen_width, screen_height))

# Load the image for the button
button_width, button_height = 50, 30
button_x = (screen_width - button_width) // 2
button_y = screen_height - 50
button_image = pygame.image.load("images/scroll_button.png")  # Replace with your image file
button_image = pygame.transform.scale(button_image, (button_width, button_height))

# Create a pygame_gui button with the image
button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(button_x, button_y, button_width, button_height),
    text='',
    manager=ui_manager,
    container=None,
    object_id='#button',
    normal_image_surface=button_image,
    hovered_image_surface=button_image,
    pressed_image_surface=button_image,
)

# Main game loop
while True:
    time_delta = pygame.time.Clock().tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == button:
                # Perform the 'expand' action
                scroll_animation.actions['expand']()

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), scroll_animation.rectangle)
    ui_manager.draw_ui(screen)

    pygame.display.flip()
