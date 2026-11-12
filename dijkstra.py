
import heapq

# Network topology
graph = {
    'R1': [('R2', 4), ('R3', 2)],
    'R2': [('R1', 4), ('R3', 1), ('R4', 5)],
    'R3': [('R1', 2), ('R2', 1), ('R4', 8), ('R5', 10)],
    'R4': [('R2', 5), ('R3', 8), ('R5', 2)],
    'R5': [('R3', 10), ('R4', 2)]
}


# Dijkstra's shortest path algorithm
def dijkstra(graph, source, destination):

    if source not in graph or destination not in graph:
        raise ValueError("Invalid source or destination router")

    distances = {
        router: float('inf') for router in graph
    }

    previous = {
        router: None for router in graph
    }

    distances[source] = 0

    priority_queue = [(0, source)]

    while priority_queue:

        current_distance, current_router = heapq.heappop(
            priority_queue
        )

        if current_distance > distances[current_router]:
            continue

        if current_router == destination:
            break

        for neighbor, cost in graph[current_router]:

            new_distance = current_distance + cost

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current_router

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    if distances[destination] == float('inf'):
        return None, float('inf')

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[destination]


# Terminal execution only
# This block will NOT execute when Streamlit imports this file.
if __name__ == "__main__":
    tables, iterations = distance_vector(graph)

    print("Number of iterations:", iterations)

    for router in graph:
        print("Routing Table:", router)
        print(tables[router])