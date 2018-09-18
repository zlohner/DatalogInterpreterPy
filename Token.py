#!/usr/bin/env python

class Token(object):
	def __init__(self, type, value, lineNum):
		self.type = type
		self.value = value
		self.lineNum = lineNum

	def __str__(self):
		sb = []
		sb.append('(')
		sb.append(str(self.type))
		sb.append(',\"')
		sb.append(self.value)
		sb.append('\",')
		sb.append(str(self.lineNum))
		sb.append(')')
		return ''.join(sb)
