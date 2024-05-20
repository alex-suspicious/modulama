import sqlite3
import vendor.env as env

class data:
	table = ""
	def __init__(self, table):
		async with aiosqlite.connect( env.get("DB_FILE") ) as db:
			await db.execute("INSERT INTO")
			await db.commit()

			async with db.execute("SELECT * FROM") as cursor:
				async for row in cursor:
					print( dir(row) )