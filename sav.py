import pygame
import random
pygame.init()

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

    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(list)
    
    def set_list(self,list):
        self.list = list
        self.min_val = min(list)
        self.max_val = max(list)

        self.bars_width = round(self.width - self.X_MARGIN / len(list))
        self.bars_max_height = round((self.height - self.Y_MARGIN) / (self.max_val - self.min_val))
        self.start_x = self.X_MARGIN // 2

