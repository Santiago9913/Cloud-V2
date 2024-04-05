import datetime
import moviepy.editor as mp
from moviepy.editor import *
from PIL import Image
from celery import Celery
from env import CELERY_BROKER_URL, CELERY_TASK_NAME
from modelos.modelos import db, Status, Task
from config import app

celery = Celery(CELERY_TASK_NAME, broker=CELERY_BROKER_URL)
app.app_context().push()

@celery.task()
def process_video(task_id):
    print(task_id)
    task = Task.query.get(task_id)

    if task is None:
        return 'La tarea para el procesamiento del video no fue encontrada'

    video = mp.VideoFileClip(filename=f'./videos/subidos/{task.filename}')

    end_time = 20
    video = video.subclip(0, end_time - 1)

    new_width = int(video.h * 16 / 9)
    video = vfx.crop(video, x1=0, y1=0, width=new_width, height=video.h)

    end_time = 20
    video = video.subclip(1, end_time - 1)

    image = Image.open('./logos/IDRL.jpeg')
    image_resized = image.resize((video.w, video.h))
    image_resized.save('./logos/IDRL.jpeg')

    image_clip = mp.ImageClip('./logos/IDRL.jpeg', duration=1)
    video = mp.concatenate_videoclips([image_clip, video, image_clip])

    video.write_videofile(f'./videos/procesados/{task.filename}', codec="libx264")

    task.status = Status.PROCESSED
    task.modified_at = datetime.datetime.now()
    db.session.commit()