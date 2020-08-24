import json

import numpy as np
from keras_preprocessing.image import load_img

from BoundBox import BoundBox

image = load_img("./IMAGES/dog.jpg")
image_width, image_height = image.size
centroid_rectangle = None
import abc


# interface for orientation certainty
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


class ClassicMethod(OrientationInterface):

    def _is_left_oriented(self):
        return self.box.XbottomRight <= self.image_width / 2

    def _certainty_factor_left(self):
        return self.box.XbottomRight / self.image_width

    def _is_right_oriented(self):
        return self.box.XtopLeft >= image_width / 2

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
            'is_top_oriented': self._is_top_oriented(),
            'certainty_factor': self._certainty_factor_top() if self._is_top_oriented() else -1
        }

    def bottom_orientation(self):
        return {
            'bottom_orientation': self._is_bottom_oriented(),
            'certainty_factor': self._certainty_factor_bottom() if self._is_bottom_oriented() else -1
        }


def print_pretty(raw_json):
    print(json.dumps(raw_json, indent=4, sort_keys=True))


def centroid_rectangle():
    centroid_rectangle_width = 220 / 283 * image_width
    centroid_rectangle_height = 115 / 163 * image_height
    Yimage_position_proportion = 18 / 163 * image_height
    Ximage_position_proportion = 42 / 283 * image_width

    XtopLeft = Ximage_position_proportion
    YtopLeft = Yimage_position_proportion
    XbottomRight = Ximage_position_proportion + centroid_rectangle_width
    YbottomRight = Yimage_position_proportion + centroid_rectangle_height
    return BoundBox(XtopLeft, YtopLeft, XbottomRight, YbottomRight)


def calculate_position_between_objects(boxA: BoundBox, boxB: BoundBox):
    # If one rectangle is on left side of other
    if boxA.XtopLeft >= boxB.XbottomRight or boxB.XtopLeft >= boxA.XtopLeft:
        return {'boxA': boxA.label, 'boxB': boxB.label, 'position_between_objects': 'left'}

        # If one rectangle is above other
    if boxA.YtopLeft <= boxB.YbottomRight or boxB.YtopLeft <= boxA.YbottomRight:
        return {'boxA': boxA.label, 'boxB': boxB.label, 'position_between_objects': 'above'}
    return False


def calculate_centroid(coorA, length):
    return np.double((coorA) + length / 2)


def centroid_distance(boxA, boxB):
    return round(np.double(np.math.sqrt((boxB.Xcentroid - boxA.Xcentroid) ** 2 +
                                        (boxB.Ycentroid - boxA.Ycentroid) ** 2)), 4)


def is_centered(boxA):
    boxB = centroid_rectangle()
    return boxA.XtopLeft < boxB.XtopLeft < boxB.XbottomRight < boxA.XbottomRight \
           and boxA.YtopLeft < boxB.YtopLeft < boxB.YbottomRight < boxA.YbottomRight


def _position_on_image(box):
    classicMethod = ClassicMethod(box, image_width, image_height)
    return {box.label: {'left_orientation': classicMethod.left_orientation(),
                        'right_orientation': classicMethod.right_orientation(),
                        'top_orientation': classicMethod.top_orientation(),
                        'bottom_orientation': classicMethod.bottom_orientation()}}


def position_on_image(v_boxes):
    position_on_image = {}
    position_on_image['position_on_image'] = []
    t = position_on_image['position_on_image']
    for i in range(len(v_boxes)):
        boxA = v_boxes[i]
        t.append(_position_on_image(boxA))
    return position_on_image


def position_between_objects(v_boxes):
    position_between_objects = {}
    position_between_objects['position_between_objects'] = []
    pos_bet_obj = position_between_objects['position_between_objects']
    for i in range(v_boxes.__len__()):
        boxA = v_boxes[i]
        for b in range(len(v_boxes)):
            boxB = v_boxes[b]
            if i is not b:
                pos_bet_obj.append(calculate_position_between_objects(boxA, boxB))
    return position_between_objects
