from tkinter import *
from copy import deepcopy
import sys
import os


class Display:

    CELL_SIZE = 50

    def __init__(self, agent_pos, room_changes_q, agent_move_q, disp_to_agent_q):
        self.agent_pos = agent_pos
        self.informed = None

        self.room_changes_q = room_changes_q
        self.agent_move_q = agent_move_q
        self.disp_to_agent_q = disp_to_agent_q

        self.window = Tk()
        self.window.title("Aspirobot")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas_list = []
        self.arrow_list = []

        self.vacuum_photo = PhotoImage(file=self.resource_path("img/vacuum.gif"))
        self.dirt_photo = PhotoImage(file=self.resource_path("img/dirt.gif"))
        self.jewel_photo = PhotoImage(file=self.resource_path("img/jewel.gif"))
        self.agent_image = None

    def add_label(self, label):
        grid_x, grid_y = self.window.grid_size()

        tk_label = Label(self.window, text=label)
        tk_label.grid(row=0, column=grid_x)

    def add_grid(self, grid):
        self.window.grid_size()
        new_canvas = Canvas(self.window, width=500, height=500, bd=0)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                self.draw_room(new_canvas, grid[j][i])

        self.draw_agent(new_canvas)
        self.canvas_list.append(new_canvas)

    def add_switch(self):
        self.informed = IntVar()
        self.informed.set(1)
        grid_x = self.window.grid_size()[0]
        informed_button = Checkbutton(self.window, text="Informed", variable=self.informed, command=self.switch_mode).grid(row=0, column=grid_x + 1)

    def start_loop(self):
        self.window.after(1, self.check_for_changes)
        self.window.mainloop()

    def check_for_changes(self):
        while not self.room_changes_q.empty():
            room = self.room_changes_q.get_nowait()
            self.draw_room(self.canvas_list[0], room)

            # Raise agent to top layer (otherwise it's hidden after redraw)
            if room.get_position() == room.get_position():
                for cv in self.canvas_list:
                    cv.tag_raise(self.agent_image)
                    for arrow in self.arrow_list:
                        cv.tag_raise(arrow)

        while not self.agent_move_q.empty():
            new_pos = self.agent_move_q.get_nowait()
            if len(new_pos) == 2:
                self.move_agent(new_pos)
            else:
                self.draw_trajectory(new_pos)
        self.window.after(1, self.check_for_changes)

    def draw_room(self, cv, room):
        cv.create_rectangle(room.x * self.CELL_SIZE,
                            room.y * self.CELL_SIZE,
                            (room.x + 1) * self.CELL_SIZE,
                            (room.y + 1) * self.CELL_SIZE,
                            fill='white')
        if room.has_dirt:
            cv.create_image(room.x * self.CELL_SIZE + 1,
                            room.y * self.CELL_SIZE + self.CELL_SIZE / 2,
                            anchor=NW, image=self.dirt_photo)
        if room.has_jewel:
            cv.create_image(room.x * self.CELL_SIZE + self.CELL_SIZE / 2 - 1,
                            room.y * self.CELL_SIZE + self.CELL_SIZE / 2,
                            anchor=NW, image=self.jewel_photo)

    def draw_agent(self, cv):
        x_agent = 1 + self.CELL_SIZE * self.agent_pos[0]
        y_agent = 1 + self.CELL_SIZE * self.agent_pos[1]
        self.agent_image = cv.create_image(x_agent, y_agent, anchor=NW, image=self.vacuum_photo)
        cv.grid(row=1, column=x_agent - 1)  # We want the grid to be below its label

    def move_agent(self, new_pos):
        x_shift = (1 + self.CELL_SIZE * new_pos[0]) - (1 + self.CELL_SIZE * self.agent_pos[0])
        y_shift = (1 + self.CELL_SIZE * new_pos[1]) - (1 + self.CELL_SIZE * self.agent_pos[1])

        for cv in self.canvas_list:
            cv.move(self.agent_image, x_shift, y_shift)
        self.agent_pos = deepcopy(new_pos)

    def draw_trajectory(self, pos_list):
        for cv in self.canvas_list:
            for line in self.arrow_list:
                cv.delete(line)
        self.arrow_list = []
        line_extremities = list()
        line_extremities.append(pos_list[0])
        pos_list = pos_list[1:]
        while len(pos_list) > 0:
            line_extremities.append(pos_list.pop(0))
            p1 = line_extremities[0].get_position()
            p2 = line_extremities[1].get_position()
            for cv in self.canvas_list:
                new = cv.create_line(p1[0] * self.CELL_SIZE + self.CELL_SIZE/2, p1[1] * self.CELL_SIZE + self.CELL_SIZE/2,
                               p2[0] * self.CELL_SIZE + self.CELL_SIZE/2, p2[1] * self.CELL_SIZE + self.CELL_SIZE/2
                               , fill="red", arrow=LAST)
                self.arrow_list.append(new)
            line_extremities.pop(0)

    def switch_mode(self):
        print("Informed:", self.informed.get())
        self.disp_to_agent_q.put(self.informed.get() == 1)

    def on_closing(self):
        self.window.destroy()

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
