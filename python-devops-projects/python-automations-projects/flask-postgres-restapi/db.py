import psycopg2
import json

# Load configuration from the JSON file
with open('config.json', 'r') as file:
    config = json.load(file)

# Database configuration
db_config = config['postgres']

def get_db_connection():
    connection = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        database=db_config['database'],
        user=db_config['user'],
        password=db_config['password']
    )
    return connection

def read_from_db(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def write_to_db(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()
