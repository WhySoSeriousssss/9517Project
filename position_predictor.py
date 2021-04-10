import cv2
import numpy as np


class PositionPredictor():
    """
    Used to predict the relative position of a vehicle to the camera
    """
    def __init__(self):
        # camera parameters
        self.fx = 714.1526
        self.fy = 710.3725
        self.cx = 713.85
        self.cy = 327.0
        self.cameraHeight = 1.8

        # average car width
        self.carWidth = 2.1
        

    def predict(self, img, bboxes, vis=True):
        """
        predict the position given bounding boxes in the image
        """
        img_copy = img.copy()
        positions = []

        for bbox in bboxes:
            xTopLeft = bbox[0] * img.shape[1]
            yTopLeft = bbox[1] * img.shape[0]
            xBottomRight = bbox[2] * img.shape[1]
            yBottomRight = bbox[3] * img.shape[0]

            
            width = xBottomRight - xTopLeft
            x = self.carWidth * self.fy / width
            
            if abs(xTopLeft - self.cx) < abs(xBottomRight - self.cx):
                h = xTopLeft - self.cx
            else:
                h = xBottomRight - self.cx
            
            v = yBottomRight - self.cy
            y = h / v * self.cameraHeight


            if vis:
                cv2.rectangle(img_copy, (int(xTopLeft), int(yTopLeft)), (int(xBottomRight), int(yBottomRight)), (0, 255, 0), 2)
                cv2.putText(
                    img_copy, f'pos:({x:.2f}, {y:.2f})m', 
                    (int(xTopLeft), int(yTopLeft) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_8
                )

            positions.append((x, y))

        if vis:
            return positions, img_copy
        else:
            return positions