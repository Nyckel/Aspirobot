from environment import Environment
class Captor:

    def IsThereJewel(self,pos):
        return Environment.grid[pos[0]][pos[1]].has_jewel

    def IsThereDirt(self,pos):
        return Environment.grid[pos[0]][pos[1]].has_dirt

