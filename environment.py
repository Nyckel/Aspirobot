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

    GRID_WIDTH = 10
    GRID_HEIGHT = 10

    PROBA_DIRTY = 0.7  # 0.9970  # 0.5
    PROBA_JEWEL = 0.92  # 0.9975  # 0.25

    def __init__(self, agent_pos, agent_action_q, room_agent_q, room_display_q):
        super(Environment, self).__init__()
        self.agent_position = agent_pos

        self.agent_action_q = agent_action_q  # Input queue where we read robot actions
        self.room_change_agent_q = room_agent_q  # Output queue where we write changes happening in the grid
        self.room_change_display_q = room_display_q  # Output queue where we write changes happening in the grid
        self.stop_request = Event()

        self.grid = [[Room(x, y) for x in range(self.GRID_WIDTH)] for y in range(self.GRID_HEIGHT)]

        for i in range(10):  # TODO: Replace to have a random number of dirt (in a range...) ?
            self.generate_dirt()

        for i in range(2):
            self.generate_jewel()

    def run(self):
        while not self.stop_request.isSet():
            time.sleep(1)
            # if self.should_there_be_a_new_dirty_space():
            #     self.generate_dirt()
            # if self.should_there_be_a_new_lost_jewel():
            #     self.generate_jewel()

            try:
                new_agent_action = self.agent_action_q.get_nowait()
                if new_agent_action == Action.LEFT:
                    if (self.agent_position[0] >= 1) :
                        self.agent_position[0] -= 1
                elif new_agent_action == Action.UP:
                    if (self.agent_position[1] >= 1):
                        self.agent_position[1] -= 1
                elif new_agent_action == Action.RIGHT:
                    if (self.agent_position[0] <=8 ):
                        self.agent_position[0] += 1
                elif new_agent_action == Action.DOWN:
                    if (self.agent_position[1] <= 8):
                        self.agent_position[1] += 1
                elif new_agent_action == Action.GET_DIRT:
                    agent_room = self.grid[self.agent_position[1]][self.agent_position[0]]
                    if agent_room.has_dirt:
                        self.remove_dirt(agent_room)
                elif new_agent_action == Action.GET_JEWEL:
                    agent_room = self.grid[self.agent_position[1]][self.agent_position[0]]
                    if agent_room.has_jewel:
                        self.remove_jewel(agent_room)
            except Empty:
                continue

    def join(self, timeout=None):
        self.stop_request.set()
        super(Environment, self).join(timeout)

    def get_grid(self):
        return self.grid

    def compute_performance_index(self):
        return 0

    def should_there_be_a_new_dirty_space(self):
        return random.random() > self.PROBA_DIRTY

    def place_of_new_dirt(self):
        return int(random.random()*10), int(random.random()*10)

    def should_there_be_a_new_lost_jewel(self):
        return random.random() > self.PROBA_JEWEL

    def place_of_new_jewel(self):
        return int(random.random()*10), int(random.random()*10)

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

    def remove_dirt(self, room):
        room.remove_dirt()
        self.notify_room_mutation(room)

    def remove_jewel(self, room):
        room.remove_jewel()
        self.notify_room_mutation(room)

    def notify_room_mutation(self, room):
        # TODO: Check if room is in viewing range of agent (for uninformed search)
        self.room_change_agent_q.put(room)
        self.room_change_display_q.put(room)
