import pygame
import random

pygame.init()

# general class with basic drawing info
class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255

    BLUE = 52, 152, 219
    GREEN = 46, 204, 113
    RED = 231, 76, 60

    BG_COLOR = WHITE

    GRADIENTS = [
        (197, 237, 245),
        (74, 135, 154),
        (135, 185, 198)
    ]

    X_MARGIN = 80
    Y_MARGIN = 120

    # windows init
    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(list)
    
    # adaptive display size with margins
    def set_list(self, list):
        self.list = list
        self.min_val = min(list)
        self.max_val = max(list)

        self.bars_width = round((self.width - self.X_MARGIN) / len(list))
        self.bars_max_height = round((self.height - self.Y_MARGIN) / (self.max_val - self.min_val))
        self.start_x = self.X_MARGIN // 2

# basically refills the window every frame
def draw(draw_info):

    # the way I have done this isn't the most optimized or efficent way of doing
    ## but it makes sure it gets rid of overlays, shadows and other artifacts
    draw_info.window.fill(draw_info.BG_COLOR)
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info):
    list = draw_info.list
    
    for i, val in enumerate(list):
        x = draw_info.start_x + i * draw_info.bars_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bars_max_height
        color = draw_info.GRADIENTS[i % 3]
        
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bars_width , draw_info.height))


def generate_starting_list(n, min_val, max_val):

    list = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        list.append(val)

    return list

def main():
    run = True 
    clock = pygame.time.Clock()

    # core editable values
    n = 50
    min_val = 1
    max_val = 100

    list = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(800, 600, list)
    draw(draw_info)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            # handling top right quit bottom
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
