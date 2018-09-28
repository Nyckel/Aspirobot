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

    def ObeserveEnvironmentWithAllMySensors(self):
        Captor.IsThereJewel(self.env,self.position)
        Captor.IsThereDirt(self.env,self.position)

    def UpdateMyState(self):
        self.gridRobot=Environment.get_grid(self.env)
        print(self.gridRobot)

    def ChooseAnAction(self):
        return 0

    def justDoIt(self):
        Effector.Down(self)
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
        position[1]=position[1]-1

    def Down(self):
        position = Agent.get_position(self)
        if(0<=position[1]+1 & position[1]+1<=9):
            position[1]=position[1]+1

    def Left(self):
        position = Agent.get_position(self)
        position[0]=position[0]-1

    def Right(self):
        position = Agent.get_position(self)
        position[0]=position[0]+1

    def Get_dirt(self):
        position = Agent.get_position(self)
        actual_room=Environment.grid[position[0][position[1]]]
        actual_room.has_dirt=False
        actual_room.has_jewel=False

    def Get_jewel(self):
        position = Agent.get_position(self)
        actual_room=Environment.grid[position[0][position[1]]]
        actual_room.has_jewel=False
