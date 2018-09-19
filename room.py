
class Room:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_dirt = False
        self.has_jewel = False

    def add_dirt(self):
        self.has_dirt = True

    def add_jewel(self):
        self.has_jewel = True
