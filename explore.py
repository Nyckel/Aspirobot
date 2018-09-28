from agent import Agent
from environment import Environment
#from agent import Action


class Effector:
    def Up(self):
        Agent.position[1]=Agent.position[1]-1

    def Down(self):
        Agent.position[1]=Agent.position[1]+1

    def Left(self):
        Agent.position[0]=Agent.position[0]-1

    def Right(self):
        Agent.position[0]=Agent.position[0]+1

    def Get_dirt(self):
        actual_room=Environment.grid[Agent.position[0][Agent.position[1]]]
        actual_room.has_dirt=False
        actual_room.has_jewel=False

    def Get_jewel(self):
        actual_room=Environment.grid[Agent.position[0][Agent.position[1]]]
        actual_room.has_jewel=False



"""
class Up(Action):
    def execute(self):
        Agent.position[1]=Agent.position[1]-1
    
    
class Down(Action):
    def execute(self):
        Agent.position[1]=Agent.position[1]+1
		
class Left(Action):
    def execute(self):
        Agent.position[0]=Agent.position[0]-1
		

class Right(Action):
    def execute(self):
        Agent.position[0]=Agent.position[0]+1
		

class Get_dirt(Action):
    def execute(self):
        actual_room=Environment.grid[Agent.position[0][Agent.position[1]]]
        actual_room.has_dirt=False
        actual_room.has_jewel=False

class Get_jewel(Action):
    def execute(self):
        actual_room=Environment.grid[Agent.position[0][Agent.position[1]]]
        actual_room.has_jewel=False
"""



