from tabulate import tabulate



class HotArg:
	def __init__(self, arg):
		self.arg = arg

	def __repr__(self):
		return f"HotArg ('{self.arg}')"


class HotFlag:
	def __init__(self, arg):
		self.flag = arg
		self.args = []
		self.n = 0

	def __iter__(self):
		return iter(self.args)

	@property
	def count(self):
		return len(self.args)

	def add_arg(self, arg):
		self.args.append(HotArg(arg))

	def row(self, idx=None):
		if idx is None:
			return [self.flag, self.count, self.args]
		else:
			return [idx, *self.row()]

	def __repr__(self):
		return f"HotArg ('{self.flag}', {self.args})"


class HotParse(HotFlag):
	def __init__(self):
		self.flags = []
		self.args = []

	def __iter__(self):
		return iter(self.flags)

	@property
	def flags_count(self):
		return len(self.flags)

	def parse_args(self, args):
		current = self.flags[-1] if self.flags else self
		for arg in args:
			if arg[0] == "-":
				current = HotFlag(arg)
				self.flags.append(current)
			else:
				current.add_arg(arg)
		return self.flags

	def row(self):
		return [ "", "", self.count, self.args ]

	def rows(self):
		rows = [hotflag.row(idx+1) for idx, hotflag in enumerate(self.flags)]
		return rows

	def print(self):
		print(tabulate([self.row(), *self.rows()], headers=["Id", "Flag", "N", "Args"]))


