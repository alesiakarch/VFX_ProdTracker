import pytest
import tempfile
import os
from tracktor_server.assets_db_map import AssetsDBMapper
from tracktor_server.projects_db_map import ProjectsDBMapper

@pytest.fixture
def projects_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    projects = ProjectsDBMapper(path)
    projects.init_project_table()
    yield projects
    os.remove(path)

@pytest.fixture
def assets_mapper(projects_mapper):
    # Use the same db file as projects_mapper
    assets = AssetsDBMapper(projects_mapper.db_name)
    assets.init_assets_table()
    yield assets

def test_get_db(assets_mapper):
    connection = assets_mapper.get_db()
    assert connection is not None
    connection.close()

def test_init_users_table(assets_mapper):
    assets_mapper.init_assets_table()

    expected_columns = [("id", "INTEGER"),
                        ("project_id", "INTEGER"),
                        ("asset_name", "TEXT"),
                        ("asset_type", "TEXT"),
                        ("asset_status", "TEXT"),
                        ("prepro_status", "TEXT"),
                        ("mod_status", "TEXT"),
                        ("srf_status", "TEXT"),
                        ("cfx_status", "TEXT"),
                        ("lit_status", "TEXT")
                        ]
    
    connection = assets_mapper.get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assets'")
    table = cursor.fetchone()
    assert table is not None, "Table 'assets' was not created"


     # Debug projects table schema
    cursor.execute("PRAGMA table_info(projects)")
    projects_columns = cursor.fetchall()
    print("Projects Table Schema:", [tuple(row) for row in projects_columns])
    
    cursor.execute("PRAGMA table_info(assets)")
    columns = cursor.fetchall()
    columns = [tuple(row) for row in columns]
    print("Assets table: ", columns)


    for i, column in enumerate(columns):
        name = column[1]
        type = column[2]
        assert name == expected_columns[i][0], f"Expected {expected_columns[i][0]} but got {name}"
        assert type == expected_columns[i][1], f"Expected {expected_columns[i][1]} but got {type}"
    
    connection.close()

def test_add_asset_for_project(assets_mapper, projects_mapper):
    assets_mapper.init_assets_table()

    # create project
    assetsNum = 2
    new_id = projects_mapper.add_project("A", "vfx", "New", assetsNum, "2025")

    # create assets
    assets_mapper.add_asset_for_project(new_id, "Sample_asset", "model")
    
    # check new assets exists
    connection = assets_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM assets WHERE project_id = ?", (new_id,))
    row = cursor.fetchone()
    assert row is not None
    connection.close()

def test_get_assets_from_project_empty(assets_mapper):
    assets_mapper.init_assets_table()

    # check 2 assets exist
    assets = assets_mapper.get_assets_from_project(5)
    assert isinstance(assets, list)
    assert len(assets) == 0

def test_get_assets_from_project(assets_mapper, projects_mapper):
    assets_mapper.init_assets_table()

    # create project
    project_id = projects_mapper.add_project("Test", "vfx", "New", 2, "2025")

    # add assets
    assets_mapper.add_asset_for_project(project_id, "sample_asset", "rig")

    # check an asset exists exists at the project id
    assets = assets_mapper.get_assets_from_project(project_id)
    assert isinstance(assets, list)
    assert len(assets) == 1
    for asset in assets:
        assert asset["project_id"] == project_id


def test_get_asset_from_project_empty(assets_mapper):
    assets_mapper.init_assets_table()

    # check 2 assets exist
    row = assets_mapper.get_asset_from_project(5, 2)
    assert row is None

def test_get_asset_from_project(assets_mapper, projects_mapper):
    # create tables
    assets_mapper.init_assets_table()

    # create project
    project_id = projects_mapper.add_project("Test", "vfx", "New", 1, "2025")
    asset_id1 = assets_mapper.add_asset_for_project(project_id, "test_asset", "model")
    asset_id2 = assets_mapper.add_asset_for_project(project_id, "sample_asset", "rig")

    # check asset exist
    row = assets_mapper.get_asset_from_project(project_id, asset_id1)
    assert row is not None
    assert row["project_id"] == project_id
    assert row["asset_name"] == "test_asset"  
    assert row["asset_type"] == "model"
    assert row["asset_status"] == "Not Started"
    assert row["prepro_status"] == "Not Started"
    assert row["mod_status"] == "Not Started"
    assert row["srf_status"] == "Not Started"
    assert row["cfx_status"] == "Not Started"
    assert row["lit_status"] == "Not Started"

def test_get_all_assets_empty(assets_mapper):
    assets_mapper.init_assets_table()
    assets = assets_mapper.get_all_assets()
    assert isinstance(assets, list)
    assert len(assets) == 0

def test_get_all_assets_multiple_projects(projects_mapper, assets_mapper):
    assets_mapper.init_assets_table()
    pid1 = projects_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = projects_mapper.add_project("B", "vfx", "New", 1, "2025")
    assets_mapper.add_asset_for_project(pid1, "text", "model")
    assets_mapper.add_asset_for_project(pid2, "sample", "rig")
    assets = assets_mapper.get_all_assets()
    assert len(assets) == 2
    project_ids = {asset["project_id"] for asset in assets}
    assert {pid1, pid2} == project_ids

def test_remove_assets_from_project(projects_mapper, assets_mapper):
    # set up tables
    assets_mapper.init_assets_table()

    # create 2 projects
    pid1 = projects_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = projects_mapper.add_project("B", "vfx", "New", 1, "2025")
    assets_mapper.add_asset_for_project(pid1, "text", "model")
    assets_mapper.add_asset_for_project(pid2, "sample", "rig")

    assets_mapper.remove_assets_from_project(pid1)

    assets1 = assets_mapper.get_assets_from_project(pid1)
    assets2 = assets_mapper.get_assets_from_project(pid2)

    assert len(assets1) == 0
    assert len(assets2) == 1

def test_remove_asset_from_project(projects_mapper, assets_mapper):
    assets_mapper.init_assets_table()
    projects_mapper.init_project_table()

    # add example project
    new_id = projects_mapper.add_project("TestName", "TestType", "New", 1, "2025")
    asset_id = assets_mapper.add_asset_for_project(new_id,"sample", "rig")

# delete project        
    assets_mapper.remove_asset_from_project(asset_id)

    # check the project is actually gone
    row = assets_mapper.get_asset_from_project(new_id, asset_id)
    assert row is None