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

        # States
        self.dirt = []
        self.position = []
        self.grid = [[None for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

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


    def ObeserveEnvironmentWithAllMySensors(self):
        Captor.IsThereJewel(self,self.position)
        Captor.IsThereDirt(self,self.position)

    def UpdateMyState(self):
        self.grid=Environment.grid

    def ChooseAnAction(self):
        return 0

    def justDoIt(self):
        return 0

    def run(self):
        while(True):
            self.ObeserveEnvironmentWithAllMySensors(self)
            self.UpdateMyState(self)
            self.ChooseAnAction(self)
            self.justDoIt(self)




    @staticmethod
    def wait():
        time.sleep(1)
