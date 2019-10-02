class Rule(object):
	def __init__(self, head, predicates, n):
		self.head = head
		self.predicates = predicates
		self.n = n

	def __repr__(self):
		sb = []
		sb.append(str(self.head))
		sb.append(' :- ')
		first = True
		for predicate in self.predicates:
			if first:
				first = False
				sb.append(str(predicate))
			else:
				sb.append(',')
				sb.append(str(predicate))
		return ''.join(sb)

class Predicate(object):
	def __init__(self, name, params):
		self.name = name
		self.params = params

	def __repr__(self):
		sb = []
		sb.append(self.name)
		sb.append('(')
		first = True
		for param in self.params:
			if first:
				first = False
				sb.append(param.value)
			else:
				sb.append(',')
				sb.append(param.value)
		sb.append(')')
		return ''.join(sb)

class DatalogProgram(object):
	def __init__(self):
		self.schemes = []
		self.facts = []
		self.rules = []
		self.queries = []
		self.domain = set([])

	def __repr__(self):
		sb = []

		sb.append('Schemes(')
		sb.append(str(len(self.schemes)))
		sb.append('):')
		for scheme in self.schemes:
			sb.append('\n  ')
			sb.append(str(scheme))

		sb.append('\nFacts(')
		sb.append(str(len(self.facts)))
		sb.append('):')
		for fact in self.facts:
			sb.append('\n  ')
			sb.append(str(fact))
			sb.append('.')

		sb.append('\nRules(')
		sb.append(str(len(self.rules)))
		sb.append('):')
		for rule in self.rules:
			sb.append('\n  ')
			sb.append(str(rule))
			sb.append('.')

		sb.append('\nQueries(')
		sb.append(str(len(self.queries)))
		sb.append('):')
		for query in self.queries:
			sb.append('\n  ')
			sb.append(str(query))
			sb.append('?')

		sb.append('\nDomain(')
		sb.append(str(len(self.domain)))
		sb.append('):')
		for item in sorted(self.domain):
			sb.append('\n  ')
			sb.append(item)

		return ''.join(sb)
