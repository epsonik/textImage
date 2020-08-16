import pandas as pd

from img_det import vbox_engine, draw_boxes, get_labels
from position_utils import calculate_centroid

photo_filename = './IMAGES/dog.jpg'
photo_boxed_filename = './dog_boxed.jpg'
v_boxes, v_labels, v_scores = vbox_engine(photo_filename)
img_id = id(v_boxes)
draw_boxes(photo_filename, photo_boxed_filename, v_boxes, v_labels, v_scores)
columns = ['img_id', 'XtopLeft', 'YtopLeft', 'XbottomRight', 'YbottomRight', 'Xcentroid', 'Ycentroid', 'area', 'label']
image_b_boxes = pd.DataFrame(columns=columns)

for i in range(len(v_boxes)):
    box = v_boxes[i]
    xmin, ymin, xmax, ymax = box.get_coordinates()
    width = box.calculate_width()
    height = box.calculate_height()
    label = box.get_label()
    b_box = pd.DataFrame({'img_id': [img_id],
                          'XtopLeft': [xmin],
                          'YtopLeft': [ymin],
                          'XbottomRight': [xmax],
                          'YbottomRight': [ymax],
                          'Xcentroid': [calculate_centroid(xmin, width)],
                          'Ycentroid': [calculate_centroid(ymin, height)],
                          'area': [box.calculate_area()],
                          'label': [get_labels()[label]]})
    image_b_boxes = image_b_boxes.append(b_box, ignore_index=True)
image_b_boxes.to_csv("dog.csv", index=False)
print(image_b_boxes)
