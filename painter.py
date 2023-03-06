from typing import NamedTuple
import logging

logging.basicConfig(level=logging.INFO)

COLORS = {
    'W': 'white',
    'Y': 'yellow',
    'O': 'orange',
    'R': 'red',
    'G': 'green',
    'B': 'blue',
}

class Recipe(NamedTuple):
    """
    Stores attributes used by a renderer to render a particular element/cubelet-face
    """
    face: str
    # Render the cubelet in the position below
    pos: int
    # Top position of the tile, relative (the precise number will be computed by the
    # renderer)
    rel_top: float
    # Left position of the tile, relative
    rel_left: float
    # Height of the tile, relative
    rel_height: float
    # Width of the tile, relative
    rel_width: float
    # Flag, show the face label or not
    show_label: bool = False


# listens to the Cube and updates its graphical representation in the tkinter canvas
class CubePainter:

    qcube_renderization_recipes = [
        # -------------------------------------
        # First line
        Recipe(face='left', pos=1, rel_top=0, rel_left=0, rel_height=1, rel_width=0.5),
        Recipe(face='front', pos=7, rel_top=0, rel_left=0.5, rel_height=1, rel_width=1),
        Recipe(face='front', pos=0, rel_top=0, rel_left=1.5, rel_height=1, rel_width=1),
        Recipe(face='front', pos=1, rel_top=0, rel_left=2.5, rel_height=1, rel_width=1),
        Recipe(face='right', pos=7, rel_top=0, rel_left=3.5, rel_height=1, rel_width=0.5),
        # -------------------------------------
        # Second line
        # -------------------------------------
        Recipe(face='left', pos=2, rel_top=1, rel_left=0, rel_height=1, rel_width=0.5),
        Recipe(face='front', pos=6, rel_top=1, rel_left=0.5, rel_height=1, rel_width=1),
        Recipe(face='front', pos=8, rel_top=1, rel_left=1.5, rel_height=1, rel_width=1,
               show_label=True),
        Recipe(face='front', pos=2, rel_top=1, rel_left=2.5, rel_height=1, rel_width=1),
        Recipe(face='right', pos=6, rel_top=1, rel_left=3.5, rel_height=1, rel_width=0.5),
        # -------------------------------------
        # Third line: the first and last tiles
        # are twice higher
        # -------------------------------------
        Recipe(face='left', pos=3, rel_top=2, rel_left=0, rel_height=2, rel_width=0.5,
               show_label=True),
        Recipe(face='front', pos=5, rel_top=2, rel_left=0.5, rel_height=1, rel_width=1),
        Recipe(face='front', pos=4, rel_top=2, rel_left=1.5, rel_height=1, rel_width=1),
        Recipe(face='front', pos=3, rel_top=2, rel_left=2.5, rel_height=1, rel_width=1),
        Recipe(face='right', pos=5, rel_top=2, rel_left=3.5, rel_height=2, rel_width=0.5,
               show_label=True),
        # -------------------------------------
        # Fourth line: has only three tiles,
        # the corners have printed in above
        # iteration
        # -------------------------------------
        Recipe(face='down', pos=7, rel_top=3, rel_left=0.5, rel_height=1, rel_width=1),
        Recipe(face='down', pos=0, rel_top=3, rel_left=1.5, rel_height=1, rel_width=1),
        Recipe(face='down', pos=1, rel_top=3, rel_left=2.5, rel_height=1, rel_width=1),
        # -------------------------------------
        # Fifth line
        # -------------------------------------
        Recipe(face='left', pos=4, rel_top=4, rel_left=0, rel_height=1, rel_width=0.5),
        Recipe(face='down', pos=6, rel_top=4, rel_left=0.5, rel_height=1, rel_width=1),
        Recipe(face='down', pos=8, rel_top=4, rel_left=1.5, rel_height=1, rel_width=1,
               show_label=True),
        Recipe(face='down', pos=2, rel_top=4, rel_left=2.5, rel_height=1, rel_width=1),
        Recipe(face='right', pos=4, rel_top=4, rel_left=3.5, rel_height=1, rel_width=0.5),
        # -------------------------------------
        # Sixth line
        # -------------------------------------
        Recipe(face='left', pos=5, rel_top=5, rel_left=0, rel_height=1, rel_width=0.5),
        Recipe(face='down', pos=5, rel_top=5, rel_left=0.5, rel_height=1, rel_width=1),
        Recipe(face='down', pos=4, rel_top=5, rel_left=1.5, rel_height=1, rel_width=1),
        Recipe(face='down', pos=3, rel_top=5, rel_left=2.5, rel_height=1, rel_width=1),
        Recipe(face='right', pos=3, rel_top=5, rel_left=3.5, rel_height=1, rel_width=0.5),
    ]

    def __init__(self, cube, canvas):
        self.canvas = canvas
        self.cube = cube
        cube.set_movement_callback(lambda: self.render())

    def render(self):
        self.render_qcube()

    def render_qcube(self):
        default_width_px = 40
        default_height_px = 40
        for r in CubePainter.qcube_renderization_recipes:
            logging.debug(f'Will render according to recipe {r=}')
            width_px = r.rel_width * default_width_px
            height_px = r.rel_height * default_height_px
            left_px = r.rel_left * default_width_px
            top_px = r.rel_top * default_height_px
            tile_position = (
                left_px, top_px, left_px + width_px, top_px + height_px
            )
            color = getattr(self.cube.get_cubelets(), r.face)[r.pos]
            logging.debug(f'Will render cubelet in position {tile_position=}')
            self.canvas.create_rectangle(
                *tile_position,
                fill=COLORS[color],
                outline='black',
            )
            if r.show_label:
                text_color = 'white' if color in ('R', 'G', 'B') else 'black'
                self.canvas.create_text(left_px + width_px // 2,
                                        top_px + height_px // 2,
                                        fill=text_color,
                                        text=r.face[0].upper())

    def render_unfolded(self):
        raise Exception('Not implemented')
