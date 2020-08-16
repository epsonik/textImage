from BoundBox import BoundBox


def calculate_position(boxA: BoundBox, boxB: BoundBox):

    # If one rectangle is on left side of other
    if(boxA.XtopLeft >= boxB.XbottomRight or boxB.XtopLeft >= boxA.XtopLeft):
        return "left"

    # If one rectangle is above other
    if(boxA.YtopLeft <= boxB.YbottomRight or boxB.YtopLeft <= boxA.YbottomRight):
        return "above"

    return False