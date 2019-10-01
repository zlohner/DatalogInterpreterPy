#!/usr/bin/env python3

import sys

from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter

def interpret(filename, project):
	s = Scanner(filename)
	if project == 1:
		print(s)
		return
	else:
		s.removeComments()

	p = Parser(s.tokens)
	if project == 2:
		if p.good:
			print('Success!')
			print(str(p.program))
		return

	i = Interpreter(p.program)
	if project == 3:
		print(i.output)
		return

project = 3
if len(sys.argv) > 2:
	project = int(sys.argv[2])
interpret(sys.argv[1], project)
