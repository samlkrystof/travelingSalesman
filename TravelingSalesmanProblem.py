class City:
    def __init__(self, start, end, time):
        self.time_slot_start = start
        self.time_slot_end = end
        self.time_slot_duration = time


def print_solution(path: list, cost, distances: list, cities: list = None):
    """Prints the solution
        :param path: list of nodes in the path
        :param cost: cost of the path
        :param distances: distance_matrix matrix
        """
    print("cost:", cost)
    print("path:", path)
    if cost == float("inf"):
        return

    sum = 0
    for i in range(len(distances)):
        if cities != None:
            city = cities[path[i]]
            print(f"time in city {city.time_slot_duration}  total {sum} time slot {city.time_slot_start} - {city.time_slot_end}")
            sum += city.time_slot_duration
        print(path[i], "->", path[i + 1], " time", distances[path[i]][path[i + 1]], f" total {sum}")
        sum += distances[path[i]][path[i + 1]]


def tsp(cache: dict, prev: dict, distance: list, util_nodes: tuple, actual_distance):
    """TSP algorithm
        :param cache: cache of the results
        :param prev: previous node
        :param distance_matrix: distance matrix
        :param util_nodes: utility nodes
        :return: cost_from_start of the path
        """
    start_node, actual_node, state, end_state, cities = util_nodes

    if cities[actual_node].time_slot_end < actual_distance or cities[actual_node].time_slot_start > actual_distance:
        return float("inf")
    # we have reached time_slot_end of the path
    if state == end_state:
        prev[(actual_node, state)] = 0
        return distance[actual_node][start_node] + cities[actual_node].time_slot_duration
    # we have already cached cost for this path
    if (actual_node, state) in cache.keys():
        return cache[(actual_node, state)]

    min_cost = float("inf")
    index = -1
    for i in range(len(distance)):
        # i was visited in this state
        if state & (1 << i) != 0:
            continue

        # mark i as visited in out path
        next_state = state | (1 << i)
        dist = actual_distance + cities[actual_node].time_slot_duration + distance[actual_node][i]
        utils = (start_node, i, next_state, end_state, cities)
        new_cost = distance[actual_node][i] + tsp(cache, prev, distance, utils, dist) + cities[actual_node].time_slot_duration

        if new_cost < min_cost:
            min_cost = new_cost
            index = i

    prev[(actual_node, state)] = index
    cache[(actual_node, state)] = min_cost
    return min_cost

def solve(matrix: list, cities: list, start):
    """Solve TSP problem
        :param matrix: distance_matrix matrix
        :param start: time_slot_start node
        :return: cost of the path
        """

    # initial state, only time_slot_start node was visited
    state = 1 << start
    # all nodes were visited
    N = len(matrix)
    end_state = (1 << N) - 1

    cache = {}
    prev = {}
    utils = (start, start, state, end_state, cities)
    cost = tsp(cache, prev, matrix, utils, 0)
    if cost == float("inf"):
        return cost, []
    index = start
    path = [start]
    for _ in range(N):
        next_index = prev[(index, state)]
        state |= (1 << next_index)
        index = next_index
        path.append(index)

    return cost, path

if __name__ == "__main__":
    matrix = [[0, 4, 1, 3],
              [3, 0, 6, 2],
              [12, 8, 0, 5],
              [6, 3, 4, 0]]
    cities = [City(0, 100, 2), City(2, 25, 6), City(5, 20, 3), City(4, 12, 2)]

    cost, path = solve(matrix, cities, 0)
    print_solution(path, cost, matrix, cities)


    # matrix_big = [[0, 5, 4, 7, 3, 9, -2, 6, 11, 24],
    #               [11, 0, 7, 6, 14, 26, -11, 8, 4, 2],
    #               [15, 5, 0, 9, 7, 6, 77, 95, 144, 15],
    #               [4, 7, 8, 0, 53, 6, 17, 8, 29, 10],
    #               [5, 6, 7, 8, 0, 1, 2, 3, 48, 5],
    #               [6, 45, 4, 3, 2, 0, 11, 2, 31, 4],
    #               [7, 40, 3, 2, 41, -2, 0, 2, 3, 4],
    #               [8, 3, 24, 1, 7, 16, 2, 0, 63, 4],
    #               [9, 22, 1, 16, 1, 72, 3, 46, 0, 3],
    #               [10, 1, 5, 14, 2, 3, 45, 5, 6, 0]]
    #
    # cost, path = solve(matrix_big, 0)
    # print_solution(path, cost, matrix_big)
