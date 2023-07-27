import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random
import pickle

class Agent_0:
    def __init__(self):
        self.location = random.randint(0, 39)
    
    def move_agent(self, graph_dict, target):
        return self.location
class Agent_1:
    def __init__(self):
        # self.location = random.randint(0, 39)
        self.location = 0

    def move_agent(self, graph_dict, target):
        shortest_path = self.dijkstra(graph_dict, self.location, target)

        # If there are no paths (agent and target are in disconnected subgraphs), don't move.
        if not shortest_path:
            print("You have made a grave error...")
            return

        # Moves agent 1 step on the shortest path
        self.location = shortest_path[1] if len(shortest_path) > 1 else shortest_path[0]

    def dijkstra(self, graph_dict, start, end):
        # Dijkstra's algorithm.
        heap = [(0, start)]
        predecessors = {start: None}
        distances = {start: 0}

        while heap:
            (distance, current) = heapq.heappop(heap)
            if current == end:
                return self.path(predecessors, end)
            for neighbor in graph_dict[current]:
                old_distance = distances.get(neighbor, float('inf'))
                new_distance = distances[current] + 1
                if new_distance < old_distance:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current
                    heapq.heappush(heap, (new_distance, neighbor))

    @staticmethod
    def path(predecessors, end):
        cursor = end
        path = []
        while cursor is not None:
            path.append(cursor)
            cursor = predecessors[cursor]
        return list(reversed(path))

class Agent_2:
    def __init__(self):
        # self.location = random.randint(0, 39)
        self.location = 0

    def move_agent(self, graph_dict, target):
        if target in graph_dict[self.location]:
            self.location = target
        else:
            potential_target_locations = graph_dict[target]
            shortest_paths = [(self.dijkstra(graph_dict, self.location, potential_location), potential_location) for potential_location in potential_target_locations]
            # Filter out None paths (unreachable nodes)
            shortest_paths = [path for path in shortest_paths if path[0]]
            if not shortest_paths:
                print("No accessible paths...")
                return
            # Selects the shortest path among the potential target's next locations
            shortest_path_to_potential_location = min(shortest_paths, key=lambda x: len(x[0]))
            # Moves agent 1 step on the chosen path
            self.location = shortest_path_to_potential_location[0][1] if len(shortest_path_to_potential_location[0]) > 1 else shortest_path_to_potential_location[0][0]


    def dijkstra(self, graph_dict, start, end):
        # Dijkstra's algorithm.
        heap = [(0, start)]
        predecessors = {start: None}
        distances = {start: 0}

        while heap:
            (distance, current) = heapq.heappop(heap)
            if current == end:
                return self.path(predecessors, end)
            for neighbor in graph_dict[current]:
                old_distance = distances.get(neighbor, float('inf'))
                new_distance = distances[current] + 1
                if new_distance < old_distance:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current
                    heapq.heappush(heap, (new_distance, neighbor))

    @staticmethod
    def path(predecessors, end):
        cursor = end
        path = []
        while cursor is not None:
            path.append(cursor)
            cursor = predecessors[cursor]
        return list(reversed(path))

class Agent_3:
    def __init__(self):
        self.location = random.randint(0, 39)

    def move_agent(self, graph_dict, target):
        return self.location
class Agent_4:
    def __init__(self):
        self.location = random.randint(0, 39)

    def move_agent(self, graph_dict, target):
        pass

class Agent_5:
    def __init__(self):
        self.location = random.randint(0, 39)

    def move_agent(self, graph_dict, target):
        pass

class Agent_6:
    def __init__(self):
        self.location = random.randint(0, 39)

    def move_agent(self, graph_dict, target):
        pass

class Agent_7:
    def __init__(self):
        self.location = random.randint(0, 39)

    def move_agent(self, graph_dict, target):
        pass

class Graph:
    def __init__(self, N_NODES, N_EDGES):
        self.G = nx.cycle_graph(N_NODES)
        while nx.number_of_edges(self.G) < N_NODES + N_EDGES:
            n1, n2 = random.sample(range(N_NODES), 2)
            if self.G.degree[n1] < 3 and self.G.degree[n2] < 3 and not self.G.has_edge(n1, n2):
                self.G.add_edge(n1, n2)
        self.time_step = 0
        self.convert_to_dict()
        self.set_target_location()
        self.initialize_agents()
    
    def run_agents(self):
        while not all (not element for element in self.agents_active):
            self.turn()
            self.move_target()
        print(self.agent_performance)

    def turn(self):
        self.time_step += 1
        for i in range(0, 7):
            if self.agents_active[i]:
                self.agents[i].move_agent(self.graph_dict, self.target)
                self.agent_locations[i] = self.agents[i].location
                self.is_target_captured(self.agent_locations[i], i)
        self.draw_graph() # draw the graph at each time step
        plt.pause(0.1) # add a pause so you can see the graphs

    def is_target_captured(self, agent_location, agent_index):
        if(agent_location == self.target):
            self.agent_performance[agent_index] = self.time_step
            self.agents_active[agent_index] = False

    def initialize_agents(self):        
        self.agents = [Agent_0(), Agent_1(), Agent_2(), Agent_3(), Agent_4(), Agent_5(), Agent_6(), Agent_7()]
        self.agent_locations = [self.agents[i].location for i in range(0, 7)]
        # self.agents_active = [True for i in range(0, 7)]
        self.agents_active = [False, True, True, False, False, False, False, False]
        self.agents_colors = ["magenta","green","pink","yellow","gray","white","cyan","purple"]
        self.agent_performance = [-1 for i in range(0, 7)]
        for i in range(0, 7):
            self.is_target_captured(self.agent_locations[i], i)

    def set_target_location(self):
        location = random.randint(0, 39)
        self.target = location

    def convert_to_dict(self):
        graph_dict = nx.to_dict_of_lists(self.G)
        self.graph_dict = graph_dict
    
    def draw_graph(self):
        colors = ["blue" for node in self.G.nodes]
        for i in range(len(self.agents)):
            if self.agents_active[i]:
                colors[self.agent_locations[i]] = self.agents_colors[i]
        colors[self.target] = "red"
        nx.draw_circular(self.G, node_color=colors, with_labels=True)
        plt.show()
    
    def print_graph_dict(self):
        print(self.graph_dict)
        print(f"TARGET LOCATION: {self.target}")
    
    def move_target(self):
        connections = self.graph_dict[self.target]
        random_choice = random.randint(0, len(connections)-1)
        self.target = connections[random_choice]


if __name__ == "__main__":
    # Generate 50 graphs and save them using pickle.
    graph_envs = []
    for i in range(0, 40):
        graph_env = Graph(40, 10)
        graph_envs.append(graph_env)
    # graphs = [create_graph(40, 10) for _ in range(10)]
    with open('graphs.pkl', 'wb') as f:
        pickle.dump(graph_envs, f)

    # Load the 7th graph (index 6) from the pickle file.
    with open('graphs.pkl', 'rb') as f:
        loaded_graphs_envs = pickle.load(f)
    example = loaded_graphs_envs[6]
    example.print_graph_dict()
    example.draw_graph()
    example.run_agents()
    
    
