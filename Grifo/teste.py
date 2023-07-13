import networkx as nx
import matplotlib
import folium
import numpy as np

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
        return hash(self.get_id())


class Connection:

    def __init__(self, line, start_station, end_station, distance, off_peak_time, am_peak_time, inter_peak_time):
        self._line = line
        self._start_station = start_station
        self._end_station = end_station
        self._distance = distance
        self._off_peak_time = off_peak_time     #since 4PM until 7AM next day, time (weight) of the edge
        self._am_peak_time = am_peak_time       #since 7AM until 10AM, time (weight) of the edge
        self._inter_peak_time = inter_peak_time #since 10AM until 4PM, time (weight) of the edge

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

    def opposite(self, station):            #devolver a estação oposta da conexão
        if station == self._start_station:
            return self._end_station
        else:
            return self._start_station

    def __hash__(self):
        return hash(self.get_path())

class LondonNetworkGraph:
    def __init__(self):
        self._graph = {}
        self._station = 0           #stations (vertex/vertices)
        self._connection = 0        #connections (edges/arestas)
        self.G = nx.Graph()

        LondonNetworkGraph = nx.Graph()

    def stations(self, file_path):
        file = open(file_path, "r")
        vect = file.read()
        vect = vect.split("\n")             #dividimos o ficheiro por linhas
        vect = vect[2:]                     #estamos a ignorar as primeiras duas linhas (estamos a ler da terceira para a frente)
        for i in range(len(vect)):          #vamos percorrer as linhas do vetor
            vect[i] = vect[i].split(",")    #vamos dividir cada informação entre vírgulas para ficarem independentes
            self.add_station(vect[i][0], vect[i][1], vect[i][2], vect[i][3], vect[i][4], vect[i][5], vect[i][6], vect[i][7])
        file.close()


    def add_station(self, id, latitude, longitude, name, display_name, zone, total_lines, rail):
        if id not in self._graph.keys():
            station = Station(id, latitude, longitude, name, display_name, zone, total_lines, rail)
            self._graph[station.get_id()] = []       #criar lista vazia para colocar as conexões da estação
            self._station = self._station + 1

    def n_station(self):
        return self._station

    # def n_station_zone(self):
    #     zonas = []
    #     i = 0
    #     for k in range(self._station):


    def connections(self, file_path):
        file = open(file_path, "r")
        vect = file.read()
        vect = vect.split("\n")             #dividimos o ficheiro por linhas
        vect = vect[1:]                     #estamos a ignorar as primeiras duas linhas (estamos a ler da segunda para a frente)
        for i in range(len(vect)):          #vamos percorrer as linhas do vetor
            vect[i] = vect[i].split(",")    #vamos dividir cada informação entre vírgulas para ficarem independentes
            self.add_connection(vect[i][0], vect[i][1], vect[i][2], vect[i][3], vect[i][4], vect[i][5], vect[i][6])
        file.close()

    def add_connection(self, line, start_station, end_station, distance, off_peak_time, am_peak_time, inter_peak_time):
        if start_station not in self._graph.keys():          #caso não exista a estação, é criada essa estação
            self.add_connection(line, start_station, end_station, distance, off_peak_time, am_peak_time, inter_peak_time)
        if end_station not in self._graph.keys():            #caso não exista a estação é criada essa estação
            self.add_connection(line, start_station, end_station, distance, off_peak_time, am_peak_time, inter_peak_time)

        connection = Connection(line, start_station, end_station, distance, off_peak_time, am_peak_time, inter_peak_time)
        self._graph[start_station].append(connection)              #adicionar Edge às arestas de v1
        self._graph[end_station].append(connection)                #adicionar Edge às arestas de v1
        self._connection = self._connection + 1

    def n_connection(self):
        return self._connection

    def degree(self, station):                      #quantas conexões tem a estação
        if station in self._graph.keys():           #se a estação existir...
            values = self._graph[station]           #criar lista com as conexões da estação
            return len(values)                      #devolve o tamanho da lista = número de conexões da estação
        else:
            raise ValueError('The station is not in this graph')

    def remove_connection(self, start, end):
        start_list = self._graph[start]                 #lista com todas as conexões da estação "start"
        end_list = self._graph[end]                     #lista com todas as conexões da estação "end"
        for i in start_list:
            for j in end_list:
                if str(i) == str(j):                    #quando encontrar duas referências de conexões iguais
                    self._graph[start] .remove(i)       #remover a referência da conexão da lista de conexões da estação "start"
                    self._graph[end] .remove(j)         #remover a referência da conexão da lista de conexões da estação "end"

    def remove_station(self, station):
        station_list = self._graph[station]                     #lista com as conexões da estação
        stations = []                                           #esta lista vai guardar todas a estções a que esta específica estação está ligada
        for i in station_list:
            stations.append(i.opposite(station))                #adicionar a estação oposta da conexão onde estamos à lista
        for i in stations:                                      #percorrer todas as estações ligados à estação específica
            connections = self._graph[i]
            for j in connections:                               #percorrer todas as conexões da estação em que estamos
                if j.opposite(i) == station:                    #se a estação oposta for igual ao à nossa estação ...
                    self._graph[i].remove(j)                    #eliminar essa conexão
                    self._connection = self._connection - 1
        del self._graph[station]                                #eliminar a nossa estação do dicionário
        self._station = self._station - 1

GraphLondon = LondonNetworkGraph()
GraphLondon.stations("./stations.csv")
GraphLondon.connections("./connections.csv")

