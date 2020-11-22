from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks, Query, Form
from fastapi.templating import Jinja2Templates
from typing import Optional, List
import shutil
import os
import pytesseract
import uuid
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/v1/extract_text")
async def extract_text(image: UploadFile = File(...), coordinates: str = Form(...)):
    temp_file = _save_file_to_disk(image, path="temp", save_as="temp")
    text = await read_image(temp_file)

    return {"filename": image.filename, "text": text, "coordinates": coordinates}


def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


async def read_image(img_path, lang='kat'):
    try:
        return pytesseract.image_to_string(img_path, lang=lang)
    except:
        return "[ERROR] Unable to process file: {0}".format(img_path)
