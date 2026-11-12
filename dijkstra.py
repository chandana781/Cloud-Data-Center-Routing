
# Cloud Data Center Network Routing
# Dijkstra's Shortest Path Algorithm

import heapq

# Step 1: Represent the network as a weighted graph
# Routers are nodes and connections are edges.
# The numbers represent the cost of each network link.

graph = {
    'R1': [('R2', 4), ('R3', 2)],
    'R2': [('R1', 4), ('R3', 1), ('R4', 5)],
    'R3': [('R1', 2), ('R2', 1), ('R4', 8), ('R5', 10)],
    'R4': [('R2', 5), ('R3', 8), ('R5', 2)],
    'R5': [('R3', 10), ('R4', 2)]
}


# Step 2: Define Dijkstra's algorithm

def dijkstra(graph, source, destination):

    # Store the minimum known distance to each router
    distances = {router: float('inf') for router in graph}

    # Store the previous router to reconstruct the shortest path
    previous = {router: None for router in graph}

    # Distance from source to itself is zero
    distances[source] = 0

    # Priority queue stores (distance, router)
    priority_queue = [(0, source)]

    while priority_queue:

        # Get the router with the smallest known distance
        current_distance, current_router = heapq.heappop(priority_queue)

        # Skip outdated entries
        if current_distance > distances[current_router]:
            continue

        # Stop when the destination is reached optimally
        if current_router == destination:
            break

        # Check all neighboring routers
        for neighbor, cost in graph[current_router]:

            # Calculate the new path cost
            new_distance = current_distance + cost

            # Update if a shorter path is found
            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current_router

                # Add updated distance to priority queue
                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # Step 3: Reconstruct the shortest path

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    # Reverse to get source-to-destination order
    path.reverse()

    # Check whether destination is reachable
    if distances[destination] == float('inf'):
        return None, float('inf')

    return path, distances[destination]


# Step 4: Display the available routers

print("======================================")
print(" CLOUD DATA CENTER NETWORK ROUTING")
print(" DIJKSTRA SHORTEST PATH ALGORITHM")
print("======================================")

print("\nAvailable Routers: R1, R2, R3, R4, R5")

# Step 5: Accept source and destination from user

source = input("\nEnter Source Router: ").strip().upper()
destination = input("Enter Destination Router: ").strip().upper()

# Step 6: Validate the input

if source not in graph or destination not in graph:
    print("\nInvalid router! Please enter R1, R2, R3, R4 or R5.")

else:

    # Step 7: Execute Dijkstra's algorithm
    shortest_path, total_cost = dijkstra(
        graph, source, destination
    )

    # Step 8: Display the results

    print("\n========== ROUTING RESULT ==========")

    if shortest_path is None:
        print("No route exists between the selected routers.")

    else:
        print("Source Router      :", source)
        print("Destination Router :", destination)

        print("\nShortest Path:")
        print(" -> ".join(shortest_path))

        print("\nTotal Path Cost:", total_cost)

    print("====================================")
