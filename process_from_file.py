import pandas as pd

import BoundBox
from position_utils import calculate_position

image_b_boxes_df = pd.read_csv("dog.csv")
v_boxes = BoundBox.read_table(image_b_boxes_df)
for i in range(len(v_boxes)):
    boxA = v_boxes[i]
    for b in range(len(v_boxes)):
        boxB = v_boxes[b]
        if i is not b:
            print(calculate_position(boxA, boxB), )
