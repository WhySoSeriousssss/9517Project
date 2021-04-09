import cv2
import json
import os.path
from pathlib import Path


# absolute path of the dataset
project_folder = Path(__file__).parent.absolute()
velocity_folder = Path('dataset/velocity')
lane_folder = Path('dataset/lane')


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
        path_annotation = project_folder / velocity_folder / f'{folder}/annotation.json'
    else: # folder is train/test
        path_img = project_folder / velocity_folder / f'{folder}/clips/{id}/imgs/040.jpg'
        path_annotation = project_folder / velocity_folder / f'{folder}/clips/{id}/annotation.json'
    
    #print(path_img)
    # read the image
    img = cv2.imread(str(path_img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # add annotation
    if annotation:
        # load the annotation file
        with open(path_annotation) as file:
            # parse json file
            annotation = json.load(file)

        if folder == 'supp':
            # extract bboxs
            bboxs = annotation[id - 1]['bbox']
            # draw bounding boxes
            for bbox in bboxs:
                cv2.rectangle(img, (int(bbox['left']), int(bbox['top'])), (int(bbox['right']), int(bbox['bottom'])), \
                              color=(0, 255, 0), thickness=2)
        
        else: # folder is train/test
            # draw annoatations
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



def crop_cars(folder, id):
    """
    crop out the cars in the image
    """

    # invalid folder
    if folder not in ['supp', 'test', 'train']:
        return None

    if folder == 'supp':
        path_img = project_folder / velocity_folder / f'{folder}/supp_img/{id:04d}.jpg'
        path_annotation = project_folder / velocity_folder / f'supp/annotation.json'
    else:
        path_img = project_folder / velocity_folder / f'{folder}/clips/{id}/imgs/040.jpg'
        path_annotation = project_folder / velocity_folder / f'{folder}/clips/{id}/annotation.json'

    # read the image
    img = cv2.imread(str(path_img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # load the annotation file
    with open(path_annotation) as file:
        # parse json file
        annotation = json.load(file)

    res = []

    # extract bboxs
    if folder == 'supp':
        bboxs = annotation[id - 1]['bbox']
        for bbox in bboxs:
            res.append(img[int(bbox['top']):int(bbox['bottom']), int(bbox['left']):int(bbox['right'])].copy())
    
    else:
        for a in annotation:
            bbox = a['bbox']
            res.append(img[int(bbox['top']):int(bbox['bottom']), int(bbox['left']):int(bbox['right'])].copy())

    return res


