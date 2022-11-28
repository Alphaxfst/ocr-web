from pdf2image import convert_from_path
import pytesseract
import os
import cv2
import re
import numpy as np
# tambahkan remark keterangan parameter Tesseract
custom_config_pdf = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
custom_config_image = r'--oem 3 --psm 1'
UPLOAD_FOLDER = 'static/uploads/'
TEMP_DIR = 'temp/'

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def convert2pdf(file, dir):
    filename = file.lower().split(".")[0]
    if dir != "":
        convertedImg = convert_from_path(os.path.join(dir, file))
    else:
        convertedImg = convert_from_path(file)
    for i in range(len(convertedImg)):
        convertedImg[i].save(os.path.join(TEMP_DIR, filename + '_page' + "{0:0=3d}".format(i) + '.jpg'), 'JPEG')

def imagePreprocess(image):
    # Grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Noise removal
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)

    return (image)

def ocr(file, dir=UPLOAD_FOLDER):
    resultsStr = ""
    if file.split(".")[-1].lower() == 'pdf':
        convert2pdf(file, dir)
        for file in os.listdir(TEMP_DIR):
            image = cv2.imread(os.path.join(TEMP_DIR, file))
            ocrResult = pytesseract.image_to_string(
                image, config=custom_config_pdf)
            newResult = re.sub(r"[\n\t]*", "", ocrResult)
            newResult = " ".join(ocrResult.split())
            resultsStr += newResult
            os.remove(os.path.join(TEMP_DIR, file))
    else:
        image = cv2.imread(os.path.join(UPLOAD_FOLDER, file))
        preprocessedImage = imagePreprocess(image)
        ocrResults = pytesseract.image_to_string(preprocessedImage, config=custom_config_image)
        resultsStr = " ".join(ocrResults.split())

    return resultsStr
    