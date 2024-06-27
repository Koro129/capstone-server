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
        idAccount = 9  # getAccountId()
        data = request.json
        from_node = data.get('from')
        to_node = data.get('dest')

        # Check if the nodes exist
        if not Node.query.filter_by(idNode=from_node, idAccount=idAccount).first():
            return jsonify({'message': 'From node not found'}), 404
        if not Node.query.filter_by(idNode=to_node, idAccount=idAccount).first():
            return jsonify({'message': 'To node not found'}), 404

        from_node_level = Node.query.filter_by(idNode=from_node, idAccount=idAccount).first().level
        to_node_level = Node.query.filter_by(idNode=to_node, idAccount=idAccount).first().level

        graph = Graph(idAccount)

        if from_node_level != to_node_level:
            # Get the nearest lift on the same level as from_node
            nearest_lift_from = Node.query.filter_by(level=from_node_level, idAccount=idAccount, nodetype='lift').first()
            if not nearest_lift_from:
                return jsonify({'message': 'No lift found on the level of from_node'}), 404

            # Get the nearest lift on the same level as to_node
            nearest_lift_to = Node.query.filter_by(level=to_node_level, idAccount=idAccount, nodetype='lift').first()
            if not nearest_lift_to:
                return jsonify({'message': 'No lift found on the level of to_node'}), 404

            # Calculate the path from from_node to nearest_lift_from
            path_to_lift, distance_to_lift = graph.dijkstra(from_node, nearest_lift_from.idNode)
            if path_to_lift is None:
                return jsonify({'message': 'No path found to the lift from from_node'}), 404

            # Calculate the path from nearest_lift_to to to_node
            path_from_lift, distance_from_lift = graph.dijkstra(nearest_lift_to.idNode, to_node)
            if path_from_lift is None:
                return jsonify({'message': 'No path found from the lift to to_node'}), 404

            # Combine the paths and distances
            total_path = path_to_lift + path_from_lift[1:]  # Avoid duplicating the lift node
            total_distance = distance_to_lift + distance_from_lift
        else:
            # Calculate the direct path if both nodes are on the same level
            total_path, total_distance = graph.dijkstra(from_node, to_node)
            if total_path is None:
                return jsonify({'message': 'No path found'}), 404

        path_names = [graph.node_map[node] for node in total_path]
        data = singlePath({
            'path': total_path,
            'path_names': path_names,
            'distance': total_distance
        })
        return response.success(data, 'success')

    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
