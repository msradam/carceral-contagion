import math
import random
import numpy
from enum import Enum
import networkx as nx

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid

from .utils import generate_sentence


class State(Enum):
    SUSCEPTIBLE = 0
    INCARCERATED = 1
    RELEASED = 2


def number_state(model, state):
    return sum([1 for a in model.grid.get_all_cell_contents() if a.state is state])


def number_incarcerated(model):
    return number_state(model, State.INCARCERATED)


def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)


def number_released(model):
    return number_state(model, State.RELEASED)


class PopuNetwork(Model):
    """
    The population network
    """

    def __init__(self, num_nodes=100, avg_node_degree=3, initial_outbreak_size=10, race="black"):
        self.num_nodes = num_nodes
        self.race = race
        self.months = 0
        prob = avg_node_degree / self.num_nodes

        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.sentence = generate_sentence(race)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        self.initial_outbreak_size = initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes

        self.datacollector = DataCollector({"Incarcerated": number_incarcerated,
                                            "Susceptible": number_susceptible,
                                            "Released": number_released})

        for i, node in enumerate(self.G.nodes()):
            a = Person(i, self, State.SUSCEPTIBLE, self.sentence)
            self.schedule.add(a)
            self.grid.place_agent(a, node)

        # Begin with some portion of the population in prison
        infected_nodes = self.random.sample(
            self.G.nodes(), self.initial_outbreak_size)
        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.state = State.INCARCERATED

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.months += 1
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()


class Person(Agent):
    def __init__(self, unique_id, model, initial_state, sentence):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.sex = random.choice(('m', 'f'))
        self.sentence = sentence
        self.time_spent = 0

    def infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(
            self.pos, include_center=False)
        susceptible_neighbors = [agent for agent in self.model.grid.get_cell_list_contents(neighbors_nodes) if
                                 agent.state is State.SUSCEPTIBLE]
        for a in susceptible_neighbors:
            if self.sex == 'm':
                if a.sex == 'm' and numpy.random.binomial(1, 0.0301729987453868) == 1:
                    a.state = State.INCARCERATED
                if a.sex == 'f' and numpy.random.binomial(1, 0.000436688659218365) == 1:
                    a.state = State.INCARCERATED

            if self.sex == 'f':
                if a.sex == 'm' and numpy.random.binomial(1, 0.0332053842229949) == 1:
                    a.state = State.INCARCERATED
                if a.sex == 'f' and numpy.random.binomial(1, 0.00801193753900653) == 1:
                    a.state = State.INCARCERATED

    def check_state(self):
        if self.state is State.INCARCERATED:
            if self.time_spent < self.sentence:
                self.time_spent += 1
            else:
                self.state = State.RELEASED

    def step(self):
        if self.state is State.INCARCERATED or self.state is State.RELEASED:
            self.infect_neighbors()
        self.check_state()
