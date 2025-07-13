import pytest
import tempfile
import os
from tracktor_server.db_map import DBMapper

@pytest.fixture
def db_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    db_mapper = DBMapper()
    db_mapper.db_name = path
    yield db_mapper
    os.remove(path)

def test_get_db(db_mapper):
    connection = db_mapper.get_db()
    assert connection is not None
    connection.close()

def test_init_project_table(db_mapper):
    db_mapper.init_project_table()

    expected_columns = [("id", "INTEGER"),
                        ("name", "TEXT"),
                        ("type", "TEXT"),
                        ("status", "TEXT"),
                        ("shotsNum", "INTEGER"),
                        ("deadline", "TEXT")
                        ]
    
    connection = db_mapper.get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
    table = cursor.fetchone()
    assert table is not None, "Table 'projects' was not created"


    cursor.execute("PRAGMA table_info(projects)")
    columns = cursor.fetchall()
    columns = [tuple(row) for row in columns]
    print(columns)

    for i, column in enumerate(columns):
        name = column[1]
        type = column[2]
        assert name == expected_columns[i][0], f"Expected {expected_columns[i][0]} but got {name}"
        assert type == expected_columns[i][1], f"Expected {expected_columns[i][1]} but got {type}"
    
    connection.close()

def test_get_projects_empty(db_mapper):
    db_mapper.init_project_table()
    connection = db_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM projects")
    connection.commit()
    connection.close()
    rows = db_mapper.get_projects()
    assert isinstance(rows, list)
    assert rows == []

