import numpy as np
from keras_preprocessing.image import load_img

from BoundBox import BoundBox

image = load_img("dog.jpg")
image_width, image_height = image.size
centroid_rectangle = None


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
    if (boxA.XtopLeft >= boxB.XbottomRight or boxB.XtopLeft >= boxA.XtopLeft):
        return "left"

        # If one rectangle is above other
    if (boxA.YtopLeft <= boxB.YbottomRight or boxB.YtopLeft <= boxA.YbottomRight):
        return "above"
    return False


def calculate_centroid(coorA, length):
    return np.double((coorA) + length / 2)


def centroid_distance(boxA, boxB):
    return round(np.double(np.math.sqrt((boxB.Xcentroid - boxA.Xcentroid) ** 2 +
                                        (boxB.Ycentroid - boxA.Ycentroid) ** 2)), 4)


def is_left_oriented(box):
    return box.XbottomRight <= image_width / 2


def is_right_oriented(box):
    return box.XtopLeft >= image_width / 2


def is_top_oriented(box):
    return box.YbottomRight <= image_height / 2


def is_bottom_oriented(box):
    return box.YtopLeft >= image_height / 2


def is_centered(boxA):
    boxB = centroid_rectangle()
    return boxA.XtopLeft < boxB.XtopLeft < boxB.XbottomRight < boxA.XbottomRight \
           and boxA.YtopLeft < boxB.YtopLeft < boxB.YbottomRight < boxA.YbottomRight


def is_cornered():
    return False


def position_on_image():
    return True
