
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
        

    def predict(self, annotation):
        """
        predict the position given bounding boxes in the image.
        """

        for i in range(len(annotation)):
            bbox = annotation[i]['bbox']
            
            width = bbox['right'] - bbox['left']
            x = self.carWidth * self.fy / width
            
            if abs(bbox['left'] - self.cx) < abs(bbox['right'] - self.cx):
                h = bbox['left'] - self.cx
            else:
                h = bbox['right'] - self.cx
            
            v = bbox['bottom'] - self.cy
            y = h / v * self.cameraHeight

            # add the predicted position to the annotation
            annotation[i]['position'] = [x, y]

        return annotation
