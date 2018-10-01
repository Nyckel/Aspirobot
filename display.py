from tkinter import *


class Display:

    CELL_SIZE = 50

    def __init__(self, agent_pos, room_changes_q, agent_move_q):
        self.agent_pos = agent_pos

        self.room_changes_q = room_changes_q
        self.agent_move_q = agent_move_q

        self.window = Tk()
        self.window.title("Aspirobot")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas_list = []

        self.vacuum_photo = PhotoImage(file="img/vacuum.gif")
        self.dirt_photo = PhotoImage(file="img/dirt.gif")
        self.jewel_photo = PhotoImage(file="img/jewel.gif")
        self.agent_image = None

    def add_label(self,label):
        grid_x, grid_y = self.window.grid_size()

        tk_label = Label(self.window, text=label)
        tk_label.grid(row=0, column=grid_x)

    def add_grid(self, grid):
        self.window.grid_size()
        new_canvas = Canvas(self.window, width=500, height=500, bd=0)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                self.draw_room(new_canvas, grid[j][i])

        # TODO: Decide if vacuum should start at 0,0 or somewhere else
        self.draw_agent(new_canvas)
        self.canvas_list.append(new_canvas)

    def start_loop(self):
        self.window.after(1, self.check_for_changes)
        self.window.mainloop()

    def check_for_changes(self):
        while not self.room_changes_q.empty():
            room = self.room_changes_q.get_nowait()
            print("In display, received mutation ", room.x, room.y)
            self.draw_room(self.canvas_list[0], room)

        while not self.agent_move_q.empty():
            new_pos = self.agent_move_q.get_nowait()
            self.move_agent(new_pos)
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
        for cv in self.canvas_list:
            cv.move(self.agent_image, new_pos[0] - self.agent_pos[0], new_pos[1] - self.agent_pos[0])
        self.agent_pos = new_pos

    def on_closing(self):
        # TODO: Get event back to main and join all threads
        self.window.destroy()
