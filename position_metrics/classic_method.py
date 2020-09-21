from position_metrics.orientation_interface import Orientation


class ClassicMethod(Orientation):

    def _is_left_oriented(self):
        return self.box.XbottomRight <= self.image_width / 2

    def _certainty_factor_left(self):
        return self.box.XbottomRight / self.image_width

    def _is_right_oriented(self):
        return self.box.XtopLeft >= self.image_width / 2

    def _certainty_factor_right(self):
        return self.box.XtopLeft / self.image_width

    def _is_top_oriented(self):
        return self.box.YbottomRight <= self.image_height / 2

    def _certainty_factor_top(self):
        return self.box.YbottomRight / self.image_height

    def _is_bottom_oriented(self):
        return self.box.YtopLeft >= self.image_height / 2

    def _certainty_factor_bottom(self):
        return self.box.YtopLeft / self.image_height

    def left_orientation(self):
        return {
            'left_orientation': self._is_left_oriented(),
            'certainty_factor': self._certainty_factor_left() if self._is_left_oriented() else -1
        }

    def right_orientation(self):
        return {
            'right_orientation': self._is_right_oriented(),
            'certainty_factor': self._certainty_factor_right() if self._is_right_oriented() else -1
        }

    def top_orientation(self):
        return {
            'top_orientation': self._is_top_oriented(),
            'certainty_factor': self._certainty_factor_top() if self._is_top_oriented() else -1
        }

    def bottom_orientation(self):
        return {
            'bottom_orientation': self._is_bottom_oriented(),
            'certainty_factor': self._certainty_factor_bottom() if self._is_bottom_oriented() else -1
        }