# interface for orientation certainty


class Orientation():
    def __init__(self, box, image_width, image_height):
        self.box = box
        self.image_width = image_width
        self.image_height = image_height

    def left_orientation(self):
        """Load in the data set"""
        raise NotImplementedError

    def right_orientation(self):
        """Extract text from the data set"""
        raise NotImplementedError

    def top_orientation(self):
        """Load in the data set"""
        raise NotImplementedError

    def bottom_orientation(self):
        """Extract text from the data set"""
        raise NotImplementedError

    def certainty_factor_left(self, X):
        return (-1) * (2 * X - self.image_width) / self.image_width

    def certainty_factor_right(self, X):
        return (2 * X - self.image_width) / self.image_width

    def certainty_factor_top(self, Y):
        return (-1) * (2 * Y - self.image_height) / self.image_height

    def certainty_factor_bottom(self, Y):
        return (2 * Y - self.image_height) / self.image_height

    def convert_top_bottom_to_polygon(self, box):
        return [(box.XtopLeft, box.YtopLeft),
                (box.XbottomRight, box.YtopLeft),
                (box.XbottomRight, box.YbottomRight),
                (box.XtopLeft, box.YbottomRight)]
