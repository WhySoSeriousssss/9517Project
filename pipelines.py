import util
import numpy as np


class VelocityPipeline():
    def __init__(self, car_detector, position_predictor, velocity_predictor):
        self.car_detector = car_detector
        self.position_predictor = position_predictor
        self.velocity_predictor = velocity_predictor

    def run(self, folder, img_id, compare=False):
        """
        Run the pipeline to do prediction.
        compare: if True, the ground truth image will be concatnated to the output image
        Returns the predicted annotation, along with the result image
        """
        annotations = []
        n_frames = 10
        for i in range(n_frames):
            img = util.read_velocity_image(folder, img_id, frame=i+41-n_frames, annotation=False)

            # predict bounding boxes
            annotation = self.car_detector.predict(img)
            
            # predict positions
            annotation = self.position_predictor.predict(annotation)

            annotations.append(annotation)

        # predict velocity
        out_annotation = self.velocity_predictor.predict2(annotations)


        # draw annotation
        out_img = util.read_velocity_image(folder, img_id, frame=40, annotation=False)
        out_img = util.draw_annotation(out_img, out_annotation)

        # concat the ground truth to the output image
        if compare:
            gt = util.read_velocity_image(folder, img_id, annotation=True)
            out_img = np.concatenate((gt, out_img), axis=1)

        return out_annotation, out_img


    def checkIntermediateOutput(self, folder, img_id, frame=40):
        img = util.read_velocity_image(folder, img_id, frame=frame, annotation=False)
        annotation = self.car_detector.predict(img)
        annotation = self.position_predictor.predict(annotation)
        img = util.draw_annotation(img, annotation)
        return img