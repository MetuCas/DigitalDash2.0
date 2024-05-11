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

# Extract configurations
box_color = eval(config.get('box_color', 'WHITE'))
box_font_size = int(config.get('box_font_size', '40'))
rpm_font_size = int(config.get('rpm_font_size', '300'))

# Define font for RPM and boxes
font_rpm = pygame.font.Font(None, rpm_font_size)
font_box = pygame.font.Font(None, box_font_size)

# Define text for RPM and each box initially
rpm_text = "RPM: 1000"
text_dict = {
    "Speed": "100 km/h",
    "Volt": "12V",
    "Oil Temp": "75°C",
    "Water Temp": "90°C",
    "Oil Pressure": "30 psi"
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
            # Update RPM and the text for each box based on new data
            rpm_text = f"RPM: {data['rpmF']}"
            for box, key in zip(boxes, text_dict.keys()):
                box.text = f"{key}: {data[key.lower() + 'F']}"

    # Clear the screen
    screen.fill(BLACK)

    # Draw RPM in the center
    rpm_surface = font_rpm.render(rpm_text, True, WHITE)
    rpm_rect = rpm_surface.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(rpm_surface, rpm_rect)

    # Draw updated boxes
    for box in boxes:
        box.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
