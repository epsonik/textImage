import pandas as pd

from img_det import get_boxes, vbox_engine, draw_boxes
photo_filename = './IMAGES/dog.jpg'
photo_boxed_filename = './dog_boxed.jpg'
v_boxes, v_labels, v_scores = vbox_engine(photo_filename )
img_id = id(v_boxes)
draw_boxes(photo_filename, photo_boxed_filename, v_boxes, v_labels, v_scores)
image_b_boxes = pd.DataFrame(columns = ['img_id','xmin', 'ymin', 'xmax', 'ymax','label'])
for i in range(len(v_boxes)):
    box = v_boxes[i]
    xmin, ymin, xmax, ymax = box.get_coordinates()
    label = box.get_label()
    b_box = pd.DataFrame({'img_id':[img_id],
                          'xmin':[xmin],
                        'ymin':[ymin],
                        'xmax':[xmax],
                       'ymax':[ymax],
                          'label':[label]})
    image_b_boxes = image_b_boxes.append(b_box, ignore_index=True)

print(image_b_boxes)