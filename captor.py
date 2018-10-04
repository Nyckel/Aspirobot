from environment import Environment


class Captor:

    #Show if the room has a jewel
    def IsThereJewel(self,pos):
        grid=Environment.get_grid(self)
        print(pos)
        return (grid[pos[0]][pos[1]]).has_jewel

    #Show if the room has dirty
    def IsThereDirt(self,pos):
        grid = Environment.get_grid(self)
        return grid[pos[0]][pos[1]].has_dirt

