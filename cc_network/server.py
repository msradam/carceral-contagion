import math
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import TextElement
from .model import PopuNetwork, State, number_incarcerated, number_released


def network_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return {
            State.INCARCERATED: '#FF0000',
            State.SUSCEPTIBLE: '#008000',
            State.RELEASED: '#FFA500'
        }.get(agent.state, '#808080')

    def edge_color(agent1, agent2):
        return '#e8e8e8'

    def edge_width(agent1, agent2):
        return 2

    def get_agents(source, target):
        return G.node[source]['agent'][0], G.node[target]['agent'][0]

    portrayal = dict()
    portrayal['nodes'] = [{'size': 6,
                           'color': node_color(agents[0]),
                           'tooltip': "id: {}<br>state: {}".format(agents[0].unique_id, agents[0].state.name),
                           }
                          for (_, agents) in G.nodes.data('agent')]

    portrayal['edges'] = [{'source': source,
                           'target': target,
                           'color': edge_color(*get_agents(source, target)),
                           'width': edge_width(*get_agents(source, target)),
                           }
                          for (source, target) in G.edges]

    return portrayal


network = NetworkModule(network_portrayal, 1000, 1000, library='d3')
chart = ChartModule([{'Label': 'incarcerated', 'Color': '#FF0000'},
                     {'Label': 'Susceptible', 'Color': '#008000'}])


class MyTextElement(TextElement):
    def render(self, model):
        months_passed = str(model.months)
        incarcerated_text = str(number_incarcerated(model))
        released_text = str(number_released(model))

        return "Months Passed: {}<br>Incarcerated: {}<br>Released:{}".format(months_passed, incarcerated_text, released_text)


model_params = {
    'num_nodes': UserSettableParameter('slider', 'Number of individuals', 100, 50, 300, 1,
                                       description='Choose the number of individuals in the population'),
    'avg_node_degree': UserSettableParameter('slider', 'Relationships per individual', 3, 3, 8, 1,
                                             description='Choose how many close relationships each individual has.'),
    'initial_outbreak_size': UserSettableParameter('slider', 'Initial number of incarcerated persons', 10, 10, 25, 1,
                                                   description='Choose the number of incarcerated persons at the beginning of the simulation.'),
    'race': UserSettableParameter('choice', 'Population Race', value='black', choices=['black', 'white']),
}

server = ModularServer(
    PopuNetwork, [network, MyTextElement()], 'Carceral Contagion', model_params)
