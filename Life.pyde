import time

from decoder import *
from objects import *

# field size:
dimension = 300
# canvas zoom:
zoom = 4

# random distribution of dots, value between 0 and 1
density = 0

population = []
generation = 0
start_time = 0

class Cell():

    def __init__(self, x, y, alive=0):
        self.x = x
        self.y = y
        self.screen_x = x * zoom
        self.screen_y = y * zoom
        self.alive = alive
        self.new_state = self.alive

def setup():
    global population
    global start_time

    size(dimension * zoom, dimension * zoom)
    background(0)
    noFill()
    strokeWeight(zoom)     # cell size
    noSmooth()
    # strokeCap(PROJECT)   # squared cells
    # frameRate(2)         # slow down

    for y in range(dimension):
        for x in range(dimension):

            if random(1) < density:
                alive = 1
            else:
                alive = 0

            population.append(Cell(x, y, alive))

    # place_object(20, 20, o_blinker)
    # place_object(40, 40, o_toad)
    # place_object(50, 50, o_beacon)
    # place_object(70, 20, o_pulsar)
    # place_object(70, 70, o_penta_decathlon)

    # place_object(0, 0, o_glider)

    # place_object(dimension/2, dimension/2, o_r_pentomino)
    # place_object(dimension/2, dimension/2, o_diehard)
    # place_object(dimension/2, dimension/2, o_acorn)
    # place_object(dimension / 4, dimension / 4, o_gosper_gun)
    # place_object(dimension *2/3, dimension * 2/3, o_generator1)
    # place_object(dimension / 2, dimension / 2, o_generator2)
    # place_object(13, dimension / 2, o_generator3)

    # place_object(dimension / 2-25, dimension / 2, decode_object(o_101P7))
    # place_object(dimension / 2, dimension / 2, decode_object(o_6P2))
    # place_object(dimension / 2, dimension / 2, decode_object(o_12P8))
    # place_object(dimension / 6, dimension / 2, decode_object(o_20P6))
    # place_object(dimension / 2, dimension / 2, decode_object(o_196P5))
    # place_object(dimension / 2, dimension / 2, decode_object(o_132P3H1V0))
    # place_object(dimension / 2, dimension / 2, decode_object(o_213P28H7V0))
    # place_object(dimension / 2, dimension / 2, decode_object(o_180P4H1V1))
    
    place_object(30, dimension / 3, decode_object(load_object(name='objects/basic-rakes.rle')))

    start_time = time.time()

def place_object(x, y, object):
    global population

    for yoff, x_row in enumerate(object, y):
        if yoff >= 0 and yoff < dimension:
            for xoff, cell_state in enumerate(x_row, x):
                if xoff >= 0 and xoff < dimension :
                    population[xoff + yoff * dimension].new_state = cell_state

def get_cell_status(x, y):

    if x >= 0 and x < dimension and y >= 0 and y < dimension:
        return population[x + y * dimension].alive
    else:
        return 0

def count(x, y):

    left = x - 1
    right = x + 1
    up = y - 1
    down = y + 1

    result = 0
    result += get_cell_status(left, up)
    result += get_cell_status(x, up)
    result += get_cell_status(right, up)
    result += get_cell_status(left, y)
    result += get_cell_status(right, y)
    result += get_cell_status(left, down)
    result += get_cell_status(x, down)

    if result == 0 or result > 3:
        # don't count any longer, it will not change the end effect
        return result

    result += get_cell_status(right, down)

    return result

def new_count(x, y):
    # fancy code, but too slow

    result = 0

    left = x - 1
    right = x + 1
    up = y - 1
    down = y + 1

    offsets = {(left, up), (x, up), (right, up), (left, y),
               (right, y), (left, down), (x, down), (right, down)}

    for offset in offsets:
        cx = offset[0]
        cy = offset[1]
        if cx >= 0 and cx < dimension and cy >= 0 and cy < dimension:
            result += population[cx + cy * dimension].alive
            if result > 3:
                # don't count any longer, it will not change the end effect
                return result

    return result

def draw():
    global generation

    are_they_evolving = False

    for cell in population:

        # does the cell require redraw?
        if cell.alive != cell.new_state:

            # copy status from previous calculation
            cell.alive = cell.new_state

            if cell.alive == 1:
                stroke(255)
            else:
                stroke(0)
            point(cell.screen_x, cell.screen_y)

    for cell in population:

        n = count(cell.x, cell.y)

        if cell.alive == 1 and (n < 2 or n > 3):  # kill
            cell.new_state = 0
            are_they_evolving = True

        elif cell.alive == 0 and n == 3:  # born
            cell.new_state = 1
            are_they_evolving = True

        # else:  # remain

    generation += 1
    print("Generation: {}").format(generation)

    # stop after generations limit
    # if generation == 1000:
    #     end_time = time.time()
    #     print("Time spent: {} s.").format(end_time - start_time)
    #     noLoop()

    if (not are_they_evolving):
        # all are dead or not changing

        end_time = time.time()
        fill(240, 200, 0, 200)
        text("End of simulation", 0, 20)
        print("Time spent: {} s.").format(end_time - start_time)
        noLoop()
