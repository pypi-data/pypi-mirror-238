
import networkx as nx

def helloword():
    G = nx.Graph()

    G.add_node(1)

    G.add_nodes_from([2, 3])

    G.add_nodes_from([
        (4, {"color": "red"}),
        (5, {"color": "green"}),
    ])



    H = nx.path_graph(10)
    G.add_nodes_from(H)

    G.add_node(H)

    G.add_edge(1, 2)
    e = (2, 3)
    G.add_edge(*e)  # unpack edge tuple*

    G.add_edges_from([(1, 2), (1, 3)])


    G.add_edges_from(H.edges)

    #There are no complaints when adding existing nodes or edges. For example, after removing all nodes and edges,

    G.clear()

    #we add new nodes/edges and NetworkX quietly ignores any that are already present.

    G.add_edges_from([(1, 2), (1, 3)])
    G.add_node(1)
    G.add_edge(1, 2)
    G.add_node("spam")        # adds node "spam"
    G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
    G.add_edge(3, 'm')
    #At this stage the graph G consists of 8 nodes and 3 edges, as can be seen by:

    G.number_of_nodes()
    #8
    G.number_of_edges()
    #3

    #Examing graph

    print(list(G.nodes))
    #[1, 2, 3, 'spam', 's', 'p', 'a', 'm']

#helloword()