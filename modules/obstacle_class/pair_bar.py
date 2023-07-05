from modules.obstacle_class.base_class import ObstacleBase
from Tkinter_template.Assets.font import font_get
import random


class PairBar(ObstacleBase):
    def __init__(self, app, outlook: dict):
        super().__init__(app, outlook)

        bar_width = random.randint(100, 300)
        bar_gap = random.randint(150+100*1.5, 150+100*1.75)
        self.point = int(bar_width//30) + int((1000-bar_gap)//20)
        self.realize(bar_width, bar_gap)

    def realize(self, width, gap):
        remain_h = self.app.canvas_side[1] - gap
        upper_h = random.randint(30, remain_h - 30)
        bottom_h = remain_h - upper_h

        # >> Top build <<
        self.app.canvas.create_rectangle(
            self.app.canvas_side[0] +
            400, 0, self.app.canvas_side[0]+400+width, upper_h,
            tags=self.tags, fill=self.fill, outline=self.outline
        )
        # >> Down build <<
        self.app.canvas.create_rectangle(
            self.app.canvas_side[0]+400, self.app.canvas_side[1] - bottom_h, self.app.canvas_side[0] +
            400+width, self.app.canvas_side[1],
            tags=self.tags, fill=self.fill, outline=self.outline
        )
        self.app.canvas.create_text(self.app.canvas_side[0]+400+int(width / 2), int(upper_h / 2), text=self.point,
                                    tags=self.tags, font=font_get(20, True),
                                    fill='white')
        self.app.canvas.create_text(self.app.canvas_side[0]+400+int(width / 2), self.app.canvas_side[1] - int(bottom_h/2), text=self.point,
                                    tags=self.tags, font=font_get(20, True),
                                    fill='white')

        for x in range(self.app.canvas_side[0] + 400, self.app.canvas_side[0] + 400 + width + 1):
            self.boundary[x] = [upper_h, self.app.canvas_side[1] - bottom_h]


def create_obstacle(app, outlook):
    return PairBar(app, outlook)
