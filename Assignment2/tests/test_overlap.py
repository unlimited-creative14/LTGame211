from utils.shapes.shape import Rect, Point, Circle
import unittest
import pytest

class OverlapTestCase(unittest.TestCase):

    def test1(self):
        r = Rect(Point(0, 0), 3, 4)
        c = Circle(Point(0, 0), 2)

        assert c.is_overlap(r)


    def test2(self):
        r = Rect(Point(2, 0), 3, 4)
        c = Circle(Point(0,0), 2)

        assert c.is_overlap(r)
    
    def test3(self):
        r1 = Rect(Point(0,0), 2,2)
        r2 = Rect(Point(1,1), 2,2)

        assert r1.is_overlap(r2)

    def test4(self):
        r1 = Rect(Point(0,0), 2,2)
        r2 = Rect(Point(2,2), 2,2)

        assert r1.is_overlap(r2)

    def test5(self):
        r1 = Rect(Point(0,0), 3, 3)
        r2 = Rect(Point(1,1), 1, 1)

        assert r1.is_overlap(r2)

    def test6(self):
        r2 = Rect(Point(0,0), 3, 3)
        r1 = Rect(Point(1,1), 1, 1)

        assert r1.is_overlap(r2)

    def test7(self):
        c1 = Circle(Point(0,0), 2)
        c2 = Circle(Point(3,0), 2)

        assert c1.is_overlap(c2)

    def test8(self):
        c1 = Circle(Point(0,0), 2)
        c2 = Circle(Point(5,0), 2)

        assert not c1.is_overlap(c2)
    
    def test9(self):
        c1 = Circle(Point(0,0), 4)
        c2 = Circle(Point(1,0), 1)

        assert c1.is_overlap(c2)

    def test10(self):
        r1 = Rect(Point(0,0), 10, 10)
        c = Circle(Point(5,5), 1)

        assert c.is_overlap(r1)