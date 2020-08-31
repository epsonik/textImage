from shapely.geometry import Polygon

from bound_box import BoundBox
from position_metrics.orientation_interface import Orientation


class AreaMethod(Orientation):

    def __init__(self, box, image_width, image_height):
        super().__init__(box, image_width, image_height)
        self.TOP = BoundBox(0, 0, image_width, image_height / 2)
        self.BOTTOM = BoundBox(0, image_height / 2, image_width, image_height)
        self.LEFT = BoundBox(0, 0, image_width / 2, image_height)
        self.RIGHT = BoundBox(image_width / 2, 0, image_width, image_height)

    def convert_top_bottom_to_polygon(self, box):
        return [(box.XtopLeft, box.YtopLeft),
                (box.XbottomRight, box.YtopLeft),
                (box.XbottomRight, box.YbottomRight),
                (box.XtopLeft, box.YbottomRight)]

    def calc_overlap_area(self, boxA, boxB):
        from shapely.geometry import Polygon

        polygon = Polygon(self.convert_top_bottom_to_polygon(boxA))
        other_polygon = Polygon(self.convert_top_bottom_to_polygon(boxB))
        intersection = polygon.intersection(other_polygon)
        return intersection.area

    def _is_left_oriented(self):
        return True if self._certainty_factor_left() > 0 else False

    def _certainty_factor_left(self):
        return self.calc_overlap_area(self.box, self.LEFT) / Polygon(self.convert_top_bottom_to_polygon(self.box)).area

    def _is_right_oriented(self):
        return True if self._certainty_factor_right() > 0 else False

    def _certainty_factor_right(self):
        return self.calc_overlap_area(self.box, self.RIGHT) / Polygon(self.convert_top_bottom_to_polygon(self.box)).area

    def _is_top_oriented(self):
        return True if self._certainty_factor_top() > 0 else False

    def _certainty_factor_top(self):
        return self.calc_overlap_area(self.box, self.TOP) / Polygon(self.convert_top_bottom_to_polygon(self.box)).area

    def _is_bottom_oriented(self):
        return True if self._certainty_factor_bottom() > 0 else False

    def _certainty_factor_bottom(self):
        return self.calc_overlap_area(self.box, self.BOTTOM) / Polygon(
            self.convert_top_bottom_to_polygon(self.box)).area

    def left_orientation(self):
        return {
            'left_orientation': self._is_left_oriented(),
            'certainty_factor': self._certainty_factor_left()
        }

    def right_orientation(self):
        return {
            'right_orientation': self._is_right_oriented(),
            'certainty_factor': self._certainty_factor_right()
        }

    def top_orientation(self):
        return {
            'is_top_oriented': self._is_top_oriented(),
            'certainty_factor': self._certainty_factor_top()
        }

    def bottom_orientation(self):
        return {
            'bottom_orientation': self._is_bottom_oriented(),
            'certainty_factor': self._certainty_factor_bottom()
        }
