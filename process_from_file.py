import json

import bound_box
from position_metrics.DE_9IM_metrics import position_on_image_area
from position_utils import area_vbox_position_on_image, \
    centroid_vbox_position_on_image, position_between_objects


def print_pretty(raw_json):
    print(json.dumps(raw_json, indent=4, sort_keys=True))


with open('./IMAGES/dog.txt') as json_file:
    image_b_boxes_df = json.load(json_file)

v_boxes = bound_box.read_table(image_b_boxes_df['bound_boxes'])
print_pretty(position_between_objects(v_boxes))
print_pretty(centroid_vbox_position_on_image(v_boxes))
area_vbox_position_on_image(v_boxes)
print_pretty(position_on_image_area(v_boxes))
