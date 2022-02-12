import pygame
import random
import time

pygame.init()

# general class with basic drawing info
class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    DARK_GREY = 40, 40, 60
    GREY = 60, 60, 70

    BLUE = 52, 152, 219
    GREEN = 32, 191, 107
    RED = 235, 59, 90

    BG_COLOR = WHITE

    GRADIENTS = [
        (197, 237, 245),
        (182, 224, 234),
        (166, 211, 222),
        (151, 198, 210),
        (135, 185, 198),
        (120, 173, 187),
        (105, 160, 176),
        (90, 148, 165),
        (74, 135, 154)
    ]

    X_MARGIN = 120
    Y_MARGIN = 180

    FONT = pygame.font.SysFont('georgia', 20)
    LARGE_FONT = pygame.font.SysFont('segoeuiblack', 30)

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
        self.bars_max_height = int((self.height - self.Y_MARGIN) / (self.max_val - self.min_val))
        self.start_x = self.X_MARGIN // 2

# basically refills the window every frame
def draw(draw_info, algo_name, ascend):
    # the way I have done this isn't the most optimized or efficent way of doing
    ## but it makes sure it gets rid of overlays, shadows and other artifacts
    draw_info.window.fill(draw_info.BG_COLOR)

    # settings in use text
    title_text = draw_info.LARGE_FONT.render(f"{algo_name} in {'Ascending' if ascend else 'Descending'} order", 1, draw_info.GREEN)
    draw_info.window.blit(title_text, (draw_info.width/2 - title_text.get_width()/2, 5))

    # controls text
    controls_text = draw_info.FONT.render("SPACE - Sort/Stop | R - Reset | A - Ascend | D - Descend", 1, draw_info.DARK_GREY)
    draw_info.window.blit(controls_text, (draw_info.width/2 - controls_text.get_width()/2, 50))
    sorting_text = draw_info.FONT.render("1 - Bubble Sort | 2 - Insertion Sort | 3 - Selection Sort | 4 - Merge Sort | 5 - Quick Sort", 1, draw_info.DARK_GREY)
    draw_info.window.blit(sorting_text, (draw_info.width/2 - sorting_text.get_width()/2, 80))


    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_pos={}, clear_bg = False):
    list = draw_info.list
    if clear_bg:
        clear_rect = (draw_info.X_MARGIN//2,
            draw_info.Y_MARGIN,
            draw_info.width - draw_info.X_MARGIN,
            draw_info.height - draw_info.Y_MARGIN)
        pygame.draw.rect(draw_info.window, draw_info.BG_COLOR, clear_rect)

    for i, val in enumerate(list):
        x = draw_info.start_x + i * draw_info.bars_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bars_max_height
        if(val < 10):
            color = draw_info.GRADIENTS[0]
        else:
            color = draw_info.GRADIENTS[round(val / 12)]

        # green/red bars replaced
        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bars_width , draw_info.height - y))
    
    if clear_bg:
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
    
    # initial settings
    sort = False
    ascend = True

    # initial algorithm
    sorting_algorithm = bubble_sort
    sort_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    # core editable values
    n = 50
    min_val = 1
    max_val = 100

    list = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(960, 600, list)

    while run:
        clock.tick(60)

        if sort:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sort = False
        else:
            draw(draw_info, sort_algo_name, ascend)

        # handling all events/key presses
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(list)
                sort = False
            elif event.key == pygame.K_SPACE and sort == False:
                sort = True
                sorting_algo_generator = sorting_algorithm(0, n - 1, draw_info.list, draw_info, ascend)
            elif event.key == pygame.K_SPACE and sort == True:
                sort = False
                sorting_algo_generator = sorting_algorithm(0, n - 1, draw_info.list, draw_info, ascend)
            elif event.key == pygame.K_a and not sort:
                ascend = True
            elif event.key == pygame.K_d and not sort:
                ascend = False
            elif event.key == pygame.K_1 and not sort:
                sorting_algorithm = bubble_sort
                sort_algo_name = "Bubble Sort"
            elif event.key == pygame.K_2 and not sort:
                sorting_algorithm = insertion_sort
                sort_algo_name = "Insertion Sort"
            elif event.key == pygame.K_3 and not sort:
                sorting_algorithm = selection_sort
                sort_algo_name = "Selection Sort"
            elif event.key == pygame.K_4 and not sort:
                sorting_algorithm = merge_sort
                sort_algo_name = "Merge Sort"

    pygame.quit()

def bubble_sort(first, last, lst, draw_info, ascend = True):
    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            num1 = lst[j]
            num2 = lst[j + 1]

            # if True swap bars
            if (ascend and num1 > num2) or (not ascend and num1 < num2 ):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(first, last, lst, draw_info, ascend = True):
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            # handles when in correct position
            ascend_sort = i > 0 and lst[i - 1] > current and ascend
            descend_sort = i > 0 and lst[i - 1] < current and not ascend
            # stops when in correct position
            if not ascend_sort and not descend_sort:
                break

            lst[i], i = lst[i - 1], i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def selection_sort(first, last, lst, draw_info, ascend = True):
    for i in range(len(lst) - 1):
        current = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[current] and ascend) or (lst[j] > lst[current] and not ascend):
                current = j
            time.sleep(0.0005)
        lst[current], lst[i] = lst[i], lst[current]
        
        draw_list(draw_info, {i - 1: draw_info.GREEN, current: draw_info.RED}, True)
        yield True
    return lst

def merge_sort(first, last, lst, draw_info, ascend = True, first_time = True):
    if first_time:
        first = 0
        last = len(draw_info.list) - 1
        lst = draw_info.list
        first_time = False
    if len(lst) > 1:
        global_middle = (first + last + 1) // 2

        middle = len(lst) // 2

        L = lst[:middle]
        R = lst[middle:]

        list(merge_sort(first, global_middle - 1, L, draw_info, ascend, False))
        list(merge_sort(global_middle, last, R, draw_info, ascend, False))

        i = j = k = 0
        while i < len(L) and j < len(R):
            if (L[i] < R[j] and ascend) or (L[i] > R[j] and not ascend):
                lst[k] = L[i]
                draw_info.list[k + first] = L[i]
                i += 1
                time.sleep(0.02)
                draw_list(draw_info, {k + first: draw_info.GREEN, (global_middle + k): draw_info.RED}, True)
                yield True
            else:
                lst[k] = R[j]
                draw_info.list[k + first] = R[j]
                j += 1
                time.sleep(0.02)
                draw_list(draw_info, {k + first: draw_info.GREEN, (global_middle + k): draw_info.RED}, True)
                yield True 
            k += 1
        
        while i < len(L):
            lst[k] = L[i]
            draw_info.list[k + first] = L[i]
            time.sleep(0.02)
            draw_list(draw_info, {k + first: draw_info.GREEN, (global_middle + k): draw_info.RED}, True)
            yield True
            i += 1
            k += 1

        while j < len(R):
            lst[k] = R[j]
            draw_info.list[k + first] = R[j]
            time.sleep(0.02)
            draw_list(draw_info, {k + first: draw_info.GREEN, (global_middle + k): draw_info.RED}, True)
            yield True
            j += 1
            k += 1
    return lst

def quick_sort(first, last, lst, draw_info, ascend = True, first_time = True):


    
    return lst

if __name__ == "__main__":
    main()
