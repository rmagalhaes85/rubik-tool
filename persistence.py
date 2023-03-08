from cube import FACES, FaceMovement, CubeMovement, Cubelets
from functools import reduce
from pathlib import Path
import sqlite3
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import NamedTuple

class DataFileInfo(NamedTuple):
    filename: str
    is_new: bool

def save(cube):
    save_(cube, ensure_filename(cube.filename))

def save_as(cube):
    save_(cube, ensure_filename(None))

def save_(cube, data_file_info):
    assert data_file_info
    assert data_file_info.filename
    cubelets = cube.cubelets
    conn = ensure_file(data_file_info)
    conn.executemany('update cubelets set colors = ? where face = ?;',
                     [(getattr(cubelets, face), face) for face in FACES])
    conn.execute('delete from movement_history;')
    conn.executemany('insert into movement_history(type, description) values(?, ?);',
                     map(translate_movement_to_string, cube.movement_history))
    conn.commit()
    conn.close()
    cube.filename = data_file_info.filename

def ensure_filename(original):
    if original and original.strip():
        return DataFileInfo(filename=original, is_new=False)
    return DataFileInfo(filename=asksaveasfilename(), is_new=True)

def ensure_file(data_file_info):
    if data_file_info.is_new:
        return create_file(data_file_info.filename)
    else:
        return open_and_validate_file(data_file_info.filename)

def create_file(filename):
    conn = sqlite3.connect(filename)
    conn.execute(
        '''
        create table cubelets(
            face text not null,
            colors text not null
        );
        '''
    )
    conn.execute(
    '''
        insert into cubelets
        values
            ('front', ''), ('back', ''),
            ('left', ''), ('right', ''),
            ('up', ''), ('down', '');
    '''
    )
    conn.execute(
        '''
        create table movement_history(
            type text not null,
            description text not null
        );
        '''
    )
    return conn

def open(cube):
    filename = askopenfilename()
    if not filename:
        return
    conn = open_and_validate_file(filename)
    res = conn.execute('select face, colors from cubelets;')
    entries = res.fetchall()
    dict_cubelets = reduce(lambda a, el: {**a, el[0]: el[1]}, entries, {})
    loaded_cubelets = Cubelets(**dict_cubelets)
    cube.set_cubelets(loaded_cubelets)
    res = conn.execute('select type, description from movement_history;')
    entries = res.fetchall()
    cube.movement_history = list(map(translate_entry_to_movement, entries))
    conn.close()

def open_and_validate_file(filename):
    conn = sqlite3.connect(filename)
    # check if tables exist and the cubelets are present
    res = conn.execute("select name from sqlite_master where type='table';")
    entries = res.fetchall()
    assert any(map(lambda e: e[0] == 'cubelets', entries)), (
        'cubelets table was not found in the data file'
    )
    assert any(map(lambda e: e[0] == 'movement_history', entries)), (
        'movement_history table was not found in the data file'
    )
    return conn

def translate_movement_to_string(m):
    if isinstance(m, FaceMovement):
        return ('face', ''.join((m.face, '\'' if m.is_prime else '')))
    elif isinstance(m, CubeMovement):
        return ('cube', m.axis)
    raise ValueError(f'Unknown movement type: {type(m)}')

def translate_entry_to_movement(e):
    if e[0] == 'face':
        face = e[1][0]
        is_prime = len(e[1]) > 1 and e[1][1] == '\''
        return FaceMovement(face=e[1][0], is_prime=is_prime)
    elif e[0] == 'cube':
        return CubeMovement(axis=e[1])
    raise ValueError(f'Unkown movement description: {e=}')
