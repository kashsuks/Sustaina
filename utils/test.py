import psycopg2
import os

databaseURL = os.getenv('DATABASE_URL')

try:    
    conn = psycopg2.connect(databaseURL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(cur.fetchone())
except Exception as e:
    print("Error:", e)