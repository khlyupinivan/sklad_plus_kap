import sqlite3
from sqlite3 import Error


def db_connection(db):
	try:
		con = sqlite3.connect(db)
		return con

	except Error:
		print(Error)


def create_table_users(db):
	try:
		cursor = db.cursor()

		cursor.execute("""CREATE TABLE IF NOT EXISTS users (
			id TEXT,
			name TEXT,
			cash INT DEFAULT 0
		)""")
		db.commit()

	except Error:
		print(Error)


def add_user(db, id_user, name_user):
	try:
		create_table_users(db)
		cursor = db.cursor()
		cursor.execute("SELECT id FROM users WHERE id = ?", [id_user])
		record = cursor.fetchone()
		if record is None:
			cursor.execute('INSERT INTO users(id, name) VALUES (?, ?)', [id_user, name_user]) 
			db.commit()
			return 'Участник добавлен'
		else:
			return 'Участник уже существует'

		print("База данных участников обновлена")

	except Error:
		print(Error)


def check_cash(db, id_user, sum_cost):
	try:
		create_table_users(db)
		cursor = db.cursor()
		cursor.execute("SELECT cash FROM users WHERE id = ?", [id_user])
		cash_user = cursor.fetchone()[0]
		if cash_user is None:
			return False
		elif cash_user < sum_cost:
			return False
		elif cash_user >= sum_cost:
			return True

	except Error:
		print(Error)


def update_users_cash(db, id_user, sum_cost, sign):
	try:
		create_table_users(db)
		cursor = db.cursor()
		cursor.execute("SELECT * FROM users WHERE id = ?", [id_user])
		record = cursor.fetchmany()[0]
		print(record)
		if record is None:
			return 'Участник не найден'
		elif sign == True:
			id_user = record[0]
			name_user = record[1]
			cash_user = record[2]
			print(id_user)
			print(name_user)
			print(cash_user)
			new_cash = cash_user + sum_cost
			cursor.execute("UPDATE users SET cash = ? WHERE id = ?", [new_cash, id_user])
			db.commit()
			return f'@id{id_user} ({name_user}) теперь вы обладаете {new_cash} душ'
		elif sign == False:
			id_user = record[0]
			name_user = record[1]
			cash_user = record[2]
			print(id_user)
			print(name_user)
			print(cash_user)
			new_cash = cash_user - sum_cost
			cursor.execute("UPDATE users SET cash = ? WHERE id = ?", [new_cash, id_user])
			print('execute?')
			db.commit()
			print('commit?')
			return f'@id{id_user} ({name_user}) теперь вы обладаете {new_cash} душ'

	except Error:
		print(Error)


def get_cash(db, id_user):
	try:
		create_table_users(db)
		cursor = db.cursor()
		cursor.execute("SELECT cash FROM users WHERE id = ?", [id_user])
		cash_user = cursor.fetchone()[0]
		if cash_user is None:
			return 'Участник не найден'
		else:
			return cash_user
	except Error:
		print(Error)


def print_user(db, id_user):
	try:
		create_table_users(db)
		cursor = db.cursor()
		cursor.execute("SELECT * FROM users WHERE id = ?", [id_user])
		record = cursor.fetchone()
		if record is None:
			return "Участник не найден"
		else:
			return f"@id{record[0]} ({record[1]}) - {record[2]}"

	except Error:
		print(Error)


def print_table_users(db):
	try:
		create_table_users(db)
		cursor = db.cursor()
		message = ""
		cursor.execute("SELECT * FROM users")
		record = cursor.fetchall()
		for row in record:
			message = message + f"\nhttps://vk.com/id{row[0]} ({row[1]}) - {row[2]}"
		return message
	except Error:
		print(Error)


def create_table_books (db):
	try:
		cursor = db.cursor()
		cursor.execute ("""CREATE TABLE IF NOT EXISTS books(
			name TEXT,
			price INT
		)""")
		db.commit()
	except Error:
		print (Error)


def add_book (db, name, price):
	try:
		create_table_books(db)
		cursor = db.cursor()
		cursor.execute("SELECT name FROM books WHERE name = ?", [name])
		if cursor.fetchone() is None:
			cursor.execute("INSERT INTO books VALUES (?, ?)", [name, price])
			db.commit()
			return "Книга добавлена в перечень"
		else:
			return "Книга уже существует"
	except Error:
		print(Error)


def get_price_book (db, name):
	try:
		create_table_books(db)
		cursor = db.cursor()
		cursor.execute("SELECT price FROM books WHERE name = ?", [name])
		record = cursor.fetchone()[0]
		if record is None:
			return 'Книга не найдена'
		else:
			return record
	except Error:
		print(Error)


def update_price(db, name, price):
	try:
		create_table_books(db)
		cursor = db.cursor()
		cursor.execute("SELECT name FROM books WHERE name = ?", [name])
		if cursor.fetchone() is None:
			return "Книга не найдена"
		else:
			cursor.execute("UPDATE books SET price = ? WHERE name = ?", [price, name])
			db.commit()
			return "Цена обновлена"
	except Error:
		print(Error)


def get_book_list(db):
	try:
		create_table_books(db)
		cursor = db.cursor()
		cursor.execute("SELECT name From books")
		record = cursor.fetchall()
		records = []
		for row in record:
			records.append(row[0])
		return records
	except Error:
		print(Error)


def print_table_books(db):
	try:
		create_table_books(db)
		cursor = db.cursor()
		cursor.execute("SELECT * FROM books")
		records = cursor.fetchall()
		message = ''
		if records is None:
			return 'Таблица книг не обнаружена'
		else:
			for record in records:
				message = message + f'{record[0]}: {record[1]}\n'
			return message

	except Error:
		print(Error)


def create_table_items(db):
	try:
		cursor = db.cursor()
		cursor.execute ("""CREATE TABLE IF NOT EXISTS items(
			name TEXT
		)""")
		db.commit()
	except Error:
		print (Error)


def update_item_list (db, name_item):
	try:
		create_table_items(db)
		cursor = db.cursor()
		cursor.execute("SELECT name FROM items WHERE name = ?", [name_item])
		if cursor.fetchone() is None:
			cursor.execute("INSERT INTO items VALUES (?)", [name_item])
			db.commit()
			return "Предмет добавлена в перечень"
		else:
			return "Предмет уже в списке"
	except Error:
		print(Error)


def get_item_list(db):
	try:
		create_table_items(db)
		cursor = db.cursor()
		cursor.execute("SELECT name From items")
		record = cursor.fetchall()
		records = []
		for row in record:
			records.append(row[0])
		return records
	except Error:
		print(Error)

def get_sum_cash(db):
    create_table_users(db)
    cursor = db.cursor()
    cursor.execute("SELECT cash FROM users")
    record = cursor.fetchall()
    if not record is None:
        sum_cost = 0
        for i in record:
            sum_cost += i[0]
        db.commit()
        return str(sum_cost)
    else:
        return "Участники не найдены"

		
# name_db = 'server.db'
# base = db_connection(name_db)
# cursor = base.cursor()
# cursor.execute("DROP TABLE IF EXISTS users")
# base.commit()