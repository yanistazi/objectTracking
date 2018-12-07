from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import time
import cv2

# For DARBY (change the path to the one containing the video
path = "physics.MP4"
path_output = "video_output"
trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
#Instruction to create the bounding box:
'''
When you run the code, go on the video press 's' in order to create the bounding box with your mouse and
when you are satisfied press enter
'''
tracker = cv2.TrackerCSRT_create()
vs = cv2.VideoCapture(path)
fps = tracker

width = vs.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
height = vs.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
fourcc = cv2.cv2.VideoWriter_fourcc(*'MP4V')

out = cv2.VideoWriter(path_output,fourcc, 20.0, (int(width),int(height)))

while (vs.isOpened()):
    ret, frame = vs.read()

    if frame is None:
        break
    (H, W) = frame.shape[:2]
    (success, box) = tracker.update(frame)
    if success:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)

    info = [
        ("Tracker:", "CSRT"),
        ("Success?", "Yes" if success else "No"),
    ]

    for (i, (k, v)) in enumerate(info):
        text = "{}: {}".format(k, v)
        cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)



    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                               showCrosshair=True)
        tracker.init(frame, initBB)
        fps = FPS().start()
    out.write(frame)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

vs.release()
out.release()

