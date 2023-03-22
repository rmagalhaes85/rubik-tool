from copy import deepcopy
from tkinter import *
from tkinter import ttk
from painter import CubePainter

class MovementViewer(Toplevel):

    def __init__(self, parent_window, parent_element, cube):
        super().__init__(parent_element)
        self.cube = cube
        self.internal_movement_history = []
        self.geometry("200x300")
        Label(self, text="This is my new window").pack()
        listbox = Listbox(self, font='Consolas, 14')
        listbox.insert(0, '--initial--')
        self.listbox = listbox
        listbox.pack()
        listbox.bind('<<ListboxSelect>>', lambda e: self.onlistselect(e))
        self.update_movements_in_list()
        self.movement_callback = lambda: self.update_movements_in_list()
        self.cube.add_movement_callback(self.movement_callback)
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def destroy(self):
        self.cube.remove_movement_callback(self.movement_callback)
        super().destroy()

    def update_movements_in_list(self):
        internal_history_len = len(self.internal_movement_history)
        cube_history_len = len(self.cube.movement_history)
        for i in range(1, max(internal_history_len, cube_history_len) + 1):
            if i > internal_history_len:
                self.listbox.insert(i, str(self.cube.movement_history[i - 1]))
                continue
            elif i > cube_history_len:
                self.listbox.delete(i, END)
                break
            # in case there's a difference between cube and internal movements,
            # update the one in the listbox
            cube_movement_str = str(self.cube.movement_history[i - 1])
            if str(self.internal_movement_history[i - 1]) != cube_movement_str:
                self.listbox.delete(i, i)
                self.listbox.insert(i, cube_movement_str)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(self.cube.movement_history_pointer + 1)
        self.internal_movement_history = deepcopy(self.cube.movement_history)

    def onlistselect(self, evt):
        w = evt.widget
        s = w.curselection()
        self.cube.set_movement_history_pointer(s[0] - 1)

class View():

    def __init__(self, cube, controller):
        # Initialization
        root = Tk()
        root.title('Rubik Tool')
        root.resizable(0, 0)
        root.bind('<KeyPress>', lambda ev: self.handle_keypress(ev))
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        canvas = Canvas(frm, width=200, height=240)
        canvas.grid(column=0, row=0, rowspan=2, pady=5)
        self.canvas = canvas
        self.root = root
        self.cube = cube
        self.controller = controller
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
        ttk.Label(rotations_frm, text="Cube").grid(row=0, column=0, columnspan=2)
        self.create_cube_rotation_buttons()
        # Command Buttons
        commands_frm = ttk.Frame(frm, padding=5)
        commands_frm.grid(column=3, row=0)
        self.commands_frm = commands_frm
        ttk.Label(commands_frm, text="Commands").grid(row=0, column=0, columnspan=2)
        self.create_cube_commands_buttons()

    def get_canvas_reference(self):
        return self.canvas

    def create_face_move_buttons(self):
        self.create_face_move_button("FRONT", 'f', column=0, row=1)
        self.create_face_move_button("UP", 'u', column=0, row=2)
        self.create_face_move_button("DOWN", 'd', column=0, row=3)
        self.create_face_move_button("LEFT", 'l', column=1, row=1)
        self.create_face_move_button("RIGHT", 'r', column=1, row=2)
        self.create_face_move_button("BACK", 'b', column=1, row=3)

    def create_face_move_button(self, text, face, **grid_args):
        ttk.Button(
            self.movement_buttons_frm,
            text=text,
            command=lambda: self.controller.rotate_cube_face(face)
        ).grid(**grid_args)

    def handle_keypress(self, event):
        char = event.char.lower()
        if char in ['f', 'b', 'd', 'u', 'l', 'r']:
            is_prime = event.state & 1 # check if shift is pressed
            self.controller.rotate_cube_face(char + ('\'' if is_prime else ''))
        elif char in ['x', 'y', 'z']:
            self.controller.rotate_cube(char)

    def create_cube_rotation_buttons(self):
        self.create_cube_rotation_button("X", 'x', column=0, row=1)
        self.create_cube_rotation_button("Y", 'y', column=0, row=2)
        self.create_cube_rotation_button("Z", 'z', column=0, row=3)

    def create_cube_commands_buttons(self):
        ttk.Button(
            self.commands_frm,
            text='RESET',
            command=lambda: self.controller.reset_cube(),
        ).grid(column=0, row=1)
        ttk.Button(
            self.commands_frm,
            text='SHUFFLE',
            command=lambda: self.controller.shuffle_cube(),
        ).grid(column=0, row=2)
        ttk.Button(
            self.commands_frm,
            text='SAVE',
            command=lambda: self.controller.save_game(),
        ).grid(column=1, row=1)
        ttk.Button(
            self.commands_frm,
            text='SAVE AS...',
            command=lambda: self.controller.save_game_as(),
        ).grid(column=1, row=2)
        ttk.Button(
            self.commands_frm,
            text='OPEN...',
            command=lambda: self.controller.open_game(),
        ).grid(column=1, row=3)
        ttk.Button(
            self.commands_frm,
            text='MOVES...',
            command=self.open_new_window,
        ).grid(column=1, row=4)

    def open_new_window(self):
        movement_window = MovementViewer(self, self.root, self.cube)

    def create_cube_rotation_button(self, text, axis, **grid_args):
        ttk.Button(
            self.rotations_frm,
            text=text,
            command=lambda: self.controller.rotate_cube(axis),
        ).grid(**grid_args)

    def mainloop(self):
        self.painter.render()
        self.root.mainloop()
