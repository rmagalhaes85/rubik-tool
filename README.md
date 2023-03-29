# rubik-tool

A Rubik's Cube simulator.

## Features

- no dependencies other than Python's Standard Library (requires an installation
  containing Tkinter)

- allows to save and load games

- cube renderization based on `qcube`'s \[0\] (although this program is based on a simpler
  theory of operation. Refer to the section on "Limitations" for details)

## Running

Clone this repository and run:

```
python3 app.py
```

## Limitations

`qCube` [0] was the source of inspiration for this program, but, eventually, the only
aspect we [partially] copied from that project was the way the cube is rendered. `qCube`
offers a number of features seemingly valued by the "computation speed-cubing" community.
As such field is unfamiliar to us, we believe it's fair to assume that all the features
lacking in our tool should be classified as limitations.

Differently than `qCube`, `rubik-tool` currently doesn't offer:

- a timer

- alternative puzzles

- arbitrarily-sized cubes

- specialized keyboard shortcuts (which we believe are related to conventions known to the
  speed-cubing community)

## Architecture

This section documents key architectural aspects, useful to contributors and to our future
self.

### How the code is organized

No particular principle or design pattern was employed. We opted for what made more sense
in face of the requirements and what emerged during development and experimentation.

The following sources represent the system's "main modules":

- **controller.py**: a thin wrapper used by the View to access underlying functionality.
  It's so thin that we even considered making the View to access underlying functions
  directly, but it seemed more reasonable to have a "façade" providing a single interface
  to system facilities

- **cube.py**: contains the `Cube` class and code to perform all the valid moves, i.e.,
  face rotations and cube rotations around the axes x, y, and z

- **painter.py**: a complement to `view.py` functions. This file contains functions to
  render a cube visualization in a `Tkinter` canvas. Currently, only a `qcube`-inspired
  renderization is available. However, the planned alternative visualizations are likely
  to be included in this same file

- **persistence.py**: contains functions related to storing and loading games into/from a
  file

- **view.py**: contains code to configure and display `Tkinter` user interfaces.

### What is the game file format

The game data is a simple `sqlite` database containing the following tables:

- **cubelets**: store cubelets' positions

- **movement_history**: store cube's movement history, allowing the player to visualize,
  navigate back/forward and undo movements performed in a previously saved game

## TODO List

- Simplify the UI: remove rotation buttons, keeping the keyboard shortcuts only; use the
  space freed by the buttons to include the list of past movements directly into the main
  UI, eliminating the additional window used for that end

- Implement a competitive mode with multi-player support, both local and network-based

- Generate videos from a previously saved game, displaying the cube, its movements and
  additional relevant information, e.g. a timer

- Generate alternative renderings, e.g., 3D, unfolded

- Implement multiple solvers and generate reports explaining each decision and the
  cube movements related to the steps of a given algorithm

## References

[0] http://mzrg.com/js/qcube-v2.html
