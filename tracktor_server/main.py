#!/usr/bin/env -S uv run --script

"""
Tracktor Server API

This is the Flask backend for the Tracktor VFX production tracker.
The file contains endpoints to connect incoming requests to their respective functions and db access.

"""
print("main.py loaded - FLATTENED IMPORTS")
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from projects_table import Projects
from shots_table import Shots
from users_table import Users
from usersProjects_table import UsersProjects
from assets_table import Assets
from notes_table import Notes


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}) # specify origins

# Use TRACKTOR_DB_PATH env variable for test DB, default to 'tracktor.db' for production
db_path = os.environ.get("TRACKTOR_DB_PATH", "tracktor.db")
projects_table = Projects(db_path)
shots_table = Shots(db_path)
users_table = Users(db_path)
usersProjects_table = UsersProjects(db_path)
assets_table = Assets(db_path)
notes_table = Notes(db_path)

@app.route("/init", methods = ['GET'])
def init_db():
    """
    Initialises all the tables in the database.

    Returns:
        Response: JSON message confirming the init.
    """
    projects_table.init_project_table()
    shots_table.init_shots_table()
    users_table.init_users_table()
    usersProjects_table.init_usersProjects_table()
    assets_table.init_assets_table()
    notes_table.init_notes_table()
    return jsonify({"message" : "Database init complete"})

@app.route("/api/users", methods =['GET'])
def existing_users():
    """
    Gets all users from the db, excluding passwords.

    Returns:
        Response: JSON list of user dicts.
    """
    rows = users_table.get_users()
    users = []
    for row in rows:
        user_dict = dict(row)
        user_dict.pop("user_password", None)
        users.append(user_dict)
    return jsonify(users)

@app.route("/api/projects", methods=['GET'])
def existing_projects():
    """
    Gets all projects from the db.

    Returns:
        Response: JSON list of project dicts.
    """

    rows = projects_table.get_projects()
    return jsonify([dict(row) for row in rows])

@app.route("/api/shots", methods=['GET'])
def existing_shots():
    """
    Gets all shots from the db.

    Returns:
        Response: JSON list of shot dicts.
    """
    shot_rows = shots_table.get_all_shots()
    return jsonify([dict(shot_row) for shot_row in shot_rows])
    
@app.route("/api/usersProjects", methods = ['GET'])
def existing_assignments():
    """
    Gets all assignments from the db.

    Args:
        user_id (int, optional) = The ID of the user to retrieve prjects for.

    Returns:
        Response: JSON list of assignment dicts if no user specified, 
        or JSON list if project IDs, assigned to the user.
    """
    user_id = request.args.get("user_id")
    if user_id is not None:
        user_assignments = usersProjects_table.get_assignments(user_id)
        return jsonify([row[0] for row in user_assignments])
    else:
        rows = usersProjects_table.get_all_assignments()
        return jsonify([dict(row) for row in rows])
    
@app.route("/api/assets", methods=['GET'])
def existing_assets():
    """
    Gets all assets from the db.

    Returns:
        Response: JSON list of assets dicts.
    """
    asset_rows = assets_table.get_all_assets()
    return jsonify([dict(asset_row) for asset_row in asset_rows])

@app.route("/api/notes", methods=['GET'])
def existing_notes():
    """
    Gets all nodes from the db.

    Returns:
        Response: JSON list of node dicts.
    """
    notes_rows = notes_table.get_all_notes()
    return jsonify([dict(note_row) for note_row in notes_rows])


@app.route("/api/projects", methods=['POST'])
def create_project():
    """
    Creates a new project.
    The user, creating it is assigned as Admin.

    Request JSON:
        name (str): Project name.
        user_id (int): ID of the user creating the project.
        type (str): Project type.
        shotsNum (int): Number of shots.
        deadline (str): Project deadline.

    Returns:
        Response: JSON with new project ID and name.
    """
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
    """
    Removes the project and its contents from the db.

    Args:
        project_id (int): The ID of the project to delete.

    Returns:
        Response: JSON message confirming deletion.
    """
    projects_table.remove_project(project_id)
    assets = assets_table.get_assets_from_project(project_id)
    shots = shots_table.get_shots_from_project(project_id)

    items = assets + shots
    
    for item in items:
        notes_table.remove_notes(item["id"])
    
    shots_table.remove_shots_from_project(project_id)
    assets_table.remove_assets_from_project(project_id)

    return jsonify({"message": "Project deleted"}), 200
    
