from google.cloud import storage
from env import BUCKET_NAME
import os
from io import BytesIO
import datetime
from google.auth import default, compute_engine
from google.auth.transport.requests import requests

# credentials_path = "../../credentials.json"


storage_client = None
credentials, _ = default()
auth_request = requests.Request()
credentials.refresh(auth_request)
signing_credentials = compute_engine.IDTokenCredentials(
    auth_request, "", service_account_email=credentials.service_account_email
)


def init_cludstorage():
    # if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
    #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    global storage_client
    storage_client = storage.Client()


def get_bucket():
    try:
        if not storage_client:
            raise Exception("Storage client not initialized")
        return storage_client.get_bucket("videos_dev_cloud_v2")
    except Exception as e:
        print(e)
        raise Exception("Error getting bucket")


def upload_blob(blob_name: str, file: BytesIO, userId: str):
    try:
        print(file)
        bucket = get_bucket()
        print(bucket)
        blob = bucket.blob(f"uploaded/{userId}/{blob_name}")
        print(blob)
        blob.upload_from_file(file)
        return True
    except Exception as e:
        print("error uploading file")
        print(e)
        raise Exception("Error uploading file")


def get_signed_url(userId: str, fileName: str):
    try:
        bucket = get_bucket()
        blob = bucket.blob(f"processed/{userId}/{fileName}")
        url = blob.generate_signed_url(
            credentials=signing_credentials,
            version="v4",
            expiration=datetime.timedelta(minutes=15),
            method="GET",
        )
        return url
    except Exception as e:
        print(e)
        raise Exception("Error generating signed url")
