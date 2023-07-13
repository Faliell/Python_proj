import csv


class Vertex:

    def __init__(self, key, payload=None):
        self._key = key
        self._payload = payload

    def get_key(self):
        return self._key

    def get_info(self):
        return self._payload

    def __hash__(self):
        return hash(self.get_key())


class Edge:

    def __init__(self, start, end, weight=None):
        self._start = start
        self._end = end
        self._weight = weight

    def get_vs(self):
        return self._start, self._end

    def get_info(self):
        return self._weight

    def opposite(self, v):      #devolver o vértice oposto da aresta
        if v == self._start:
            return self._end
        else:
            return self._start

    def __hash__(self):
        return hash(self.get_vs())


class Graph:

    def __init__(self):     
        self._graph = {}    
        self._vertex = 0    #contador de vertices
        self._edge = 0      #contador de arestas

    def add_vertex(self, key, payload=None):
        if key not in self._graph.keys():
            vertex = Vertex(key, payload)            #criar objeto do tipo Vertex
            self._graph[vertex.get_key()] = []       #criar lista vazia para colocar as arestas do vertice da key
            self._vertex = self._vertex + 1

    def vertex_count(self):
        return self._vertex

    def add_edge(self, start, end, payload=None, weight=None):
        if start not in self._graph.keys():          #caso não exista v1 é criado esse vértice
            self.add_vertex(start, payload)
        if end not in self._graph.keys():            #caso não exista v2 é criado esse vértice
            self.add_vertex(end, payload)

        edge = Edge(start, end, weight)              #criar objeto do tipo Edge
        self._graph[start].append(edge)              #adicionar Edge às arestas de v1
        self._graph[end].append(edge)                #adicionar Edge às arestas de v1
        self._edge = self._edge + 1

    def edge_count(self):
        return self._edge

    def degree(self, vertex):
        if vertex in self._graph.keys():            #se o vértice existir...
            values = self._graph[vertex]            #criar lista com as arestas de vertex
            return len(values)                      #devolve o tamanho da lista = número de arestas do vértice
        else:
            raise ValueError('The vertex is not on this graph')

    def remove_edge(self, v1, v2):
        v1_list = self._graph[v1]                  #lista com todas as arestas de v1
        v2_list = self._graph[v2]                  #lista com todas as arestas de v2
        for i in v1_list:
            for j in v2_list:
                if str(i) == str(j):               #quando encontrar duas referências de arestas igual
                    self._graph[v1] .remove(i)     #remover a referência da aresta da lista de aresta do vértive v1
                    self._graph[v2] .remove(j)     #remover a referência da aresta da lista de aresta do vértive v1

    def remove_vertex(self, v1):
        v1_list = self._graph[v1]                  #lista com as arestas de v1
        v1_vertexs = []                            #esta lista vai guardar todos os vertices a que v1 está ligado
        for i in v1_list:
            v1_vertexs.append(i.opposite(v1))      #adicionar o vértice oposto da aresta onde estamos à lista
        for i in v1_vertexs:                       #percorrer todos os vértices ligados a v1
            arestas = self._graph[i]
            for j in arestas:                      #percorrer todas as arestas do vértice em que estamos
                if j.opposite(i) == v1:            #se o vertice oposto for igual ao vértice v1 ...
                    self._graph[i].remove(j)       #eliminar essa aresta
                    self._edge = self._edge - 1
        del self._graph[v1]                        #eliminar o vértice v1 do dicionário
        self._vertex = self._vertex - 1

    def _iter_vertex(self):
        return self._graph.keys()

    def _iter_edges(self):
        return self._graph.values()

 


