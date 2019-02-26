import time

import cv2
import numpy as np
import pytesseract
from imutils.object_detection import non_max_suppression


class PyTextractor:
    layer_names = ('feature_fusion/Conv_7/Sigmoid', 'feature_fusion/concat_3',)

    def __init__(self, *args, **kwargs):
        self.east = kwargs.get('east', './assets/models/frozen_east_text_detection.pb')
        self._load_assets()

    def get_image_text(self,
                       image,
                       width=320,
                       height=320,
                       display=False,
                       numbers=False,
                       confidence=0.5,
                       percentage=2.0,
                       **kwargs):
        loaded_image = self._load_image(image)
        image, width, height, ratio_width, ratio_height = self._resize_image(
            loaded_image, width, height
        )
        scores, geometry = self._compute_scores_geometry(image, width, height)
        (num_rows, num_cols) = scores.shape[2:4]

        start = time.time()
        boxes = self._get_boxes(num_rows, num_cols, confidence, geometry, scores)
        end = time.time()
        print('Found {boxes} ROIs {seconds:.6f} seconds'.format(boxes=len(boxes), seconds=(end - start)))

        return self._extract_text(
            loaded_image, boxes, percentage, display, numbers, ratio_width, ratio_height
        )

    def _load_image(self, image):
        return cv2.imread(image)

    def _resize_image(self, image, width, height):
        (H, W) = image.shape[:2]

        (newW, newH) = (width, height)
        ratio_width = W / float(newW)
        ratio_height = H / float(newH)

        # resize the image and grab the new image dimensions
        resized_image = cv2.resize(image, (newW, newH))
        (H, W) = resized_image.shape[:2]
        return (resized_image, height, width, ratio_width, ratio_height)

    def _compute_scores_geometry(self, image, width, height):
        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(
            image, 1.0, (width, height), (123.68, 116.78, 103.94), swapRB=True, crop=False
        )
        start = time.time()
        self.east_net.setInput(blob)
        (scores, geometry) = self.east_net.forward(self.layer_names)
        end = time.time()

        # show timing information on text prediction
        print('[INFO] text detection took {:.6f} seconds'.format(end - start))
        return (scores, geometry)

    def _load_assets(self):
        start = time.time()
        self.east_net = cv2.dnn.readNet(self.east)
        end = time.time()
        print('[INFO] Loaded EAST text detector {:.6f} seconds ...'.format(end - start))

    def _get_boxes(self, num_rows, num_cols, confidence, geometry, scores, min_boxes=1, max_iterations=20):
        iterations = 0
        boxes = []
        rects = []
        confidences = []
        while(iterations < max_iterations):
            for y in range(0, num_rows):
                # extract the scores (probabilities), followed by the geometrical
                # data used to derive potential bounding box coordinates that
                # surround text
                scores_data = scores[0, 0, y]
                x_data_0 = geometry[0, 0, y]
                x_data_1 = geometry[0, 1, y]
                x_data_2 = geometry[0, 2, y]
                x_data_3 = geometry[0, 3, y]
                angles_data = geometry[0, 4, y]

                # loop over the number of columns
                for x in range(0, num_cols):
                    # if our score does not have sufficient probability, ignore it
                    if scores_data[x] < confidence:
                        continue

                    # compute the offset_ factor as our resulting feature maps will
                    # be 4x smaller than the input image
                    (offset_X, offset_Y) = (x * 4.0, y * 4.0)

                    # extract the rotation angle for the prediction and then
                    # compute the sin and cosine
                    angle = angles_data[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)

                    # use the geometry volume to derive the width and height of
                    # the bounding box
                    h = x_data_0[x] + x_data_2[x]
                    w = x_data_1[x] + x_data_3[x]

                    # compute both the start_ing and end_ing (x, y)-coordinates for
                    # the text prediction bounding box
                    end_X = int(offset_X + (cos * x_data_1[x]) + (sin * x_data_2[x]))
                    end_Y = int(offset_Y - (sin * x_data_1[x]) + (cos * x_data_2[x]))
                    start_X = int(end_X - w)
                    start_Y = int(end_Y - h)

                    # add the bounding box coordinates and probability score to
                    # our respective lists
                    rects.append((start_X, start_Y, end_X, end_Y))
                    confidences.append(scores_data[x])

            # apply non-maxima suppression to suppress weak, overlapping bounding
            # boxes
            boxes = non_max_suppression(np.array(rects), probs=confidences)
            if len(boxes) >= min_boxes:
                return boxes
            else:
                confidence /= 2
                print('Couldn\'t find at least {min_boxes} boxe(s), halving confidence to {confidence}'.
                      format(min_boxes=min_boxes, confidence=confidence))

    def _extract_text(self, image, boxes, percent, display, numbers, ratio_width, ratio_height):
        extracted_text = []
        for (start_X, start_Y, end_X, end_Y) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            percent = (percent / 100 + 1) if percent >= 0 else ((100 - percent) / 100)
            start_X = int(start_X * ratio_width * percent)
            start_Y = int(start_Y * ratio_height * percent)
            end_X = int(end_X * ratio_width * percent)
            end_Y = int(end_Y * ratio_height * percent)

            # draw the bounding box on the image
            if display:
                cv2.rectangle(image, (start_X, start_Y), (end_X, end_Y), (0, 255, 0), 2)

            ROIImage = image.copy()[start_Y:end_Y, start_X:end_X]
            config = '--psm 6' if numbers else ''
            extracted_text.append(pytesseract.image_to_string(
                ROIImage, config=config)
            )
            if display:
                cv2.imshow('SubImage', ROIImage)

        # show the output image
        if display:
            cv2.imshow('Text Detection', image)
            cv2.waitKey(0)

        return extracted_text
