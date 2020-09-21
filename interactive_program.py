# import the necessary packages
import cv2
import numpy as np
import pandas as pd

from bound_box import Reading
from position_utils import centroid_vbox_position_on_image, area_vbox_position_on_image, print_pretty, \
    calculate_centroid


def _interactive_mode(image_path):
    image = cv2.imread(image_path)
    img_h, image_w, channels = image.shape

    def show_rectangles():
        for ref_point in ref_points:
            cv2.rectangle(image, ref_point[0], ref_point[1], ref_point[2], 2)
        cv2.imshow("image", image)

    def adj_x(corner):
        corner_l = list(corner)
        corner_l[0] += 5
        return tuple(corner_l)

    def unadj_x(corner):
        corner_l = list(corner)
        corner_l[0] -= 5
        return tuple(corner_l)

    def unadj_y(corner):
        corner_l = list(corner)
        corner_l[1] -= 5
        return tuple(corner_l)

    def adj_y(corner):
        corner_l = list(corner)
        corner_l[1] += 5
        return tuple(corner_l)

    clone = image.copy()
    cv2.namedWindow("image")

    ref_points = [[(0, 0), (30, 30), (0, 255, 0)]]
    actual_rectangle = ref_points[0]
    actual_rectangle_idx = 0
    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()
        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break
        elif key == ord("1"):
            actual_rectangle = ref_points[0]
            actual_rectangle_idx = 0
            print("You chose rectangle number 1.")
        elif key == ord("2"):
            actual_rectangle = ref_points[1]
            actual_rectangle_idx = 1
            print("You chose rectangle number 2.")
        elif key == ord("3"):
            actual_rectangle = ref_points[2]
            actual_rectangle_idx = 2
            print("You chose rectangle number 3.")
        elif key == ord("4"):
            actual_rectangle = ref_points[3]
            actual_rectangle_idx = 3
            print("You chose rectangle number 4.")
        elif key == ord("n"):
            color = list(np.random.random(size=3) * 256)
            ref_points.append([(0, 0), (30, 30), color])
            actual_rectangle = ref_points[-1]
            actual_rectangle_idx = len(ref_points) - 1
            print(ref_points)
            print(actual_rectangle_idx)
            # draw a rectangle around the region of interest
            print(ref_points)
            show_rectangles()
        elif key == ord("d"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_x(actual_rectangle[0])
            actual_rectangle[1] = adj_x(actual_rectangle[1])

            # draw a rectangle around the region of interest
            image = clone.copy()
            show_rectangles()
            print(ref_points)
        elif key == ord("w"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_y(actual_rectangle[0])
            actual_rectangle[1] = unadj_y(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        elif key == ord("s"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_y(actual_rectangle[0])
            actual_rectangle[1] = adj_y(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        elif key == ord("a"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_x(actual_rectangle[0])
            actual_rectangle[1] = unadj_x(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        # up arrow
        elif key == ord("i"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_y(actual_rectangle[0])
            actual_rectangle[1] = adj_y(actual_rectangle[1])
            image = clone.copy()
            # draw a rectangle around the region of interest
            show_rectangles()
        # down arrow
        elif key == ord("k"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_y(actual_rectangle[0])
            actual_rectangle[1] = unadj_y(actual_rectangle[1])
            image = clone.copy()
            show_rectangles()
        # right arrow
        elif key == ord("l"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = unadj_x(actual_rectangle[0])
            actual_rectangle[1] = adj_x(actual_rectangle[1])
            # draw a rectangle around the region of interest
            image = clone.copy()
            show_rectangles()
            print(ref_points)
        # left arrow
        elif key == ord("j"):
            ref_points[actual_rectangle_idx] = actual_rectangle

            actual_rectangle[0] = adj_x(actual_rectangle[0])
            actual_rectangle[1] = unadj_x(actual_rectangle[1])
            # draw a rectangle around the region of interest
            image = clone.copy()
            show_rectangles()
            print(ref_points)
        elif key == ord("y"):
            if ref_points.__len__() > 1:
                _calculate_pos(ref_points, image_w, img_h)
    # close all open windows
    cv2.destroyAllWindows()


def _calculate_pos(ref_points, image_w, image_h):
    v_boxes = list()
    for ref_point in ref_points:
        XtopLeft, YtopLeft = ref_point[0][0], ref_point[0][1]
        XbottomRight, YbottomRight = ref_point[1][0], ref_point[1][1]
        reading = Reading(11, XtopLeft, YtopLeft, XbottomRight, YbottomRight,
                          calculate_centroid(XtopLeft, image_w), calculate_centroid(YtopLeft,
                                                                                    image_h), None,
                          ref_points.index(ref_point))
        v_boxes.append(reading)

    # print_pretty(position_between_objects(v_boxes))
    centroid_vbox_position = centroid_vbox_position_on_image(v_boxes, image_w, image_h)
    print_pretty(centroid_vbox_position)
    area_vbox_position = area_vbox_position_on_image(v_boxes, image_w, image_h)
    print_pretty(area_vbox_position)
    orientation_pointer_dict_centroid = {}
    full = {}
    for box in centroid_vbox_position.keys():
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
        print(box, df.to_string())
    return full


_interactive_mode("bicycle_boxed.jpg")
