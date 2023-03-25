# rubik-tool

A Rubik's Cube simulator

## Features

- no dependencies other than Python's Standard Library (requires an installation
  containing Tkinter)

- allows to save and load games

- cube renderization based on the one used here: http://mzrg.com/js/qcube-v2.html
  (although this program is based on a different, way simpler theory of operation. Refer
  to the section on "Limitations" for details)

## Running

Clone this repository and run

```
python3 app.py
```

## Limitations

*Compare to qCube and its features. There's a number of conventions and features valued by
speedcubers which are not addressed here, but this might be done in the feature*

## Architecture

*Data structure used to represent the cube*

*Experimentation with a 3D matrix of vectors, which allowed representing cubes of
arbitrary sizes and rotations as simple linear transformations. That would probably have
facilitated the representation of other solids too. But this flexibility came with its
costs in complexity, then we've opted for dropping it in favor of a simple dictionary with
6 entries, each entry representing a cube face*

## TODO List

- Simplify the UI: remove rotation buttons and leave the keyboard shortcuts only; use the
  space freed by the buttons to include the list of past movements directly in the main UI

- Implement a competitive mode with support to multiplayer

- Generate videos from a previously saved game

- Generate alternate sorts of renderings
