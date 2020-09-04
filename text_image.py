import json

from img_det import get_labels
from position_utils import calculate_centroid


def save_to_csv(v_boxes, photo_filename):
    image_b_boxes = {}
    img_id = id(v_boxes)
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
    photo_filename='./IMAGES/{}'.format(photo_filename)
    photo_filename = photo_filename.replace('.jpg', '.txt')
    with open(photo_filename, 'w') as outfile:
        json.dump(image_b_boxes, outfile)
    return image_b_boxes, photo_filename
