import time
from threading import Thread, Event
from queue import Queue
from heapq import heappop, heappush

from enum import Enum
from room import Room
from node import Node


class Action(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    GET_JEWEL = 5
    GET_DIRT = 6
    WAIT = 7


class Agent(Thread):
    """ A thread managing lifecycle of the agent.
        It uses its representation of the world, its goal
        and its exploration algorithm to plan for its next actions.

        It receives room changes by reading in a Queue
        It sends its actions by writing them in a Queue
    """
    GRID_WIDTH = 10
    GRID_HEIGHT = 10
    EXPLORATION_INTERVAL = 20

    def __init__(self, room_change_q, agent_action_env_q, agent_action_disp_q):

        super(Agent, self).__init__()
        # Communication mechanism
        self.room_change_q = room_change_q  # Input queue where we read changes happening in the grid (seen by sensors)
        self.agent_action_env_q = agent_action_env_q  # Output queue where we write robot actions
        self.agent_action_disp_q = agent_action_disp_q  # Output queue where we write robot actions
        self.stop_request = Event()

        # States
        self.informed = True
        self.interesting_rooms = []  # rooms dirty or with jewel
        self.rooms_planned = [] # plan of destination
        self.position = [0, 0]
        self.grid = [[Room(x, y) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]
        self.exploration_interval_cnt = self.EXPLORATION_INTERVAL

        # Actions
        self.actions_possibles = [
            Action.UP,
            Action.RIGHT,
            Action.DOWN,
            Action.LEFT,
            Action.GET_JEWEL,
            Action.GET_DIRT,
            Action.WAIT
        ]

        self.move_actions = [
            Action.UP,
            Action.RIGHT,
            Action.DOWN,
            Action.LEFT
        ]

        self.actions_planned = Queue()  # List of actions planned for the agent, they will be executed sequentially

    def get_position(self):
        return self.position

    def get_dest(self):
        return self.dest

    def get_grid(self):
        return self.grid

    def set_position(self,pos):
        self.position=pos

    #Observation of the environment by the aspirobot
    def observe_environment_with_sensors(self):
        while not self.room_change_q.empty():
            room = self.room_change_q.get_nowait()
            self.grid[room.y][room.x] = room  # TODO: Maybe have a class GridRepresentation with a mutate() method
            if room.has_dirt or room.has_jewel:
                self.interesting_rooms.append(room)
            elif room in self.interesting_rooms:
                self.interesting_rooms.remove(room)

    def update_state(self):
        pass
        # self.grid=Environment.get_grid(self.env)

    def plan_actions(self):
        while not self.actions_planned.empty():
            self.actions_planned.get()

        start_room = self.grid[self.position[1]][self.position[0]]
        start_node = Node(start_room, self.interesting_rooms.copy())
        self.rooms_planned = []
        self.rooms_planned.append(start_node)

        if self.informed:
            print("Explore A*", len(self.interesting_rooms))

            self.explore_a_star(start_node, self.rooms_planned)
        else:
            self.explore_iterative_deep_search(start_node, self.rooms_planned, 99)
            print("Here, nodes rooms to explore: ", len(self.rooms_planned))

        self.agent_action_disp_q.put(self.rooms_planned.copy())
        for node in self.rooms_planned:
            print(node.get_position())
        # Generate action_suite from dirty room ordered list
        self.generate_moves_from_path()
        self.exploration_interval_cnt = self.EXPLORATION_INTERVAL

    def explore_a_star(self, start_node, output_list):

        frontier = []
        heappush(frontier, (0, start_node))
        came_from = dict()
        partial_cost = dict()
        came_from[start_node] = None
        partial_cost[start_node] = 0
        current = None

        while not len(frontier) == 0:
            current_priority, current = heappop(frontier)
            if current.is_goal():
                break

            for child in current.get_children():
                cost_to_child = partial_cost[current] + current.cost_to(child)
                if child not in partial_cost or cost_to_child < partial_cost[child]:
                    partial_cost[child] = cost_to_child
                    priority = cost_to_child + child.heuristic_to_goal()
                    heappush(frontier, (priority, child))
                    came_from[child] = current

        output_list.append(current)
        if current.is_goal():
            while came_from[current] is not None:
                output_list.insert(0, came_from[current])
                current = came_from[current]

    # exploration non informée
    def depth_limited_search(self, start_node, output_list, limit):
        return self.recursive_dls(start_node, output_list, limit, 0)

    def recursive_dls(self, node, output_list,limit, depth):
        sol_found = False
        if node.is_goal():
            return node, True
        elif depth == limit:  # profondeur à laquelle on est actuellement
            return None, sol_found
        else:
            for child_node in node.get_children() :
                result, sol_found = self.recursive_dls(child_node, limit, depth+1)
                if sol_found:
                    output_list.append(child_node)
                return result, sol_found

    def explore_iterative_deep_search(self, start_node, output_list, max_depth):
        for depth in range(max_depth):
            result, sol_found = self.depth_limited_search(depth, start_node, output_list)
            if sol_found:
                print("Sol found with depth", depth, result, result.get_position())
                output_list.append(result)
                break

    def generate_moves_from_path(self):
        line_extremities = list()
        line_extremities.append(self.rooms_planned[0])
        self.rooms_planned = self.rooms_planned[1:]
        while len(self.rooms_planned) > 0:
            line_extremities.append(self.rooms_planned.pop(0))
            x1, y1 = line_extremities[0].get_position()
            x2, y2 = line_extremities[1].get_position()
            x_diff = x1 - x2
            y_diff = y1 - y2
            for i in range(x_diff):
                self.actions_planned.put(Action.LEFT)
            for i in range(-x_diff):
                self.actions_planned.put(Action.RIGHT)
            for i in range(y_diff):
                self.actions_planned.put(Action.UP)
            for i in range(-y_diff):
                self.actions_planned.put(Action.DOWN)
            if line_extremities[1].has_jewel():  # TODO: Find a way to make that accessible from Node obj
                self.actions_planned.put(Action.GET_JEWEL)
            if line_extremities[1].has_dirt():  # TODO: Find a way to make that accessible from Node obj
                self.actions_planned.put(Action.GET_DIRT)

            line_extremities.pop(0)

    def execute_next_action(self):
        """ Action execution simply consists of sending what the agent does to the environment (and the display) """
        if not self.actions_planned.empty():
            next_action = self.actions_planned.get_nowait()
            if next_action == Action.LEFT:
                self.position[0] -= 1
            elif next_action == Action.RIGHT:
                self.position[0] += 1
            elif next_action == Action.UP:
                self.position[1] -= 1
            elif next_action == Action.DOWN:
                self.position[1] += 1

            print("Agent: Doing action ", next_action, ", pos: ", self.position)
            if self.is_move_action(next_action):
                self.agent_action_disp_q.put(self.position)
            self.agent_action_env_q.put(next_action)

    @staticmethod
    def wait():
        time.sleep(1)

    def run(self):
        while not self.stop_request.isSet():
            self.observe_environment_with_sensors()
            self.update_state()
            if self.actions_planned.empty() or self.exploration_interval_cnt == 0:
                self.plan_actions()  # TODO: Learn exploration frequency
            self.execute_next_action()
            self.wait()
            self.exploration_interval_cnt -= 1

    def join(self, timeout=None):
        self.stop_request.set()
        super(Agent, self).join(timeout)

    def is_move_action(self, action):
        return action in self.move_actions
