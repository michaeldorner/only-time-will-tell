import networkx as nx


def time_ignoring(B: nx.Graph, node, check_bipartite: bool = False) -> set:
    if check_bipartite and not nx.is_bipartite(B):
        raise Exception('B is not a bipartite graph')
    seen_nodes: set = set()
    seen_neighbors: set = set()
    next: set = {node}
    while next:
        n = next.pop()
        for neighbor in B.neighbors(n):
            if neighbor not in seen_neighbors:
                for neighborneighbor in B.neighbors(neighbor):
                    if neighborneighbor not in seen_nodes:
                        seen_nodes.add(neighborneighbor)
                        next.add(neighborneighbor)
                seen_neighbors.add(neighbor)
    return seen_nodes - {node}


def time_respecting(B: nx.Graph, node, seed_time, node_presence_attr: str = 'end', check_bipartite: bool = False) -> dict:
    if check_bipartite and not nx.is_bipartite(B):
        raise Exception('B is not a bipartite graph')
    seen_nodes: dict = {node: seed_time}
    stack: set = {node}
    while stack:
        n = stack.pop()
        for neighbor in B.neighbors(n):
            t = B.nodes[neighbor][node_presence_attr]
            if seen_nodes[n] < t:
                for neighborneighbor in B.neighbors(neighbor):
                    if neighborneighbor not in seen_nodes or t < seen_nodes[neighborneighbor]:
                        seen_nodes[neighborneighbor] = t
                        stack.add(neighborneighbor)
    seen_nodes.pop(node)  # remove the seed node
    return seen_nodes
