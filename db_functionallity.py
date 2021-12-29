import psycopg2 as psycopg2

conn = psycopg2.connect('users.db')
cur = conn.cursor()