import pytest
import tempfile
import os
from tracktor_server.notes_table import Notes
from tracktor_server.projects_table import Projects
from tracktor_server.shots_table import Shots

@pytest.fixture
def projects_mapper():
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    
    os.close(fd)
    projects = Projects(path)
    projects.init_project_table()
    yield projects
    os.remove(path)

@pytest.fixture
def notes_mapper(projects_mapper):
    notes = Notes(projects_mapper.db_name)
    notes.init_notes_table()
    yield notes

@pytest.fixture
def shots_mapper(projects_mapper):
    shots= Shots(projects_mapper.db_name)
    shots.init_shots_table()
    yield shots

def test_get_db(notes_mapper):
    connection = notes_mapper.get_db()
    assert connection is not None
    connection.close()

def test_init_notes_table(notes_mapper):
    notes_mapper.init_notes_table()

    expected_columns = [("id", "INTEGER"),
                        ("item_type", "TEXT"),
                        ("item_id", "INTEGER"),
                        ("item_dept", "TEXT"),
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
    projects_mapper.init_project_table()
    notes_mapper.init_notes_table()
    shots_mapper.init_shots_table()

    # create project
    shots_num = 1
    project_id = projects_mapper.add_project("A", "vfx", "New", shots_num, "2025")
    shots = shots_mapper.add_shots_for_project(project_id, shots_num)

    # get the shot id 
    shots = shots_mapper.get_shots_from_project(project_id)
    shot_id = shots[0]["id"]
    # create new note 
    notes_mapper.add_note("shot", shot_id, "LAY", "message", "12:30", "username")

    connection = notes_mapper.get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes WHERE item_id= ?", (shot_id,))
    row = cursor.fetchone()
    assert row is not None
    connection.close()

def test_get_notes_empty(notes_mapper):
    notes_mapper.init_notes_table()
    notes = notes_mapper.get_notes("shot", 2)
    assert isinstance(notes, list)
    assert len(notes) == 0
    

def test_get_notes(notes_mapper, projects_mapper, shots_mapper):
    projects_mapper.init_project_table()
    notes_mapper.init_notes_table()
    shots_mapper.init_shots_table()

    # create project
    shots_num = 1
    project_id = projects_mapper.add_project("A", "vfx", "New", shots_num, "2025")
    shots = shots_mapper.add_shots_for_project(project_id, shots_num)

    # get the shot id 
    shots = shots_mapper.get_shots_from_project(project_id)
    shot_id = shots[0]["id"]
    # create new note 
    notes_mapper.add_note("shot", shot_id, "ANI", "message", "12:30", "username")

    # check the note exists in the item id
    notes = notes_mapper.get_notes("shot", shot_id)
    assert isinstance(notes, list)
    assert len(notes) == 1
    for note in notes:
        assert note["item_id"] == shot_id

def test_get_all_notes(notes_mapper, projects_mapper, shots_mapper):
    notes_mapper.init_notes_table()
    shots_mapper.init_shots_table()
    projects_mapper.init_project_table()

    pid1 = projects_mapper.add_project("A", "vfx", "New", 1, "2025")
    pid2 = projects_mapper.add_project("B", "vfx", "New", 1, "2025")
    shots_mapper.add_shots_for_project(pid1, 1)
    shots_mapper.add_shots_for_project(pid2, 1)
    shots = shots_mapper.get_all_shots()
    shot_id1 = shots[0]["id"]
    shot_id2 = shots[1]["id"]

    note1 = notes_mapper.add_note("shot",shot_id1, "LAY", "message", "12:30", "username")
    note2 = notes_mapper.add_note("shot", shot_id2, "ANI", "message", "12:50", "username")
     
    all_notes = notes_mapper.get_all_notes()
    note_ids = [note["id"] for note in all_notes]
    assert note1 in note_ids
    assert note2 in note_ids
    assert any(note["item_dept"] == "LAY" for note in all_notes)
    assert any(note["item_dept"] == "ANI" for note in all_notes)
    assert any(note["note_body"] == "message" for note in all_notes)


def test_get_notes_for_dept(notes_mapper):
    id1 = notes_mapper.add_note("shot", 1, "LAY", "Lay note", "alice")
    id2 = notes_mapper.add_note("shot", 1, "ANI", "Ani note", "bob")
    lay_notes = notes_mapper.get_notes_for_dept("shot", 1, "LAY")
    ani_notes = notes_mapper.get_notes_for_dept("shot", 1, "ANI")
    assert len(lay_notes) == 1
    assert lay_notes[0]["note_body"] == "Lay note"
    assert lay_notes[0]["item_dept"] == "LAY"
    assert len(ani_notes) == 1
    assert ani_notes[0]["note_body"] == "Ani note"
    assert ani_notes[0]["item_dept"] == "ANI"

def test_get_note_by_id(notes_mapper):
    note_id = notes_mapper.add_note("shot", 2, "CFX", "CFX note", "carol")
    note = notes_mapper.get_note_by_id(note_id)
    assert note is not None
    assert note["id"] == note_id
    assert note["note_body"] == "CFX note"
    assert note["author"] == "carol"
    assert note["item_dept"] == "CFX"

def test_remove_notes(notes_mapper):
    # Add multiple notes for the same item, then remove them
    notes_mapper.add_note("shot", 3, "LAY", "Note 1", "dave")
    notes_mapper.add_note("shot", 3, "LAY", "Note 2", "eve")
    before = notes_mapper.get_notes_for_dept("shot", 3, "LAY")
    assert len(before) == 2
    notes_mapper.remove_notes(3)
    after = notes_mapper.get_notes_for_dept("shot", 3, "LAY")
    assert len(after) == 0






    