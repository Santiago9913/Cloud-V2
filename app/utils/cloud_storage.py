from google.cloud import storage
from env import BUCKET_NAME
import os
from io import BytesIO

credentials_path = './cloud-dev-421516-a73c9ed72f6b.json'


storage_client = None


def init_cludstorage():
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    global storage_client
    storage_client = storage.Client()


def get_bucket():

    if not storage_client:
        raise Exception("Storage client not initialized")
    return storage_client.get_bucket(BUCKET_NAME)


def upload_blob(blob_name: str, file: BytesIO, userId: str):
    try:
        bucket = get_bucket()
        blob = bucket.blob(f"uploaded/{userId}/{blob_name}")
        blob.upload_from_file(file)
        return True
    except Exception as e:
        raise Exception("Error uploading file")
