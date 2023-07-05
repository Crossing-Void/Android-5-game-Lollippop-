from Tkinter_template.Assets.soundeffect import play_sound
import time


class MoveInfomation:
    def __init__(self, app) -> None:
        self.app = app

        self.arguments = {
            "y-speed": self.app.moveArgs_0.get(),
            "dt": self.app.moveArgs_1.get(),
            "acceleration": self.app.moveArgs_2.get()
        }

    def move(self):
        self.app.canvas.move(
            'player', 0, self.arguments['y-speed'] * self.arguments['dt'])

    def freefall(self):
        final_yspeed = self.arguments['y-speed'] +\
            self.arguments['acceleration'] *\
            self.arguments['dt']

        self.arguments['y-speed'] = final_yspeed

    def sleep(self):
        time.sleep(self.arguments['dt'])

    def jump(self, rate):
        self.arguments['y-speed'] = -1 * self.arguments['acceleration'] / rate

    # ----- check -----
    def judge_touch_top(self, coords: tuple):
        if coords[1] <= 0 and self.arguments['y-speed'] < 0:
            self.arguments['y-speed'] = 0
            self.app.canvas.coords(
                'player-image', self.app.canvas.coords('player-image')[0], 0)
            self.app.Players.create_rectangle()
            play_sound(self.app.collideTopSound.get())

    def judge_touch_bottom(self, coords: tuple):
        if coords[3] >= self.app.canvas_side[1] - self.app.bottomLineWidth.get()//2:
            self.app.canvas.itemconfigure(
                'bottom-line', fill=self.app.bottomLineColor_1.get())
            # >> Refine outlook <<
            y_diff = coords[3] - self.app.canvas_side[1] + \
                self.app.bottomLineWidth.get()//2
            self.app.canvas.move('player', 0, -y_diff)
            # >> Refine outlook <<
            play_sound(self.app.loseSound.get())
            self.app.lose()

    def judge_touch_obstacle(self, coords: tuple):

        for obs in self.app.Obstacles.obstacle_list:
            b = obs.boundary
            Max, Min = max(b.keys()), min(b.keys())
            if Max < 0:
                self.app.Obstacles.remove_a_obstacle(obs)
                continue
            if Min > coords[2]:
                continue
            if Max < coords[0]:
                if obs.be_add_point == False:
                    obs.be_add_point = True
                    play_sound(self.app.obstaclePassSound.get())
                    self.app.scoreBoard_0.set(
                        str(int(self.app.scoreBoard_0.get()) + obs.point))
                continue

            for my_x in range(coords[0], coords[2] + 1):
                if my_x in b:
                    if coords[1] <= b[my_x][0]:
                        # >> Refine outlook <<
                        y_diff = b[my_x][0] - coords[1]
                        if y_diff <= 4:
                            self.app.canvas.move('player', 0, y_diff+1)
                        # >> Refine outlook <<
                        obs.to_red()
                        play_sound(self.app.collideLoseSound.get())
                        self.app.lose()

                    if coords[3] >= b[my_x][1]:
                        # >> Refine outlook <<
                        y_diff = coords[3] - b[my_x][1]
                        if y_diff <= 4:
                            self.app.canvas.move('player', 0, -y_diff-1)
                        # >> Refine outlook <<
                        obs.to_red()
                        play_sound(self.app.collideLoseSound.get())
                        self.app.lose()
