import json

import numpy as np
from keras_preprocessing.image import load_img

from BoundBox import BoundBox

image = load_img("./IMAGES/dog.jpg")
image_width, image_height = image.size
centroid_rectangle = None


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


def is_left_oriented(box):
    return box.XbottomRight <= image_width / 2


def certainty_factor_left(box):
    return box.XbottomRight / image_width


def left_orientation(box):

    return {
        'left_orientation': is_left_oriented(box),
        'certainty_factor': certainty_factor_left(box) if is_left_oriented(box) else -1
    }


def is_right_oriented(box):
    return box.XtopLeft >= image_width / 2


def certainty_factor_right(box):
    return box.XtopLeft / image_width


def right_orientation(box):
    return {
        'right_orientation': is_right_oriented(box),
        'certainty_factor': certainty_factor_right(box) if is_right_oriented(box) else -1
    }


def is_top_oriented(box):
    return box.YbottomRight <= image_height / 2


def certainty_factor_top(box):
    return box.YbottomRight / image_height


def top_orientation(box):
    return {
        'is_top_oriented': is_top_oriented(box),
        'certainty_factor': certainty_factor_top(box) if is_top_oriented(box) else -1
    }


def is_bottom_oriented(box):
    return box.YtopLeft >= image_height / 2


def certainty_factor_bottom(box):
    return box.YtopLeft / image_height


def bottom_orientation(box):
    return {
        'bottom_orientation': is_bottom_oriented(box),
        'certainty_factor': certainty_factor_bottom(box) if is_bottom_oriented(box) else -1
    }


def is_centered(boxA):
    boxB = centroid_rectangle()
    return boxA.XtopLeft < boxB.XtopLeft < boxB.XbottomRight < boxA.XbottomRight \
           and boxA.YtopLeft < boxB.YtopLeft < boxB.YbottomRight < boxA.YbottomRight


def _position_on_image(box):
    return {box.label: {'left_orientation': left_orientation(box),
                        'right_orientation': right_orientation(box),
                        'top_orientation': top_orientation(box),
                        'bottom_orientation': bottom_orientation(box)}}


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
