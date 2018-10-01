import time
from threading import Thread, Event
from queue import Queue

from enum import Enum
from environment import Environment
from room import Room
from captor import Captor


class Action(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    GET_JEWEL = 5
    GET_DIRT = 6
    WAIT = 7

    def execute(self):
        return 0


class Agent(Thread):
    """ A thread managing lifecycle of the agent.
        It uses its representation of the world, its goal
        and its exploration algorithm to plan for its next actions.

        It receives room changes by reading in a Queue
        It sends its actions by writing them in a Queue
    """
    GRID_WIDTH = 10
    GRID_HEIGHT = 10

    informed=False

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

    def get_position(self):
        return self.position

    def get_grid(self):
        return self.grid

    def set_position(self,pos):
        self.position=pos

    def observe_environment_with_sensors(self):
        while not self.room_change_q.empty():
            x, y, room = self.room_change_q.get_nowait()
            self.grid[y][x] = room  # TODO: Maybe have a class GridRepresentation with a mutate() method
            # self.room_change_q.put((self.name, ))

        # Captor.IsThereJewel(self.env,self.position)
        # Captor.IsThereDirt(self.env,self.position)

    def update_state(self):
        pass
        # self.grid=Environment.get_grid(self.env)

    def choose_an_action(self):
        return 0

    def just_do_it(self):
        Effector.down(self)  # a changer
        return 0

    @staticmethod
    def wait():
        time.sleep(1)

    def run(self):
        while not self.stop_request.isSet():
            print("Agent loop")
            self.observe_environment_with_sensors()
            self.update_state()
            self.choose_an_action()
            self.just_do_it()
            self.wait()

    def join(self, timeout=None):
        self.stop_request.set()
        super(Agent, self).join(timeout)






class Effector:

    def up(self):
        position=Agent.get_position(self)
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