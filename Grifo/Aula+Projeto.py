import heapq

def dijkstra(graph, start):
    # Initialize distances to all nodes as infinity except the start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Create a priority queue to store nodes to visit
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # Skip if already visited
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Update distance if shorter path found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances

# Example graph
graph = {
    'A': {'B': 5, 'C': 2},
    'B': {'D': 4, 'E': 2},
    'C': {'B': 8, 'E': 7},
    'D': {'E': 6, 'F': 3},
    'E': {'F': 1},
    'F': {}
}

start_node = 'A'
distances = dijkstra(graph, start_node)

print(f"Shortest distances from node '{start_node}':")
for node, distance in distances.items():
    print(f"To node '{node}': {distance}")