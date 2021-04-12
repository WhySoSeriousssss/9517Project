
class VelocityPredictor():
    """
    Used to predict the relative velocity of a vehicle to the camera
    """

    def predict(self, annotations):
        """
        predict the relative velocity given a set of position information of vehicles in the imagea
        """
        annotation_prev = annotations[0]
        annotation_curr = annotations[1]

        for i in range(len(annotation_curr)):
            distance_threshold = 3
            interval = 0.05
            pos = annotation_curr[i]['position']
            min_dist = float('inf')
            min_dist_id = -1

            for j in range(len(annotation_prev)):
                pos_0 = annotation_prev[j]['position']
                dist = (pos[0] - pos_0[0]) ** 2 + (pos[1] - pos_0[1]) ** 2
                if dist < min_dist:
                    min_dist = dist
                    min_dist_id = j
            print(pos)
            print(annotation_prev[min_dist_id]['position'])

            if min_dist < distance_threshold:
                pos_0 = annotation_prev[min_dist_id]['position']
                velocity = [(pos[0] - pos_0[0]) / interval, (pos[1] - pos_0[1]) / interval]
                annotation_curr[i]['velocity'] = velocity
            print('----------------------')

        return annotation_curr