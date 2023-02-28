from tkinter import *
from tkinter import ttk
from cube import Movement, CubeMovement
from painter import CubePainter

class View():

    def __init__(self, cube):
        root = Tk()
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        buttons_frm = ttk.Frame(frm, padding=5)
        buttons_frm.grid(column=1, row=0)
        canvas = Canvas(frm)
        canvas.grid(column=0, row=0, rowspan=2)
        self.cube = cube
        self.painter = CubePainter(cube, canvas)
        self.buttons_frm = buttons_frm
        ttk.Label(buttons_frm, text="Faces").grid(row=0, column=0, columnspan=2)
        self.create_face_move_buttons()
        ttk.Label(buttons_frm, text="Cube").grid(row=4, column=0, columnspan=2)
        self.create_cube_rotation_buttons()
        self.canvas = canvas
        self.root = root

    def get_canvas_reference(self):
        return self.canvas

    def create_face_move_buttons(self):
        self.create_face_move_button("FRONT", 'front', column=0, row=1)
        self.create_face_move_button("TOP", 'top', column=0, row=2)
        self.create_face_move_button("DOWN", 'down', column=0, row=3)
        self.create_face_move_button("LEFT", 'left', column=1, row=1)
        self.create_face_move_button("RIGHT", 'right', column=1, row=2)
        self.create_face_move_button("BACK", 'back', column=1, row=3)

    def create_face_move_button(self, text, face, **grid_args):
        ttk.Button(
            self.buttons_frm,
            text=text,
            command=lambda: self.cube.rotate_face(
                Movement(face=face, is_prime=False)
            )
        ).grid(**grid_args)

    def create_cube_rotation_buttons(self):
        self.create_cube_rotation_button("X", 'x', column=0, row=5)
        self.create_cube_rotation_button("Y", 'y', column=0, row=6)
        self.create_cube_rotation_button("Z", 'z', column=0, row=7)

    def create_cube_rotation_button(self, text, axis, **grid_args):
        ttk.Button(
            self.buttons_frm,
            text=text,
            command=lambda: self.cube.rotate_cube(axis),
        ).grid(**grid_args)

    def mainloop(self):
        self.painter.render()
        self.root.mainloop()
