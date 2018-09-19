"""
    8INF846 - Intelligence Artificielle
    Création d'un agent aspirateur

    Rachel Noireau - Camille Breen - Mathis Ouarnier

    Consignes:
        - Implémentation d'un agent aspirateur qui cherche à nettoyer 100 pièces de la poussière et des bijoux présents
        - Un thread pour l'agent, un pour l'environement.
        - Bonus = implémentation d'un module d'apprentissage

        1.L’agent et l’environnement doivent s’exécuter sur deux fils d’exécution différents.
        2.De la poussière et des bijoux doivent être générés sporadiquement par l’environnement.
        3.L’agent dépense une unité d’électricité par action.
        4.Si l’agent aspire et qu’un bijou se trouve à cet endroit, l’environnement devrait considérer que
            celui-ci a été aspiré (le robot n’a pas nécessairement à le savoir, puisqu’il ne l’avait pas perçu)
            –Il perd des points pour ça (dans sa mesure de performance)!
        5.L’agent doit posséder un état mental BDI.
        6.L’agent doit utiliser l’exploration afin de planifier ses actions.
        7.L’agent doit avoir accès à une heuristique pour effectuer de l’exploration informée.
        8.L’agent doit apprendre la meilleure fréquence d’exploration par rapport à sa mesure de performance
            (vous pouvez faire un apprentissage épisodique)

    Idées pour la mesure de performance :
        - 1 point par carré propre à chaque intervalle de temps
        - Mesure pour vérifier qu'il ne nettoie pas toujours la même zone

    Environnement: Complètement observable, Stochastique, Séquentiel, Dynamique, Discret, Mono-agent

"""

from tkinter import *

from environment import Environment
from agent import Agent


class Simulation:

    def __init__(self):
        self.env = Environment()
        self.agent = Agent(self.env)
        self.window, self.canvas = self.create_board(self.env.get_grid())

        self.is_running = True

        self.window.after(1, self.run)
        self.window.mainloop()

    def create_board(self, grid):
        win = Tk()
        win.title("Aspirobot")
        win.protocol("WM_DELETE_WINDOW", self.on_closing)

        cv = Canvas(win, width=500, height=500, bd=0)
        cv.pack()

        self.vacuum_photo = PhotoImage(file="img/vacuum.gif")
        self.dirt_photo = PhotoImage(file="img/dirt.gif")
        self.jewel_photo = PhotoImage(file="img/jewel.gif")

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                cv.create_rectangle(i * 50, j * 50, (i + 1) * 50, (j + 1) * 50, fill='white')
                if grid[i][j].has_dirt:
                    dirt_image = cv.create_image(i*50+1, j*50+25, anchor=NW, image=self.dirt_photo) # TODO: Find how to keep reference to the image
                if grid[i][j].has_jewel:
                    jewel_image = cv.create_image(i*50+26, j*50+25, anchor=NW, image=self.jewel_photo)

        vacuum_image = cv.create_image(1, 1, anchor=NW, image=self.vacuum_photo) # TODO: Decide if vacuum should start at 0,0 or somewhere else

        return win, cv

    def run(self):
        if self.is_running:
            if self.env.should_there_be_a_new_dirty_space():
                self.env.generate_dirt()
            if self.env.should_there_be_a_new_lost_jewel():
                self.env.generate_jewel()
        self.window.after(1, self.run)

    def on_closing(self):
        # TODO: Join all threads
        self.is_running = False
        self.window.destroy()


if __name__ == '__main__':
    Simulation()
