import base64
import functions_framework
import moviepy.editor as mp
from moviepy.editor import *
from google.cloud import storage
from io import BytesIO
import json
import tempfile


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def process_video(cloud_event):
    try:
        data = base64.b64decode(cloud_event.data["message"]["data"])
        data = json.loads(data.decode("utf-8"))
        temp = tempfile.NamedTemporaryFile(delete=True)
        temp.name = data["userId"] + "--" + data["fileName"]
        fileName = data["userId"] + "--" + data["fileName"]
        fileNameInBucket = f"uploaded/{data['userId']}/{data['fileName']}"
        retrieveVideo(temp, fileName, fileNameInBucket)
        return {
            "message": "Video processed successfully",
        }
    except Exception as e:
        return e


def retrieveVideo(temp, fileName, fileNameInBucket):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket("videos_dev_cloud_v2")
        blob = bucket.blob(fileNameInBucket)
        blobFile = blob.download_as_bytes()
        editVideo(fileName, blobFile, temp)
    except Exception as e:
        print(e)
        return e


def upload_blob(blob_name: str, file: BytesIO, userId: str):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket("videos_dev_cloud_v2")
        blob = bucket.blob(f"processed/{userId}/{blob_name}")
        blob.upload_from_filename(file)
    except Exception as e:
        print(e)
        raise Exception("Error uploading file")


# Esta funcion solo realiza un corte en el clip
# Se puede agregar mas funcionalidades segun lo que se busque
def editVideo(
    fileName,
    blobFile,
    temp,
):
    try:
        with open(f"/tmp/{fileName}", "wb") as f:
            f.write(blobFile)
        f.close()
        video: mp.VideoFileClip = mp.VideoFileClip(f"/tmp/{fileName}")
        end_time = 20
        video = video.subclip(0, end_time - 1)

        new_width = int(video.h * 16 / 9)
        video = vfx.crop(video, x1=0, y1=0, width=new_width, height=video.h)

        end_time = 20
        video = video.subclip(1, end_time - 1)

        video.write_videofile(f"/tmp/processed--{fileName}", codec="libx264")

        upload_blob(
            f"{fileName.split('--')[1]}",
            f"/tmp/processed--{fileName}",
            fileName.split("--")[0],
        )
        temp.close()
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()
