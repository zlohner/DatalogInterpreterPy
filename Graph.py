#!/usr/bin/env python3

class Graph(object):
	def __init__(self, n):
		self.nodes = [i for i in range(n)]
		self.edges = {}
		for i in self.nodes:
			self.edges[i] = set([])
		self.visited = [False for i in range(n)]

	def clearVisited(self):
		self.visited = [False for i in range(len(visited))]

	def action(self, node):
		pass

	def cleanup(self):
		pass

	def DFS(self, node):
		if not self.visited[node]:
			self.visited[node] = True
			for edge in self.edges[node]:
				self.DFS(edge)
			self.action(node)

	def DFSForest(self, order):
		while len(order) > 0:
			self.DFS(order.pop())
			self.cleanup()

	def __len__(self):
		return len(self.nodes)

	def __repr__(self):
		sb = []
		for node in self.nodes:
			sb.append('R')
			sb.append(str(node))
			sb.append(':')
			sb.append(','.join(['R' + str(edge) for edge in sorted(self.edges[node])]))
			sb.append('\n')
		return ''.join(sb)

class PostorderGraph(Graph):
	def __init__(self, n):
		Graph.__init__(self, n)
		self.postorder = []

	def action(self, node):
		self.postorder.append(node)

	def cleanup(self):
		pass

class SCCGraph(Graph):
	def __init__(self, n):
		Graph.__init__(self, n)
		self.SCCs = []
		self.SCC = set([])

	def action(self, node):
		self.SCC.add(node)

	def cleanup(self):
		if len(self.SCC) > 0:
			self.SCCs.append(self.SCC)
			self.SCC = set([])

	def reverse(self):
		reversed = PostorderGraph(len(self))
		for node in self.edges:
			for edge in self.edges[node]:
				reversed.edges[edge].add(node)
		return reversed
