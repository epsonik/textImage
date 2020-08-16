from BoundBox import BoundBox
from img_det import get_labels
import numpy as np

def calculate_position(boxA: BoundBox, boxB: BoundBox):

    # If one rectangle is on left side of other
    if(boxA.XtopLeft >= boxB.XbottomRight or boxB.XtopLeft >= boxA.XtopLeft):
        return "left", get_labels()[boxA.label], get_labels()[boxB.label]

        # If one rectangle is above other
    if(boxA.YtopLeft <= boxB.YbottomRight or boxB.YtopLeft <= boxA.YbottomRight):
        return "above", get_labels()[boxA.label], get_labels()[boxB.label]
    return False

def calculate_centroid(coorA, coorB):
    return np.double((coorB - coorA) / 2)