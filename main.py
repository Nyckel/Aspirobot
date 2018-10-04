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
from queue import Queue
from copy import deepcopy


class Simulation:

    def __init__(self):

        agent_to_display = Queue()  # For agent to signal its actions to the display
        agent_to_env = Queue()  # for agent to signal its actions to the environment
        env_to_agent = Queue()  # for environment to signal its mutations to the agent
        env_to_display = Queue()  # for environment to signal its mutations to the display

        display_to_agent = Queue()  # Only used for display to tell agent to switch mode (informed/uninformed)

        self.agent = Agent(env_to_agent, agent_to_env, agent_to_display, display_to_agent)
        self.env = Environment(deepcopy(self.agent.get_position()), agent_to_env, env_to_agent, env_to_display)
        self.display = Display(deepcopy(self.agent.get_position()), env_to_display, agent_to_display, display_to_agent)

        self.display.add_label("Environment")
        self.display.add_grid(self.env.get_grid())

        self.display.add_switch()  # For switching between informed and uninformed search

        self.env.start()
        self.agent.start()
        self.display.start_loop()  # (blocking method)


if __name__ == '__main__':
    Simulation()
