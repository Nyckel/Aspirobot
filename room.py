
class Room:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_dirt = False
        self.has_jewel = False

    def get_position(self):
        return self.x, self.y

    def get_position_x(self):
        return self.x

    def get_position_y(self):
        return self.y

    def add_dirt(self):
        self.has_dirt = True

    def add_jewel(self):
        self.has_jewel = True

    def remove_dirt(self):
        self.has_dirt = False

    def remove_jewel(self):
        self.has_jewel = False
