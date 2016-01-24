import cv2
import sys
import glob

global pt_x 
global pt_y 

def clickPoint(event, x, y, flags, param):
    global pt_x, pt_y
    if event == cv2.EVENT_LBUTTONDOWN:
        #param is the image array
        clone = param.copy()
        cv2.circle(clone, (x,y), 10, (0,255,0), 1)
        offset = 10 
        cv2.line(clone,(x - offset, y - offset),(x + offset, y + offset),(0,255,0),1)
        cv2.line(clone,(x + offset, y - offset),(x - offset, y + offset),(0,255,0),1)
        cv2.imshow('img', clone)
        pt_x, pt_y = x,y
        print (pt_x, pt_y)

def annotate(img_name):
    global pt_x, pt_y
    pt_x = -1
    pt_y = -1

    img = cv2.imread(img_name)
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', clickPoint, img)

    # display image and wait for a keypress
    cv2.imshow('img', img)
    k = cv2.waitKey(0) & 0xFF
    
    # press n or spacebar to go to the next photo
    if k == ord('n') or k == 32:
        print (img_name, pt_x, pt_y)
        cv2.destroyAllWindows()
        return

if __name__ == "__main__":
    fs = glob.glob(sys.argv[1] + "*")
    for fname in fs:
        annotate(fname)
