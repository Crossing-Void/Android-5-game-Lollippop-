from abc import ABC, abstractmethod


class ObstacleBase(ABC):
    counter = 0

    def __init__(self, app, outlook: dict):
        self.app = app
        self.fill = outlook['fill']
        self.outline = outlook['outline']
        self.be_add_point = False
        self.__tags = f'obstacle{ObstacleBase.counter}'
        self.__boundary = {}
        self.__point = 0
        self.__x_speed = 4
        ObstacleBase.counter += 1

    @property
    def tags(self):
        return self.__tags

    @property
    def boundary(self):
        return self.__boundary

    @boundary.setter
    def boundary(self, value):
        if (t := type(value)) != dict:
            raise TypeError(f"boundary expect a dict, but get {t}")
        self.__boundary = value

    @property
    def point(self):
        return self.__point

    @point.setter
    def point(self, value):
        if (t := type(value)) != int:
            raise TypeError(f"point expect a dict, but get {t}")
        self.__point = value

    def moving(self):
        self.app.canvas.move(self.tags, -self.__x_speed, 0)

        new = {}
        for x, boundary in self.boundary.items():
            new[x-self.__x_speed] = boundary
        self.boundary = new

    def to_red(self):
        try:
            # rectangle
            self.app.canvas.itemconfig(self.tags, fill='red', outline='red')
        except:
            pass

    def delete(self):
        self.app.canvas.delete(self.tags)

    @abstractmethod
    def realize(self):
        return NotImplemented
