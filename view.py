from tkinter import *
from tkinter import ttk
from painter import CubePainter

class View():

    def __init__(self, cube):
        # Initialization
        root = Tk()
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        canvas = Canvas(frm, width=200, height=240)
        canvas.grid(column=0, row=0, rowspan=2, pady=5)
        self.canvas = canvas
        self.root = root
        self.cube = cube
        self.painter = CubePainter(cube, canvas)
        # Face movement buttons
        movement_buttons_frm = ttk.Frame(frm, padding=5)
        movement_buttons_frm.grid(column=1, row=0)
        self.movement_buttons_frm = movement_buttons_frm
        ttk.Label(movement_buttons_frm, text="Faces").grid(row=0, column=0, columnspan=2)
        self.create_face_move_buttons()
        # Rotations buttons
        rotations_frm = ttk.Frame(frm, padding=5)
        rotations_frm.grid(column=2, row=0)
        self.rotations_frm = rotations_frm
        ttk.Label(rotations_frm, text="Cube").grid(row=4, column=0, columnspan=2)
        self.create_cube_rotation_buttons()
        # Command Buttons
        commands_frm = ttk.Frame(frm, padding=5)
        commands_frm.grid(column=3, row=0)
        ttk.Label(commands_frm, text="Commands").grid(row=0, column=0, columnspan=2)

    def get_canvas_reference(self):
        return self.canvas

    def create_face_move_buttons(self):
        self.create_face_move_button("FRONT", 'f', column=0, row=1)
        self.create_face_move_button("TOP", 't', column=0, row=2)
        self.create_face_move_button("DOWN", 'd', column=0, row=3)
        self.create_face_move_button("LEFT", 'l', column=1, row=1)
        self.create_face_move_button("RIGHT", 'r', column=1, row=2)
        self.create_face_move_button("BACK", 'b', column=1, row=3)

    def create_face_move_button(self, text, face, **grid_args):
        ttk.Button(
            self.movement_buttons_frm,
            text=text,
            command=lambda: self.cube.rotate_face(face)
        ).grid(**grid_args)

    def create_cube_rotation_buttons(self):
        self.create_cube_rotation_button("X", 'x', column=0, row=5)
        self.create_cube_rotation_button("Y", 'y', column=0, row=6)
        self.create_cube_rotation_button("Z", 'z', column=0, row=7)

    def create_cube_rotation_button(self, text, axis, **grid_args):
        ttk.Button(
            self.rotations_frm,
            text=text,
            command=lambda: self.cube.rotate_cube(axis),
        ).grid(**grid_args)

    def mainloop(self):
        self.painter.render()
        self.root.mainloop()
