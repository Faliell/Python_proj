import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()

# G.add_node(1)
# G.add_nodes_from([2, 3])
# G.add_nodes_from([
#     (4, {"color": "red"}),
#     (5, {"color": "green"}),
# ])
# H = nx.path_graph(10)
# G.add_nodes_from(H)
#
# G.add_edge(1, 2)
# e = (2, 3)
# G.add_edge(*e)  # unpack edge tuple*
# G.add_edges_from([(1, 2), (1, 3)])
# G.add_edges_from(H.edges)
#
# G.clear()

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

print(G.number_of_nodes())
G.number_of_edges()

DG = nx.DiGraph()
DG.add_edge(2, 1)   # adds the nodes in order 2, 1
DG.add_edge(1, 3)
DG.add_edge(2, 4)
DG.add_edge(1, 2)
assert list(DG.successors(2)) == [1, 4]
assert list(DG.edges) == [(2, 1), (2, 4), (1, 3), (1, 2)]

print(list(G.nodes))

G = nx.petersen_graph()
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold')
subax2 = plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

plt.show()