# pytextractor
python ocr using tesseract/ with EAST opencv text detector

Use the EAST opencv detector defined [here](https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/) with [pytesseract](https://github.com/madmaze/pytesseract) to get text/numbers from images

```
usage: text_detection.py [-h] [-east EAST] [-c CONFIDENCE] [-w WIDTH]
                         [-e HEIGHT] [-d] [-n] [-p PERCENTAGE]
                         images [images ...]

Text/Number extractor from image

positional arguments:
  images                path(s) to input image(s)

optional arguments:
  -h, --help            show this help message and exit
  -east EAST, --east EAST
                        path to input EAST text detector
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
```
