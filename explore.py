from agent import Agent
from agent import Action
from environment import Environment

class Up(Action):
    def execute(self):
        Agent.position[1]=Agent.position[1]-1
    
    
class Down(Action):
    def execute(self):
        Agent.position[1]=Agent.position[1]+1
		
class Left(Action):
    def execute(self):
        Agent.position[0]=Agent.position[0]-
		

class Right(Action):
    def execute(self):
        Agent.position[0]=Agent.position[0]+1
		

class Get_dirt(Action):
    def execute(self):
        actual_room=evironement.grid[Agent.position[0][Agent.position[1]]
        actual_room.has_dirt=false
        actual_room.has_jewel=false

class Get_jewzl(Action):
    def execute(self):
        actual_room=evironement.grid[Agent.position[0][Agent.position[1]]
        actual_room.has_jewel=false