@app.route("/api/projects/<int:project_id>", methods=['GET'])
def display_project(project_id):
    """
    Gets the data of a specified project.

    Args:
        project_id (int): The ID of the project.
    
    Returns:
        Response: JSON dict with project data.
    """
    row = projects_table.get_project(project_id)
    if row is None:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(dict(row))

@app.route("/api/projects/<int:project_id>/shots", methods=['GET'])
def display_shots_for_project(project_id):
    """
    Gets details of all shots for a specific project.

    Args:
        project_id (int): The ID of the project.

    Returns:
        Response: JSON list of shot dicts with the same project_id.
    """
    shots = shots_table.get_shots_from_project(project_id)
    return jsonify([dict(shot) for shot in shots])

@app.route("/api/projects/<int:project_id>/assets", methods=['GET'])
def display_assets_for_project(project_id):
    """
    Gets details of all assets for a specific project.

    Args:
        project_id (int): The ID of the project.

    Returns:
        Response: JSON list of asset dicts with the same project_id.
    """
    assets = assets_table.get_assets_from_project(project_id)
    return jsonify([dict(asset) for asset in assets])

@app.route("/api/projects/<int:project_id>/shots/<int:shot_id>", methods = ['PATCH'])
def change_shot_status(project_id, shot_id):
    """
    Updates the status of a specific shot (LAY, ANI, etc)

    Args:
        project_id (int): The ID of the project.
        shot_id (int): The ID of the shot.

    Request JSON:
        status_item (str): The status field to update.
        value (str): The new status value.

    Returns:
        Response: JSON message confirming update or error.
    """
    data = request.get_json()
    status_item = data.get("status_item")
    value = data.get("value")
    if not status_item or value is None:
        return jsonify({"error" : "Missing required components to update the shot"})
    shots_table.change_shot_status(shot_id, status_item, value)
    return jsonify({"message" : "Shot updated"})

@app.route("/api/projects/<int:project_id>/assets/<int:asset_id>", methods=['PATCH'])
def change_asset_status(project_id, asset_id):
    """
    Updates the status of a specific asset (MOD, LIT, etc).

    Args:
        project_id (int): The ID of the project.
        asset_id (int): The ID of the asset.

    Request JSON:
        status_item (str): The status field to update.
        value (str): The new status value.

    Returns:
        Response: JSON message confirming update or error.
    """
    data = request.get_json()
    status_item = data.get("status_item")
    value = data.get("value")
    if not status_item or value is None:
        return jsonify({"error" : "Missing required components to update the asset"})
    assets_table.change_asset_status(asset_id, status_item, value)
    return jsonify({"message" : "Asset updated"})

@app.route("/api/users", methods = ['POST'])
def create_new_user():
    """
    Creates a new user in the db.

    Request JSON:
        user_name (str): The username.
        user_password (str): The plaintext password.

    Returns:
        Response: JSON message confirming creation or error.
    """
    data = request.get_json()
    if "user_name" not in data or "user_password" not in data:
        return jsonify({"error":"Missing user name or password"}), 400
    
    name = data.get("user_name")
    password = data.get("user_password")

    user_id = users_table.add_user(name, password)
    return jsonify({"message": "New user created!"})

@app.route("/api/login", methods = ['POST'])
def login_user():
    """
    Authenticates a user with username and password.

    Request JSON:
        user_name (str): The username.
        user_password (str): The plaintext password.

    Returns:
        Response: JSON with success status and user ID, or error message.
    """

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
    """
    Generates or gets a share code for a project.

    Args:
        project_id (int): The ID of the project.

    Returns:
        Response: JSON with share code or error.
    """
    code = projects_table.get_sharecode(project_id)
    if code is None:
        return jsonify({"error":"Failed to generate project code"})
    return jsonify({"sharecode": code})

@app.route("/api/join_project", methods = ['POST'])
def join_project():
    """
    Adds a user to a project using a share code.

    Request JSON:
        sharecode (str): The project share code.
        user_id (int): The ID of the user joining.

    Returns:
        Response: JSON message confirming join or error.
    """
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

