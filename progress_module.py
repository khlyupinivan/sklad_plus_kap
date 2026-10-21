import sqlite3
from sqlite3 import Error
import datetime
import pandas as pd


def db_connection(db):
    try:
        con = sqlite3.connect(db)
        return con
 
    except Error:
        print(Error)


def create_tables(db):
    cursor  = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                name TEXT,
                id TEXT,
                lvl INT DEFAULT 0,
                stran INT DEFAULT 0,
                agil INT DEFAULT 0,
                stam INT DEFAULT 0,
                dates DATETIME DEFAULT 0
            )""")
    db.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS upgrades_users (
                name TEXT,
                id TEXT,
                lvl INT DEFAULT 0,
                stran INT DEFAULT 0,
                agil INT DEFAULT 0,
                stam INT DEFAULT 0,
                dates DATETIME DEFAULT 0
            )""")
    db.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS upgrades_this_week (
                name TEXT,
                id TEXT,
                lvl INT DEFAULT 0,
                stran INT DEFAULT 0,
                agil INT DEFAULT 0,
                stam INT DEFAULT 0
            )""")
    db.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS upgrades_last_week (
                name TEXT,
                id TEXT,
                lvl INT DEFAULT 0,
                stran INT DEFAULT 0,
                agil INT DEFAULT 0,
                stam INT DEFAULT 0
            )""")
    db.commit()


def add_user(db, id_user, name_user):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT id FROM users WHERE id = ?", [id_user])
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO upgrades_users(id, name) VALUES (?, ?)', [id_user, name_user])
            db.commit()
            cursor.execute('INSERT INTO upgrades_this_week(id, name) VALUES (?, ?)', [id_user, name_user])
            db.commit()
            cursor.execute('INSERT INTO upgrades_last_week(id, name) VALUES (?, ?)', [id_user, name_user])
            db.commit()
            cursor.execute('INSERT INTO users(id, name) VALUES (?, ?)', [id_user, name_user])
            db.commit()
            return 'Участник добавлен'
        else:
            return 'Участник уже существует'

    except Error:
        print(Error)


def update_user_progress(db, id_user, lvl, stran, agil, stam, dates):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT lvl FROM upgrades_users WHERE id = ?", [id_user])
        lvl_in_table = cursor.fetchone()
        if lvl_in_table is None:
            return 'Участник не найден'
        elif lvl_in_table[0] == 0:
            cursor.execute('UPDATE upgrades_users SET lvl = ?, stran = ?, agil = ?, stam = ?, dates = ? WHERE id = ?', (lvl, stran, agil, stam, dates, id_user))
            db.commit()
            return 'База обновлена'
        print("База данных участников обновлена")

    except Error:
        print(Error)


def update_user_progress_last_week(db):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT * FROM upgrades_this_week")
        record_this = cursor.fetchall()
        cursor.execute("SELECT * FROM users")
        record_user = cursor.fetchall()
        if record_this is None:
            return 'База не заполнена'
        else:
            for row in record_this:
                cursor.execute('UPDATE upgrades_last_week SET lvl = ?, stran = ?, agil = ?, stam = ? WHERE id = ?', (row[2], row[3], row[4], row[5], row[1]))
                db.commit()
            for row in record_user:
                cursor.execute('UPDATE upgrades_this_week SET lvl = ?, stran = ?, agil = ?, stam = ? WHERE id = ?', (row[2], row[3], row[4], row[5], row[1]))
                db.commit()
            return 'База обновлена'

    except Error:
        print(Error)


def update_user_stats(db, id_user, lvl, stran, agil, stam, dates):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT id FROM users WHERE id = ?", [id_user])
        if cursor.fetchone() is None:
            return 'Участник не найден'
        else:
            cursor.execute('UPDATE users SET lvl = ?, stran = ?, agil = ?, stam = ?, dates = ? WHERE id = ?', ( lvl, stran, agil, stam, dates, id_user))
            db.commit()
            return 'База обновлена'

    except Error:
        print(Error)


def delete_progress(db, id_user):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT * FROM upgrades_users WHERE id = ?", [id_user])
        if cursor.fetchall() is None:
            return "Участник не найден"
        else:
            cursor.execute('UPDATE upgrades_users SET lvl = ? WHERE id = ?', (0, id_user))
            db.commit()
            return 'База обновлена'
        
    except Error:
        print(Error)


