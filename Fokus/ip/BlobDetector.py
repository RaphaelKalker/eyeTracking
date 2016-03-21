import logging
import math
import numpy as np
import cv2
import CV_
import BlobCenter

logger = logging.getLogger(__name__)

class BlobDetector():
    def __init__(self, image, mask, params, eyeball):

        self.image = image
        self.mask = mask
        self.eyeBall = eyeball

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

        self.minRepeatability = params.blob.minRepeatability
        
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
            dists.append(np.linalg.norm([center[0] - cnt_xy[0][0], center[1] - cnt_xy[0][1]]))

        dists.sort()
        radius = dists[(len(dists)-1)/2]/2.0 + dists[(len(dists)/2)]/2.0
        
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
                return True

            ratio = imin / imax
        else:
            ratio = 1

        if (ratio < self.minInertiaRatio or ratio >= self.maxInertiaRatio):
            return True

        center_confidence = ratio * ratio
        return float(center_confidence)
    

    def f_filterByConvexity(self, contour):
        hull = cv2.convexHull(contour)
        area = cv2.contourArea(contour)
        hullArea = cv2.contourArea(hull)
        ratio = area/hullArea

        if (ratio < self.minConvexity or ratio >= self.maxConvexity):
            return True
        return False
    
    def f_filterByCircularity(self, M, contour):
        area = M['m00']
        perimeter = cv2.arcLength(contour, True)
        ratio = 4*math.pi*area / (perimeter * perimeter)
        if (ratio < self.minCircularity or ratio >= self.maxCircularity):
            return True 
        return False
    
    def f_filterByArea(self, M):
        area = M['m00']
        if (area < self.minArea or area > self.maxArea):
            return True 
        return False

    def detect(self):
        numSteps = (self.maxThreshold - self.minThreshold)/self.thresholdStep + 1
        thresholds = np.linspace(self.minThreshold, self.maxThreshold, numSteps, endpoint=True)

        centers = []
        keypoints = []
        newCenters = []
        for thresh in thresholds:
            currentCenters = self.findBlobs(thresh)

            for curCenter in currentCenters:
                isNew = True
                for j in np.arange(len(centers)):
                    curPt = curCenter.center
                    midIndex = len(centers[j])/2
                    centerPt = centers[j][midIndex].center
                    diff = (curPt[0] - centerPt[0], curPt[1] - centerPt[1])
                    dist = np.linalg.norm(diff)
                    isNew = dist >= self.minDistBetweenBlobs and dist >= centers[j][midIndex].radius and dist >= curCenter.radius

                    if not isNew:
                        centers[j].append(curCenter)

                        k = len(centers[j]) - 1
                        while( k > 0 and centers[j][k].radius < centers[j][k-1].radius):
                            centers[j][k] = centers[j][k-1]
                            k -= 1
                        centers[j][k] = curCenter
                        break 
                if isNew:
                    newCenters.append([curCenter])
            centers = centers + newCenters

        for i in np.arange(len(centers)):
            if (len(centers[i]) < self.minRepeatability):
                continue

            sumPoint = np.asarray([0.0,0.0])
            normalizer = 0.0
            for j in np.arange(len(centers[i])):
                x = centers[i][j].confidence * centers[i][j].center[0]
                y = centers[i][j].confidence * centers[i][j].center[1]
                sumPoint += np.asarray([x,y])           
                normalizer += centers[i][j].confidence

            sumPoint  = sumPoint * ( 1/ float(normalizer))
            radius = centers[i][len(centers[i])/2].radius * 2.0
            keyPt = BlobCenter.BlobCenter( (int(sumPoint[0]), int(sumPoint[1])), radius, 1)
            keypoints.append(keyPt)

        return keypoints 

    def findBlobs(self, thresh):

        _, img_thresh = cv2.threshold(self.image, thresh, 255, cv2.THRESH_BINARY)
        img_contours, _ = CV_.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        for cnt in img_contours:
            M = cv2.moments(cnt)
            
            if M['m00'] == 0:
                continue

            if self.filterByArea and self.f_filterByArea(M):
                    continue
            if self.filterByCircularity and self.f_filterByCircularity(M, cnt):
                    continue

            confidence = 1
            if self.filterByInertia:
                ret = self.f_filterByInertia(M)
                if isinstance(ret, (int)):
                    continue
                confidence = ret

            if self.filterByConvexity and self.f_filterByConvexity(cnt):
                    continue

            center = self.computeCenter(M)
            radius = self.computeRadius(center, cnt)

            blobCenter = BlobCenter.BlobCenter(center, radius, confidence)
            yield blobCenter 




    def findReflectionPoints(self):

        # detector = cv2.SimpleBlobDetector_create(self.params.blob)

        keypoints = self.detect() 
        validKP = []

        for keyPt in keypoints:
            x = keyPt.center[0]
            y = keyPt.center[1]
            size = '%.2f' % keyPt.radius


            # Filter out key points according to mask
            # We do this because the mask passed into the Simple Blob Detector doesn't work
            # WARNING orientation is reverse so use y, x coordinates
            if  self.mask[y,x] == 255:
                # logging.debug('REFLECTION: x={} y={} size={}'.format(x,y, size))
                self.eyeBall.addReflection(y,x, size)
                validKP.append((x,y,size))
            else:
                # logger.debug('IGNORED: x={} y={} size={}'.format(x,y, size))
                pass

        # if  FeatureDebug.SHOW_CV2_IMAGES and FeatureDebug.DEBUG_BLOB_DETECTOR:
        #     mask_with_keypoints = cv2.drawKeypoints(self.mask, keypoints, None, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #     im_with_keypoints = cv2.drawKeypoints(self.image, validKP, None, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #     ImageHelper.showImage('Blob Starting Image', self.image)
        #     ImageHelper.showImage('Mask with Points', mask_with_keypoints)
        #     ImageHelper.showImage('Mask applied', cv2.bitwise_and(im_with_keypoints,im_with_keypoints, mask=self.mask))

        return validKP
