import json

import bound_box
from position_utils import position_on_image, position_between_objects, AreaMethod, vbox_position


def print_pretty(raw_json):
    print(json.dumps(raw_json, indent=4, sort_keys=True))

with open('./IMAGES/dog.txt') as json_file:
    image_b_boxes_df = json.load(json_file)

# # print_pretty(image_b_boxes_df['bound_boxes'])
v_boxes = bound_box.read_table(image_b_boxes_df['bound_boxes'])
# # print(centroid_rectangle().get_coordinates())
# print_pretty(position_on_image(v_boxes))
# print_pretty(position_between_objects(v_boxes))
# print_pretty(vbox_position(v_boxes))
vbox_position(v_boxes)