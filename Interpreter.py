from Token import Token
from DatalogProgram import DatalogProgram, Predicate, Rule

class Interpreter(object):
	def __init__(self, program):
		self.program = program
		self.db = {}
		self.interpret()

	def interpret(self):
		for scheme in program.schemes:
			self.db[scheme.name]
