import pytest
import tempfile
import os
from tracktor_server.assets_db_map import AssetsDBMapper

@pytest.fixture
def db_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    db_mapper = AssetsDBMapper(path)
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
                        ("asset_name", "TEXT"),
                        ("asset_type", "TEXT"),
                        ("asset_status", "TEXT"),
                        ("prepro_status", "TEXT"),
                        ("mod_status", "TEXT"),
                        ("srf_status", "TEXT"),
                        ("cfx_status", "TEXT"),
                        ("lit_status", "TEXT")
                        ]
    
    connection = db_mapper.get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assets'")
    table = cursor.fetchone()
    assert table is not None, "Table 'assets' was not created"


    cursor.execute("PRAGMA table_info(assets)")
    columns = cursor.fetchall()
    columns = [tuple(row) for row in columns]
    print(columns)

    for i, column in enumerate(columns):
        name = column[1]
        type = column[2]
        assert name == expected_columns[i][0], f"Expected {expected_columns[i][0]} but got {name}"
        assert type == expected_columns[i][1], f"Expected {expected_columns[i][1]} but got {type}"
    
    connection.close()
