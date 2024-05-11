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
rpm_font_size = 200  # Larger font for RPM in the center
font_rpm = pygame.font.Font(None, rpm_font_size)
box_font_size = 40
font_box = pygame.font.Font(None, box_font_size)

# Initial text setup for boxes (except RPM)
text_dict = {
    "KPH": "NULL",
    "WTR": "NULL",
    "BAR": "NULL",
    "VLT": "NULL",
    "OIL": "NULL"
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

# Create box objects for bottom display
boxes = []
box_width = screen_width * 0.2
box_height = 50
num_boxes = len(text_dict)
total_box_width = num_boxes * (box_width + 10) - 10  # Adjust spacing between boxes
start_x = (screen_width - total_box_width) / 2
for i, (key, value) in enumerate(text_dict.items()):
    box_x = start_x + i * (box_width + 10)
    box_y = screen_height - box_height - 10  # Position boxes at the bottom
    boxes.append(Box(box_x, box_y, box_width, box_height, color_map['PURPLE'], value))

def draw_rpm(surface, rpm_value):
    rpm_surface = font_rpm.render(f"RPM: {rpm_value}", True, color_map['WHITE'])
    rpm_rect = rpm_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    surface.blit(rpm_surface, rpm_rect)

def draw_circles(surface, rpm_value):
    radius = 20
    gap = 10
    total_width = 10 * (2 * radius + gap) - gap
    start_x = (screen_width - total_width) / 2
    for i in range(10):
        x = start_x + i * (2 * radius + gap)
        y = 50  # Top of the screen
        color = color_map['GRAY']  # Default color
        if rpm_value >= (i + 1) * 750:
            if i < 5:
                color = color_map['GREEN']
            elif i < 7:
                color = color_map['YELLOW']
            else:
                color = color_map['RED']
        pygame.draw.circle(surface, color, (x, y), radius)

# Main event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fetch data
    data = get_data()

    # Update box texts and RPM display
    try:
        rpm_value = data['rpmF']
        for box, key in zip(boxes, text_dict.keys()):
            box.text = f"{key}: {data[key.lower().replace(' ', '') + 'F']}"
    except KeyError as e:
        print(f"Data key missing: {str(e)}")

    # Redraw everything
    screen.fill(color_map['BLACK'])
    draw_rpm(screen, rpm_value)
    draw_circles(screen, int(rpm_value))
    for box in boxes:
        box.draw(screen)

    # Update display
    pygame.display.flip()

    # Frame rate control
    pygame.time.delay(100)  # Adjust as needed
