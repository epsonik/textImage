# interface for orientation certainty
import abc


class OrientationInterface(metaclass=abc.ABCMeta):
    def __init__(self, box, image_width, image_height):
        self.box = box
        self.image_width = image_width
        self.image_height = image_height

    @abc.abstractmethod
    def left_orientation(self):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def right_orientation(self):
        """Extract text from the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def top_orientation(self):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def bottom_orientation(self):
        """Extract text from the data set"""
        raise NotImplementedError
