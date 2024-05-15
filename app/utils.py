import random
import shutil
import string
from os import path, makedirs
from pathlib import Path

from fastapi import UploadFile

from app.api_models import UploadFileResponse


def upload_picture(image: UploadFile) -> UploadFileResponse:
    letter = string.ascii_letters
    rand_str = "".join(random.choice(letter) for i in range(6))
    append_str = f"_{rand_str}."
    image_name = append_str.join(image.filename.rsplit('.', 1))
    home_dir = Path.home()
    upload_dir = path.join(home_dir, "Meetup", "Pictures")
    if not path.isdir(upload_dir):
        makedirs(upload_dir)
    upload_path = path.join(upload_dir, image_name)
    with open(upload_path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return UploadFileResponse(filename=image_name, type=image.content_type, url=upload_path)
