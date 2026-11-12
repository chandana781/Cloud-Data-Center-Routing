
graph = {
    'R1': {'R2': 4, 'R3': 2},
    'R2': {'R1': 4, 'R3': 1, 'R4': 5},
    'R3': {'R1': 2, 'R2': 1, 'R4': 8, 'R5': 10},
    'R4': {'R2': 5, 'R3': 8, 'R5': 2},
    'R5': {'R3': 10, 'R4': 2}
}

def distance_vector(graph):
    routers = list(graph.keys())

    routing_tables = {}

    for router in routers:
        routing_tables[router] = {}

        for destination in routers:
            if router == destination:
                routing_tables[router][destination] = (0, "-")
            elif destination in graph[router]:
                routing_tables[router][destination] = (
                    graph[router][destination], destination
                )
            else:
                routing_tables[router][destination] = (
                    float('inf'), "-"
                )

    iteration = 0

    while True:
        iteration += 1

        old_tables = {
            router: routing_tables[router].copy()
            for router in routers
        }

        new_tables = {
            router: old_tables[router].copy()
            for router in routers
        }

        for router in routers:
            for neighbor, link_cost in graph[router].items():
                for destination in routers:

                    if destination == router:
                        continue

                    neighbor_cost = old_tables[neighbor][destination][0]

                    if neighbor_cost == float('inf'):
                        continue

                    new_cost = link_cost + neighbor_cost

                    current_cost, current_next_hop = (
                        new_tables[router][destination]
                    )

                    if (
                        new_cost < current_cost
                        or (
                            new_cost == current_cost
                            and (
                                current_next_hop == "-"
                                or neighbor < current_next_hop
                            )
                        )
                    ):
                        new_tables[router][destination] = (
                            new_cost, neighbor
                        )

        changed = any(
            new_tables[r] != old_tables[r]
            for r in routers
        )

        routing_tables = new_tables

        if not changed:
            break

    return routing_tables, iteration


if __name__ == "__main__":
    tables, iterations = distance_vector(graph)

    print("Number of iterations:", iterations)

    for router in graph:
        print("\nRouting Table:", router)
        print("Destination | Cost | Next Hop")

        for destination, (cost, hop) in tables[router].items():
            print(destination, cost, hop)

    print("\nAll routing tables have converged!")
