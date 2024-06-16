from flask import Flask, request, jsonify, send_from_directory
import pymysql.cursors
import time

app = Flask(__name__)

time.sleep(10)

connection = pymysql.connect(
    host='db',
    user='root',
    password='example',
    database='test_db',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/add', methods=['POST'])
def add_entry():
    data = request.get_json()
    with connection.cursor() as cursor:
        sql = "INSERT INTO entries (content) VALUES (%s)"
        cursor.execute(sql, (data['content'],))
        connection.commit()
    return jsonify({'message': 'Entry added'}), 201

@app.route('/entries', methods=['GET'])
def get_entries():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM entries")
        result = cursor.fetchall()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

