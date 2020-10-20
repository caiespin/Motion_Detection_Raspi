import imutils
import cv2

def motion_detection_background_substraction(background, frame, min_area_threshold, debug=False):
    motion = False
    max_area = 0
    min_area = 0
    # compute the absolute difference between the current frame and background
    absolute_difference = cv2.absdiff(background, frame)
    frame_binary = cv2.threshold(absolute_difference, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    frame_binary = cv2.dilate(frame_binary, None, iterations=2)
    contours = cv2.findContours(frame_binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    areas = []

    # loop over the contours
    for contour in contours:
        areas.append(cv2.contourArea(contour))
    
    if areas:
        max_area = max(areas)
        min_area = min(areas)

    if max_area > min_area_threshold:
        motion = True

    if debug:
        cv2.imshow("Contours", frame_binary)
        cv2.imshow("Frame Delta", absolute_difference)

    return (motion, min_area, max_area)