def doOverlap(boxA, boxB):

    # If one rectangle is on left side of other
    if(boxA.XtopLeft >= boxB.XbottomRigh or boxB.XtopLeft >= boxA.XtopLeft):
        return "left"

    # If one rectangle is above other
    if(boxA.YtopLeft <= boxB.YbottomRight or boxB.YtopLeft <= boxA.YbottomRight):
        return "above"

    return True