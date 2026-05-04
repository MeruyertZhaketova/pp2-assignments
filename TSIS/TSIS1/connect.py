import psycopg2
from config import config

def connect():
    try:
        return psycopg2.connect(**config)
    except Exception as e:
        print("Database connection error:", e)
        raise