def create_progress_message(db, id_user):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT * FROM upgrades_users WHERE id = ?", [id_user])
        record_progress = cursor.fetchall()
        if record_progress is None:
            return 'Участник не найден'
        else:
            record_progress = record_progress[0]
            cursor.execute("SELECT * FROM users WHERE id = ?", [id_user])
            record_user = cursor.fetchall()[0]
            date_now = record_progress[6]
            date_progress = date_now[0:10]
            message = f'[{record_user[1]}|{record_user[0]}], ваш прогресс от {date_progress}:\nlvl +{record_user[2]-record_progress[2]} 👊 +{record_user[3]-record_progress[3]} 🖐 +{record_user[4]-record_progress[4]} ❤ +{record_user[5]-record_progress[5]}'
            return message
        
    except Error:
        print(Error)


def create_stats_message(db, id_user):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT * FROM users WHERE id = ?", [id_user])
        record = cursor.fetchone()
        max_stam = record[2]*3 + 45
        max_str_agil = max_stam*2
        return f'[{record[1]}|{record[0]}], ваш кап:\n(👊+🖐) = {(record[3]+record[4])}/{max_str_agil} ({max_str_agil - record[3] - record[4]})\n(❤) = {record[5]}/{max_stam} ({max_stam - record[5]})'
        
    except Error:
        print(Error)


def create_all_progress(db):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT * FROM upgrades_last_week")
        record_last = cursor.fetchall()
        cursor.execute("SELECT * FROM upgrades_this_week")
        record_this = cursor.fetchall()
        message = ""
        list_progress = {"Имя": [record_this[0][0]],
                      "Уровень": [record_this[0][2]],
                      "Сила": [record_this[0][3]],
                      "Ловкость": [record_this[0][4]],
                      "Выносливость": [record_this[0][5]],
                      "+Уровень": [record_this[0][2]-record_last[0][2]],
                      "+Сила": [record_this[0][3]-record_last[0][3]],
                      "+Ловкость": [record_this[0][4]-record_last[0][4]],
                      "+Выносливость": [record_this[0][5]-record_last[0][5]]
                      }
        for i in range(1, len(record_last)):
            list_progress["Имя"].append(record_this[i][0])
            list_progress["Уровень"].append(record_this[i][2])
            list_progress["Сила"].append(record_this[i][3])
            list_progress["Ловкость"].append(record_this[i][4])
            list_progress["Выносливость"].append(record_this[i][5])
            list_progress["+Уровень"].append(record_this[i][2]-record_last[i][2])
            list_progress["+Сила"].append(record_this[i][3]-record_last[i][3])
            list_progress["+Ловкость"].append(record_this[i][4]-record_last[i][4])
            list_progress["+Выносливость"].append(record_this[i][5]-record_last[i][5])
        statistic_list = pd.DataFrame(list_progress)
        statistic_list.to_excel("statistics.xlsx")
        return list_progress

    except Error:
        print(Error)


def show_user_progress(db, id_user):
    try:
        cursor = db.cursor()
        create_tables(db)
        cursor.execute("SELECT * FROM upgrades_users WHERE id = ?", [id_user])
        record_progress = cursor.fetchall()[0]
        cursor.execute("SELECT * FROM users WHERE id = ?", [id_user])
        record_user = cursor.fetchall()[0]
        message = f'[{record_user[1]}|{record_user[0]}] за {(record_user[6]-record_progress[6]).days}дней:\nlvl = {record_user[2]}({record_user[2]-record_progress[2]})\n(👊) = {record_user[3]}({record_user[3]-record_progress[3]})\n(🖐) = {record_user[4]}({record_user[4]-record_progress[4]})\n(❤) = {record_user[5]}({record_user[5]-record_progress[5]})'
        return message
        
    except Error:
        print(Error)


def delete_user(db, id_user):
    cursor = db.cursor()
    create_tables(db)
    cursor.execute("SELECT id FROM users WHERE id = ?", [id_user])
    record = cursor.fetchone()
    if record is not None:
        cursor.execute("DELETE FROM users WHERE id = ?", [id_user])
        cursor.execute("DELETE FROM upgrades_users WHERE id = ?", [id_user])
        cursor.execute("DELETE FROM upgrades_this_week WHERE id = ?", [id_user])
        cursor.execute("DELETE FROM upgrades_last_week WHERE id = ?", [id_user])
        return 'Душа изгнанника не заслуживает быть увековеченой в списке достойных'
    else: return 'Невозможно изгнать того, кого нет'
 