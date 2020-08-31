from position_metrics.orientation_interface import Orientation


class CentroidMethod(Orientation):

    def _is_left_oriented(self):
        return True if self._certainty_factor_left() > 0 else False

    def _certainty_factor_left(self):
        return super().certainty_factor_left(self.box.Xcentroid)

    def _is_right_oriented(self):
        return True if self._certainty_factor_right() > 0 else False

    def _certainty_factor_right(self):
        return super().certainty_factor_right(self.box.Xcentroid)

    def _is_top_oriented(self):
        return True if self._certainty_factor_top() > 0 else False

    def _certainty_factor_top(self):
        return super().certainty_factor_top(self.box.Ycentroid)

    def _is_bottom_oriented(self):
        return True if self._certainty_factor_bottom() > 0 else False

    def _certainty_factor_bottom(self):
        return super().certainty_factor_bottom(self.box.Ycentroid)

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