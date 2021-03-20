# VELOCITY ESTIMATION DATASET FROM TUSIMPLE: SUPPLEMENTARY DATA

## Introduction
This supplementary dataset includes additional training data for training a vehicle detector. You can use the data freely during your training process

## Size 
5066 images.

## Directory Structure:
      |----readme.md              # description
      |
      |----annotation.json      # bounding box annotations
      |----supp_img/               # 5066 images

## Label Data Format
  - supp_img/: folder contains all the training images, named in 4 digit numbers.
  - annotation.json: a json file, containing the ground truth bounding box for all vehicles in all training images, structured as follows:
```
{
  [img]: an array of [img], representing the ground truth bounding box annotations for each image.
}

img:
{
  "file_name": a string representing the image file name.
  "bbox": a list of json structure [{'left', 'top', 'bottom', 'right'}], each representing the axis-aligned rectangle specifying the extend of a vehicle in this image.
}
```