from copy import deepcopy

from Token import Token
from DatalogProgram import DatalogProgram, Predicate, Rule
from Relation import Relation
from Graph import SCCGraph, PostorderGraph

class Interpreter(object):
	def __init__(self, program):
		self.program = program
		self.db = {}
		self.passes = {}
		self.queryEvaluation = ''
		self.dependency = None
		self.SCCs = []

	def query(self, query):
		R = deepcopy(self.db[query.name])

		values = []
		columns = []

		for i, token in enumerate(query.params):
			if token.type == 'STRING':
				values.append((i, token.value))
			if token.type == 'ID':
				columns.append(i)

		R.select(values)
		R.project(columns)
		R.rename(query.params)

		return R

	def projectDelta(self, head, schema):
		delta = []
		for parameter in head.params:
			for i, s in enumerate(schema):
				if parameter.value == s:
					delta.append(i)
					break
		return delta

	def evaluateRule(self, i):
		head = self.program.rules[i].head
		predicates = self.program.rules[i].predicates

		answer = self.query(predicates[0])
		for i in range(1, len(predicates)):
			answer.join(self.query(predicates[i]))

		delta = self.projectDelta(head, answer.schema)
		answer.project(delta);
		self.db[head.name].tuples.update(answer.tuples)

	def evaluateRuleSet(self, S, simple=False):
		passes = 0
		dbsize = 0
		while dbsize < self.dbsize():
			passes += 1
			dbsize = self.dbsize()
			for i in S:
				self.evaluateRule(i)
			if simple:
				break
		return passes

	def dependencyGraph(self):
		G = SCCGraph(len(self.program.rules))
		for rule in self.program.rules:
			for p in rule.predicates:
				for produces in self.program.rules:
					if produces.head.name == p.name:
						G.edges[rule.n].add(produces.n)
		return G

	def findSCCs(self):
		D = self.dependencyGraph()
		self.dependency = D

		P = D.reverse()
		order = [len(D.nodes) - i - 1 for i in range(len(D.nodes))]
		P.DFSForest(order)

		D.DFSForest(P.postorder)

		return D.SCCs

	def dependsOnSelf(self, n):
		for p in self.program.rules[n].predicates:
			if p.name == self.program.rules[n].head.name:
				return True
		return False

	def dbsize(self):
		return sum([len(R) for R in self.db.values()])

	def interpret(self, project):
		for scheme in self.program.schemes:
			self.db[scheme.name] = Relation([t.value for t in scheme.params])

		for fact in self.program.facts:
			self.db[fact.name].tuples.add(tuple(t.value for t in fact.params))

		if project == 4:
			passes = self.evaluateRuleSet(set([i for i in range(len(self.program.rules))]))
			self.passes['single'] = passes
		elif project == 5:
			self.SCCs = self.findSCCs()
			for i, SCC in enumerate(self.SCCs):
				self.passes[i] = self.evaluateRuleSet(SCC, len(SCC) == 1 and not self.dependsOnSelf(list(SCC)[0]))

		sb = []
		for query in self.program.queries:
			R = self.query(query)

			sb.append(str(query) + '?')
			if len(R) > 0:
				sb.append(' Yes(' + str(len(R)) + ')')
			else:
				sb.append(' No')

			sb.append(str(R))
			sb.append('\n')

		self.queryEvaluation = ''.join(sb[:-1])

	def output(self, project):
		sb = []
		if project == 3:
			sb.append(self.queryEvaluation)
		elif project == 4:
			sb.append('Schemes populated after %d passes through the Rules.\n' % self.passes['single'])
			sb.append(self.queryEvaluation)
		elif project == 5:
			sb.append('Dependency Graph\n')
			sb.append(str(self.dependency))
			sb.append('\nRule Evaluation\n')
			for i in range(len(self.SCCs)):
				sb.append(str(self.passes[i]))
				sb.append(' passes: ')
				sb.append(','.join(['R' + str(i) for i in sorted(self.SCCs[i])]))
				sb.append('\n')
			sb.append('\nQuery Evaluation\n')
			sb.append(self.queryEvaluation)
		return ''.join(sb)
