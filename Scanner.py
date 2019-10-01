#!/usr/bin/env python

import os

from Token import Token

keywords = { 'Schemes' : 'SCHEMES', 'Facts' : 'FACTS', 'Rules' : 'RULES', 'Queries' : 'QUERIES' }

class Scanner(object):
	def __init__(self):
		self.file = None
		self.c = None
		self.tokens = []
		self.lineNum = 1

	def __repr__(self):
		sb = []
		for token in self.tokens:
			sb.append(str(token))
			sb.append('\n')
		sb.append('Total Tokens = ')
		sb.append(str(len(self.tokens)))
		return ''.join(sb)

	# scan the input file for an ID token
	def scanID(self):
		type = 'ID'
		value = ''
		# is it a letter/number?
		while self.c.isalnum():
			# add to value and read next char
			value += self.c
			self.c = self.file.read(1)
		# 'unget' the last character
		self.file.seek(self.file.tell() - 1, os.SEEK_SET)

		# if it's a keyword, create that keyword token
		if value in keywords:
			type = keywords[value]

		return Token(type, value, self.lineNum)

	# scan the input file for a string token
	def scanString(self):
		type = 'STRING'
		value = '\''
		startLine = self.lineNum

		# looking for ' not followed by another '
		end = False
		while not end and self.c:
			self.c = self.file.read(1)
			value += self.c
			if self.c == '\'':
				self.c = self.file.read(1)
				if self.c == '\'':
					value += self.c
				else:
					# 'unget' the last character
					self.file.seek(self.file.tell() - 1, os.SEEK_SET)
					end = True
			elif self.c == '\n':
				self.lineNum += 1

		if not end:
			type = 'UNDEFINED'

		return Token(type, value, startLine)

	# scan the input file for a comment token
	def scanComment(self):
		type = 'COMMENT'
		value = '#'
		startLine = self.lineNum
		end = True

		self.c = self.file.read(1)

		# multiline; looking for | followed by #
		if self.c == '|':
			value += self.c

			end = False
			while not end and self.c:
				self.c = self.file.read(1)
				value += self.c
				if self.c == '|':
					self.c = self.file.read(1)
					value += self.c
					if self.c == '#':
						end = True
				if self.c == '\n':
					self.lineNum += 1
		# single line
		else:
			while self.c != '\n':
				value += self.c
				self.c = self.file.read(1)
			# 'unget' the last character
			self.file.seek(self.file.tell() - 1, os.SEEK_SET)

		# didn't find |# at the end of a multiline comment
		if not end:
			type = 'UNDEFINED'

		return Token(type, value, startLine)

	def removeComments(self):
		self.tokens = [token for token in self.tokens if token.type != 'COMMENT']

	# scans the file and splits into tokens, stored in tokens
	def scan(self, filename):
		self.file = open(filename, 'r')
		self.c = self.file.read(1)
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
				self.c = self.file.read(1)
				if self.c == '-':
					self.tokens.append(Token('COLON_DASH', ':-', self.lineNum))
				else:
					self.tokens.append(Token('COLON', ':', self.lineNum))
					# 'unget' the last character
					self.file.seek(self.file.tell() - 1, os.SEEK_SET)
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
					# skip whitespace
				else:
					self.tokens.append(Token('UNDEFINED', self.c, self.lineNum))
			self.c = self.file.read(1)
		# manually add EOF token
		self.tokens.append(Token('EOF', '', self.lineNum))
