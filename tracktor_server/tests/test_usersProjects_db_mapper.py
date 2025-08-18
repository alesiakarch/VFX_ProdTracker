import pytest
import tempfile
import os
from tracktor_server.usersProjects_table import UsersProjectsDBMapper

@pytest.fixture
def db_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    db_mapper = UsersProjectsDBMapper(path)
    db_mapper.db_name = path
    yield db_mapper
    os.remove(path)

def test_get_db(db_mapper):
    connection = db_mapper.get_db()
    assert connection is not None
    connection.close()

def test_init_users_table(db_mapper):
    db_mapper.init_usersProjects_table()

    expected_columns = [("id", "INTEGER"),
                        ("user_id", "INTEGER"),
                        ("project_id", "INTEGER"),
                        ("role", "TEXT")
                        ]
    
    connection = db_mapper.get_db()    
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usersProjects'")
    table = cursor.fetchone()
    assert table is not None, "Table 'usersProjects' was not created"


    cursor.execute("PRAGMA table_info(usersProjects)")
    columns = cursor.fetchall()
    columns = [tuple(row) for row in columns]
    print(columns)

    for i, column in enumerate(columns):
        name = column[1]
        type = column[2]
        assert name == expected_columns[i][0], f"Expected {expected_columns[i][0]} but got {name}"
        assert type == expected_columns[i][1], f"Expected {expected_columns[i][1]} but got {type}"
    
    connection.close()

def test_add_assignment(db_mapper):
    db_mapper.init_usersProjects_table()

    user_id = 2
    project_id = 1

    role = "Observer"
    new_id = db_mapper.add_assignment(user_id, project_id, role)
    assert isinstance(new_id, int)

    connection = db_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usersProjects WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    assert row is not None
    connection.close()

def test_get_assignments(db_mapper):
    db_mapper.init_usersProjects_table()

    user_id = 2
    db_mapper.add_assignment(user_id, 3, "Observer")
    db_mapper.add_assignment(user_id, 1, "Admin")
    db_mapper.add_assignment(3, 32, "Admin")

    assignments = db_mapper.get_assignments(user_id)
    assert isinstance(assignments, list)
    assert len(assignments) == 2

def test_get_all_assignments(db_mapper):
    db_mapper.init_usersProjects_table()

    db_mapper.add_assignment(2, 3, "Admin")
    db_mapper.add_assignment(1, 3, "Observer")

    rows = db_mapper.get_all_assignments()
    assert isinstance(rows, list)
    assert len(rows) == 2