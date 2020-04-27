import time

from decoder import *
from objects import *
from cell import Cell

# field size:
dimension = 200
# canvas zoom:
zoom = 4
# random distribution of dots, value between 0 and 1
density = 0

Cell.create(dimension, zoom, density)

start_time = 0

def setup():
    global start_time

    size(Cell.canvasX(), Cell.canvasY() )
    background(0)
    noFill()
    strokeWeight(zoom)     # cell size
    noSmooth()
    # strokeCap(PROJECT)   # squared cells
    # frameRate(2)         # slow down

    
    # Cell.place_object(20, 20, o_blinker)
    # Cell.place_object(40, 40, o_toad)
    # Cell.place_object(50, 50, o_beacon)
    # Cell.place_object(70, 20, o_pulsar)
    # Cell.place_object(70, 70, o_penta_decathlon)

    # Cell.place_object(0, 0, o_glider)

    # Cell.place_object(Cell.dimension/2, Cell.dimension/2, o_r_pentomino)
    # Cell.place_object(Cell.dimension/2, Cell.dimension/2, o_diehard)
    # Cell.place_object(Cell.dimension/2, Cell.dimension/2, o_acorn)
    # Cell.place_object(Cell.dimension / 4, Cell.dimension / 4, o_gosper_gun)
    # Cell.place_object(Cell.dimension *2/3, Cell.dimension * 2/3, o_generator1)
    # Cell.place_object(Cell.dimension / 2, Cell.dimension / 2, o_generator2)
    # Cell.place_object(13, Cell.dimension / 2, o_generator3)

    # Cell.place_object(Cell.dimension / 2-25, Cell.dimension / 2, decode_object(o_101P7))
    # Cell.place_object(Cell.dimension / 2, Cell.dimension / 2, decode_object(o_6P2))
    # Cell.place_object(Cell.dimension / 2, Cell.dimension / 2, decode_object(o_12P8))
    # Cell.place_object(Cell.dimension / 6, Cell.dimension / 2, decode_object(o_20P6))
    # Cell.place_object(Cell.dimension / 2, Cell.dimension / 2, decode_object(o_196P5))
    # Cell.place_object(Cell.dimension / 2, Cell.dimension / 2, decode_object(o_132P3H1V0))
    # Cell.place_object(Cell.dimension / 2, Cell.dimension / 2, decode_object(o_213P28H7V0))
    # Cell.place_object(Cell.dimension / 2, Cell.dimension / 2, decode_object(o_180P4H1V1))
    
    Cell.place_object(30, Cell.dimension / 3, decode_object(load_object(name='objects/basic-rakes.rle')))

    start_time = time.time()

def draw():

    are_they_evolving = False

    for cell in Cell.population:

        # does the cell require redraw?
        if cell.alive != cell.new_state:

            # copy status from previous calculation
            cell.alive = cell.new_state

            stroke(255) if cell.alive == 1 else stroke(0)
                
            point(cell.screen_x, cell.screen_y)

    for cell in Cell.population:

        n = cell.count(cell.x, cell.y)

        if cell.alive == 1 and (n < 2 or n > 3):  # kill
            cell.new_state = 0
            are_they_evolving = True

        elif cell.alive == 0 and n == 3:  # born
            cell.new_state = 1
            are_they_evolving = True

        # else:  # remain

    gen = Cell.incGeneration()
    
    print("Generation: {}").format(gen)

    # stop after generations limit
    # if gen == 1000:
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
