#!/usr/bin/env python

import os

from Token import Token

keywords = { 'Schemes' : 'SCHEMES', 'Facts' : 'FACTS', 'Rules' : 'RULES', 'Queries' : 'QUERIES' }

class Scanner(object):
	def __init__(self):
		self.content = None
		self.index = -1
		self.c = None
		self.tokens = []
		self.lineNum = 1

	def __str__(self):
		sb = []
		for token in self.tokens:
			sb.append(str(token))
			sb.append('\n')
		sb.append('Total Tokens = ')
		sb.append(str(len(self.tokens)))
		return ''.join(sb)
	
	def open(self, filename):
		self.index = -1
		with open(filename, 'r', encoding='utf8') as file:
			self.content = file.read()
		self.get()

	def get(self):
		self.index += 1
		if self.index < len(self.content):
			self.c = self.content[self.index]
		else:
			self.c = ''
		return self.c

	def unget(self):
		self.index -= 1
		self.c = self.content[self.index]

	def scanID(self):
		type = 'ID'
		value = ''
		while self.c.isalnum():
			value += self.c
			self.get()
		self.unget()

		if value in keywords:
			type = keywords[value]

		return Token(type, value, self.lineNum)

	def scanString(self):
		type = 'STRING'
		value = '\''
		startLine = self.lineNum

		end = False
		while not end and self.c:
			value += self.get()
			if self.c == '\'':
				self.get()
				if self.c == '\'':
					value += self.c
				else:
					self.unget()
					end = True
			elif self.c == '\n':
				self.lineNum += 1

		if not end:
			type = 'UNDEFINED'

		return Token(type, value, startLine)

	def scanComment(self):
		type = 'COMMENT'
		value = '#'
		startLine = self.lineNum
		end = True

		self.get()

		if self.c == '|':
			value += self.c

			end = False
			while not end and self.c:
				value += self.get()
				if self.c == '|':
					value += self.get()
					if self.c == '#':
						end = True
				if self.c == '\n':
					self.lineNum += 1
		else:
			while self.c != '\n':
				value += self.c
				self.get()
			self.unget()

		if not end:
			type = 'UNDEFINED'

		return Token(type, value, startLine)

	def removeComments(self):
		self.tokens = [token for token in self.tokens if token.type != 'COMMENT']

	def scan(self, filename):
		self.open(filename)
		self.tokens = []
		self.lineNum = 1
		while self.c:
			if self.c == ',':
				self.tokens.append(Token('COMMA', ',', self.lineNum))
			elif self.c == '.':
				self.tokens.append(Token('PERIOD', '.', self.lineNum))
			elif self.c == '?':
				self.tokens.append(Token('Q_MARK', '?', self.lineNum))
			elif self.c == '(':
				self.tokens.append(Token('LEFT_PAREN', '(', self.lineNum))
			elif self.c == ')':
				self.tokens.append(Token('RIGHT_PAREN', ')', self.lineNum))
			elif self.c == ':':
				self.get()
				if self.c == '-':
					self.tokens.append(Token('COLON_DASH', ':-', self.lineNum))
				else:
					self.tokens.append(Token('COLON', ':', self.lineNum))
					self.unget()
			elif self.c == '*':
				self.tokens.append(Token('MULTIPLY', '*', self.lineNum))
			elif self.c == '+':
				self.tokens.append(Token('ADD', '+', self.lineNum))
			elif self.c == '\'':
				self.tokens.append(self.scanString())
			elif self.c == '#':
				self.tokens.append(self.scanComment())
			else:
				if (self.c.isalpha()):
					self.tokens.append(self.scanID())
				elif (self.c.isspace()):
					if (self.c == '\n'):
						self.lineNum += 1
				else:
					self.tokens.append(Token('UNDEFINED', self.c, self.lineNum))
			self.get()
		self.tokens.append(Token('EOF', '', self.lineNum))
