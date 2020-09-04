import json

# simple_demo.py
import pandas as pd
import xlsxwriter

import bound_box
from img_det import draw_boxes, vbox_engine
from position_utils import print_pretty, centroid_vbox_position_on_image, area_vbox_position_on_image
from text_image import save_to_csv


def create_report(input_filename):
    photo_boxed_filename = './IMAGES/{}'.format(input_filename.replace('.jpg', '_boxed.jpg'))
    v_boxes, v_labels, v_scores, image_w, image_h = vbox_engine('./IMAGES/{}'.format(input_filename))
    draw_boxes('./IMAGES/{}'.format(input_filename), photo_boxed_filename, v_boxes, v_labels, v_scores)
    image_b_boxes, photo_filename_boxed_csv = save_to_csv(v_boxes, input_filename)
    with open(photo_filename_boxed_csv) as json_file:
        image_b_boxes_df = json.load(json_file)

    v_boxes = bound_box.read_table(image_b_boxes_df['bound_boxes'])
    # print_pretty(position_between_objects(v_boxes))
    centroid_vbox_position = centroid_vbox_position_on_image(v_boxes)
    print_pretty(centroid_vbox_position)
    area_vbox_position = area_vbox_position_on_image(v_boxes)
    print_pretty(area_vbox_position)
    orientation_pointer_dict_centroid = {}
    full = {}
    for box in centroid_vbox_position.keys():
        print(box)
        orientation_pointer_dict_centroid['name'] = [*centroid_vbox_position[box]]
        t = {}
        t['center'] = []
        area = {}
        area['area'] = []
        for orientation_pointer in centroid_vbox_position[box].keys():
            t['center'].append(centroid_vbox_position[box][orientation_pointer]['certainty_factor'])
            area['area'].append(area_vbox_position[box][orientation_pointer]['certainty_factor'])
        df = pd.DataFrame({'position_on_image'.upper(): [*centroid_vbox_position[box]],
                           'centeroid_method_certainty_factor'.upper(): t['center'],
                           'area_method_certainty_factor'.upper(): area['area']})
        full[box] = df
    return full, photo_boxed_filename


def create_excel(box_df, input_filename_full_path, photo_boxed_filename, report_file_name):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(report_file_name)
    worksheet = workbook.add_worksheet('images')

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 30)

    # Insert an image.
    worksheet.write('A2', 'Original photo:')
    worksheet.insert_image('B2', input_filename_full_path, {'x_scale': 2, 'y_scale': 2})

    # Insert an image.
    worksheet.write('A20', 'Photo with boxes:')
    worksheet.insert_image('B20', photo_boxed_filename)
    worksheet = workbook.add_worksheet('data')
    def write_data_frame():
        i = 0
        for box in box_df.keys():
            worksheet.write(i, 0, box)
            for idx, col in enumerate(box_df[box].columns, 1):
                worksheet.write(i + 1, idx, col)
                for index, value in box_df[box][col].items():
                    worksheet.write(i + 2 + index, idx, value)
            i = i + len(box_df[box]) + 3
    write_data_frame()
    workbook.close()


input_filename = 'bicycle/COCO_train2014_000000344067.jpg'
full, photo_boxed_filename = create_report(input_filename)
input_filename_full_path = './IMAGES/{}'.format(input_filename)
create_excel(full, input_filename_full_path, photo_boxed_filename, 'report.xlsx')
