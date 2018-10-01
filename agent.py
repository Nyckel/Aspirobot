import time
from threading import Thread, Event
from queue import Queue

from enum import Enum
# from environment import Environment
from room import Room
# from captor import Captor


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

    informed = False

    def __init__(self, room_change_q, agent_action_env_q, agent_action_disp_q):

        super(Agent, self).__init__()
        self.room_change_q = room_change_q  # Input queue where we read changes happening in the grid (seen by sensors)
        self.agent_action_env_q = agent_action_env_q  # Output queue where we write robot actions
        self.agent_action_disp_q = agent_action_disp_q  # Output queue where we write robot actions
        self.stop_request = Event()

        # States
        self.dirt = []
        self.position = [0,0]
        self.grid = [[Room(x, y) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

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

    def get_grid(self):
        return self.grid

    def set_position(self,pos):
        self.position=pos

    def observe_environment_with_sensors(self):
        while not self.room_change_q.empty():
            room = self.room_change_q.get_nowait()
            self.grid[room.y][room.x] = room  # TODO: Maybe have a class GridRepresentation with a mutate() method

        # Captor.IsThereJewel(self.env,self.position)
        # Captor.IsThereDirt(self.env,self.position)

    def update_state(self):
        pass
        # self.grid=Environment.get_grid(self.env)

    def plan_actions(self):
        # For testing purpose. TODO: Replace by exploration algorithm
        for i in range(9):
            self.actions_planned.put(Action.RIGHT)
            self.actions_planned.put(Action.GET_DIRT)
            self.actions_planned.put(Action.GET_JEWEL)
        for i in range(9):
            self.actions_planned.put(Action.DOWN)
            self.actions_planned.put(Action.GET_DIRT)
            self.actions_planned.put(Action.GET_JEWEL)

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
            if self.actions_planned.empty():
                self.plan_actions() # TODO: Learn exploration frequency
            self.execute_next_action()
            self.wait()

    def join(self, timeout=None):
        self.stop_request.set()
        super(Agent, self).join(timeout)

    def is_move_action(self, action):
        return action in self.move_actions

class Effector:

    def up(self):
        position = Agent.get_position(self)
        if (0 <= position[1] - 1 & position[1] - 1 <= 9):
            position[1]=position[1]-1
            Agent.set_position(self,position)

    def down(self):
        position = Agent.get_position(self)
        if(0<=position[1]+1 & position[1]+1<=9):
            position[1]=position[1]+1
            Agent.set_position(self,position)

    def left(self):
        position = Agent.get_position(self)
        if (0 <= position[0] - 1 & position[0] - 1 <= 9):
            position[0] =position[0] - 1
            Agent.set_position(self,position)

    def right(self):
        position = Agent.get_position(self)
        if (0 <= position[0] + 1 & position[0] + 1 <= 9):
            position[0]=position[0]+1
            Agent.set_position(self,position)

    def get_dirt(self):
        position = Agent.get_position(self)
        actual_room=Environment.grid[position[0]][position[1]]
        actual_room.has_dirt=False
        actual_room.has_jewel=False

    def get_jewel(self):
        position = Agent.get_position(self)
        actual_room=Environment.grid[position[0]][position[1]]
        actual_room.has_jewel=False

    def explore_close(self):
        dest = self.dirt
        waist = self.dirt.shape
        min = abs(self.dirt[0][0] - self.position[0][0] + self.dirt[1][0] - self.position[1][0])
        coord = self.dirt[0]
        for i in range(1, waist[1]):
            dest[0][i] = -1
            dest[1][i] = -1
            test = abs(self.dirt[0][i] - self.position[0][i] + self.dirt[1][i] - self.position[1][i])
            if test < min :
                min = test
                coord[0]=self.dirt[0][i]
                coord[1] = self.dirt[1][i]

        if min < 10 :
             dest[0][0] = coord[0]
             dest[1][0] = coord[1]
             return dest;

        return dest;

    def explore_by_area(self):
        dest = self.dirt
        waist = self.dirt.shape
        coord = self.dirt[0]
        min = abs(self.dirt[0][0] - self.position[0][0] + self.dirt[1][0] - self.position[1][0])
        for j in range(0, waist[1]):
            min = min + abs(self.dirt[0][0] - self.dirt[0][0] + self.dirt[1][0] - self.dirt[1][0])

        for i in range(1, waist[1]):
            test = abs(self.dirt[0][i] - self.position[0][i] + self.dirt[1][i] - self.position[1][i])
            for j in range(0,waist[1]):
                test = test + abs(self.dirt[0][i] - self.dirt[0][j] + self.dirt[1][i] - self.dirt[1][j])
            if test < min:
                min = test
                coord[0] = self.dirt[0][i]
                coord[1] = self.dirt[1][i]
            dest[0][0] = coord[0]
            dest[1][0] = coord[1]
        return dest;

    def shorter_way(self,dest,node):
        waist = self.node.shape
        coord = [-1,-1]
        lastcoord  = [dest[0][0],dest[1][0]]
        min = abs(self.node[0][0] - lastcoord[0] + self.node[1][0] - lastcoord[1])
        for i in range(1, waist[1]):
            test = abs(self.node[0][i] - lastcoord[0] + self.node[1][i] - lastcoord[1])
            if test < min:
                min = test
                coord[0] = self.node[0][i]
                coord[1] = self.node[1][i]
        node.remove(coord)
        dest.add(coord)
        lastcoord == coord
        return dest;
