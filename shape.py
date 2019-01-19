import random
from tetris import *


class Tetrominoe(object):
    Empty = 0
    Z = 1
    S = 2
    Line = 3
    T = 4
    Square = 5
    L = 6
    MirroredL = 7


class Shape(object):
    table_coords = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        self.coords = [[0, 0] for i in range(4)]
        self.BlockShape = Tetrominoe.Empty
        self.setShape(Tetrominoe.Empty)

    def shape(self):
        return self.BlockShape

    def setShape(self, shape):
        table = Shape.table_coords[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]
        self.BlockShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])
        return m

    def rotateLeft(self):
        if self.BlockShape == Tetrominoe.Square:
            return self
        result = Shape()
        result.BlockShape = self.BlockShape
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))
        clap.play()
        return result

    def rotateRight(self):
        if self.BlockShape == Tetrominoe.Square:
            return self
        result = Shape()
        result.BlockShape = self.BlockShape
        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))
        clap.play()
        return result
