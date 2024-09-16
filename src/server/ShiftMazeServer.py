from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'leaderboard.db'


def getDb():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initDb():
    with getDb() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')
        conn.commit()


def addScoreToDb(name, score):
    with getDb() as conn:
        conn.execute('''
            INSERT INTO leaderboard (name, score)
            VALUES (?, ?)
        ''', (name, score))
        conn.commit()

        # Remove rows if there are more than 10
        conn.execute('''
            DELETE FROM leaderboard
            WHERE id NOT IN (
                SELECT id FROM leaderboard
                ORDER BY score DESC
                LIMIT 10
            )
        ''')
        conn.commit()


def getLeaderboardFromDb():
    with getDb() as conn:
        cur = conn.execute('''
            SELECT name, score FROM leaderboard
            ORDER BY score DESC
            LIMIT 10
        ''')
        return cur.fetchall()


@app.route('/add-score', methods=['POST'])
def addScore():
    data = request.get_json()
    name = data['name']
    score = data['score']

    addScoreToDb(name, score)
    return jsonify({'message': 'Score added successfully.'})


@app.route('/get-leaderboard', methods=['GET'])
def getLeaderboard():
    leaderboard = getLeaderboardFromDb()
    return jsonify([dict(row) for row in leaderboard])


if __name__ == '__main__':
    initDb()
    app.run()
