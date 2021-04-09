import cv2 as cv
import glob
import numpy as np
import matplotlib.pyplot as plt

def plot_BGR(temp_image):
    temp_image = cv.cvtColor(temp_image,cv.COLOR_BGR2RGB)
    plt.imshow(temp_image)
    plt.show()

inWidth = 600
inHeight = 600
whRatio = 1
inScaleFactor = 0.007843
net = cv.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt","MobileNetSSD_deploy.caffemodel")
img_paths = glob.glob('performance/*')
image_height = 720
image_weigth = 1280
# set threshold
confidenceThreshold = 0.15
for path in img_paths:
    img = cv.imread(path)

    plot_BGR(img)
    blob = cv.dnn.blobFromImage(img,inScaleFactor,(inWidth,inHeight))
    net.setInput(blob,"data")
    detection = net.forward("detection_out")
    detectionMat = np.resize(detection,(detection.shape[2],detection.shape[3]))
    for i in range(detectionMat.shape[0]):
        # 6 equal to bus 7 equal to car
        if detectionMat[i,1]==7 or detectionMat[i,1]==6:
            confidence = detectionMat[i,2]
            if confidence>= confidenceThreshold:
                xleftBottom = detectionMat[i,3]*img.shape[1]
                yleftBottom = detectionMat[i,4]*img.shape[0]
                xrightTop = detectionMat[i,5]*img.shape[1]
                yrightTop = detectionMat[i,6]*img.shape[0]
                cv.rectangle(img,(int(xleftBottom),int(yleftBottom)),(int(xrightTop),int(yrightTop)),(0,0,255),12)
                plot_BGR(img)
    
    