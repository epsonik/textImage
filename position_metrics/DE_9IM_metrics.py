from shapely.geometry import Polygon

from bound_box import BoundBox


class DE9IM:

    def convert_top_bottom_to_polygon(self, box):
        return [(box.XtopLeft, box.YtopLeft),
                (box.XbottomRight, box.YtopLeft),
                (box.XbottomRight, box.YbottomRight),
                (box.XtopLeft, box.YbottomRight)]

    def position_between_objects(self, v_boxes):
        position_between_objects = {}
        position_between_objects['position_between_objects'] = []
        pos_bet_obj = position_between_objects['position_between_objects']
        for i in range(v_boxes.__len__()):
            boxA = v_boxes[i]
            for b in range(len(v_boxes)):
                boxB = v_boxes[b]
                if i is not b:
                    pos_bet_obj.append(self._calculate_position_between_objects(boxA, boxB))
        return position_between_objects

    def _calculate_position_between_objects(self, boxA: BoundBox, boxB: BoundBox):
        polygon = Polygon(self.convert_top_bottom_to_polygon(boxA))
        other_polygon = Polygon(self.convert_top_bottom_to_polygon(boxB))
        vsName = boxA.label + ' vs ' + boxB.label
        positions = { vsName: {}}
        # positions[vsName]
        if polygon.crosses(other_polygon):
            positions[vsName]['crosses'] = polygon.crosses(other_polygon)
        if polygon.contains(other_polygon):
            positions[vsName]['contains'] = polygon.contains(other_polygon)
        if polygon.disjoint(other_polygon):
            positions[vsName]['disjoint'] = polygon.disjoint(other_polygon)
        if polygon.intersects(other_polygon):
            positions[vsName]['intersects'] = polygon.intersects(other_polygon)
        if polygon.overlaps(other_polygon):
            positions[vsName]['overlaps'] = polygon.overlaps(other_polygon)
        if polygon.touches(other_polygon):
            positions[vsName]['touches'] = polygon.touches(other_polygon)
        if polygon.within(other_polygon):
            positions[vsName]['within'] = polygon.within(other_polygon)
        return positions


def position_on_image_area(v_boxes):
    return DE9IM().position_between_objects(v_boxes)
