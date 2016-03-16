#!/usr/bin/python
import sys;

class Database:
	__db = {};
	__history = [];
	__db_val = {};

	def set(self, name, val):
		if self.__history: 
			if name not in self.__db:
				self.__history[-1][name] = None;
			if name in self.__db and \
					name not in self.__history[-1]:
				self.__history[-1][name] = self.get(name);

		if val in self.__db_val: self.__db_val[val] += 1;
		else: self.__db_val[val] = 1;

		if self.get(name) in self.__db_val:
			self.__db_val[self.get(name)] -= 1;

		self.__db[name] = val;

	def get(self, name):
		try:
			return self.__db[name];
		except KeyError:
			return None;

	def unset(self, name):
		if self.__history and name in self.__db and \
				name not in self.__history[-1]:
			self.__history[-1][name] = self.get(name);
		try:
			self.__db_val[self.get(name)] -= 1;
			del self.__db[name];
		except KeyError:
			return;

	def num_equal_to(self, value):
		try:
			return self.__db_val[value];
		except KeyError:
			return 0;

	def begin(self):
		self.__history.append({});

	def rollback(self):
		if not self.__history: 
			return False;
		
		for (name, val) in self.__history.pop().items():
			cur_val = self.get(name);
			if cur_val in self.__db_val:
				self.__db_val[cur_val] -= 1;

			if val is None: del self.__db[name];
			else: self.__db[name] = val;

			if val in self.__db_val: self.__db_val[val] += 1;
			else: self.__db_val[val] = 1;

		return True;

	def commit(self):
		if not self.__history: 
			return False;
		self.__history = [];
		return True;

class Command:
	__cmd = "";

	def _set(self, db):
		db.set(self.__cmd[1], self.__cmd[2]);

	def _get(self, db):
		val = db.get(self.__cmd[1]);
		if not val: print 'NULL';
		else: print val;

	def _unset(self, db):
		db.unset(self.__cmd[1]);

	def _num_equal_to(self, db):
		print db.num_equal_to(self.__cmd[1]);

	def _begin(self, db):
		db.begin();

	def _rollback(self, db):
		if not db.rollback(): print 'NO TRANSACTION';

	def _commit(self, db):
		if not db.commit(): print 'NO TRANSACTION';

	def _exception(self):
		print ' '.join(self.__cmd) + " is an UNKNOWN command";

	options = {'SET' : _set,
			   'GET' : _get,
			   'UNSET' : _unset,
			   'NUMEQUALTO' : _num_equal_to,
			   'BEGIN' : _begin,
			   'ROLLBACK' : _rollback,
			   'COMMIT' : _commit};

	def __init__(self, line):
		self.__cmd = line.split();

	def __del__(self):
		del self.__cmd;
		
	def execute(self, db):
		try:
			Command.options[self.__cmd[0]](self, db);
		except KeyError:
			self._exception();

def main():

	db = Database();

	while True:
		line = raw_input();
		if line == 'END' : break;
		cmd = Command(line);
		cmd.execute(db);

if __name__ == "__main__" : main();