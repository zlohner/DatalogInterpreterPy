from Token import Token
from DatalogProgram import DatalogProgram, Predicate, Rule

class InvalidToken(Exception):
	def __init__(self, Token):
		self.token = Token

class Parser(object):
	def __init__(self, tokens):
		self.tokens = tokens
		self.marker = 0
		self.program = DatalogProgram()
		self.good = True
		self.domain = False
		self.parse()

	def match(self, types):
		t = self.tokens[self.marker]
		if t.type in types:
			self.marker += 1
		else:
			raise InvalidToken(t)
		if t.type == 'STRING' and self.domain:
			self.program.domain.add(t.value)
		return t

	def parse(self):
		try:
			self.datalogProgram()
		except InvalidToken as i:
			self.good = False
			print('Failure!\n ' + str(i.token))

	def datalogProgram(self):
		self.match({'SCHEMES'})
		self.match({'COLON'})
		self.scheme()
		self.schemeList()
		self.match({'FACTS'})
		self.match({'COLON'})
		self.factList()
		self.match({'RULES'})
		self.match({'COLON'})
		self.ruleList()
		self.match({'QUERIES'})
		self.match({'COLON'})
		self.query()
		self.queryList()

	def scheme(self):
		self.program.schemes.append(self.predicate({'ID'}))

	def schemeList(self):
		if self.tokens[self.marker].type == 'ID':
			self.scheme()
			self.schemeList()

	def fact(self):
		self.domain = True
		self.program.facts.append(self.predicate({'STRING'}))
		self.match({'PERIOD'})
		self.domain = False

	def factList(self):
		if self.tokens[self.marker].type == 'ID':
			self.fact()
			self.factList()

	def rule(self):
		headPredicate = self.predicate({'ID', 'STRING'})
		preds = []
		self.match({'COLON_DASH'})
		preds.append(self.predicate({'ID', 'STRING'}))
		self.predicateList({'ID', 'STRING'}, preds)
		self.match({'PERIOD'})
		self.program.rules.append(Rule(headPredicate, preds))

	def ruleList(self):
		if self.tokens[self.marker].type == 'ID':
			self.rule()
			self.ruleList()

	def query(self):
		self.program.queries.append(self.predicate({'ID', 'STRING'}))
		self.match({'Q_MARK'})

	def queryList(self):
		if self.tokens[self.marker].type == 'ID':
			self.query()
			self.queryList()

	def predicate(self, types):
		name = self.match({'ID'}).value
		params = []
		self.match({'LEFT_PAREN'})
		params.append(self.match(types))
		self.parameterList(types, params)
		self.match({'RIGHT_PAREN'})
		return Predicate(name, params)

	def predicateList(self, types, preds):
		if self.tokens[self.marker].type == 'COMMA':
			self.match({'COMMA'})
			preds.append(self.predicate(types))
			self.predicateList(types, preds)

	def parameterList(self, types, params):
		if self.tokens[self.marker].type == 'COMMA':
			self.match({'COMMA'})
			params.append(self.match(types))
			self.parameterList(types, params)
