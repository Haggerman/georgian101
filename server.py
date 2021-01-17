from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks, Query, Form
from fastapi.templating import Jinja2Templates
from typing import Optional
import shutil
import os
import pytesseract
import cv2

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Radek:
    def __init__(self, xStart, yStart, xKonec, yKonec):
        self.x = xStart
        self.y = yStart
        self.xKonec = xKonec
        self.yKonec = yKonec
        self.sirka = xKonec - xStart
        self.vyska = yKonec - yStart


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/v1/extract_text")
def extract_text(image: UploadFile = File(...), coordinates: Optional[str] = Form(None)):
    temp_file = _save_file_to_disk(image, path="temp", save_as="temp")
    img = cv2.imread(temp_file, cv2.IMREAD_GRAYSCALE)
    radky = []
    text = ''

    if coordinates is not None:
        coordList = coordinates.split(',')
        for x in range(0, len(coordList) - 3, 4):
            radky.append(Radek(xStart=int(coordList[x]), yStart=int(coordList[x + 1]), xKonec=int(coordList[x + 2]),
                               yKonec=int(coordList[x + 3])))

        radky.sort(key=lambda item: (item.y, item.x))

        for radek in radky:
            text = text + read_image(img, int(radek.x), int(radek.y), int(radek.xKonec),
                                           int(radek.yKonec),
                                           'kat')
    else:
        text = text + read_image_noCoord(img, lang='kat')

    if not text or text.isspace():
        text = "Na obrázku se nepodařilo rozpoznat žádný text"

    return {"filename": image.filename, "text": text}


def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


def read_image(img, x, y, xEnd, yEnd, lang='kat'):
    try:
        conf = r'--oem 1 --psm 3'
        return pytesseract.image_to_string(img[y:yEnd, x:xEnd], lang=lang, config=conf)
    except:
        return ""


def read_image_noCoord(img, lang='kat'):
    try:
        conf = r'--oem 1 --psm 3'
        return pytesseract.image_to_string(img, lang=lang, config=conf)
    except:
        return "[ERROR] Obrázek se nepodařilo zpracovat"

