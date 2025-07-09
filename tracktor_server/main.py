#!/usr/bin/env -S uv run --script

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from db_map import DBMapper

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}) # specify origins

db = DBMapper()

@app.route("/init", methods = ['GET'])
def init_db():
    db.init_project_table()
    db.init_shots_table()
    return jsonify({"message" : "Database init complete"})

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
    rows = db.get_projects()
    return jsonify([dict(row) for row in rows])

@app.route("/api/projects", methods=['POST'])
def create_project():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error":"Missing the project's name"}), 400
    
    name = data.get("name")
    type = data.get("type")
    status = "New"
    shotsNum = data.get("shotsNum")
    deadline = data.get("deadline")

    project_id = db.add_project(name, type, status, shotsNum, deadline)
    new_shot_list = db.add_shots_for_project(project_id, shotsNum)
    return jsonify({"project_id" : project_id, "project_name": name}), 201

@app.route("/api/projects/<int:project_id>", methods=['DELETE'])
def delete_project(project_id):
    db.remove_project(project_id)
    db.remove_shots_for_project(project_id)
    return jsonify({"message": "Project deleted"}), 200
    

@app.route("/api/projects/<int:project_id>", methods=['GET'])
def display_project(project_id):
    row = db.get_project(project_id)
    if row is None:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(dict(row))

@app.route("/api/shots", methods=['GET'])
def existing_shots():
    shot_rows = db.get_all_shots()
    return jsonify([dict(shot_row) for shot_row in shot_rows])

@app.route("/api/projects/<int:project_id>/shots", methods=['GET'])
def display_shots_for_project(project_id):
    shots = db.get_shots_from_project(project_id)
    return jsonify([dict(shot) for shot in shots])

@app.route("/api/projects/<int:project_id>/shots/<int:shot_id>", methods = ['PATCH'])
def change_status(project_id, shot_id):
    data = request.get_json()
    status_item = data.get("status_item")
    value = data.get("value")
    if not status_item or value is None:
        return jsonify({"error" : "Missing required components to update the shot"})
    db.change_shot_status(shot_id, status_item, value)
    return jsonify({"message" : "Shot updated"})


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, port=8080)