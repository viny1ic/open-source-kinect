import cv2
import numpy as np
import pyautogui
import face_removal

pyautogui.FAILSAFE=False

def getROI(frame):
    frame = face_removal.remove_face(frame)

    height = frame.shape[0]
    width = frame.shape[1]

    x1 = int((80 / 100) * width)
    y1 = int((10 / 100) * height)
    x2 = int((10 / 100) * width)
    y2 = int((80 / 100) * height)

    start_point = (x1, y1)
    end_point = (x2, y2)

    return start_point, end_point


def preprocess(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_skin, upper_skin, cv2.THRESH_BINARY)
    mask = cv2.dilate(mask, SE, iterations=4)
    mask_c = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, SE)  # Dilation followed by Erosion
    mask_c = cv2.morphologyEx(mask_c, cv2.MORPH_CLOSE, SE)
    mask_c = cv2.morphologyEx(mask_c, cv2.MORPH_CLOSE, SE)
    dilation = cv2.dilate(mask_c, (11, 11), iterations=8)

    return dilation


def mouse_control(x, y, width, height):
    x_val = (SX // width) * x
    y_val = (SY // height) * y
    pyautogui.moveTo(x_val, y_val)


SX, SY = pyautogui.size()                           # Gets the size of screen
lower_skin = np.array([0, 20, 0], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)                     # HSV UpperBound
SE = np.ones((3, 3), np.uint8)           	                    # will be used for dilation and erosion
capture = cv2.VideoCapture(0)

while capture.isOpened():
    var, frame = capture.read()
    frame = cv2.flip(frame, 1)

    start_point, end_point = getROI(frame)

    frame = cv2.rectangle(frame, start_point, end_point, (0, 0, 255), 1)
    frame = frame[start_point[1]: end_point[1], end_point[0]: start_point[0]]

    frame_copy = frame.copy()
    start_point = (frame.shape[1] - 40, 0)
    end_point = (40, frame.shape[0] - 90)
    frame_copy = frame_copy[start_point[1]: end_point[1], end_point[0]: start_point[0]]

    width = frame_copy.shape[1]
    height = frame_copy.shape[0]

    mask = preprocess(frame)

    contours, heir = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find contours
    cnt = max(contours, key=lambda x: cv2.contourArea(x))                               # find contour with maximum area
    hull = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull)

    x, y = 10000, 10000
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt[s][0])
        if start[1] <= y:
            x = start[0]
            y = start[1]

    cv2.circle(frame_copy, (x-5, y-3), 5, (255, 255, 255), -1)
    cv2.circle(frame, (x, y), 5, (255, 255, 255), -1)
    mouse_control(x, y, width, height)

    cv2.imshow('binary', mask)
    cv2.imshow('Mouse_Pad', frame_copy)
    cv2.imshow('ori', frame)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

capture.release()