"""
Tesseract-OCR Parameters

> Usage:
    tesseract --help | --help-extra | --help-oem | --version
    tesseract --list-langs [--tesdata-dir PATH]
    tesseract --print-parameters [options...] [configfile...]
    tesseract imagename|imagelist|stdin outputbase|stdout []

> Page segmentation mode:
    0   Orientation and script detection (OSD) only
    1   Automatic page segmentation without OSD
    2   Automatic page segmentation, but no OSD or OCR
    3   Fully automatic page segmentation, but no OSD
    4   Assume a singgle column of text of variable sizes
    5   Assume a single uniform block of vertically aligned text
    6   Assume a single uniform block of text
    7   Treat the image as single text line
    8   Treat the image as single word
    9   Treat the image as single word in a circle
    10  Treat the image as a single character
    11  Sparse text. Find as much as text as possible in no particular order
    12  Sparser text with OSD
    13  Red line. Treat image as a single text line.
        bypassing hacks that are Tesseract-specific

> OCR Engine modes:
    0   Legacy engine only
    1   Neural nets LSTM engine only
    2   Legacy + LSTM engine
    3   Default, based on what is available
"""

from pdf2image import convert_from_path
import pytesseract
import os
import cv2
import re
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def convert2pdf(file, dir):
    """
        Fungsi ini digunakan untuk melakukan konversi file file pdf ke bentuk gambar
        @params:
            file = nama file yang akan dikonversi
            dir = path direktori tujuan konversi
    """
    filename = file.lower().split(".")[0]
    path = os.path.join(dir, file) if dir != "" else file
    convertedImg = convert_from_path(path)
    for i in range(len(convertedImg)):
        convertedImg[i].save(os.path.join(os.path.join(dir, 'temp'), filename + '_page' + "{0:0=3d}".format(i) + '.jpg'), 'JPEG')

def imagePreprocess(image):
    """
        Fungsi ini digunakan untuk melakukan tahap preprocessing gambar
        @params:
            image = object opencv
        @return:
            image = object opencv
    """
    # Noise remove
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

    # Normalize
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)

    # Thinning and skeletonize
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations = 1)

    return (image)

def ocr(image):
    """
    Fungsi ini digunakan untuk menjalankan ocr pada 1 gambar
        @params:
            image = object opencv
        @return
            result = string hasil ocr menggunakan Tesseract-OCR
        @rtype: string
    """
    custom_config = r'--oem 3 --psm 6'
    preprocessedImage = imagePreprocess(image)
    ocrResult = pytesseract.image_to_string(preprocessedImage, config=custom_config)
    result = re.sub(r"\s+", " ", ocrResult)
    return result

def scan(file, dir):
    """
        Fungsi ini digunakan untuk melakukan pembacaan teks pada gambar atau pdf dengan 1 atau lebih halaman
        @params:
            file = nama file
            dir = direktori file
        @return
            resultStr = string hasil ocr
        @rtype: string
    """
    resultsStr = ""
    TEMP_DIR = os.path.join(dir, 'temp')
    if file.split(".")[-1].lower() == 'pdf':
        convert2pdf(file, dir)
        for file in os.listdir(TEMP_DIR):
            image = cv2.imread(os.path.join(TEMP_DIR, file))
            resultOCR = ocr(image)
            resultsStr += resultOCR
            os.remove(os.path.join(TEMP_DIR, file))
    else:
        image = cv2.imread(os.path.join(dir, file))
        resultOCR = ocr(image)
        resultsStr += resultOCR
    return resultsStr
    