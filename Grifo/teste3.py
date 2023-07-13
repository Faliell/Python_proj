import networkx as nx
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import folium
import numpy as np
import scipy as sp
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

class Station:

    def __init__(self, id, latitude, longitude, name, display_name, zone, total_lines, rail):
        self._id = id
        self._latitude = latitude
        self._longitude = longitude
        self._name = name
        self._display_name = display_name
        self._zone = zone
        self._total_lines = total_lines
        self._rail = rail

    def get_id(self):
        return self._id

    def get_location(self):
        return self._latitude, self._longitude

    def get_name(self):
        return self._name

    def get_display_name(self):
        return self._display_name

    def get_zone(self):
        return self._zone

    def get_total_lines(self):
        return self._total_lines

    def get_rail(self):
        return self._rail

    def __hash__(self):
        return hash((self._id, self._latitude, self._longitude))


class Connection:

    def __init__(self, line, start_station, end_station, distance, off_peak_time, am_peak_time, inter_peak_time):
        self._line = line
        self._start_station = start_station
        self._end_station = end_station
        self._distance = distance
        self._off_peak_time = off_peak_time
        self._am_peak_time = am_peak_time
        self._inter_peak_time = inter_peak_time

    def get_path(self):
        return self._start_station, self._end_station

    def get_line(self):
        return self._line

    def get_distance(self):
        return self._distance

    def get_off_peak_time(self):
        return self._off_peak_time

    def get_am_peak_time(self):
        return self._am_peak_time

    def get_inter_peak_time(self):
        return self._inter_peak_time

    def opposite(self, station):
        if station == self._start_station:
            return self._end_station
        else:
            return self._start_station

    def __hash__(self):
        return hash((self._line, self._start_station, self._end_station))


class LondonNetworkGraph:

    def __init__(self):
        self.graph = nx.Graph()

    def add_station(self, station):
        self.graph.add_node(station)

    def add_connection(self, station1, station2, connection):
        self.graph.add_edge(station1, station2, connection=connection)

    def get_stations(self):
        return [node for node in self.graph.nodes() if isinstance(node, Station)]

    def get_connections(self):
        return [data["connection"] for _, _, data in self.graph.edges(data=True) if "connection" in data]

    def get_line(self):
        return self._line

    def count_stations(self):
        return len(self.get_stations())

    def count_stations_by_zone(self):
        station_count_by_zone = {}
        for station in self.get_stations():
            zone = station.get_zone()
            if zone in station_count_by_zone:
                station_count_by_zone[zone] += 1
            else:
                station_count_by_zone[zone] = 1
        return station_count_by_zone

    def count_connections(self):
        return self.graph.number_of_edges()

    def count_edges_per_line(self):
        edge_counts = {}
        for connection in self.get_connections():
            line = connection._line
            if line in edge_counts:
                edge_counts[line] += 1
            else:
                edge_counts[line] = 1
        return edge_counts

    def calculate_mean_degree_per_station(self):
        mean_degrees = {}
        for station in self.get_stations():
            degree_sum = 0
            neighbor_count = 0
            for neighbor in self.graph.neighbors(station):
                degree_sum += self.graph.degree(neighbor)
                neighbor_count += 1
            mean_degree = degree_sum / neighbor_count if neighbor_count > 0 else 0
            mean_degrees[station] = mean_degree
        return mean_degrees

    def calculate_mean_weight_per_connection(self):
        mean_weights = {}
        for connection in self.get_connections():
            start_station, end_station = connection.get_path()
            weight_sum = self.graph.get_edge_data(start_station, end_station)["connection"].get_distance()
            mean_weight = weight_sum / 2  # Since connections are bidirectional
            mean_weights[connection] = mean_weight
        return mean_weights

    def visualize_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        plt.show()


GraphLondon = LondonNetworkGraph()

stations_df = pd.read_csv('../stations.csv')
stations = {}  # Store stations by ID for easy access

for _, row in stations_df.iterrows():
    station = Station(
        row['id'],
        row['latitude'],
        row['longitude'],
        row['name'],
        row['display_name'],
        row['zone'],
        row['total_lines'],
        row['rail']
    )
    GraphLondon.add_station(station)
    stations[row['id']] = station  # Store station by ID

connections_df = pd.read_csv('../connections.csv')
for _, row in connections_df.iterrows():
    connection = Connection(
        row['Line'],
        stations[row['From Station Id']],  # Convert ID to Station object
        stations[row['To Station Id']],  # Convert ID to Station object
        row['Distance (Kms)'],
        row['Off Peak Running Time (mins)'],
        row['AM peak (0700-1000) Running Time (Mins)'],
        row['Inter peak (1000 - 1600) Running time (mins)']
    )
    GraphLondon.add_connection(connection._start_station, connection._end_station, connection)

print(GraphLondon.count_stations())
station_counts = GraphLondon.count_stations_by_zone()
print(station_counts)
print(GraphLondon.count_connections())
edge_counts = GraphLondon.count_edges_per_line()
print(edge_counts)
mean_degrees = GraphLondon.calculate_mean_degree_per_station()
print(mean_degrees)
mean_weights = GraphLondon.calculate_mean_weight_per_connection()
print(mean_weights)

# Create a layout for the graph using Kamada-Kawai layout
layout = nx.kamada_kawai_layout(GraphLondon.graph)

# Set node positions based on the layout
node_positions = {node: (pos[0], pos[1]) for node, pos in layout.items() if isinstance(node, Station)}

# Set node labels based on the station names
node_labels = {node: node.get_name() for node in node_positions}

# Set edge labels based on the connection lines
edge_labels = {(start, end): data["connection"].get_line() for start, end, data in GraphLondon.graph.edges(data=True) if "connection" in data}

# Get the valid edges with positions
valid_edges = [edge for edge in edge_labels.keys() if edge[0] in node_positions and edge[1] in node_positions]

# Draw the graph with improved visualization
plt.figure(figsize=(24, 16))
nx.draw_networkx_nodes(GraphLondon.graph, pos=node_positions, nodelist=node_positions.keys(), node_color='lightblue', node_size=100)
nx.draw_networkx_edges(GraphLondon.graph, pos=node_positions, edgelist=valid_edges, edge_color='gray')
nx.draw_networkx_labels(GraphLondon.graph, pos=node_positions, labels=node_labels, font_size=8)
valid_edge_labels = {edge: label for edge, label in edge_labels.items() if edge[0] in node_positions and edge[1] in node_positions}
nx.draw_networkx_edge_labels(GraphLondon.graph, pos=node_positions, edge_labels=valid_edge_labels, font_size=6)

plt.axis('off')
plt.tight_layout()
plt.savefig('graph.png')  # Save the plot as an image file

dijkstra(GraphLondon, "Acton Town")































