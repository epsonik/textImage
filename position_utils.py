import numpy as np

from BoundBox import BoundBox


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


def position_on_image():
    return True
