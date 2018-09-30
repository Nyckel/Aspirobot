"""
    8INF846 - Intelligence Artificielle
    Creation d'un agent aspirateur

    Rachel Noireau - Camille Breen - Mathis Ouarnier

    Consignes:
        - Implementation d'un agent aspirateur qui cherche a nettoyer 100 pieces de la poussiere et des bijoux presents
        - Un thread pour l'agent, un pour l'environement.
        - Bonus = implementation d'un module d'apprentissage

        1.L'agent et l’environnement doivent s’executer sur deux fils d’execution differents.
        2.De la poussiere et des bijoux doivent être generes sporadiquement par l’environnement.
        3.L’agent depense une unite d’electricite par action.
        4.Si l’agent aspire et qu’un bijou se trouve a cet endroit, l’environnement devrait considerer que
            celui-ci a ete aspire (le robot n’a pas necessairement a le savoir, puisqu’il ne l’avait pas perçu)
            –Il perd des points pour ça (dans sa mesure de performance)!
        5.L’agent doit posseder un etat mental BDI.
        6.L’agent doit utiliser l’exploration afin de planifier ses actions.
        7.L’agent doit avoir acces a une heuristique pour effectuer de l’exploration informee.
        8.L’agent doit apprendre la meilleure frequence d’exploration par rapport a sa mesure de performance
            (vous pouvez faire un apprentissage episodique)

    Idees pour la mesure de performance :
        - 1 point par carre propre a chaque intervalle de temps
        - Mesure pour verifier qu'il ne nettoie pas toujours la même zone

    Environnement: Completement observable, Stochastique, Sequentiel, Dynamique, Discret, Mono-agent

"""

from environment import Environment
from agent import Agent
from display import Display
from threading import Thread

class Simulation:

    def __init__(self):
        #Thread.__init__(self)
        self.env = Environment()
        self.agent = Agent(self.env)
        self.display = Display(self.agent)

        self.display.add_label("Environment")
        self.display.add_grid(self.env.get_grid())
        # self.display.add_grid(self.agent.get_grid(), "Agent's mental state")

        self.is_running = True
        self.display.start_loop(self.run)

    def environment_run(self):
        if self.is_running:
            if self.env.should_there_be_a_new_dirty_space():
                self.env.generate_dirt()
            if self.env.should_there_be_a_new_lost_jewel():
                self.env.generate_jewel()
        self.display.window.after(1, self.environment_run)

        self.display.add_grid(self.env.get_grid())
        #self.display.window.configure()




    def agen_run(self):
        self.agent.run()

    def run(self):
        Thread(target=self.environment_run).start()
        Thread(target=self.agen_run).start()



if __name__ == '__main__':
    Simulation()

