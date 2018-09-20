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

from environment import Environment
from agent import Agent
from display import Display


class Simulation:

    def __init__(self):
        self.env = Environment()
        self.agent = Agent(self.env)
        self.display = Display()

        self.display.add_grid(self.env.get_grid(), "Environment")
        # self.display.add_grid(self.agent.get_grid(), "Agent's mental state")

        self.is_running = True
        self.display.start_loop(self.run)

    def run(self):
        if self.is_running:
            if self.env.should_there_be_a_new_dirty_space():
                self.env.generate_dirt()
            if self.env.should_there_be_a_new_lost_jewel():
                self.env.generate_jewel()
        self.display.window.after(1, self.run)


if __name__ == '__main__':
    Simulation()
