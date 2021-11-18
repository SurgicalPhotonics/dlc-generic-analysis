"""
Author: Frank Ma and Louis Adamian
"""
from typing import Tuple


class Line:
    """A line between two points. Used to measure scarring or other deformation
    in vocal cords.
    end1: point
        first point to calc line Endpoint with smaller x value if x1 \neq x2
    end2: point
        second point to calc line. Endpoint with greater x if x1 \neq x2
    slope: float
        slope of the line
    yint: float
        y intercept of line
    """

    def __init__(
        self,
        end1: Tuple[float, float] = None,
        end2: Tuple[float, float] = None,
        slope: float = None,
        intercept: float = None,
    ):
        """
        creates a Line either based on 2 points or a slope and intercept
        :param end1:
        :param end2:
        :param slope:
        :param intercept:
        """
        if end1 is not None and end2 is not None:
            if end1[0] > end2[0]:
                self.end1 = end2
                self.end2 = end1
            else:
                self.end1 = end1
                self.end2 = end2
            if not self.end2[0] == self.end1[0]:
                slope = (self.end2[1] - self.end1[1]) / (self.end2[0] - self.end1[0])
            else:
                slope = 999999999999999
            self.slope = slope
            self.intercept = end1[1] - slope * end1[0]
        elif slope is not None and intercept is not None:
            self.intercept = intercept
            self.slope = slope
            self.end1 = (0, self.intercept)
            self.end2 = (1, int(self.intercept + self.slope))
        else:
            raise AttributeError

    def set_ends(self, cord):
        """Allows a new end2 point to be passed from outside."""
        c = []
        for point in cord:
            if point is not None:
                c.append(point)
        y = c[len(c) - 1][1]
        if self.slope != 0:
            self.end2 = (int((y - self.intercept) / self.slope), int(y))
        else:
            self.end2 = (1, int(y))
        y = c[0][1]
        if self.slope != 0:
            self.end1 = (int((y - self.intercept) / self.slope), int(y))
        else:
            self.end1 = (1, int(y))