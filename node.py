class Node:
    def __init__(self, p_room, other_nodes_list):
        # print("Creating node with pos", p_room.get_position(), "and children", len(other_nodes_list))
        self.room = p_room
        self.children = other_nodes_list

    def get_position(self):
        return self.room.get_position()

    def is_goal(self):
        return len(self.children) == 0  # As it means we would have cleaned all dirty rooms

    def has_dirt(self):
        return self.room.has_dirt

    def has_jewel(self):
        return self.room.has_jewel

    def get_children(self):
        # print("Getting children of", self.room.get_position(), "who has", len(self.children), "children")
        children = []
        for room in self.children:
            cp = self.children.copy()
            cp.remove(room)
            children.append(Node(room, cp))

        # print("Getting children of ", self.pos, " -> ", children)
        return children

    def cost_to(self, other_room):
        other_pos = other_room.get_position()
        return abs(self.room.get_position()[0] - other_pos[0]) + abs(self.room.get_position()[1] - other_pos[1])

    def heuristic_to_goal(self):
        remaining_items_value = 0
        distance_sum = 0
        # print("Accessing heuristics for ", self.pos, " with children ", self.other_nodes_list)
        for room in self.children:
            # if room.has_dirt:
            #     remaining_items_value += 1
            # if room.has_jewel:
            #     remaining_items_value += 1
            distance_sum += self.cost_to(room)
        return remaining_items_value + distance_sum / 3

    def __lt__(self, other):
        return True
