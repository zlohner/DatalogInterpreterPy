class Relation(object):
	def __init__(self, schema=None, tuples=None):
		if schema:
			self.schema = schema
		else:
			self.schema = []

		if tuples:
			self.tuples = tuples
		else:
			self.tuples = set([])

	def select(self, values):
		selected = set([])
		for t in self.tuples:
			add = True
			for index, value in values:
				if not t[index] == value:
					add = False
					break
			if add:
				selected.add(t)
		self.tuples = selected
		return self

	def selectEqual(self, equal):
		selected = set([])
		for t in self.tuples:
			add = True
			for pair in equal:
				if t[pair[0]] != t[pair[1]]:
					add = False
					break
			if add:
				selected.add(t)
		self.tuples = selected
		return self

	def project(self, columns):
		projectSchema = []
		for column in columns:
			projectSchema.append(self.schema[column])
		self.schema = projectSchema

		projected = set([])
		for t in self.tuples:
			projected.add(tuple(t[column] for column in columns))

		self.tuples = projected
		return self

	def rename(self, params):
		idCount = 0
		for t in params:
			if t.type == 'ID':
				self.schema[idCount] = t.value
				idCount += 1

		equal = []
		for i in range(len(self.schema)):
			for j in range(i + 1, len(self.schema)):
				if self.schema[i] == self.schema[j]:
					equal.append((i, j))

		self.selectEqual(equal)

	def restrictions(self, R):
		return [(i, j) for i, s1 in enumerate(self.schema) for j, s2 in enumerate(R.schema) if s1 == s2]

	def joinSchema(self, R, restrictions):
		joinedSchema = self.schema
		for i in range(len(R.schema)):
			add = True
			for restriction in restrictions:
				if i == restriction[1]:
					add = False
					break
			if add:
				joinedSchema.append(R.schema[i])
		return joinedSchema

	def joinable(self, t1, t2, restrictions):
		for restriction in restrictions:
			if t1[restriction[0]] != t2[restriction[1]]:
				return False
		return True

	def tupleJoin(self, t1, t2, restrictions):
		joined = list(t1)

		for i, s in enumerate(t2):
			add = True
			for restriction in restrictions:
				if i == restriction[1]:
					add = False
					break
			if add:
				joined.append(s)

		return tuple(joined)

	def join(self, R):
		restrictions = self.restrictions(R)

		self.schema = self.joinSchema(R, restrictions)

		joined = set([])
		for t1 in self.tuples:
			for t2 in R.tuples:
				if self.joinable(t1, t2, restrictions):
					joined.add(self.tupleJoin(t1, t2, restrictions))

		self.tuples = joined

		return self

	def __len__(self):
		return len(self.tuples)

	def __str__(self):
		sb = []

		if len(self.schema) > 0:
			uniques = set([])
			columns = []

			for i, id in enumerate(self.schema):
				if id not in uniques:
					uniques.add(id)
					columns.append(i)

			for t in sorted(self.tuples):
				sb.append('\n  ' + self.schema[0] + '=' + t[0])
				for i in columns[1:]:
					sb.append(', ' + self.schema[i] + '=' + t[i])

		return ''.join(sb)
