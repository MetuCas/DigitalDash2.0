import pygame
import sys
from Input import get_data

def load_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=')
                config[key.strip()] = value.strip()
    return config

# Load configuration from file
config = load_config('FrontConfig.txt')

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dashboard")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Extract configurations
box_color = eval(config.get('box_color', 'BLUE'))
rpm_color = eval(config.get('rpm_color', 'RED'))
bottom_gauge_color = eval(config.get('bottom_gauge_color', 'YELLOW'))
bottom_gauge_text_color = eval(config.get('bottom_gauge_text_color', 'BLACK'))
box_font_size = int(config.get('box_font_size', '40'))
rpm_font_size = int(config.get('rpm_font_size', '300'))
circle_colors = [eval(color) for color in config.get('circle_colors', '').split() if color]

# Define font for boxes
font_box = pygame.font.Font(None, box_font_size)

# Define text for each box initially
text_dict = {
    "MPH": "50",
    "Volt": "12",
    "Oil": "75",
    "WTR": "90",
    "PSI": "30"
}

# Define box class
class Box:
    def __init__(self, x, y, width, height, color, text, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, font_size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

# Calculate box dimensions and positions
box_width_percent = 0.15
box_height_percent = 0.15
box_margin_percent = 0.02
box_bottom_margin_percent = 0.1
box_width = int(screen_width * box_width_percent)
box_height = int(screen_height * box_height_percent)
box_margin = int(screen_width * box_margin_percent)
box_bottom_margin = int(screen_height * box_bottom_margin_percent)

# Create boxes
boxes = []
num_boxes = len(text_dict)
total_box_width = num_boxes * box_width + (num_boxes - 1) * box_margin
start_x = (screen_width - total_box_width) / 2
for i, (key, value) in enumerate(text_dict.items()):
    box_x = start_x + i * (box_width + box_margin)
    box_y = screen_height - box_height - box_bottom_margin
    box_text = f"{key}: {value}"
    boxes.append(Box(box_x, box_y, box_width, box_height, box_color, box_text, box_font_size))

# Define the refresh rate and set up the timer event
refresh_rate = int(config.get('RefreshRate', '1000'))  # Default to 1000 ms
refresh_event = pygame.USEREVENT + 1
pygame.time.set_timer(refresh_event, refresh_rate)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == refresh_event:
            data = get_data()  # Assume get_data() returns a dictionary with the necessary values
            # Update the text for each box based on new data
            boxes[0].text = f"RPM: {data['rpmF']}"
            boxes[1].text = f"Speed: {data['speedF']} km/h"
            boxes[2].text = f"Engine Coolant Temp: {data['tempF']}°C"
            boxes[3].text = f"Oil Pressure: {data['pressureF']} bar"

    # Clear the screen
    screen.fill(BLACK)

    # Draw updated boxes
    for box in boxes:
        box.draw(screen)

    # Additional drawing logic here...

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