def test_get_projects(db_mapper):
    db_mapper.init_project_table()
    # now create a project and check its there
    connection = db_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO projects (name, type, status, shotsNum, deadline)
        VALUES ('Test Project', 'vfx', 'Active', 10, '2025-12-31')
    """)
    connection.commit()
    connection.close()

    rows = db_mapper.get_projects()
    # Assert the returned rows match the inserted data
    assert len(rows) == 1, "Expected 1 row in the result"
    assert rows[0]['name'] == 'Test Project', "Expected project name to be 'Test Project'"
    assert rows[0]['type'] == 'vfx', "Expected project type to be 'vfx"
    assert rows[0]['status'] == 'Active', "Expected project status to be 'Active'"
    assert rows[0]['shotsNum'] == 10, "Expected shotsNum to be 10"
    assert rows[0]['deadline'] == '2025-12-31', "Expected deadline to be '2025-12-31'"

def test_add_project(db_mapper):
    # check the table exists
    db_mapper.init_project_table()

    # add project
    new_id = db_mapper.add_project("TestName", "TestType", "New", 5, "2025")
    assert isinstance(new_id, int)

    # check new id exists
    connection = db_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    assert row is not None
    connection.close()

def test_remove_project(db_mapper):
    # check the table exists
    db_mapper.init_project_table()

    # add example project
    new_id = db_mapper.add_project("TestName", "TestType", "New", 5, "2025")

    # delete project
    db_mapper.remove_project(new_id)

    # check the project is actually gone
    row = db_mapper.get_project(new_id)
    assert row is None

def test_get_project_empty(db_mapper):
    # check the table exists
    db_mapper.init_project_table()

    # get an empty project
    row = db_mapper.get_project(1)
    assert row is None

def test_get_project(db_mapper):

    # check the table exists
    db_mapper.init_project_table()

    # add example project
    new_id = db_mapper.add_project("TestName", "TestType", "New", 5, "2025")

    # get the created project
    row = db_mapper.get_project(new_id)
    assert row is not None
    assert row["name"] == "TestName"
    assert row["type"] == "TestType"
    assert row["status"] == "New"
    assert row["shotsNum"] == 5
    assert row["deadline"] == "2025"

def test_init_shots_table(db_mapper):
    db_mapper.init_shots_table()

    expected_columns = [("project_id", "INTEGER"),
                        ("shot_id", "INTEGER"),
                        ("shot_name", "TEXT"),
                        ("status", "TEXT"),
                        ("lay_status", "TEXT"),
                        ("anim_status", "TEXT"),
                        ("cfx_status", "TEXT"),
                        ("lit_status", "TEXT")
                        ]
    
    connection = db_mapper.get_db()
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

def test_get_shots_from_project_empty(db_mapper):
    # create tables
    db_mapper.init_project_table()
    db_mapper.init_shots_table()

    # check 2 shots exist
    shots = db_mapper.get_shots_from_project(5)
    assert isinstance(shots, list)
    assert len(shots) == 0

def test_get_shots_from_project(db_mapper):
    # create tables
    db_mapper.init_project_table()
    db_mapper.init_shots_table()

    # create project
    project_id = db_mapper.add_project("Test", "vfx", "New", 2, "2025")

    # add shots
    db_mapper.add_shots_for_project(project_id, 2)

    # check 2 shots exist
    shots = db_mapper.get_shots_from_project(project_id)
    assert isinstance(shots, list)
    assert len(shots) == 2
    for shot in shots:
        assert shot["project_id"] == project_id

def test_get_shot_from_project_empty(db_mapper):
    # create tables
    db_mapper.init_project_table()
    db_mapper.init_shots_table()

    # get shot
    row = db_mapper.get_shot_from_project(4, 2)
    assert row is None

def test_get_shot_from_project(db_mapper):
    # create tables
    db_mapper.init_project_table()
    db_mapper.init_shots_table()

    # create project
    project_id = db_mapper.add_project("Test", "vfx", "New", 2, "2025")

    # add shots
    db_mapper.add_shots_for_project(project_id, 2)

    # check 2 shots exist
    row = db_mapper.get_shot_from_project(project_id, 1)
    assert row is not None
    assert row["project_id"] == project_id
    assert row["shot_name"] == "SHT_0010"  
    assert row["status"] == "Not Started"
    assert row["lay_status"] == "Not Started"
    assert row["anim_status"] == "Not Started"
    assert row["cfx_status"] == "Not Started"
    assert row["lit_status"] == "Not Started"

def test_get_all_shots_empty(db_mapper):
    db_mapper.init_shots_table()
    shots = db_mapper.get_all_shots()
    assert isinstance(shots, list)
    assert len(shots) == 0

def test_get_all_shots_multiple_projects(db_mapper):
    db_mapper.init_project_table()
    db_mapper.init_shots_table()
    pid1 = db_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = db_mapper.add_project("B", "vfx", "New", 1, "2025")
    db_mapper.add_shots_for_project(pid1, 1)
    db_mapper.add_shots_for_project(pid2, 1)
    shots = db_mapper.get_all_shots()
    assert len(shots) == 2
    project_ids = {shot["project_id"] for shot in shots}
    assert {pid1, pid2} == project_ids

def test_add_shots_for_project(db_mapper):
    # set up the tables
    db_mapper.init_project_table()
    db_mapper.init_shots_table()

    # create project
    shotsNum = 2
    new_id = db_mapper.add_project("A", "vfx", "New", shotsNum, "2025")

    # create shots
    db_mapper.add_shots_for_project(new_id, shotsNum)
    
    # check new shots exists
    connection = db_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM shots WHERE project_id = ?", (new_id,))
    rows = cursor.fetchall()
    assert isinstance(rows, list)
    assert len(rows) == shotsNum
    connection.close()

def test_remove_shots_for_project(db_mapper):
    # set up tables
    db_mapper.init_project_table()
    db_mapper.init_shots_table()

    # create 2 projects
    pid1 = db_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = db_mapper.add_project("B", "vfx", "New", 1, "2025")
    db_mapper.add_shots_for_project(pid1, 1)
    db_mapper.add_shots_for_project(pid2, 1)

    db_mapper.remove_shots_for_project(pid1)

    shots1 = db_mapper.get_shots_from_project(pid1)
    shots2 = db_mapper.get_shots_from_project(pid2)

    assert len(shots1) == 0
    assert len(shots2) == 1

def test_change_shot_status(db_mapper):
    # init the tables
    db_mapper.init_project_table()
    db_mapper.init_shots_table()

    # create projetand shots
    project_id = db_mapper.add_project("Test", "vfx", "New", 1, "2025")
    db_mapper.add_shots_for_project(project_id, 1)

    # get the shot
    shot = db_mapper.get_shots_from_project(project_id)[0]
    shot_id = shot["shot_id"]

    # change status
    db_mapper.change_shot_status(shot_id, "anim_status", "WIP")

    # get the shot again and see if the status changed
    updated_shot = db_mapper.get_shot_from_project(project_id, shot_id)
    assert updated_shot["anim_status"] == "WIP"







    



    
