import cv2
import json
from pathlib import Path

project_folder = Path()
velocity_folder = Path('dataset/velocity')

def read_velocity_image(folder, id, annotation=False):
    """
    Reads a certain image from the velocity dataset. Adds annotations if needed.
    If folder is 'test' or 'train', read the last frame of the clip.
    """
    
    # invalid folder
    if folder not in ['supp', 'test', 'train']:
        return None
    
    if folder == 'supp':
        path_img = project_folder / velocity_folder / f'{folder}/supp_img/{id:04d}.jpg'
    else: # folder is train/test
        path_img = project_folder / velocity_folder / f'{folder}/clips/{id}/imgs/040.jpg'
    
    print(path_img)
    # read the image
    img = cv2.imread(str(path_img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # add annotation
    if annotation:
        if folder == 'supp':
            path_annotation = project_folder / velocity_folder / f'{folder}/annotation.json'
            # load the annotation file
            with open(path_annotation) as file:
                # parse json file and extract bboxs
                annotation = json.load(file)
                bboxs = annotation[id - 1]['bbox']
                # draw bounding boxes
                for b in bboxs:
                    cv2.rectangle(img, (int(b['left']), int(b['top'])), (int(b['right']), int(b['bottom'])), \
                                  color=(0, 255, 0), thickness=2)
        
        else: # folder is train/test
            path_annotation = project_folder / velocity_folder / f'{folder}/clips/{id}/annotation.json'
            # load the annotation file
            with open(path_annotation) as file:
                # parse json file and extract bboxs
                annotation = json.load(file)
                for a in annotation:
                    bbox = a['bbox']
                    # draw bounding boxes
                    cv2.rectangle(img, (int(bbox['left']), int(bbox['top'])), (int(bbox['right']), int(bbox['bottom'])), \
                                  color=(0, 255, 0), thickness=2) 
                    if folder == 'train':
                        vel, pos = a['velocity'], a['position']
                        # put velocity and position labels
                        cv2.putText(img, f'pos:({pos[0]:.2f}, {pos[1]:.2f})m', \
                                    (int(bbox['left']), int(bbox['top']) - 10), \
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_8)
                        cv2.putText(img, f'v:({vel[0]:.2f}, {vel[1]:.2f})m/s', \
                                    (int(bbox['left']), int(bbox['top']) - 22), \
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_8)
					            
    return img