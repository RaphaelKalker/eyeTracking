import logging
import math
import numpy as np
import cv2

logger = logging.getLogger(__name__)

class blobDetector():
#    def __init__(self, minThresh, maxThresh, threshStep, filterByArea, minArea, maxArea, minDistBetweenBlobs):
    def __init__(self, params):

        # init all the params
        self.minThreshold = params.blob.minThreshold
        self.maxThreshold = params.blob.maxThreshold
        self.thresholdStep = params.blob.thresholdStep

        self.filterByArea = params.blob.filterByArea
        self.minArea = params.blob.minArea
        self.maxArea = params.blob.maxArea

        self.minDistBetweenBlobs = params.blob.minDistBetweenBlobs
        
        self.filterByCircularity = params.blob.filterByCircularity 
        self.minCircularity = params.blob.minCircularity
        self.maxCircularity = params.blob.maxCircularity

        self.filterByInertia = params.blob.filterByInertia 
        self.minInertiaRatio = params.blob.minInertiaRatio
        self.maxInertiaRatio = params.blob.maxInertiaRatio

        self.filterByConvexity = params.blob.filterByConvexity
        self.minConvexity = params.blob.minConvexity
        self.maxConvexity = params.blob.maxConvexity
        
    def detect(self, img):
        blobs = self.findBlobs(img)
        return blobs 

    def find_if_close(self, cnt1, cnt2):
        row1, row2 = cnt1.shape[0], cnt2.shape[0]
        for i in xrange(row1):
            for j in xrange(row2):
                dist = np.linalg.norm(cnt1[i]-cnt2[j])
                if abs(dist) < self.minDistBetweenBlobs :
                    return True
                elif i==row1-1 and j==row2-1:
                    return False

    def computeRadius(self, center, contour):
        dists = []
        for cnt_xy in contour:
            dists.append([center[0] - cnt_xy[0][0], center[1] - cnt_xy[0][1]])
        xy = np.mean(dists, 0)
        radius = math.sqrt(xy[0]**2 + xy[1]**2)
        return radius
    
    def computeCenter(self, M):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return [cx, cy] 

    def f_filterByInertia(self, M):
        den = math.sqrt( (2*M['mu11'])**2 + (M['mu20']-M['mu02'])**2 )
        eps = 1e-2
        if den > eps:
            cosmin = (M['mu20'] - M['mu02']) / float(den)
            sinmin = 2 * M['mu11'] / float(den)
            cosmax = -cosmin
            sinmax = -sinmin

            imin = 0.5*(M['mu20'] + M['mu02']) - 0.5*(M['mu20'] + M['mu02'])*cosmin - M['mu11']*sinmin
            imax = 0.5*(M['mu20'] + M['mu02']) - 0.5*(M['mu20'] + M['mu02'])*cosmax - M['mu11']*sinmax

            if imax == 0:
                return None

            ratio = imin / imax
        else:
            ratio = 1

        if (ratio < self.minInertiaRatio or ratio >= self.maxInertiaRatio):
            return None

        center_confidence = ratio * ratio
        return center_confidence 

    def f_filterByConvexity(self, contour):
        hull = cv2.convexHull(contour)
        area = cv2.contourArea(contour)
        hullArea = cv2.contourArea(hull)
        ratio = area/hullArea

        if (ratio < self.minConvexity or ratio >= self.maxConvexity):
            return None
        return True
    
    def f_filterByCircularity(self, M, contour):
        area = M['m00']
        perimeter = cv2.arcLength(contour, True)
        ratio = 4*math.pi*area / (perimeter * perimeter)
        if (ratio < self.minCircularity or ratio >= self.maxCircularity):
            return None
        return True

    def findBlobs(self, img):
        numSteps = (self.maxThreshold - self.minThreshold)/self.thresholdStep + 1
        thresholds = np.linspace(self.minThreshold, self.maxThreshold, numSteps, endpoint=True)

        contours = []
        for i in np.arange(numSteps):
            _, img_thresh = cv2.threshold(~img, thresholds[i], 255, cv2.THRESH_BINARY)
            img_contours, _ = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            print "threshold %i" % (thresholds[i])
            print "%i number of contours for threshold" % (len(img_contours))

            # filter the contours if needed
            for cnt in img_contours:
                M = cv2.moments(cnt)
                
                if M['m00'] == 0:
                    continue

                if self.filterByArea:
                    area = M['m00']
                    if (area < self.minArea or area > self.maxArea):
                        continue
                if self.filterByCircularity and self.f_filterByCircularity(M, cnt):
                        continue
                if self.filterByInertia and self.f_filterByInertia(M) is None:
                        continue
                if self.filterByConvexity and self.f_filterByConvexity(cnt) is None:
                        continue

                contours.append(cnt)

        # merge the centers from all the thresholded images by minDistBetweenBlobs
        LENGTH = len(contours)
        status = np.zeros((LENGTH,1))
        print "number contours to merge %i" % (LENGTH)

        for i,cnt1 in enumerate(contours):
            x = i    
            if i != LENGTH-1:
                for j,cnt2 in enumerate(contours[i+1:]):
                    x = x+1
                    dist = self.find_if_close(cnt1, cnt2)
                    if dist == True:
                        val = min(status[i],status[x])
                        status[x] = status[i] = val
                    else:
                        if status[x]==status[i]:
                            status[x] = i+1

        unified = []
        maximum = int(status.max())+1
        centers = []
        for i in xrange(maximum):
            pos = np.where(status==i)[0]
            if pos.size != 0:
                cont = np.vstack(contours[i] for i in pos)
                hull = cv2.convexHull(cont)

                #find center and radius of hull
                M = cv2.moments(hull)
                if M['m00'] == 0:
                    continue
                center = self.computeCenter(M)
                radius = self.computeRadius(center, cnt)
                centers.append(center)
                cv2.circle(img, (center[0], center[1]), int(radius),(0,0,255))
                cv2.circle(img, (center[0], center[1]), 3, (255,0, 0))
                unified.append(hull)
        return centers

#        cv2.imshow('image', img)
#        cv2.waitKey()
#        cv2.destroyAllWindows() 
