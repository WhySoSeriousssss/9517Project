# VELOCITY ESTIMATION DATASET FROM TUSIMPLE: TRAINING SET

The goal of this challenge is to estimate the motion and position of vehicles relative to the camera. The benchmark dataset consists of 1074 training image sequences. 

## Task Definition
For each test sequence, predict the planar velocity and position of certain vehicles relative to the camera on a given specific frame. All the velocity and position displacements in the up/down direction are ignored in this dataset. The output from your system should be a 2d vector representing the velocity vector, and a 2d coordinate in meters representing the closest point of the vehicle to the camera for each vehicle. The output should be formatted similarly with the ground truth given, whose format will be defined in the following section.

## Size 
1074 training clips, each containing 40 frames of 20fps video.

## Directory Structure:
      |----readme.md                  # description
      |
      |----calibration.txt            #intrinsic parameters of the used camera
      |----clips/                     # 1074 video clips
      |------|----...
      |------|----some_clip/              # images and json labels for each clip
      |------|--------|
      |------|--------|----imgs/              # 40 frames of 20 fps video recorded, 2 seconds in total
      |------|--------|
      |------|--------|----annotation.json    # json annotation of designated vehicles.

## Label Data Format
 - calibration.txt: a text file containing the intrinsic parameters of the camera used, structured in a 3*3 matrix and the camera height to the ground.

Each of the training clip can be found under a clip folder named after a integer.
The files in the folder are structured as follows:
 - imgs/:  subfolder contains 40 frames of images recorded at 20 fps, the end of the which, 040.jpg, is the frame that ground truth annotation on, and the frame that needs to estimate velocity on.
 - annotation.json: a json file, containing the ground truth velocity and position for designated vehicles.

And the ground truth json file is structured as follows:
```
{ 
   [vehicle]: an array of [vehicle], defining the velocity and position of each vehicle in the image.
}

vehicle:
{
  "bbox": a json structure with 4 fields 'top','left','bottom','right': The axis-aligned rectangle specifying the extent of the vehicle in the image.
  "velocity": a float pair [x,y]. Relative planar velocity of the vehicle in meters per second. x direction is the same with the camera optical axis and y direction is vertical to x and towards right.
  "position": a float pair [x,y]. Planar position of the nearest point on vehicle in meters. x direction is the same with the camera optical axis, and y direction is vertical to x and towards right.
}
```

## Evaluation Protocol
The metric we use in evaluating velocity estimation is Mean Squared Velocity Error:
$$E_v = \frac{\sum_{c\in C}\|V^{gt}_c-V^{est}_c\|^2}{|C|}$$
with $C$ denotes the set of submitted results for each vehicle, $V^{gt}_c$ represents the ground truth velocity for a certain vehicle, and $V^{est}_c$ represents the estimated velocity for such vehicle. Similarly, we use Mean Squared Position Error to evaluate position esitimation: 
$$E_p = \frac{\sum_{c\in C}\|P^{gt}_c-P^{est}_c\|^2}{|C|}$$
$P^{gt}_c$ represents the ground truth position of the nearest point on a certain vehicle, and $P^{est}_c$ represents the estimated position of the nearest point on such vehicle.

You are supposed to predict 'velocity' and 'position' according to specified 'bbox' on a given image sequence. For details about the result you are supposed to submit, please refer to the README.md file for the test set.
