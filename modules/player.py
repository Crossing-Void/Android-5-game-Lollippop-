from Tkinter_template.Assets.image import tk_image
import random
import os


class Player:
    def __init__(self, app):
        self.app = app

    def create_image(self):
        path = self.app.playerImagePath.get()
        files = []
        for now, _, filelist in os.walk(path):
            for filename in filelist:
                files.append(os.path.join(now, filename))
        file = random.choice(files)
        x, y = random.randint(0, 100), random.randint(
            0, self.app.canvas_side[1]-300)

        self.app.canvas.create_image(x, y, anchor='nw', tags=('player', 'player-image'),
                                     image=tk_image(os.path.split(file)[-1],
                                                    100, 100, dirpath=os.path.split(file)[0]))
        self.create_rectangle()

    def get_image_box(self):
        # four element
        return self.app.canvas.bbox('player-image')

    def create_rectangle(self):
        self.app.canvas.delete('player-rectangle')
        self.app.canvas.create_rectangle(
            *self.get_image_box(), tags=('player', 'player-rectangle'), outline=self.app.rectangleColor_0.get())
