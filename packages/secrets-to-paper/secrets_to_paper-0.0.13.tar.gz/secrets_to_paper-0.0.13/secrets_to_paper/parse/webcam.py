#!/usr/local/bin/python

import pyzbar.pyzbar as pyzbar # type: ignore
import numpy as np
import cv2


def get_code_parts(capture_device):

    # get the webcam:
    cap = cv2.VideoCapture(capture_device)

    cap.set(3, 640)
    cap.set(4, 480)
    # 160.0 x 120.0   # 176.0 x 144.0   # 320.0 x 240.0   # 352.0 x 288.0
    # 640.0 x 480.0   # 1024.0 x 768.0  # 1280.0 x 1024.0

    font = cv2.FONT_HERSHEY_SIMPLEX

    while cap.isOpened():

        ret, frame = cap.read()

        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # get all qr codes from the frame
        decodedObjects = pyzbar.decode(im)

        for decodedObject in decodedObjects:
            points = decodedObject.polygon

            # If the points do not form a quad, find convex hull
            if len(points) > 4:
                hull = cv2.convexHull(
                    np.array([point for point in points], dtype=np.float32)
                )
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            # Number of points in the convex hull
            n = len(hull)
            # Draw the convext hull
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

            x = decodedObject.rect.left
            y = decodedObject.rect.top

            barCode = str(decodedObject.data)
            cv2.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
