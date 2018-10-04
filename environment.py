import random
import time

from threading import Thread, Event
from queue import Queue, Empty

from room import Room
from agent import Action


class Environment(Thread):
    """ A thread managing lifecycle of the environment.
        It randomly generates dust and jewels and manages room state changes.

        It receives robot actions by reading in a Queue
        It sends room changes by writing them in a Queue
    """
    #Size of the manor
    GRID_WIDTH = 10
    GRID_HEIGHT = 10

    #Probability for generate dirt or jewel
    PROBA_DIRTY = 0.80  # 0.9970  # 0.5
    PROBA_JEWEL = 0.97  # 0.9975  # 0.25

    def __init__(self, agent_pos, agent_action_q, room_agent_q, room_display_q):
        super(Environment, self).__init__()
        self.agent_position = agent_pos

        self.agent_action_q = agent_action_q  # Input queue where we read robot actions
        self.room_change_agent_q = room_agent_q  # Output queue where we write changes happening in the grid
        self.room_change_display_q = room_display_q  # Output queue where we write changes happening in the grid
        self.stop_request = Event()

        self.grid = [[Room(x, y) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

        self.performance = 50 #Initial performance is 50 it's increase when the aspirobot get dirt or jewel

        for i in range(10):  # TODO: Replace to have a random number of dirt (in a range...) ?
            self.generate_dirt()

        for i in range(2):
            self.generate_jewel()

    #Update the environnement after generation or aspirobot's action
    #Calculate performance
    def run(self):
        while not self.stop_request.isSet():
            time.sleep(1)
            if self.should_there_be_a_new_dirty_space():
                self.generate_dirt()
            if self.should_there_be_a_new_lost_jewel():
                self.generate_jewel()

            try:
                new_agent_action = self.agent_action_q.get_nowait()
                if new_agent_action == Action.LEFT:
                    self.perf_move()
                    if (self.agent_position[0] >= 1) :
                        self.agent_position[0] -= 1
                elif new_agent_action == Action.UP:
                    self.perf_move()
                    if (self.agent_position[1] >= 1):
                        self.agent_position[1] -= 1
                elif new_agent_action == Action.RIGHT:
                    self.perf_move()
                    if (self.agent_position[0] <=8 ):
                        self.agent_position[0] += 1
                elif new_agent_action == Action.DOWN:
                    self.perf_move()
                    if (self.agent_position[1] <= 8):
                        self.agent_position[1] += 1
                elif new_agent_action == Action.GET_DIRT:
                    agent_room = self.grid[self.agent_position[1]][self.agent_position[0]]
                    self.perf_dirt(agent_room)
                    if agent_room.has_dirt:
                        self.remove_dirt(agent_room)
                    if agent_room.has_jewel:
                        self.remove_jewel(agent_room)
                elif new_agent_action == Action.GET_JEWEL:
                    self.perf_jewel()
                    agent_room = self.grid[self.agent_position[1]][self.agent_position[0]]
                    if agent_room.has_jewel:
                        self.remove_jewel(agent_room)
                print(self.performance)
            except Empty:
                continue

    def join(self, timeout=None):
        self.stop_request.set()
        super(Environment, self).join(timeout)

    #return grid
    def get_grid(self):
        return self.grid

    def compute_performance_index(self):
        return 0
    #return performance
    def get_performance(self):
        return self.performance

    #Decide if we generate dirty
    def should_there_be_a_new_dirty_space(self):
        return random.random() > self.PROBA_DIRTY

    #Found a place to generate dirt
    def place_of_new_dirt(self):
        return int(random.random()*10), int(random.random()*10)

    #Decide if we generate a jewel
    def should_there_be_a_new_lost_jewel(self):
        return random.random() > self.PROBA_JEWEL

    #Found a place to generate jewel
    def place_of_new_jewel(self):
        return int(random.random()*10), int(random.random()*10)

    #generation of dirty in a room
    def generate_dirt(self):
        room_ok = False
        room = None
        while not room_ok:
            x, y = self.place_of_new_dirt()
            room = self.grid[y][x]
            if not room.has_dirt:
                room_ok = True

        room.add_dirt()
        self.notify_room_mutation(room)

    #generation of jewel in a room
    def generate_jewel(self):
        room_ok = False
        room = None
        while not room_ok:
            x, y = self.place_of_new_jewel()
            room = self.grid[y][x]
            if not room.has_jewel:
                room_ok = True

        room.add_jewel()
        self.notify_room_mutation(room)

    #Delete dirty
    def remove_dirt(self, room):
        room.remove_dirt()
        self.notify_room_mutation(room)

    #Delete jewel
    def remove_jewel(self, room):
        room.remove_jewel()
        self.notify_room_mutation(room)

    def notify_room_mutation(self, room):
        # TODO: Check if room is in viewing range of agent (for uninformed search)
        self.room_change_agent_q.put(room)
        self.room_change_display_q.put(room)

    #Update performance for each action
    def calc_performance(self, action, room):
        if action == Action.GET_DIRT :
            if room.has_jewel :
                self.performance = ((self.performance - 31)/111)*100
            else :
                self.performance = ((self.performance + 11)/111)*100
        if action == Action.GET_JEWEL :
            self.performance = ((self.performance + 11)/111)*100
        if action == Action.DOWN or Action.LEFT or Action.RIGHT or Action.UP:
            self.performance = ((self.performance - 1)/101)*100

    #Update performance after Get dirt action
    def perf_dirt(self, room):
        if room.has_jewel:
            self.performance = ((self.performance - 31) / 111) * 100
        else:
            self.performance = ((self.performance + 11) / 111) * 100

    #Update performance after Get jewel action
    def perf_jewel(self):
        self.performance = ((self.performance + 11) / 111) * 100

    #Update performance after movement action
    def perf_move(self):
        self.performance = ((self.performance - 1) / 101) * 100
