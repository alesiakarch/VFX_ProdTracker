import pytest
import tempfile
import os
from tracktor_server.projects_table import ProjectsDBMapper

@pytest.fixture
def db_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    db_mapper = ProjectsDBMapper(path)
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
                        ("deadline", "TEXT"),
                        ("project_sharecode", "TEXT")
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
