import pytest
from shape import *


class TestTetris:

    def test_shape(self):
        block = Shape()
        assert(block.shape() is Tetrominoe.Empty)

    def test_tetrominoe(self):
        tetrominoe = Tetrominoe()
        assert(tetrominoe.Empty == 0)
        assert(tetrominoe.Line == 3)
        assert(tetrominoe.Square == 5)

    def test_block_shape(self):
        shape = Shape()
        block_shape = shape.BlockShape
        assert(shape.shape() == block_shape)

    def test_set_shape(self):
        block = Shape()
        block.setShape(Tetrominoe.Line)
        assert(block.BlockShape is Tetrominoe.Line)
        block.setShape(Tetrominoe.MirroredL)
        assert (block.BlockShape is Tetrominoe.MirroredL)
        block.setShape(Tetrominoe.T)
        assert (block.BlockShape is Tetrominoe.T)

    def test_set_coord_x(self):
        block = Shape()
        block.setShape(Tetrominoe.Line)
        block.setX(0, 1)
        assert(block.x(0) == 1)

    def test_set_coord_y(self):
        block = Shape()
        block.setShape(Tetrominoe.Line)
        block.setY(0, 1)
        assert(block.y(0) == 1)

    def test_rotation_left(self):
        block = Shape()
        block.setShape(Tetrominoe.Line)
        block1 = Shape()
        block1.setShape(Tetrominoe.Line)
        for i in range(4):
            block.setX(i, block.y(i))
            block.setY(i, -block.x(i))
        assert(block1.rotateLeft().y(0) == block.x(1))

    def test_rotation_right(self):
        block = Shape()
        block.setShape(Tetrominoe.Line)
        block1 = Shape()
        block1.setShape(Tetrominoe.Line)
        for i in range(4):
            block.setX(i, -block.y(i))
            block.setY(i, block.x(i))
        assert(block1.rotateRight().y(0) == block.x(1))

    def test_min_y(self):
        block = Shape()
        m = block.coords[0][1]
        for i in range(4):
            m = min(m, block.coords[i][1])
        assert(m == block.minY())

    def test_random_shape(self):
        block = Shape()
        block.setRandomShape()
        set_of_shapes = {0, 1, 2, 3, 4, 5, 6, 7}
        assert(block.shape() in set_of_shapes)



