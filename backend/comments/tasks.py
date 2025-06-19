from celery import shared_task
from PIL import Image
import os


@shared_task
def resize_image_task(path):
    try:
        img = Image.open(path)
        img.thumbnail((320, 240))
        img.save(path)
    except Exception as e:
        print(f"Помилка при обробці зображення: {e}")
