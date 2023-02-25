from cube import Cube
from view import View

class App:

    def __init__(self):
        self.cube = Cube()
        self.view = View(self.cube)

    def run(self):
        self.view.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()

