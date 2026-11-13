
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

START_TIME = time.time()


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "taskdb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "postgres123"),
        cursor_factory=RealDictCursor
    )


@app.route('/api/health', methods=['GET'])
def health_check():
    db_status = "Disconnected"
    latency_ms = None

    try:
        start = time.time()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()

        latency_ms = round((time.time() - start) * 1000, 2)
        db_status = "Connected"

    except Exception as e:
        db_status = f"Error: {str(e)}"

    return jsonify({
        "status": "healthy",
        "uptime": f"{int(time.time() - START_TIME)}s",
        "database": db_status,
        "db_latency_ms": latency_ms,
        "container": os.environ.get("HOSTNAME", "backend-container")
    })


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, priority, is_completed,
        to_char(created_at, 'HH24:MI:SS') AS time
        FROM tasks
        ORDER BY id DESC;
    """)

    tasks = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(tasks)


@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json(silent=True) or {}

    title = data.get('title', '').strip()
    priority = data.get('priority', 'MED').upper()

    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400

    if priority not in ['HIGH', 'MED', 'LOW']:
        priority = 'MED'

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (title, priority, is_completed)
        VALUES (%s, %s, false)
        RETURNING id, title, priority, is_completed,
        to_char(created_at, 'HH24:MI:SS') AS time;
    """, (title, priority))

    new_task = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_task), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def toggle_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET is_completed = NOT is_completed
        WHERE id = %s
        RETURNING id, title, priority, is_completed;
    """, (task_id,))

    updated = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(updated)


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id = %s RETURNING id;",
        (task_id,)
    )

    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"})


@app.route('/api/tasks/seed', methods=['POST'])
def seed_tasks():
    sample_tasks = [
        ('Validate PostgreSQL Volume Persistence', 'HIGH'),
        ('Test Horizontal Scalability', 'HIGH'),
        ('Calculate RAM Overhead using docker stats', 'MED'),
        ('Document Bridge Network Routing', 'LOW')
    ]

    conn = get_db_connection()
    cur = conn.cursor()

    for title, priority in sample_tasks:
        cur.execute("""
            INSERT INTO tasks (title, priority, is_completed)
            VALUES (%s, %s, false);
        """, (title, priority))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Sample tasks loaded successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
