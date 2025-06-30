from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}) # specify origins

def get_db():
    connection = sqlite3.connect("projects.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/init", methods = ['GET'])
def init_db():
    conn = get_db()
    conn.execute("""
                    CREATE TABLE IF NOT EXISTS projects(
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 name TEXT NOT NULL
                 )
                 """)
    conn.commit()
    conn.close()
    return jsonify({"message" : "Database init complete"})
projects = []

@app.route("/api/users", methods =['GET'])
def users():
    return jsonify(
        {
            "users": [
                'zack',
                'pan',
                'jessy'
            ]
        }
    )

@app.route("/api/projects", methods=['GET'])
def existing_projects():
    conn = get_db()
    rows = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/projects", methods=['POST'])
def create_project():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error":"Missing the project's name"}), 400
    
    name = data.get("name")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects(name) VALUES(?)", (name,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    new_project = {"id": new_id, "name" : name}

    print("Current projects:", projects)
    return jsonify(new_project), 201

@app.route("/api/projects/<int:project_id>", methods=['DELETE'])
def delete_project(project_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Project deleted"}), 200
    

@app.route("/api/projects/<int:project_id>", methods=['GET'])
def get_project(project_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(dict(row))



if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, port=8080)