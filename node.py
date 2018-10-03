from heapq import heappush


class Node:
    def __init__(self, p_pos, other_nodes_list):
        print("Creating node with pos ", p_pos, " and children ", other_nodes_list)
        self.pos = p_pos
        # self.childrens = []
        self.other_nodes_list = other_nodes_list

    def get_position(self):
        return self.pos

    def is_goal(self):
        return len(self.other_nodes_list) == 0  # As it means we would have cleaned all dirty rooms

    def get_children(self):
        print("Getting children of ", self.pos, " -> ", [Node(room.get_position(), self.other_nodes_list.copy().remove(room))
                for room in self.other_nodes_list])
        return [Node(room.get_position(), self.other_nodes_list.copy().remove(room))
                for room in self.other_nodes_list]

    def cost_to(self, other_room):
        return abs(self.pos[0] - other_room.get_position()[0]) + abs(self.pos[1] - other_room.get_position()[1])

    def heuristic_to_goal(self):
        remaining_items_value = 0
        distance_sum = 0
        print("Accessing heuristics for ", self.pos, " with children ", self.other_nodes_list)
        if self.other_nodes_list is None:
            print("Children NONE for ", self.pos)
        for room in self.other_nodes_list:
            if room.has_dirt:
                remaining_items_value += 10
            if room.has_jewel:
                remaining_items_value += 15
            distance_sum += self.cost_to(room)
        return remaining_items_value + distance_sum / 2


    # def generate_children(self):
    #     for room in self.other_nodes_list:
    #         heappush(self.childrens,
    #                  (self.evaluate_f(room),
    #                   Node(room.get_position(), self.other_nodes_list.copy().remove(room))))
    #     return self.childrens

    # def evaluate_f(self, room):

