import json

import numpy as np
from keras_preprocessing.image import load_img

from bound_box import BoundBox
from position_metrics.area_method import AreaMethod
from position_metrics.centroid_method import CentroidMethod

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


def is_centered(boxA):
    boxB = centroid_rectangle()
    return boxA.XtopLeft < boxB.XtopLeft < boxB.XbottomRight < boxA.XbottomRight \
           and boxA.YtopLeft < boxB.YtopLeft < boxB.YbottomRight < boxA.YbottomRight


def _position_on_image(box):
    classicMethod = CentroidMethod(box, image_width, image_height)
    return {box.label: {'left_orientation': classicMethod.left_orientation(),
                        'right_orientation': classicMethod.right_orientation(),
                        'top_orientation': classicMethod.top_orientation(),
                        'bottom_orientation': classicMethod.bottom_orientation()}}


def centroid_vbox_position_on_image(v_boxes):
    position_on_image = {}
    position_on_image['centroid_position_on_image'] = []
    t = position_on_image['centroid_position_on_image']
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


def area_vbox_position_on_image(v_boxes):
    position_on_image = {}
    position_on_image['area_position_on_image'] = []
    t = position_on_image['area_position_on_image']
    for i in range(v_boxes.__len__()):
        box = v_boxes[i]
        t.append(_position_on_image_area(box))
    return position_on_image

def _position_on_image_area(box):
    areaMethod = AreaMethod(box, image_width, image_height)
    return {box.label: {'left_orientation': areaMethod.left_orientation(),
                        'right_orientation': areaMethod.right_orientation(),
                        'top_orientation': areaMethod.top_orientation(),
                        'bottom_orientation': areaMethod.bottom_orientation()}}
