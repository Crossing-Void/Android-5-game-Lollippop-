from modules.obstacle_class import *
from modules.obstacle_class import __all__ as availiable_obstacle
import random


class ObstacleMaker:
    color_list = ["gold", "chocolate", "purple", "#ff6b87"]

    def __init__(self, app):
        self.__obstacle_list = []
        self.app = app

    @property
    def obstacle_list(self):
        '''not provide setter'''
        return self.__obstacle_list

    def setting_a_obstacle(self):
        arguments = {}
        # fill
        arguments['fill'] = random.choice(ObstacleMaker.color_list) if \
            (f := self.app.obstacleColor_0.get()) == 'random' else f

        # outline
        arguments['outline'] = random.choice(ObstacleMaker.color_list) if \
            (f := self.app.obstacleColor_1.get()) == 'random' else f

        # create and append

        self.__obstacle_list.append(
            eval(random.choice(availiable_obstacle)
                 ).create_obstacle(self.app, arguments)
        )

    def remove_a_obstacle(self, obstacle: object):
        obstacle.delete()
        self.obstacle_list.remove(obstacle)

    def move_all_obstacle(self):
        for obs in self.obstacle_list:
            obs.moving()
