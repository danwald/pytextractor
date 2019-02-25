# USAGE
# python text_detection.py --image images/lebron_james.jpg --east frozen_east_text_detection.pb

# import the necessary packages
import argparse
import time

import cv2
import numpy as np
import pytesseract
from imutils.object_detection import non_max_suppression

def get_boxes(numRows, numCols, confidence, min_boxes=1, max_iterations=20):
    iterations = 0
    boxes = []
    rects = []
    confidences = []
    while(iterations < max_iterations):
        for y in range(0, numRows):
            # extract the scores (probabilities), followed by the geometrical
            # data used to derive potential bounding box coordinates that
            # surround text
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            # loop over the number of columns
            for x in range(0, numCols):
                # if our score does not have sufficient probability, ignore it
                if scoresData[x] < confidence:
                    continue

                # compute the offset factor as our resulting feature maps will
                # be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                # extract the rotation angle for the prediction and then
                # compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                # use the geometry volume to derive the width and height of
                # the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                # compute both the starting and ending (x, y)-coordinates for
                # the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                # add the bounding box coordinates and probability score to
                # our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        if len(boxes) >= min_boxes:
            return boxes
        else:
            confidence /= 2
            print('Couldn\'t find at least {min_boxes} boxe(s), halving confidence to {confidence}'.
                  format(min_boxes=min_boxes, confidence=confidence))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
	help="path to input image")
ap.add_argument("-east", "--east", type=str, default='./frozen_east_text_detection.pb',
	help="path to input EAST text detector")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
	help="minimum probability required to inspect a region")
ap.add_argument("-w", "--width", type=int, default=320,
        help="resized image width (should be multiple of 32)")
ap.add_argument("-e", "--height", type=int, default=320,
	help="resized image height (should be multiple of 32)")
ap.add_argument("-d", "--display", action='store_true',
	help="Display bounding boxes")
ap.add_argument("-n", "--numbers", action='store_true',
	help="Detect only numbers")
ap.add_argument("-b", "--box-percentage", type=float, default=2,
	help="Expand/shrink detected bound box")
args = vars(ap.parse_args())

# load the input image and grab the image dimensions
image = cv2.imread(args["image"])
orig = image.copy()
(H, W) = image.shape[:2]

# set the new width and height and then determine the ratio in change
# for both the width and height
(newW, newH) = (args["width"], args["height"])
rW = W / float(newW)
rH = H / float(newH)

# resize the image and grab the new image dimensions
image = cv2.resize(image, (newW, newH))
(H, W) = image.shape[:2]

# define the two output layer names for the EAST detector model that
# we are interested -- the first is the output probabilities and the
# second can be used to derive the bounding box coordinates of text
layerNames = [
	"feature_fusion/Conv_7/Sigmoid",
	"feature_fusion/concat_3"]

# load the pre-trained EAST text detector
start = time.time()
net = cv2.dnn.readNet(args["east"])
end = time.time()
print("[INFO] Loaded EAST text detector {:.6f} seconds ...".format(end-start))

# construct a blob from the image and then perform a forward pass of
# the model to obtain the two output layer sets
blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
	(123.68, 116.78, 103.94), swapRB=True, crop=False)
start = time.time()
net.setInput(blob)
(scores, geometry) = net.forward(layerNames)
end = time.time()

# show timing information on text prediction
print("[INFO] text detection took {:.6f} seconds".format(end - start))

# grab the number of rows and columns from the scores volume, then
# initialize our set of bounding box rectangles and corresponding
# confidence scores
(numRows, numCols) = scores.shape[2:4]
#import ipdb; ipdb.set_trace();
# loop over the number of rows
start = time.time()
boxes = get_boxes(numRows, numCols, args['min_confidence'])
end = time.time()
# loop over the bounding boxes
print('Found {boxes} ROIs {seconds:.6f} seconds'.format(boxes=len(boxes),seconds=(end-start)))
extracted_text=[]
for (startX, startY, endX, endY) in boxes:
    # scale the bounding box coordinates based on the respective
    # ratios
    percent = args['box_percentage']
    percent = (percent/100+1) if percent >= 0 else ((100 - percent)/100)
    startX = int(startX * rW * percent)
    startY = int(startY * rH * percent)
    endX = int(endX * rW * percent)
    endY = int(endY * rH * percent)


    # draw the bounding box on the image
    if args['display']:
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    ROIImage = orig.copy()[startY:endY, startX:endX]
    config = '--psm 6' if args['numbers'] else ''
    extracted_text.append(pytesseract.image_to_string(
        ROIImage, config=config)
    )
    if args['display']:
        cv2.imshow("SubImage", ROIImage)


# show the output image
if args['display']:
    cv2.imshow("Text Detection", orig)
    cv2.waitKey(0)

print('Extracted text')
for text in extracted_text:
    print(text)
