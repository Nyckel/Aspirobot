from environment import Environment
class Captor:

    def IsThereJewel(self,pos):
        grid=Environment.get_grid(self)
        print(pos)
        return (grid[pos[0]][pos[1]]).has_jewel

    def IsThereDirt(self,pos):
        grid = Environment.get_grid(self)
        return grid[pos[0]][pos[1]].has_dirt

