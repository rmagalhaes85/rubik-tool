from cube import Cube
from view import View
from controller import Controller

class App:

    def __init__(self):
        self.cube = Cube()
        self.controller = Controller(self.cube)
        self.view = View(self.cube, self.controller)

    def run(self):
        self.view.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()

