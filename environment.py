import random
from room import Room


class Environment:

    GRID_WIDTH = 10
    GRID_HEIGHT = 10

    PROBA_DIRTY = 0.5
    PROBA_JEWEL = 0.25

    def __init__(self):
        self.grid = [[None for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

        # Replace by numpy array
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                self.grid[row][col] = Room(col, row)

        for i in range(10): # TODO: Replace to have a random number of dirt (in a range...) ?
            x, y = self.place_of_new_dirt()
            self.grid[y][x].add_dirt()

        for i in range(2):
            x, y = self.place_of_new_jewel()
            self.grid[y][x].add_jewel()

    def get_grid(self):
        return self.grid

    def compute_performance_index(self):
        return 0

    def should_there_be_a_new_dirty_space(self):
        return random.random() > self.PROBA_DIRTY

    def place_of_new_dirt(self):
        return int(random.random()*10), int(random.random()*10)

    def should_there_be_a_new_lost_jewel(self):
        return random.random() > self.PROBA_JEWEL

    def place_of_new_jewel(self):
        return int(random.random()*10), int(random.random()*10)

    def generate_dirt(self):

        return True

    def generate_jewel(self):
        return True
