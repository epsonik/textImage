# import the necessary packages
import cv2
import numpy as np

image = cv2.imread("bicycle_boxed.jpg")
height, width, channels = image.shape


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

# close all open windows
cv2.destroyAllWindows()
