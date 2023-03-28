# rubik-tool

A Rubik's Cube simulator

## Features

- no dependencies other than Python's Standard Library (requires an installation
  containing Tkinter)

- allows to save and load games

- cube renderization based on the one used here: http://mzrg.com/js/qcube-v2.html [0]
  (although this program is based on a different, way simpler theory of operation. Refer
  to the section on "Limitations" for details)

## Running

Clone this repository and run

```
python3 app.py
```

## Limitations

`qCube` [0] was the source of inspiration for this program, but, eventually, the only
aspect we [partially] copied from that project was the way it renders the cube. `qCube`
offers a number of features which seems to be valuable in the "computation speed-cubing"
realm. As such field is unfamiliar to us, we believe it's fair to assume that all the
features lacking in this tool could be classified as limitations.

Differently than `qCube`, `rubik-tool` currently doesn't offer:

- a timer

- alternative puzzles

- arbitrarily-sized cubes

- specialized keyboard shortcuts (which we believe are related to conventions known to the
  speed-cubing community)

## Architecture

This section documents architectural aspects, useful to contributors and to our future
self.

### How the code is organized

### How the Cube's data is represented

*Data structure used to represent the cube*

*Experimentation with a 3D matrix of vectors, which allowed representing cubes of
arbitrary sizes and rotations as simple linear transformations. That would probably have
facilitated the representation of other solids too. But this flexibility came with its
costs in complexity, then we've opted for dropping it in favor of a simple dictionary with
6 entries, each entry representing a cube face*

### What is the game file format



## TODO List

- Simplify the UI: remove rotation buttons, leaving the keyboard shortcuts only; use the
  space freed by the buttons to include the list of past movements directly in the main
  UI, eliminating the additional window currently in use

- Implement a competitive mode with multi-player support, both local and network-based

- Generate videos from a previously saved game

- Generate alternate renderings, e.g., 3D, unfolded

- Implement multiple solvers and generate reports displaying each decision and the
  cube movements related to each step of the selected algorithm

## References

[0] http://mzrg.com/js/qcube-v2.html
