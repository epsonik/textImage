import io
import json

# simple_demo.py
import pandas as pd
import xlsxwriter
from PIL import Image

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
    centroid_vbox_position = centroid_vbox_position_on_image(v_boxes, image_w, image_h)
    print_pretty(centroid_vbox_position)
    area_vbox_position = area_vbox_position_on_image(v_boxes)
    print_pretty(area_vbox_position)
    create_df(centroid_vbox_position, area_vbox_position)

    return full, photo_boxed_filename


def create_df(c_vbox_position, a_vbox_position):
    full = {}
    orientation_pointer_dict_centroid = {}
    for box in c_vbox_position.keys():
        print(box)
    orientation_pointer_dict_centroid['name'] = [*c_vbox_position[box]]
    t = {}
    t['center'] = []
    area = {}
    area['area'] = []
    for orientation_pointer in c_vbox_position[box].keys():
        t['center'].append(c_vbox_position[box][orientation_pointer]['certainty_factor'])
        area['area'].append(a_vbox_position[box][orientation_pointer]['certainty_factor'])
    df = pd.DataFrame({'position_on_image'.upper(): [*c_vbox_position[box]],
                       'centeroid_method_certainty_factor'.upper(): t['center'],
                       'area_method_certainty_factor'.upper(): area['area']})
    full[box] = df
    return full


def create_excel(box_df, input_filename_full_path, photo_boxed_filename, report_file_name):
    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(report_file_name)
    worksheet = workbook.add_worksheet('images')

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 30)

    # Insert an image.
    worksheet.write('A2', 'Original photo:')

    def get_resized_image_data(file_path, bound_width_height):
        # get the image and resize it
        im = Image.open(file_path)
        im.thumbnail(bound_width_height, Image.ANTIALIAS)  # ANTIALIAS is important if shrinking

        # stuff the image data into a bytestream that excel can read
        im_bytes = io.BytesIO()
        im.save(im_bytes, format='PNG')
        return im_bytes

    bound_width_height = (480, 480)
    image_data = get_resized_image_data(input_filename_full_path, bound_width_height)
    im = Image.open(image_data)
    im.seek(0)
    worksheet.insert_image('B2', input_filename_full_path, {'image_data': image_data})

    # Insert an image.
    worksheet.write('A20', 'Photo with boxes:')
    bound_width_height = (600, 600)
    image_data = get_resized_image_data(photo_boxed_filename, bound_width_height)
    im = Image.open(image_data)
    im.seek(0)
    worksheet.insert_image('B20', photo_boxed_filename, {'image_data': image_data})
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
