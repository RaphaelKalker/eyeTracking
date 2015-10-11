import numpy as np
import cv2


class FacetimeCam(object):

    def __init__(self):
        self.name = "RAPH"

    @staticmethod
    def doItLive():

        cap = cv2.VideoCapture(0)

        x, y, h, w = (493, 305, 125, 90)

        while (True):

            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

            img = np.zeros((512, 512, 3), np.uint8)

            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('frameee', gray)

            # cv2.imshow('frameee', gray)

            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        FacetimeCam.clean(cap)

    @staticmethod
    def clean(capVid):
        capVid.release()
        cv2.destroyAllWindows()





        # http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
