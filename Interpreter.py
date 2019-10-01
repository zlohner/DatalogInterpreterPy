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

	def interpret(self):
		for scheme in self.program.schemes:
			self.db[scheme.name] = Relation([t.value for t in scheme.params])

		for fact in self.program.facts:
			self.db[fact.name].tuples.add(tuple(t.value for t in fact.params))

		# for rule in rules:
		#	...

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

		return ''.join(sb[:-1])
