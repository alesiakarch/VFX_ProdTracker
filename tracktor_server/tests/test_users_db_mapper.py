import pytest
import tempfile
import os
from tracktor_server.users_db_map import UsersDBMapper

@pytest.fixture
def db_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    db_mapper = UsersDBMapper(path)
    db_mapper.db_name = path
    yield db_mapper
    os.remove(path)

def test_get_db(db_mapper):
    connection = db_mapper.get_db()
    assert connection is not None
    connection.close()

def test_init_users_table(db_mapper):
    db_mapper.init_users_table()

    expected_columns = [("name", "TEXT"),
                        ("password", "TEXT")
                        ]
    
    connection = db_mapper.get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table = cursor.fetchone()
    assert table is not None, "Table 'users' was not created"


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