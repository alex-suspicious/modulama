import sqlite3
import vendor.env as env
import os

def createDBFolder():
	db_directory = env.get("DB_FILE").split("/")
	db_directory.pop()
	db_directory = "/".join(db_directory)

	if not os.path.exists(db_directory):
		os.makedirs(db_directory)

class data:
	table = ""
	createItem = False
	whereConn = []
	attributes = {}
	variables = {}

	def __init__(self, table, attributes):
		self.createItem = False
		self.whereConn = []
		self.variables = {}
		self.table = table
		self.attributes = attributes
		self.keys = list(self.attributes.keys())

		self.conn = sqlite3.connect( env.get("DB_FILE") )
		self.cur = self.conn.cursor()

	@staticmethod
	def replaceTypes( string ):
		return string.replace("int","INTEGER").replace("str","TEXT").replace("float","NUMERIC")

	def getWhereQuery(self):
		whereQuery = ""
		if( len(self.whereConn) > 0 ):
			whereQuery = " WHERE"
			whereRaw = []
			for x in range(len(self.whereConn)):
				whereRaw.append( f" {self.whereConn[x][0]} {self.whereConn[x][1]} {self.whereConn[x][2]} " )
			whereQuery += "AND".join(whereRaw)

		return whereQuery

	def interpreteWhereAsCreation(self):
		createQuery = {}
		if( len(self.whereConn) > 0 ):
			for x in range(len(self.whereConn)):
				createQuery[self.whereConn[x][0]] = self.whereConn[x][2]

		return createQuery

	def where(self, A="",B="=",C="", create = False):
		self.createItem = create
		if( len( str(B) ) > 2 ):
			self.whereConn.append([A,"=",str(B)])
		else:
			self.whereConn.append([A,B,C])

	def load(self):
		query = f"CREATE TABLE IF NOT EXISTS \"{str(self.table)}\" ( id INTEGER PRIMARY KEY AUTOINCREMENT"
		for x in range(len(self.keys)):
			query += f", {self.keys[x]} { self.replaceTypes( self.attributes[self.keys[x]] ).upper()}"
		query += ");"

		self.conn.execute(query)
		self.conn.commit()

		self.cur.execute(f"PRAGMA table_info({self.table});")
		columns = [column[1] for column in self.cur.fetchall()]
		print(columns)

		for x in range(len(self.keys)):
			if self.keys[x] not in columns:
				self.cur.execute(f"ALTER TABLE {self.table} ADD COLUMN {self.keys[x]} { self.replaceTypes( self.attributes[self.keys[x]] ).upper()};")

		for x in range(len(columns)):
			if columns[x] not in self.keys and columns[x] != "id":
				self.cur.execute(f"ALTER TABLE {self.table} DROP COLUMN {columns[x]};")

		self.conn.commit()


	def update(self, rows):
		for x in range( len(rows[0]) ):
			typeCheck = self.replaceTypes( self.attributes[self.keys[x]] ).upper()
			if( not rows[0][x] ):
				if( typeCheck == "INTEGER" or typeCheck == "NUMERIC" ):
					self.variables[ self.keys[x] ] = 0
				else:
					self.variables[ self.keys[x] ] = ""
			else:
				if( typeCheck == "INTEGER" ):
					self.variables[ self.keys[x] ] = int(rows[0][x])
				elif( typeCheck == "NUMERIC" ):
					self.variables[ self.keys[x] ] = float(rows[0][x])
				else:
					self.variables[ self.keys[x] ] = rows[0][x]

	def create(self,parameters):
		self.load()
		tempKeys = list(parameters.keys())
		items = parameters.values()

		query = f"INSERT INTO {self.table} ({','.join(tempKeys)}) VALUES (\"" + "\",\"".join(str(v) for v in items) + "\");"
		print(query)
		self.cur.execute(query)
		self.conn.commit()

		self.whereConn = [["id","=", self.cur.lastrowid]]
		rows = self.cur.execute(f"SELECT {','.join(self.keys)} FROM ({self.table}){self.getWhereQuery()}" ).fetchall()
		
		if( len(rows) > 0 ):
			self.update(rows)


	def save(self):
		variableKeys = list(self.variables.keys())
		query = []

		for x in range( len(variableKeys) ):
			if( variableKeys[x] != "id" ):
				query.append( f"{variableKeys[x]} = '{self.variables[variableKeys[x]]}'" )

		self.conn.execute(f"UPDATE {self.table} SET {','.join(query)}{self.getWhereQuery()}")
		self.conn.commit()

	def first(self):
		rows = self.cur.execute(f"SELECT {','.join(self.keys)} FROM ({self.table}){self.getWhereQuery()}" ).fetchall()
		print(rows)
		if( len(rows) > 0 ):
			self.update(rows)
		elif( self.createItem ):
			self.create( self.interpreteWhereAsCreation() )

