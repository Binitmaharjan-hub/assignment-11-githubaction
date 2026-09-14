import os
from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)


def ensure_users_table():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(500) NOT NULL
                )
                """
            )
            cursor.execute(
                "INSERT INTO users (name) SELECT 'binit' WHERE NOT EXISTS (SELECT 1 FROM users WHERE name = 'binit')"
            )
            cursor.execute(
                "INSERT INTO users (name) SELECT 'alina' WHERE NOT EXISTS (SELECT 1 FROM users WHERE name = 'alina')"
            )
        conn.commit()
    finally:
        conn.close()


def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD', 'userpassword'),
        database=os.getenv('DB_NAME', 'appdb'),
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/api/users', methods=['GET'])
def get_users():
    ensure_users_table()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM users")
            users = cursor.fetchall()
            return jsonify(users), 200
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
