import random
from room import Room

class Environment:
    GRID_WIDTH = 10
    GRID_HEIGHT = 10
    
    PROBA_DIRTY = 0.5
    PROBA_JEWEL = 0.25
    
    def __init__(self):
        self.grid = [[0 for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

    def get_grid(self):
        return self.grid

    def compute_performance_index(self):
        return 0

    def should_there_be_a_new_dirty_space(self):
        return (random.random()>PROBA_DIRTY)

    def place_of_new_dirty(self):
        return int(random.random()*100) #room_number
    
    def should_there_be_a_new_lost_jewel(self):
        return (random.random()>PROBA_JEWEL)
		
    def place_of_new_jewel(self):
        return int(random.random()*100) #room_number

    def generate_dirt(self):
        
        return True

    def generate_jewel(self):
        return True
