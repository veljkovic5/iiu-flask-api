from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Tabela uređaja / senzora
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. GET - Prikaz svih uređaja
@app.route('/api/devices', methods=['GET'])
def get_devices():
    conn = get_db_connection()
    devices = conn.execute('SELECT * FROM devices').fetchall()
    conn.close()
    return jsonify([dict(d) for d in devices]), 200

# 2. GET sa parametrima - Pretraga po tipu
@app.route('/api/devices/search', methods=['GET'])
def search_devices():
    device_type = request.args.get('type')
    conn = get_db_connection()
    devices = conn.execute('SELECT * FROM devices WHERE type = ?', (device_type,)).fetchall()
    conn.close()
    return jsonify([dict(d) for d in devices]), 200

# 3. POST - Dodavanje novog uređaja
@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    name = data.get('name')
    dev_type = data.get('type')
    status = data.get('status', 'off')

    conn = get_db_connection()
    conn.execute('INSERT INTO devices (name, type, status) VALUES (?, ?, ?)',
                 (name, dev_type, status))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Uređaj uspešno dodat!"}), 201

# 4. PUT - Izmena postojećeg uređaja
@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.get_json()
    status = data.get('status')

    conn = get_db_connection()
    conn.execute('UPDATE devices SET status = ? WHERE id = ?', (status, device_id))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Uređaj uspešno izmenjen!"}), 200

# 5. DELETE - Brisanje uređaja
@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM devices WHERE id = ?', (device_id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Uređaj uspešno obrisan!"}), 200

if __name__ == '__main__':
    app.run(debug=True)