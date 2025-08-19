import pytest
import tempfile
import os
from tracktor_server.shots_table import Shots
from tracktor_server.projects_table import Projects


@pytest.fixture
def projects_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    print("TEST DB PATH:", path)
    os.close(fd)
    projects = Projects(path)
    projects.init_project_table()
    yield projects
    os.remove(path)

@pytest.fixture
def shots_mapper(projects_mapper):
    # Use the same db file as projects_mapper
    shots = Shots(projects_mapper.db_name)
    shots.init_shots_table()
    yield shots

def test_init_shots_table(shots_mapper):
    shots_mapper.init_shots_table()

    expected_columns = [("project_id", "INTEGER"),
                        ("id", "INTEGER"),
                        ("shot_name", "TEXT"),
                        ("status", "TEXT"),
                        ("lay_status", "TEXT"),
                        ("anim_status", "TEXT"),
                        ("cfx_status", "TEXT"),
                        ("lit_status", "TEXT")
                        ]
    
    connection = shots_mapper.get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shots'")
    table = cursor.fetchone()
    assert table is not None, "Table 'shots' was not created"


    cursor.execute("PRAGMA table_info(shots)")
    columns = cursor.fetchall()
    columns = [tuple(row) for row in columns]
    print(columns)

    for i, column in enumerate(columns):
        name = column[1]
        type = column[2]
        assert name == expected_columns[i][0], f"Expected {expected_columns[i][0]} but got {name}"
        assert type == expected_columns[i][1], f"Expected {expected_columns[i][1]} but got {type}"
    
    connection.close()

def test_get_shots_from_project_empty(shots_mapper):
    # create tables
    shots_mapper.init_shots_table()

    # check 2 shots exist
    shots = shots_mapper.get_shots_from_project(5)
    assert isinstance(shots, list)
    assert len(shots) == 0

def test_get_shots_from_project(projects_mapper, shots_mapper):
    # create tables
    shots_mapper.init_shots_table()

    # create project
    project_id = projects_mapper.add_project("Test", "vfx", "New", 2, "2025")

    # add shots
    shots_mapper.add_shots_for_project(project_id, 2)

    # check 2 shots exist
    shots = shots_mapper.get_shots_from_project(project_id)
    assert isinstance(shots, list)
    assert len(shots) == 2
    for shot in shots:
        assert shot["project_id"] == project_id

def test_get_shot_from_project_empty(shots_mapper):
    # create tables
    shots_mapper.init_shots_table()

    # get shot
    row = shots_mapper.get_shot_from_project(4, 2)
    assert row is None

def test_get_shot_from_project(projects_mapper, shots_mapper):
    # create tables
    shots_mapper.init_shots_table()

    # create project
    project_id = projects_mapper.add_project("Test", "vfx", "New", 2, "2025")

    # add shots
    shots_mapper.add_shots_for_project(project_id, 2)

    # check 2 shots exist
    row = shots_mapper.get_shot_from_project(project_id, 1)
    assert row is not None
    assert row["project_id"] == project_id
    assert row["shot_name"] == "SHT_0010"  
    assert row["status"] == "Not Started"
    assert row["lay_status"] == "Not Started"
    assert row["anim_status"] == "Not Started"
    assert row["cfx_status"] == "Not Started"
    assert row["lit_status"] == "Not Started"

def test_get_all_shots_empty(shots_mapper):
    shots_mapper.init_shots_table()
    shots = shots_mapper.get_all_shots()
    assert isinstance(shots, list)
    assert len(shots) == 0

def test_get_all_shots_multiple_projects(projects_mapper, shots_mapper):
    shots_mapper.init_shots_table()
    pid1 = projects_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = projects_mapper.add_project("B", "vfx", "New", 1, "2025")
    shots_mapper.add_shots_for_project(pid1, 1)
    shots_mapper.add_shots_for_project(pid2, 1)
    shots = shots_mapper.get_all_shots()
    assert len(shots) == 2
    project_ids = {shot["project_id"] for shot in shots}
    assert {pid1, pid2} == project_ids

def test_add_shots_for_project(projects_mapper, shots_mapper):
    # set up the tables
    shots_mapper.init_shots_table()

    # create project
    shotsNum = 2
    new_id = projects_mapper.add_project("A", "vfx", "New", shotsNum, "2025")

    # create shots
    shots_mapper.add_shots_for_project(new_id, shotsNum)
    
    # check new shots exists
    connection = shots_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM shots WHERE project_id = ?", (new_id,))
    rows = cursor.fetchall()
    assert isinstance(rows, list)
    assert len(rows) == shotsNum
    connection.close()

def test_remove_shots_from_project(projects_mapper, shots_mapper):
    # set up tables
    shots_mapper.init_shots_table()

    # create 2 projects
    pid1 = projects_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = projects_mapper.add_project("B", "vfx", "New", 1, "2025")
    shots_mapper.add_shots_for_project(pid1, 1)
    shots_mapper.add_shots_for_project(pid2, 1)

    shots_mapper.remove_shots_from_project(pid1)

    shots1 = shots_mapper.get_shots_from_project(pid1)
    shots2 = shots_mapper.get_shots_from_project(pid2)

    assert len(shots1) == 0
    assert len(shots2) == 1

def test_remove_shot_from_project(projects_mapper, shots_mapper):
    shots_mapper.init_shots_table()
    projects_mapper.init_project_table()

    # add example project
    shots_num = 1
    new_id = projects_mapper.add_project("TestName", "TestType", "New", shots_num, "2025")
    shots = shots_mapper.add_shots_for_project(new_id, shots_num)
    # Get the shot_id of the automatically created shot
    shots = shots_mapper.get_shots_from_project(new_id)
    shot_id = shots[0]["id"]

    # delete project
    shots_mapper.remove_shot_from_project(shot_id)

    # check the project is actually gone
    row = shots_mapper.get_shot_from_project(new_id, shot_id)
    assert row is None

def test_change_shot_status(projects_mapper, shots_mapper):
    # init the tables
    shots_mapper.init_shots_table()

    # create project and shots
    project_id = projects_mapper.add_project("Test", "vfx", "New", 1, "2025")
    shots_mapper.add_shots_for_project(project_id, 1)

    # get the shot
    shot = shots_mapper.get_shots_from_project(project_id)[0]
    shot_id = shot["id"]

    # change status
    shots_mapper.change_shot_status(shot_id, "anim_status", "WIP")

    # get the shot again and see if the status changed
    updated_shot = shots_mapper.get_shot_from_project(project_id, shot_id)
    assert updated_shot["anim_status"] == "WIP"







    

