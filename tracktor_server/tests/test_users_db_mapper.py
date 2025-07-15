import pytest
import bcrypt
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

    expected_columns = [("id", "INTEGER"),
                        ("user_name", "TEXT"),
                        ("user_password", "TEXT")
                        ]
    
    connection = db_mapper.get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table = cursor.fetchone()
    assert table is not None, "Table 'users' was not created"


    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    columns = [tuple(row) for row in columns]
    print(columns)

    for i, column in enumerate(columns):
        name = column[1]
        type = column[2]
        assert name == expected_columns[i][0], f"Expected {expected_columns[i][0]} but got {name}"
        assert type == expected_columns[i][1], f"Expected {expected_columns[i][1]} but got {type}"
    
    connection.close()

def test_add_user(db_mapper):
    db_mapper.init_users_table()

    username = "Mike03"
    password = "BigBang23"
    # test the function
    new_id = db_mapper.add_user(username, password)
    assert isinstance(new_id, int)

    # check new id user exists in table
    connection = db_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    assert row is not None
    connection.close()

def test_get_user(db_mapper):
    db_mapper.init_users_table()

    # add a sample user
    new_id = db_mapper.add_user("sampleUser", "samplePass")
    
    # test the get
    row = db_mapper.get_user(new_id)
    assert row is not None
    assert row["user_name"] == "sampleUser"
    assert bcrypt.checkpw("samplePass".encode("utf-8"), row["user_password"].encode("utf-8"))

def test_get_users(db_mapper):
    db_mapper.init_users_table()

    db_mapper.add_user("sampleUser1", "samplePass1")
    db_mapper.add_user("sampleUser2", "samplePass2")

    rows = db_mapper.get_users()
    assert isinstance(rows, list)
    assert len(rows) == 2