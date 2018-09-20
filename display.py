from tkinter import *


class Display:

    def __init__(self):
        self.window = Tk()
        self.window.title("Aspirobot")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.vacuum_photo = PhotoImage(file="img/vacuum.gif")
        self.dirt_photo = PhotoImage(file="img/dirt.gif")
        self.jewel_photo = PhotoImage(file="img/jewel.gif")

    def add_grid(self, grid, label):
        grid_x, grid_y = self.window.grid_size()

        tk_label = Label(self.window, text=label)
        tk_label.grid(row=0, column=grid_x)

        new_canvas = Canvas(self.window, width=500, height=500, bd=0)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                new_canvas.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='white')
                if grid[i][j].has_dirt:
                    # TODO: Find how to keep reference to the image
                    new_canvas.create_image(i * 50 + 1, j * 50 + 25, anchor=NW, image=self.dirt_photo)
                if grid[i][j].has_jewel:
                    new_canvas.create_image(i * 50 + 26, j * 50 + 25, anchor=NW, image=self.jewel_photo)

        # TODO: Decide if vacuum should start at 0,0 or somewhere else
        new_canvas.create_image(1, 1, anchor=NW, image=self.vacuum_photo)
        new_canvas.grid(row=1, column=grid_x)

    def start_loop(self, method):
        self.window.after(1, method)
        self.window.mainloop()

    def on_closing(self):
        # TODO: Get event back to main and join all threads
        self.window.destroy()
