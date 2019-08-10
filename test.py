import networkx as nx

G = nx.erdos_renyi_graph(50, (3 / 50))
for i, node in enumerate(G.nodes()):
    print(i, node)
