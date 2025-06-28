from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*') # specify origins

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
    return jsonify(projects)

@app.route("/api/projects", methods=['POST'])
def create_project():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error":"Missing the project's name"}), 400
    
    new_project = {"id": len(projects) + 1, "name" : data["name"]}

    projects.append(new_project)
    print("Current projects:", projects)
    return jsonify(new_project), 201



if __name__ == "__main__":
    app.run(debug=True, port=8080)