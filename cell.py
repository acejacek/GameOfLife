

class Cell:

    population = []
    zoom = 4
    density = 0.05
    dimension = 100
    generation = 0

    def __init__(self, x, y, alive=0):
        self.x = x
        self.y = y
        self.screen_x = x * Cell.zoom
        self.screen_y = y * Cell.zoom
        self.alive = alive
        self.new_state = self.alive

        self.population.append(self)

    @classmethod
    def incGeneration(cls):
        Cell.generation += 1
        return Cell.generation

    @classmethod
    def canvasX(cls):
        return Cell.dimension * Cell.zoom

    @classmethod
    def canvasY(cls):
        return Cell.canvasX()

    @classmethod
    def place_object(cls, x, y, object):

        for yoff, x_row in enumerate(object, y):
            if yoff >= 0 and yoff < Cell.dimension:
                for xoff, cell_state in enumerate(x_row, x):
                    if xoff >= 0 and xoff < Cell.dimension:
                        Cell.population[
                            xoff + yoff * Cell.dimension].new_state = cell_state

    @classmethod
    def count(cls, x, y):
        """ count how many neighbours are around cell """

        def get_cell_status(x, y):

            if x >= 0 and x < Cell.dimension and y >= 0 and y < Cell.dimension:
                return Cell.population[x + y * Cell.dimension].alive
            else:
                return 0
            
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

    @classmethod
    def new_count(cls, x, y):
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
            if cx >= 0 and cx < Cell.dimension and cy >= 0 and cy < Cell.dimension:
                result += Cell.population[cx + cy * Cell.dimension].alive
                if result > 3:
                    # don't count any longer, it will not change the end effect
                    return result

        return result

    @staticmethod
    def create(dimension, zoom, density):
        """ initiate population """

        if len(Cell.population) == 0:
            Cell.dimension = dimension
            Cell.zoom = zoom
            Cell.density = density
            for y in range(Cell.dimension):
                for x in range(Cell.dimension):

                    alive = 0
                    if Cell.density > 0:
                        if random(1) < Cell.density:
                            alive = 1

                    Cell(x, y, alive)
        else:
            print("Popoulation already exists")
