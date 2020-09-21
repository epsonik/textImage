import numpy as np


class BoundBox:

    def __init__(self, XtopLeft, YtopLeft, XbottomRight, YbottomRight, objness=None, classes=None):
        self.XtopLeft = XtopLeft
        self.YtopLeft = YtopLeft
        self.XbottomRight = XbottomRight
        self.YbottomRight = YbottomRight
        self.objness = objness
        self.classes = classes
        self.label = -1
        self.score = -1

    def get_coordinates(self):
        return self.XtopLeft, self.YtopLeft, self.XbottomRight, self.YbottomRight

    def get_label(self):
        if self.label == -1:
            self.label = np.argmax(self.classes)

        return self.label

    def get_score(self):
        if self.score == -1:
            self.score = self.classes[self.get_label()]

        return self.score

    def calculate_width(self):
        return self.XbottomRight - self.XtopLeft

    def calculate_height(self):
        return self.YbottomRight - self.YtopLeft

    def calculate_area(self):
        return self.calculate_width() * self.calculate_height()


class Reading(BoundBox):

    def __init__(self, img_id, XtopLeft, YtopLeft, XbottomRight, YbottomRight, Xcentroid, Ycentroid, area, label):
        super().__init__(XtopLeft, YtopLeft, XbottomRight, YbottomRight)
        self.label = label
        self.img_id = img_id
        self.Xcentroid = Xcentroid
        self.Ycentroid = Ycentroid
        self.area = area


def read_table(json):
    return [Reading(**t) for t in json]
