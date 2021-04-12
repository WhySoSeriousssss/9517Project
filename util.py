import cv2
import json
import os.path
from pathlib import Path


# absolute path of the dataset
project_folder = Path(__file__).parent.absolute()
velocity_folder = Path('dataset/velocity')
lane_folder = Path('dataset/lane')


def draw_annotation(img, annotation):
    """
    draw annotation to the copy of the image.
    img: the original image
    annotation: the json-formatted annotation
    """
    img_copy = img.copy()
    for item in annotation:
        ## draw bounding boxes
        if 'bbox' in item.keys():
            bbox = item['bbox']
            cv2.rectangle(
                img_copy, (int(bbox['left']), int(bbox['top'])), (int(bbox['right']), int(bbox['bottom'])), 
                color=(0, 255, 0), thickness=2
            )

        ## put position text
        if 'position' in item.keys():
            pos = item['position']
            cv2.putText(
                img_copy, f'pos:({pos[0]:.2f}, {pos[1]:.2f})m', 
                (int(bbox['left']), int(bbox['top']) - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_8
            )

        ## put velocity text
        if 'velocity' in item.keys():
            vel = item['velocity']
            cv2.putText(
                img_copy, f'v:({vel[0]:.2f}, {vel[1]:.2f})m/s', 
                (int(bbox['left']), int(bbox['top']) - 22), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_8
            )

    return img_copy


def read_velocity_image(folder, id, frame=40, annotation=False):
    """
    Reads an image from the velocity dataset. Adds annotations if needed.
    folder: be one of ['supp', 'test', 'train']
    id: the id of the image/clip
    frame: a number between 1 to 40
    annotation: whether to draw annotation to the image
    """
    
    # invalid folder
    if folder not in ['supp', 'test', 'train']:
        return None
    # invalid frame
    if folder != 'supp' and frame < 1 or frame > 40:
        return  None

    if folder == 'supp':
        path_img = project_folder / velocity_folder / f'{folder}/supp_img/{id:04d}.jpg'
        path_annotation = project_folder / velocity_folder / f'{folder}/annotation.json'
    else: # folder is train/test
        path_img = project_folder / velocity_folder / f'{folder}/clips/{id}/imgs/{frame:03d}.jpg'
        path_annotation = project_folder / velocity_folder / f'{folder}/clips/{id}/annotation.json'
    
    #print(path_img)
    # read the image
    img = cv2.imread(str(path_img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # add annotation
    if annotation and frame==40:
        # load the annotation file
        with open(path_annotation) as file:
            # parse json file
            annotation = json.load(file)

        if folder == 'supp':
            # reform the annotation for supp because it is kind of different
            temp = []
            for bbox in annotation[id - 1]['bbox']:
                temp.append({
                    'bbox': {
                        'top': bbox['top'],
                        'right': bbox['right'],
                        'bottom': bbox['bottom'],
                        'left': bbox['left']
                    }
                })
            annotation = temp

        img = draw_annotation(img, annotation)
          
    return img



def crop_cars(folder, id):
    """
    crop out the cars in the image given annotated bounding boxes
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



