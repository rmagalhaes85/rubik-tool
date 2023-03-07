import persistence

class Controller:

    def __init__(self, cube):
        self.cube = cube

    def rotate_cube_face(self, face):
        self.cube.rotate_face(face)

    def rotate_cube(self, axis):
        self.cube.rotate_cube(axis)

    def reset_cube(self):
        self.cube.reset()

    def shuffle_cube(self):
        self.cube.shuffle()

    def save_game(self):
        persistence.save(self.cube)

    def save_game_as(self):
        persistence.save_as(self.cube)

    def open_game(self):
        persistence.open(self.cube)
