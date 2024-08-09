from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'host': 'mysql',  # MySQL service name in Minikube
    'user': 'root',
    'password': 'password123',
    'database': 'tic_tac_toe_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Here you would typically verify the username and password
    # For simplicity, assume the login is always successful
    return jsonify({'status': 'success', 'message': f'Welcome {username}'})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM leaderboard ORDER BY wins DESC")
    leaderboard = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(leaderboard)

@app.route('/game/progress', methods=['POST'])
def save_game_progress():
    data = request.get_json()
    winner = data.get('winner')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leaderboard (player, wins) VALUES (%s, 1)
        ON DUPLICATE KEY UPDATE wins = wins + 1
    """, (winner,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'message': f'{winner} updated successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
