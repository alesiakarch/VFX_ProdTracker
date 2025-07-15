import pytest
import json
from tracktor_server.main import app
from tracktor_server.db_map import DBMapper

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_init_db(client):
    # init the db
    response = client.get('/init')
    assert response.status_code == 200
    # add check for tables
    assert isinstance(response.get_json(), dict)
    assert response.get_json().get("message") == "Database init complete"

def test_existing_projects(client):
    response = client.get('/api/projects')
    assert isinstance(response.get_json(), list)

def test_create_project(client,):
    data = { "name" : "test",
             "type" : "vfx",
             "shotsNum" : 2,
             "deadline" : "2025"
             }
    response = client.post('/api/projects', json=data)
    assert response.status_code == 201
    project = response.get_json()
    assert "project_id" in project
    assert project["project_name"] == "test"

def test_delete_project(client):
    data = { "name" : "test",
             "type" : "vfx",
             "shotsNum" : 2,
             "deadline" : "2025"
             }
    create_response = client.post('/api/projects', json=data)
    project = create_response.get_json()
    project_id = project["project_id"]

    response = client.delete(f'/api/projects/{project_id}')
    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)
    assert response.get_json().get("message") == "Project deleted"

def test_display_project_found(client):
    data = { "name" : "test",
             "type" : "vfx",
             "shotsNum" : 2,
             "deadline" : "2025"
             }
    create_response = client.post('/api/projects', json=data)
    project = create_response.get_json()
    project_id = project["project_id"]

    response = client.get(f'/api/projects/{project_id}')
    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)

def test_display_project_not_found(client):
    response = client.get(f'/api/projects/999')
    assert response.status_code == 404
    assert isinstance(response.get_json(), dict)
    assert response.get_json().get("error") == "Project not found"

def test_existing_shots(client):
    response = client.get('/api/shots')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_display_shots_for_project(client):
    # create a mock project
    data = { "name" : "test",
             "type" : "vfx",
             "shotsNum" : 2,
             "deadline" : "2025"
             }
    create_response = client.post('/api/projects', json=data)
    project = create_response.get_json()
    project_id = project["project_id"]

    # run the test
    response = client.get(f'/api/projects/{project_id}/shots')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == 2

def test_change_status_success(client):
    # create a mock project
    data = { "name" : "test",
             "type" : "vfx",
             "shotsNum" : 2,
             "deadline" : "2025"
             }
    create_response = client.post('/api/projects', json=data)
    project = create_response.get_json()
    project_id = project["project_id"]

    # get shots
    shots_response = client.get(f'/api/projects/{project_id}/shots')
    shots = shots_response.get_json()
    assert len(shots) == 2
    shot_id = shots[0]["shot_id"]
    # run the test
    changes_data = {"status_item" : "anim_status",
                    "value" : "WIP"}
    response = client.patch(f'/api/projects/{project_id}/shots/{shot_id}', json = changes_data)
    assert response.status_code == 200
    assert response.get_json().get("message") == "Shot updated"








