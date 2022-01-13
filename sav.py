import pygame
import random

from pygame import draw
pygame.init()

# general class with basic drawing info
class DrawInfo:
    BLACK = 0,0,0
    WHITE = 255,255,255

    BLUE = 0,0,255
    GREEN = 0,255,0
    RED = 255,0,0

    GREY = 128,128,128
    BG_COLOR = WHITE
    X_MARGIN = 80
    Y_MARGIN = 120

    # windows init
    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(list)
    
    # adaptive display size with margins
    def set_list(self,list):
        self.list = list
        self.min_val = min(list)
        self.max_val = max(list)

        self.bars_width = round(self.width - self.X_MARGIN / len(list))
        self.bars_max_height = round((self.height - self.Y_MARGIN) / (self.max_val - self.min_val))
        self.start_x = self.X_MARGIN // 2

# basically refills the window every frame
def draw(draw_info):
    # the way I have done this isn't the most optimized or efficent way of doing
    ## but it makes sure it gets rid of overlays, shadows and other artifacts
    draw_info.window.fill(draw_info.BG_COLOR)
    pygame.display.update()

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
    min = 1
    max = 100

    list = generate_starting_list(n, min, max)
    draw_info = DrawInfo(800, 600, list)

    while run:
        clock.tick(60)

        draw(draw_info)

        for event in pygame.event.get():
            # handling top right quit bottom
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