@app.route("/api/ping")
def ping():
    """
    Health check endpoint to verify API is reachable.

    Used in Tracktor plugin for TIK Manager.

    Returns:
        Response: JSON message confirming API is reachable.
    """
    return jsonify({"message": "Tracktor API is reachable"})

@app.route("/api/projects/<int:project_id>/create_asset", methods = ['POST'])
def create_asset(project_id):
    """
    Creates a new asset for a project.

    Args:
        project_id (int): The ID of the project.

    Request JSON:
        asset_name (str): The name of the asset.
        asset_type (str): The type of the asset.

    Returns:
        Response: JSON dict with the new asset, or error.
    """
    data = request.get_json()
    if "asset_name" not in data:
        return jsonify({"error" : "Missing the asset's name"}), 400
    project_id = data.get("project_id")
    asset_name = data.get("asset_name")
    asset_type = data.get("asset_type")

    asset_id = assets_table.add_asset_for_project(project_id, asset_name, asset_type)
    asset = assets_table.get_asset_from_project(project_id, asset_id)
    return jsonify(dict(asset)), 201

@app.route("/api/projects/<int:project_id>/create_shot", methods=['POST'])
def create_shot(project_id):
    """
    Creates a new shot for a project.

    Args:
        project_id (int): The ID of the project.

    Request JSON:
        shot_name (str): The name of the shot.

    Returns:
        Response: JSON dict with the new shot, or error.
    """
    data = request.get_json()
    shot_name = data.get("shot_name")
    if not shot_name:
        return jsonify({"error": "Missing shot name"}), 400
    
    shot_id = shots_table.add_shot_for_project(project_id, shot_name)
    shot = shots_table.get_shot_from_project(project_id, shot_id)
    return jsonify(dict(shot)), 201

@app.route("/api/projects/<int:project_id>/assets/<int:asset_id>", methods=['GET'])
def display_asset(project_id, asset_id):
    """
    Gets a specific asset from a project.

    Args:
        project_id (int): The ID of the project.
        asset_id (int): The ID of the asset.

    Returns:
        Response: JSON dict with the asset.
    """
    asset = assets_table.get_asset_from_project(project_id, asset_id)
    return jsonify(dict(asset))

@app.route("/api/projects/<int:project_id>/shots/<int:shot_id>", methods=['GET'])
def display_shot(project_id, shot_id):
    """
    Gets a specific shot from a project.

    Args:
        project_id (int): The ID of the project.
        asset_id (int): The ID of the shot.

    Returns:
        Response: JSON dict with the shot.
    """
    shot = shots_table.get_shot_from_project(project_id, shot_id)
    return jsonify(dict(shot))

@app.route("/api/projects/<int:project_id>/<item_type>/<int:item_id>/<item_dept>/notes", methods=['GET'])
def display_notes(project_id, item_type, item_id, item_dept):
    """
    Gets all notes for the item.

    Args:
        project_id (int): The ID of the project.
        item_type (str): The type of item (e.g., 'shot', 'asset').
        item_id (int): The ID of the item.
        item_dept (str): The department.

    Returns:
        Response: JSON list of note dicts.
    """
    notes = notes_table.get_notes_for_dept(item_type, item_id, item_dept)
    return jsonify([dict(note) for note in notes])

@app.route("/api/projects/<int:project_id>/<item_type>/<int:item_id>/<item_dept>/notes", methods=['POST'])
def add_note(project_id, item_type, item_id, item_dept):
    """
    Adds a note for a specific item and department in a project.

    Args:
        project_id (int): The ID of the project.
        item_type (str): The type of item.
        item_id (int): The ID of the item.
        item_dept (str): The department.

    Request JSON:
        note_body (str): The content of the note.

    Returns:
        Response: JSON dict with the new note, or error.
    """
    data = request.get_json()
    note_body = data.get("note_body")
    if not note_body:
        return jsonify({"error" : "Missing the note itself"}), 400
    
    new_note_id = notes_table.add_note(item_type, item_id, item_dept, note_body, user="janedoe")
    new_note = notes_table.get_note_by_id(new_note_id)
    return jsonify(dict(new_note)), 201

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="0.0.0.0", port=8080)