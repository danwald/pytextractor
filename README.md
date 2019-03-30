# pytextractor
python ocr using tesseract/ with EAST opencv text detector

Uses the EAST opencv detector defined [here](https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/) with [pytesseract](https://github.com/madmaze/pytesseract) to extract text(default) or numbers from images.

```
usage: text_detection.py [-h] [--east EAST] [-c CONFIDENCE] [-w WIDTH]
                         [-e HEIGHT] [-d] [-n] [-p PERCENTAGE] [-b MIN_BOXES]
                         [-i MAX_ITERATIONS]
                         images [images ...]

Text/Number extractor from image

positional arguments:
  images                path(s) to input image(s)

optional arguments:
  -h, --help            show this help message and exit
  --east EAST           path to input EAST text detector
  -c CONFIDENCE, --confidence CONFIDENCE
                        minimum probability required to inspect a region
  -w WIDTH, --width WIDTH
                        resized image width (should be multiple of 32)
  -e HEIGHT, --height HEIGHT
                        resized image height (should be multiple of 32)
  -d, --display         Display bounding boxes
  -n, --numbers         Detect only numbers
  -p PERCENTAGE, --percentage PERCENTAGE
                        Expand/shrink detected bound box
  -b MIN_BOXES, --min-boxes MIN_BOXES
                        minimum number of detected boxes to return
  -i MAX_ITERATIONS, --max-iterations MAX_ITERATIONS
                        max number of iterations finding min_boxes
```
