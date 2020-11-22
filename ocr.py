import pytesseract
import os
import sys


async def read_image(img_path, lang='kat'):
    try:
        return pytesseract.image_to_string(img_path, lang=lang)
    except:
        return "[ERROR] Unable to process file: {0}".format(img_path)
