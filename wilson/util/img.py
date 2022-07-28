import os
import requests
import shutil


def get_image(img_url: str) -> str:
    path = '.wilson/tmp/'

    if not os.path.exists(path):
        os.mkdir(path)

    file_extension = img_url.split('.')[-1]
    file_path = f'{path}temp.{file_extension}'
    response = requests.get(img_url, stream=True)

    with open(file_path, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
        del response
    return file_path


def get_image_bytes(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()


def get_image_url_bytes(url: str) -> bytes:
    img_path = get_image(url)
    img_bytes = get_image_bytes(img_path)

    os.remove(img_path)
    return img_bytes
