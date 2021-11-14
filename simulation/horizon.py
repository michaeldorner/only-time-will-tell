def time_ignoring(neighbors: dict, node) -> set:
    seen_nodes: set = set()
    seen_neighbors: set = set()
    next_nodes: set = {node}
    while next_nodes:
        n = next_nodes.pop()
        for neighbor in neighbors[n]:
            if neighbor not in seen_neighbors:
                for neighborneighbor in neighbors[neighbor]:
                    if neighborneighbor not in seen_nodes:
                        seen_nodes.add(neighborneighbor)
                        next_nodes.add(neighborneighbor)
                seen_neighbors.add(neighbor)
    return seen_nodes - {node}


def time_respecting(neighbors: dict, edge_availability: dict, node, seed_time) -> dict:
    seen_nodes: dict = {node: seed_time}
    stack: set = {node}
    while stack:
        n = stack.pop()
        for neighbor in neighbors[n]:
            t = edge_availability[neighbor]
            if seen_nodes[n] < t:
                for neighborneighbor in neighbors[neighbor]:
                    if neighborneighbor not in seen_nodes or t < seen_nodes[neighborneighbor]:
                        seen_nodes[neighborneighbor] = t
                        stack.add(neighborneighbor)
    seen_nodes.pop(node)  # remove the seed node
    return seen_nodes
