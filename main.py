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

pygame.init()

config = load_config('FrontConfig.txt')
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Digital Dashboard")

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

rpm_font_size = 200
font_rpm = pygame.font.Font(None, rpm_font_size)
box_font_size = 40
font_box = pygame.font.Font(None, box_font_size)

text_dict = {
    "KPH": "NULL",
    "WTR": "NULL",
    "BAR": "NULL",
    "VLT": "NULL",
    "OIL": "NULL"
}

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

boxes = []
box_width = screen_width * 0.2
box_height = 50
num_boxes = len(text_dict)
total_box_width = num_boxes * (box_width + 10) - 10
start_x = (screen_width - total_box_width) / 2
for i, (key, value) in enumerate(text_dict.items()):
    box_x = start_x + i * (box_width + 10)
    box_y = screen_height - box_height - 10
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
        y = 50
        color = color_map['GRAY']
        if rpm_value >= (i + 1) * 1000:
            if i < 5:
                color = color_map['GREEN']
            elif i < 7:
                color = color_map['YELLOW']
            else:
                color = color_map['RED']
        pygame.draw.circle(surface, color, (x, y), radius)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fetch data for each frame to update the display
    data = get_data()  # Make sure this line is correctly fetching data
    print("Current Data:", data)  # Debug print to see the fetched data

    # Define a default value for rpm in case it's missing
    rpm_value = data.get('rpm', "0")  # Use a default value if 'rpm' is not in data

    screen.fill(color_map['BLACK'])
    
    # Draw RPM and RPM circles
    draw_rpm(screen, rpm_value)
    draw_circles(screen, int(rpm_value))

    # Update text and draw each box
    for box, key in zip(boxes, text_dict.keys()):
        box.text = f"{key}: {data.get(key.lower(), 'N/A')}"  # Update the text for each box
        box.draw(screen)  # Draw the box after updating the text

    # Update the display
    pygame.display.flip()
    pygame.time.delay(100)
