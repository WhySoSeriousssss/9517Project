import cv2
import numpy as np


class YOLOv3CarDetector():
    """
    Car Detector implemented with pre-trained YOLOv3 on COCO dataset
    """
    def __init__(self):
        self.minBBoxSize = 310
        self.maxBBoxSize = float('inf')

        self.net = cv2.dnn.readNet("ObjectDetectionModels/YOLOv3/yolov3.weights", "ObjectDetectionModels/YOLOv3/yolov3.cfg")
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        
        self.confidenceThreshold = 0.5
        self.inScaleFactor = 0.00392
        
        with open("ObjectDetectionModels/YOLOv3/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
    
    def predict(self, img):
        """
        Predicts the cars in the image.
        """
        height, width = img.shape[0], img.shape[1]
        
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        # forward pass
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if class_id in [2, 5, 7] and confidence > 0.5: # class id 2, 5, 7 stands for car, bus, and truck
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
        
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
        
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # non-max suppression
        res = []
        class_map = {2:'car', 5:'bus', 7:'truck'}
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                if self.minBBoxSize < w * h < self.maxBBoxSize:
                    res.append({
                        'bbox': {
                            'top': y,
                            'right': x + w,
                            'bottom': y + h,
                            'left': x
                        },
                        'class':class_map[class_ids[i]]
                    })
        return res
                
        
        
class MobileNetSSDCarDetector():
    """
    Car Detector implemented with pre-trained MobileNet SSD
    """
    def __init__(self):
        self.inWidth = 600
        self.inHeight = 600
        self.inScaleFactor = 0.007843
        self.net = cv2.dnn.readNetFromCaffe("ObjectDetectionModels/MobileNetSSD_deploy.prototxt", "ObjectDetectionModels/MobileNetSSD_deploy.caffemodel")
        self.confidenceThreshold = 0.15

    def predict(self, img):
        """
        Predicts the cars in the image.
        """
        res = []
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (600, 600)), self.inScaleFactor, (self.inWidth, self.inHeight))
        self.net.setInput(blob, "data")
        detection = self.net.forward("detection_out")
        detectionMat = np.resize(detection, (detection.shape[2], detection.shape[3]))
        for i in range(detectionMat.shape[0]):
            # 6 equal to bus 7 equal to car
            if detectionMat[i,1] == 7 or detectionMat[i, 1] == 6:
                confidence = detectionMat[i, 2]
                if confidence >= self.confidenceThreshold:
                    res.append({
                        'bbox': {
                            'top': detectionMat[i, 4] * img.shape[0],
                            'right': detectionMat[i, 5] * img.shape[1],
                            'bottom': detectionMat[i, 6] * img.shape[0],
                            'left': detectionMat[i, 3] * img.shape[1]
                        }
                    })
        return res
