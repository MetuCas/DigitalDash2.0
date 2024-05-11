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

# Initialize Pygame
pygame.init()

# Load configuration from file
config = load_config('FrontConfig.txt')

# Set up the screen dimensions
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Digital Dashboard")

# Define colors using a dictionary for ease of reference
color_map = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'BLUE': (0, 0, 255),
    'GRAY': (150, 150, 150),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'YELLOW': (255, 255, 0),
    'ORANGE': (255, 165, 0),
    'PURPLE': (128, 0, 128)
}

# Font configurations
box_font_size = int(config.get('box_font_size', '40'))
font_box = pygame.font.Font(None, box_font_size)

# Initial text setup for boxes with correct data keys
text_dict = {
    "RPM": "RPM: 0",
    "Speed": "Speed: 0",
    "Temp": "Temperature: 0°C",
    "Pressure": "Pressure: 0",
    "Voltage": "Voltage: 0",
    "Oil Temp": "Oil Temp: 0°C"
}

# Box class definition
class Box:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font_box.render(self.text, True, color_map['WHITE'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

# Create box objects
boxes = []
box_width = screen_width * 0.2
box_height = 50
box_x = (screen_width - box_width) / 2
for i, key in enumerate(text_dict.keys()):
    box_y = 100 + i * (box_height + 10)
    boxes.append(Box(box_x, box_y, box_width, box_height, color_map['BLUE'], text_dict[key]))

# Main event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fetch data
    data = get_data()

    # Update box texts
    try:
        for box, key in zip(boxes, text_dict.keys()):
            value_key = key.lower().replace(' ', '') + 'F'  # Ensure the key transformation matches data keys
            box.text = f"{key}: {data[value_key]}"
    except KeyError as e:
        print(f"Data key missing: {str(e)}")  # Helps diagnose any further key mismatches

    # Redraw the screen
    screen.fill(color_map['BLACK'])
    for box in boxes:
        box.draw(screen)
    pygame.display.flip()

    # Frame rate control
    pygame.time.delay(100)  # Refresh rate, adjust as needed
