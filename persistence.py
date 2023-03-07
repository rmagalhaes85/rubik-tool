from cube import FACES
from pathlib import Path
from tkinter.filedialog import asksaveasfile
import sqlite3

def save(cube):
    save_(cube, ensure_filename(cube.get_filename()))

def save_as(cube):
    save_(cube, ensure_filename(None))

def save_(cube, filename):
    if not filename:
        return
    cubelets = cube.get_cubelets()
    conn = ensure_file(filename)
    conn.executemany('update cubelets set colors = ? where face = ?;', [
        (getattr(cubelets, face), face) for face in FACES
    ])
    conn.execute('delete from movement_history;')
    #conn.executemany('insert into movement_history(type, description) values(?, ?);', [])
    conn.commit()
    cube.set_filename(filename)

def ensure_filename(original):
    if original and original.strip():
        return original
    dialog = asksaveasfile()
    if dialog is None:
        return None
    return dialog.name

def ensure_file(filename):
    try:
        p = Path(filename)
        full_path = p.resolve(strict=True)
    except FileNotFoundError:
        return create_file(filename)
    else:
        return open_and_validate_file(str(full_path))

def create_file(filename):
    print('create_file')
    conn = sqlite3.connect(filename)
    conn.execute(
        '''
        create table cubelets(
            face text not null,
            colors text not null
        );
        insert into cubelets
        values
            ('front', ''), ('back', ''),
            ('left', ''), ('right', ''),
            ('up', ''), ('down', '');
        create table movement_history(
            type text not null,
            description text not null
        );
        '''
    )
    return conn

def open(cube):
    conn = open_and_validate_file(filename)
    # load cube with data retrieved from the file
    return conn

def open_and_validate_file(filename):
    print('open_and_validate_file')
    conn = sqlite3.connect(filename)
    # check if tables exist and the cubelets are present
    return conn
