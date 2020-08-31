import json

from img_det import vbox_engine, draw_boxes, get_labels
from position_utils import calculate_centroid


def save_to_csv(v_boxes, photo_filename):
    image_b_boxes = {}
    image_b_boxes['bound_boxes'] = []
    for i in range(len(v_boxes)):
        box = v_boxes[i]
        xmin, ymin, xmax, ymax = box.get_coordinates()
        width = box.calculate_width()
        height = box.calculate_height()
        label = box.get_label()
        image_b_boxes['bound_boxes'].append({'img_id': img_id,
                              'XtopLeft': xmin,
                              'YtopLeft': ymin,
                              'XbottomRight': xmax,
                              'YbottomRight': ymax,
                              'Xcentroid': calculate_centroid(xmin, width),
                              'Ycentroid': calculate_centroid(ymin, height),
                              'area': box.calculate_area(),
                              'label': get_labels()[label]})

    photo_filename = photo_filename.replace('.jpg','.txt')
    with open(photo_filename, 'w') as outfile:
        json.dump(image_b_boxes, outfile)
    return image_b_boxes

photo_filename = './IMAGES/bicycle/COCO_train2014_000000294933.jpg'
photo_boxed_filename = './bicycle_boxed.jpg'
v_boxes, v_labels, v_scores, image_w, image_h = vbox_engine(photo_filename)
img_id = id(v_boxes)
draw_boxes(photo_filename, photo_boxed_filename, v_boxes, v_labels, v_scores)

print(save_to_csv(v_boxes, photo_filename))
