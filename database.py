import os

import psycopg2
import datetime
from dotenv import load_dotenv

load_dotenv()


def con():
    return psycopg2.connect(
        dbname=os.getenv('dbname'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        host=os.getenv('host'),
        port=os.getenv('port')
    )


def create_table():
    conn = con()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(30)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(30),
            last_name VARCHAR(30),
            img VARCHAR(255),
            birth_date TIMESTAMP,
            role_id INTEGER REFERENCES Roles(id)
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()


def info():
    conn = con()
    cur = conn.cursor()
    today = datetime.datetime.now().strftime('%m-%d')
    query = f"SELECT * FROM Users WHERE to_char(birth_date, 'MM-DD') = '{today}'"
    cur.execute(query)
    birthdays = cur.fetchall()
    messages = []
    for user in birthdays:
        #message = f"Bugun {first_name} {last_name}ning tug'ilgan kuni, tabriklaymiz! 🎉🎂"
        messages.append(user)
    return messages


def insert_user(first_name, last_name, img, birth_date, role_id):
    conn = con()
    cur = conn.cursor()
    cur.execute(
        '''
        INSERT INTO Users(first_name, last_name, img, birth_date, role_id)
        VALUES (%s, %s, %s, %s, %s)
        ''', (first_name, last_name, img, birth_date, role_id)
    )