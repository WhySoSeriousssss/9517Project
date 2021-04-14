
class VelocityPredictor():
    """
    Used to predict the relative velocity of a vehicle to the camera
    """
    def __init__(self):
        self.distance_threshold = float('inf')
        self.min_interval = 0.05

    def predict(self, annotations):
        """
        predict the relative velocity given a set of position information of vehicles in the imagea
        """
        n_frames = len(annotations)

        annotation_prev = annotations[0]
        annotation_curr = annotations[-1]

        for i in range(len(annotation_curr)): # iterate over all bounding boxes in the last frame
            pos_curr = annotation_curr[i]['position']
            min_dist = float('inf')
            min_dist_id = -1

            for j in range(len(annotation_prev)):
                pos_prev = annotation_prev[j]['position']
                dist = (pos_curr[0] - pos_prev[0]) ** 2 + (pos_curr[1] - pos_prev[1]) ** 2
                if dist < min_dist:
                    min_dist = dist
                    min_dist_id = j
            print(pos_curr)
            print(annotation_prev[min_dist_id]['position'])

            if min_dist < self.distance_threshold:
                pos_prev = annotation_prev[min_dist_id]['position']
                interval = self.min_interval * (n_frames - 1)
                velocity = [(pos_curr[0] - pos_prev[0]) / interval, (pos_curr[1] - pos_prev[1]) / interval]
                annotation_curr[i]['velocity'] = velocity
            print('----------------------')

        return annotation_curr


    def predict2(self, annotations):
        n_frames = len(annotations)
        n_bboxes = len(annotations[-1]) # number of bboxes in the 40th frame
        flow = [[annotations[-1][i]] for i in range(n_bboxes)]

        for i in range(n_bboxes): # iterate over all bounding boxes in the 40th frame
            for j in range(n_frames - 2, -1, -1): # iterate over all previous frames
                bbox_curr = flow[i][-1]
                pos_curr = bbox_curr['position']

                bboxes_prev = annotations[j]

                min_dist = float('inf')
                min_dist_id = -1

                for k in range(len(bboxes_prev)): # compare with all bounding boxes in the previous frame
                    pos_prev = bboxes_prev[k]['position']
                    dist = (pos_curr[0] - pos_prev[0]) ** 2 + (pos_curr[1] - pos_prev[1]) ** 2
                    if dist < min_dist:
                        min_dist = dist
                        min_dist_id = k
                
                if min_dist_id == -1:
                    flow[i].append(flow[i][-1])
                else:
                    flow[i].append(bboxes_prev[min_dist_id])
        
        print(flow)
 
        # compute the average velocity of all vehicles in the 40th frame
        for i in range(n_bboxes):
            temp1 = []
            temp2 = []
            pos_curr = flow[i][0]['position']
            for j in range(1, n_frames):
                pos_prev = flow[i][j]['position']
                interval = self.min_interval * j
                temp1.append((pos_curr[0] - pos_prev[0]) / interval)
                temp2.append((pos_curr[1] - pos_prev[1]) / interval)
                        
            velocity = [sum(temp1) / len(temp1), sum(temp2) / len(temp2)]
            annotations[-1][i]['velocity'] = velocity
            print(temp1)
        return annotations[-1]


