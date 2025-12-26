import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL server
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="4056",
    port=5432
)

# Set autocommit mode to create database
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Create database
cursor = conn.cursor()
cursor.execute("SELECT 1 FROM pg_database WHERE datname='taskdb'")
exists = cursor.fetchone()

if not exists:
    cursor.execute("CREATE DATABASE taskdb")
    print("Database 'taskdb' created successfully!")
else:
    print("Database 'taskdb' already exists!")

cursor.close()
conn.close()
