import time
from enum import Enum
from environment import Environment
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


class Agent:
    GRID_WIDTH = 10
    GRID_HEIGHT = 10

    informed=False

    def __init__(self, env):

        self.env=env

        # States
        self.dirt = []
        self.position = [0,0]
        self.gridRobot = [[None for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

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

    def get_gridRobot(self):
        return self.gridRobot

    def set_position(self,pos):
        self.position=pos


    def ObeserveEnvironmentWithAllMySensors(self):
        Captor.IsThereJewel(self.env,self.position)
        Captor.IsThereDirt(self.env,self.position)

    def UpdateMyState(self):
        self.gridRobot=Environment.get_grid(self.env)

    def ChooseAnAction(self):
        return 0

    def justDoIt(self):
        Effector.Down(self) #a changer
        return 0

    @staticmethod
    def wait():
        time.sleep(1)

    def run(self):
        while(True):
            self.ObeserveEnvironmentWithAllMySensors()
            self.UpdateMyState()
            self.ChooseAnAction()
            self.justDoIt()
            self.wait()








class Effector:
    def Up(self):
        position=Agent.get_position(self)
        if (0 <= position[1] - 1 & position[1] - 1 <= 9):
            position[1]=position[1]-1
            Agent.set_position(self,position)

    def Down(self):
        position = Agent.get_position(self)
        if(0<=position[1]+1 & position[1]+1<=9):
            position[1]=position[1]+1
            Agent.set_position(self,position)

    def Left(self):
        position = Agent.get_position(self)
        if (0 <= position[0] - 1 & position[0] - 1 <= 9):
            position[0] =position[0] - 1
            Agent.set_position(self,position)

    def Right(self):
        position = Agent.get_position(self)
        if (0 <= position[0] + 1 & position[0] + 1 <= 9):
            position[0]=position[0]+1
            Agent.set_position(self,position)

    def Get_dirt(self):
        position = Agent.get_position(self)
        actual_room=Environment.grid[position[0]][position[1]]
        actual_room.has_dirt=False
        actual_room.has_jewel=False

    def Get_jewel(self):
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
        return destdest;

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