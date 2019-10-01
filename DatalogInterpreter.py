#!/usr/bin/env python3

import sys

from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter

class DatalogInterpreter(object):
	def interpret(self, filename):
		s = Scanner(filename)
		p = Parser(s.tokens)
		# if p.good:
		# 	print('Success!')
		# 	print(str(p.program))

		i = Interpreter(p.program)
		# print interpreter output

if __name__ == "__main__":
	d = DatalogInterpreter()
	d.interpret(sys.argv[1])
