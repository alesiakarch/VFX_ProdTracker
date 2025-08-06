import pytest
import tempfile
import os
from tracktor_server.notes_db_map import NotesDBMapper
from tracktor_server.projects_db_map import ProjectsDBMapper
from tracktor_server.shots_db_map import ShotsDBMapper

@pytest.fixture
def projects_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    projects = ProjectsDBMapper(path)
    projects.init_project_table()
    yield projects
    os.remove(path)

@pytest.fixture
def notes_mapper(project_mapper):
    notes = NotesDBMapper(projects_mapper.db_name)
    notes.init_notes_table()
    yield notes

@pytest.fixture
def shots_mapper(projects_mapper):
    shots= ShotsDBMapper(shots_mapper.db_name)
    shots.init_shots_table()
    yield shots

def test_get_db(notes_mapper):
    connection = notes_mapper.get_db()
    assert connection is not None
    connection.close()

def test_init_notes_table(notes_mapper):
    notes_mapper.init_notes_table()

    expected_columns = [("id", "INTEGER"),
                        ("item_id", "INTEGER"),
                        ("timestamp", "TEXT"),
                        ("note_body", "TEXT"),
                        ("author", "TEXT")]
    
    connection = notes_mapper.get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes'")
    table = cursor.fetchone()
    assert table is not None, "Table 'notes' was not created"

    cursor.execute("PRAGMA table_info(notes)")
    columns = cursor.fetchall()
    columns = [tuple(row) for row in columns]
    print(columns)

    for i, column in enumerate(columns):
        name = column[1]
        type = column[2]
        assert name == expected_columns[i][0], f"Expected {expected_columns[i][0]} but got {name}"
        assert type == expected_columns[i][1], f"Expected {expected_columns[i][0]} but got {type}"

    connection.close()

def test_add_note(notes_mapper, projects_mapper, shots_mapper):
    projects_mapper.init_projects_table()
    notes_mapper.init_notes_table()
    shots_mapper.init_shots_table()

    # create project
    shots_num = 1
    project_id = projects_mapper.add_project("A", "vfx", "New", shots_num, "2025")
    shots = shots_mapper.add_shots_for_project(project_id, shots_num)

    # get the shot id 
    shots = shots_mapper.get_shots_from_project(project_id)
    shot_id = shots[0]["shots_id"]
    # create new note 
    notes_mapper.add_note(shot_id, "message", "12:30", "username")

    connection = notes_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes WHERE item_id= ?", (shot_id,))
    row = cursor.fetchone()
    assert row is not None
    connection.close()


def test_get_notes_empty(notes_mapper):
    notes_mapper.init_notes_table()
    notes = notes_mapper.get_notes(2)
    assert isinstance(notes, list)
    assert len(notes) == 0

def test_get_notes(notes_mapper, projects_mapper, shots_mapper):
    projects_mapper.init_projects_table()
    notes_mapper.init_notes_table()
    shots_mapper.init_shots_table()

    # create project
    shots_num = 1
    project_id = projects_mapper.add_project("A", "vfx", "New", shots_num, "2025")
    shots = shots_mapper.add_shots_for_project(project_id, shots_num)

    # get the shot id 
    shots = shots_mapper.get_shots_from_project(project_id)
    shot_id = shots[0]["shots_id"]
    # create new note 
    notes_mapper.add_note(shot_id, "message", "12:30", "username")

    # check the note exists in the item id
    notes = notes_mapper.get_notes(shot_id)
    assert isinstance(notes, list)
    assert len(notes) == 1
    for note in notes:
        assert note("item_id") == shot_id

def test_get_all_notes(notes_mapper, projects_mapper, shots_mapper):
    notes_mapper.init_notes_table()
    shots_mapper.init_shots_table()
    projects_mapper.init_projects_table()

    pid1 = projects_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = projects_mapper.add_project("B", "vfx", "New", 1, "2025")
    shots_mapper.add_shots_for_project(pid1, 1)
    shots_mapper.add_shots_for_project(pid2, 1)
    shots = shots_mapper.get_add_shots()
    shot_id1 = shots[0]["shots_id"]
    shot_id2 = shots[1]["shots_id"]

    note1 = notes_mapper.add_note(shot_id1, "message", "12:30", "username")
    note2 = notes_mapper.add_note(shot_id2, "message", "12:50", "username")

    






    