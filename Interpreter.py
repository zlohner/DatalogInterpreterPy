from copy import deepcopy

from Token import Token
from DatalogProgram import DatalogProgram, Predicate, Rule
from Relation import Relation

class Interpreter(object):
	def __init__(self, program):
		self.program = program
		self.db = {}
		self.output = self.interpret()

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

	def evaluateRuleSet(self, S):
		passes = 0
		dbsize = 0
		while dbsize < self.dbsize():
			passes += 1
			dbsize = self.dbsize()
			for i in S:
				self.evaluateRule(i)
		return passes

	def interpret(self):
		sb = []

		for scheme in self.program.schemes:
			self.db[scheme.name] = Relation([t.value for t in scheme.params])

		for fact in self.program.facts:
			self.db[fact.name].tuples.add(tuple(t.value for t in fact.params))

		passes = self.evaluateRuleSet(set([i for i in range(len(self.program.rules))]))
		sb.append('Schemes populated after %d passes through the Rules.\n' % passes)

		for query in self.program.queries:
			R = self.query(query)

			sb.append(str(query) + '?')
			if len(R) > 0:
				sb.append(' Yes(' + str(len(R)) + ')')
			else:
				sb.append(' No')

			sb.append(str(R))
			sb.append('\n')

		return ''.join(sb[:-1])

	def dbsize(self):
		return sum([len(R) for R in self.db.values()])
