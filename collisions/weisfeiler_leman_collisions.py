import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from collections import defaultdict

def is_unique(graph, graphs):
    for g in graphs:
        if nx.is_isomorphic(graph, g):
            return False
    return True

def get_degree_sequence(G):
    return tuple(sorted(d for _, d in G.degree()))

def generate_graphs(degree_sequences, length):
    unique_graphs = defaultdict(list)
    nodes = range(length)

    unique_sums = defaultdict(list)
    for ds in degree_sequences:
        unique_sums[sum(ds)].append(ds)
    for deg_seq_sum, equal_sum_deg_sequences in unique_sums.items():
        for edges in combinations(combinations(nodes, 2), deg_seq_sum//2):
            G = nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            current_deg_seq = get_degree_sequence(G)
            
            if current_deg_seq in equal_sum_deg_sequences and is_unique(G, unique_graphs[current_deg_seq]):
                unique_graphs[current_deg_seq].append(G.copy())
    return unique_graphs

def generate_non_decreasing_sequences(n, max_degree, start=1, current_list=[]):
    
    if len(current_list) == n:
        yield current_list
        return
    
    for i in range(start, max_degree+1):
        # Recurse with the next value, ensuring non-decreasing order
        yield from generate_non_decreasing_sequences(n, max_degree, i, current_list + [i])


def generate_non_decreasing_sequences_opt(n, max_degree, start=1, current_list=[]):
    
    if len(current_list) == n:
        yield current_list
        return
    
    if start == max_degree:
        yield current_list + [start] * (n - len(current_list))
        return
    
    for i in range(start, max_degree+1):
        # Recurse with the next value, ensuring non-decreasing order
        yield from generate_non_decreasing_sequences(n, max_degree, i, current_list + [i])

def generate_non_decreasing_sequences_it(n, max_degree):
    stack = [(1, [])]
    while stack:
        start, current_list = stack.pop()
        if len(current_list) == n:
            yield current_list
        else:
            for i in range(start, max_degree+1):
                stack.append((i, current_list + [i]))

def generate_non_decreasing_sequences_it_opt(n, max_degree):
    stack = [(1, [])]
    while stack:
        start, current_list = stack.pop()
        if len(current_list) == n:
            yield current_list
        else:
            for i in range(start, max_degree+1):
                if i == max_degree:
                    stack.append((n, current_list + [i] * (n - len(current_list))))
                else:
                    stack.append((i, current_list + [i]))

def generate_graphical_sequences(n, max_degree):
    sequences = []
    for sequence in generate_non_decreasing_sequences(n, max_degree):
        if sum(sequence) % 2 == 0 and nx.is_graphical(sequence):
            sequences.append(tuple(sequence))
    return sequences

def find_weisfeiler_leman_collisions():
    
    for n in range(3, 8):
        deg_seq_to_graphs = generate_graphs(generate_graphical_sequences(n, n - 1), n)
            
        for graphs in deg_seq_to_graphs.values():
            for graph1, graph2 in combinations(graphs, 2):
                if nx.weisfeiler_lehman_graph_hash(graph1) == nx.weisfeiler_lehman_graph_hash(graph2):
                    yield (graph1, graph2)



if __name__ == '__main__':
    
    collisions = find_weisfeiler_leman_collisions()

    for graph1, graph2 in collisions:
        with open('graphs.txt', 'a') as f:
            f.write(str(graph1.edges()) + '\n')
            f.write(str(graph2.edges()) + '\n')
            f.write('\n')
    
    c = list(collisions)
    print(len(c))