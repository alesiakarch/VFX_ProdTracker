#!/usr/bin/env -S uv run --script

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from tracktor_server.projects_db_map import ProjectsDBMapper
from tracktor_server.shots_db_map import ShotsDBMapper
from tracktor_server.users_db_map import UsersDBMapper
from tracktor_server.usersProjects_db_map import UsersProjectsDBMapper
from tracktor_server.assets_db_map import AssetsDBMapper

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}) # specify origins

db_path = "tracktor.db"
projects_table = ProjectsDBMapper(db_path)
shots_table = ShotsDBMapper(db_path)
users_table = UsersDBMapper(db_path)
usersProjects_table = UsersProjectsDBMapper(db_path)
assets_table = AssetsDBMapper(db_path)

@app.route("/init", methods = ['GET'])
def init_db():
    projects_table.init_project_table()
    shots_table.init_shots_table()
    users_table.init_users_table()
    usersProjects_table.init_usersProjects_table()
    assets_table.init_assets_table()
    return jsonify({"message" : "Database init complete"})

@app.route("/api/users", methods =['GET'])
def existing_users():
    rows = users_table.get_users()
    users = []
    for row in rows:
        user_dict = dict(row)
        user_dict.pop("user_password", None)
        users.append(user_dict)
    return jsonify(users)

@app.route("/api/projects", methods=['GET'])
def existing_projects():
    rows = projects_table.get_projects()
    return jsonify([dict(row) for row in rows])

@app.route("/api/shots", methods=['GET'])
def existing_shots():
    shot_rows = shots_table.get_all_shots()
    return jsonify([dict(shot_row) for shot_row in shot_rows])
    
@app.route("/api/usersProjects", methods = ['GET'])
def existing_assignments():
    user_id = request.args.get("user_id")
    if user_id is not None:
        user_assignments = usersProjects_table.get_assignments(user_id)
        return jsonify([row[0] for row in user_assignments])
    else:
        rows = usersProjects_table.get_all_assignments()
        return jsonify([dict(row) for row in rows])

@app.route("/api/projects", methods=['POST'])
def create_project():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error":"Missing the project's name"}), 400
    user_id = data.get("user_id")
    name = data.get("name")
    type = data.get("type")
    status = "New"
    shotsNum = data.get("shotsNum")
    deadline = data.get("deadline")

    project_id = projects_table.add_project(name, type, status, shotsNum, deadline)
    new_shot_list = shots_table.add_shots_for_project(project_id, shotsNum)
    usersProjects_table.add_assignment(user_id,project_id, "Admin")
    return jsonify({"project_id" : project_id, "project_name": name}), 201

@app.route("/api/projects/<int:project_id>", methods=['DELETE'])
def delete_project(project_id):
    projects_table.remove_project(project_id)
    shots_table.remove_shots_for_project(project_id)
    return jsonify({"message": "Project deleted"}), 200
    
@app.route("/api/projects/<int:project_id>", methods=['GET'])
def display_project(project_id):
    row = projects_table.get_project(project_id)
    if row is None:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(dict(row))

@app.route("/api/projects/<int:project_id>/shots", methods=['GET'])
def display_shots_for_project(project_id):
    shots = shots_table.get_shots_from_project(project_id)
    return jsonify([dict(shot) for shot in shots])

@app.route("/api/projects/<int:project_id>/assets", methods=['GET'])
def display_assets_for_project(project_id):
    assets = assets_table.get_assets_from_project(project_id)
    return jsonify([dict(asset) for asset in assets])

@app.route("/api/projects/<int:project_id>/shots/<int:shot_id>", methods = ['PATCH'])
def change_status(project_id, shot_id):
    data = request.get_json()
    status_item = data.get("status_item")
    value = data.get("value")
    if not status_item or value is None:
        return jsonify({"error" : "Missing required components to update the shot"})
    shots_table.change_shot_status(shot_id, status_item, value)
    return jsonify({"message" : "Shot updated"})

@app.route("/api/users", methods = ['POST'])
def create_new_user():
    data = request.get_json()
    if "user_name" not in data or "user_password" not in data:
        return jsonify({"error":"Missing user name or password"}), 400
    
    name = data.get("user_name")
    password = data.get("user_password")

    user_id = users_table.add_user(name, password)
    return jsonify({"message": "New user created!"})

@app.route("/api/login", methods = ['POST'])
def login_user():
    data = request.get_json()
    if "user_name" not in data or "user_password" not in data:
        return jsonify({"error":"Missing user name or password"}), 400
    
    name = data.get("user_name")
    password = data.get("user_password")

    success, user_id = users_table.verify_user(name, password)
    if success:
        return jsonify({"success": True, "user_id": user_id}), 200
    else:
        return jsonify({"success": False, "error": "Invalid username or password!"})

@app.route("/api/projects/<int:project_id>/share", methods = ['GET'])
def share_project(project_id):
    code = projects_table.get_sharecode(project_id)
    if code is None:
        return jsonify({"error":"Failed to generate project code"})
    return jsonify({"sharecode": code})

@app.route("/api/join_project", methods = ['POST'])
def join_project():
    data = request.get_json()
    sharecode = data.get("sharecode")
    user_id = data.get("user_id")
    if not sharecode or not user_id:
        return jsonify({"error": "Something went wrong, check your project code and try again"})
    
    project_id = projects_table.get_project_id_by_sharecode(sharecode)
    if not project_id:
        return jsonify({"error": "Invalid sharecode"}), 404

    usersProjects_table.add_assignment(user_id, project_id, "Member")
    return jsonify({"message": "Project joined!", "project_id": project_id})

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, port=8080)