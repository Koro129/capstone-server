from collections import defaultdict, deque
from flask import Flask, jsonify, request
from app import db, app, response
from app.model.node import Node
from app.model.noderelation import NodeRelation
from app.controller.AccountController import getAccountId

class Graph:
    def __init__(self, idAccount):
        self.idAccount = idAccount
        self.V = 0
        self.adj = defaultdict(list)
        self.weight = {}
        self.node_map = {}
        self.load_graph()

    def load_graph(self):
        nodes = Node.query.filter_by(idAccount=self.idAccount).all()
        for node in nodes:
            self.node_map[node.idNode] = node.name
            self.V += 1

        edges = NodeRelation.query.join(Node, Node.idNode == NodeRelation.idNode1).filter(Node.idAccount == self.idAccount).all()
        for edge in edges:
            self.add_edge(edge.idNode1, edge.idNode2, edge.weight)

    def add_edge(self, u, v, w):
        self.adj[u].append(v)
        self.weight[(u, v)] = w

    def min_dist(self, dist, vis):
        min_val = float('inf')
        min_index = -1
        for node in self.node_map.keys():
            if not vis[node] and dist[node] < min_val:
                min_val = dist[node]
                min_index = node
        return min_index

    def dijkstra(self, source, dest):
        dist = {node: float('inf') for node in self.node_map.keys()}
        data = {node: None for node in self.node_map.keys()}
        vis = {node: False for node in self.node_map.keys()}
        dist[source] = 0

        for _ in range(self.V):
            min_index = self.min_dist(dist, vis)
            if min_index == -1:
                break
            vis[min_index] = True
            for neighbor in self.adj[min_index]:
                if self.weight[(min_index, neighbor)] and not vis[neighbor] and dist[min_index] + self.weight[(min_index, neighbor)] < dist[neighbor]:
                    dist[neighbor] = dist[min_index] + self.weight[(min_index, neighbor)]
                    data[neighbor] = min_index

        if dist[dest] == float('inf'):
            return None, float('inf')
        
        path = []
        current = dest
        while current is not None:
            path.insert(0, current)
            current = data[current]
        
        return path, dist[dest]

def singlePath(data):
    data = {
        'path': data['path'],
        'path_names': data['path_names'],
        'distance': data['distance']
    }
    return data

def shortest_path():
    try:
        idAccount = 9 #getAccountId()
        from_node = int(request.form.get('from'))
        to_node = int(request.form.get('dest'))

        graph = Graph(idAccount)
        path, distance = graph.dijkstra(from_node, to_node)

        if path is None:
            return jsonify({'message': 'No path found'}), 404

        path_names = [graph.node_map[node] for node in path]
        data = singlePath({
            'path': path,
            'distance': distance
        })
        return response.success(data, 'success')

    except Exception as e:
        print(e)
        # return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
