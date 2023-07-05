from Tkinter_template.Assets.project_management import making_widget
from Tkinter_template.Assets.universal import parse_json_to_property
from Tkinter_template.Assets.font import font_get
from Tkinter_template.Assets.music import Music
from Tkinter_template.base import Interface
from modules.obstacle import ObstacleMaker
from modules.move import MoveInfomation
from modules.player import Player
import time


class LollipopGame(Interface):
    def __init__(self, title: str, icon=None, default_menu=True):
        Interface.rate = 1.0
        super().__init__(title, icon, default_menu)

        parse_json_to_property(self, 'modules\\setting\main_setting.json')
        parse_json_to_property(self, 'modules\\setting\obstacle.json')
        parse_json_to_property(self, 'modules\\setting\sounds.json')
        self.Musics = Music()
        self.Musics.set_volume(0.8)
        self.Players = Player(self)
        self.Moves = MoveInfomation(self)
        self.Obstacles = ObstacleMaker(self)
        self.__start_page()
        self.__set_score_board()
        self.__set_timer()
        self.__set_score_rate()

        self.__build_player()
        self.__bind_jump()
        self.__start_sec = None
        self.is_start = False

    def __start_page(self):
        self.canvas.create_line(0, self.canvas_side[1],
                                self.canvas_side[0], self.canvas_side[1],
                                width=self.bottomLineWidth.get(), fill=self.bottomLineColor_0.get(), tags=('bottom-line'))
        self.canvas.create_text(
            self.side[0] / 2, self.side[1] - 35, text='Floor', font=font_get(20), anchor='s', tags=('hint')
        )

    def __set_score_board(self):
        self.score_board_label = making_widget("Label")(self.root, textvariable=self.scoreBoard_0, width=7,
                                                        font=font_get(20, True), relief="solid", bg=self.scoreBoard_1.get())
        self.canvas.create_window(self.canvas_side[0], 0, anchor='ne',
                                  window=self.score_board_label, tags=('score-board'))

    def __set_timer(self):
        self.timer_label = making_widget("Label")(self.root, textvariable=self.timer, width=7,
                                                  font=font_get(20, True), relief="solid")
        self.canvas.create_window(self.canvas_side[0], 30, anchor='ne',
                                  window=self.timer_label, tags=('timer'))

    def __set_score_rate(self):
        self.rate_label = making_widget("Label")(self.root, textvariable=self.rate, width=7,
                                                 font=font_get(20, True), relief="solid")
        self.canvas.create_window(self.canvas_side[0], 60, anchor='ne',
                                  window=self.rate_label, tags=('rate'))

    def __build_player(self):
        self.Players.create_image()

    def __bind_jump(self):
        self.can_jump = True

        def small_jump(e):
            self.__start_a_new_round()
            if self.can_jump:
                self.Moves.jump(self.jumpsRate_0.get())
                self.can_jump = False

        def big_jump(e):
            self.__start_a_new_round()
            if self.can_jump:
                self.Moves.jump(self.jumpsRate_1.get())
                self.can_jump = False

        def release(e):
            self.can_jump = True
        self.canvas.bind('<Left>', small_jump)
        self.canvas.bind('<Right>', big_jump)

        self.canvas.bind('<KeyRelease>', release)

    def __start_a_new_round(self):
        self.is_start = True
        if self.__start_sec is None:
            self.Musics.music = self.BGM.get()
            self.__start_sec = time.time()
            self.canvas.delete('hint')

    def flush_timer(self):
        self.time_delta = self.get_time_delta()
        offset = str(self.time_delta).find(".")
        self.timer.set(
            f"{int(self.time_delta)}:{str(self.time_delta)[offset+1:offset+3]}")

    def get_time_delta(self):
        return time.time() - self.__start_sec

    def basic_func(self):
        self.canvas.update()
        self.Moves.sleep()

    def basic_move(self):
        self.Moves.freefall()
        self.Moves.move()
        self.Moves.judge_touch_top(app.Players.get_image_box())
        self.Moves.judge_touch_bottom(self.Players.get_image_box())

        self.Moves.judge_touch_obstacle(self.Players.get_image_box())

    def lose(self):
        self.is_start = False

        self.Musics.music = None
        self.canvas.itemconfig(
            'player-rectangle', outline=self.rectangleColor_1.get())


if __name__ == '__main__':
    app = LollipopGame("Lollipop Game", 'lollipop.ico')

    while True:
        if app.is_start:
            app.basic_func()
            app.flush_timer()
            app.Musics.judge()
            app.basic_move()
            if app.get_time_delta() % 3 < 0.01:
                app.Obstacles.setting_a_obstacle()
            app.Obstacles.move_all_obstacle()
        else:
            app.basic_func()
