import sys

from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter

def interpret(filename, project):
	s = Scanner()
	s.scan(filename)
	if project == 1:
		print(s)
		return
	s.removeComments()

	p = Parser()
	p.parse(s.tokens)
	if project == 2:
		if p.good:
			print('Success!\n' + str(p.program))
		return

	i = Interpreter(p.program)
	i.interpret(project)
	print(i.output(project))

project = 5
if len(sys.argv) > 2:
	project = int(sys.argv[2])
interpret(sys.argv[1], project)
