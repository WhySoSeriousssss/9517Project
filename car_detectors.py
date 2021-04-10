import cv2
import numpy as np

## MobileNet SSD car detector
class MobileNetSSDCarDetector():
    def __init__(self):
        self.inWidth = 600
        self.inHeight = 600
        self.whRatio = 1
        self.inScaleFactor = 0.007843
        self.net = cv2.dnn.readNetFromCaffe("car detector/MobileNetSSD_deploy.prototxt", "car detector/MobileNetSSD_deploy.caffemodel")
        # set threshold
        self.confidenceThreshold = 0.15

    def predict(self, img):
        """
        Predicts the cars in the image. Returns a list of bounding boxes.
        Each bounding box is a tuple formed as (xTopLeft, yTopLeft, xBottomRight, yBottomRight), normalized to (0, 1)
        """
        bboxes = []
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (600, 600)), self.inScaleFactor, (self.inWidth, self.inHeight))
        self.net.setInput(blob, "data")
        detection = self.net.forward("detection_out")
        detectionMat = np.resize(detection, (detection.shape[2], detection.shape[3]))
        for i in range(detectionMat.shape[0]):
            # 6 equal to bus 7 equal to car
            if detectionMat[i,1] == 7 or detectionMat[i, 1] == 6:
                confidence = detectionMat[i, 2]
                if confidence >= self.confidenceThreshold:
                    bboxes.append(tuple(detectionMat[i, 3:7]))
        return bboxes
