from fastapi import APIRouter, Depends, File, UploadFile
from typing import Annotated
from sqlmodel import Session
from utils.auth_utils import OAuth2_scheme
from utils.db_engine import get_session
from utils.pub_sub import publish_message
from utils.cloud_storage import upload_blob, get_signed_url
from jose import jwt, JWTError
from .users import getUser
from models.models import User
import io
from models.models import Task
from dtos.auth import RetrieveVideoDto

router = APIRouter(
    prefix="/tasks",
)


@router.post("", tags=["task"])
async def createTask(
    *,
    token: Annotated[str, Depends(OAuth2_scheme)],
    session: Session = Depends(get_session),
    file: UploadFile = File(...),
):
    try:
        user: User = await getUser(token=token, session=session)
        stream = io.BytesIO(file.file.read())
        upload_blob(blob_name=file.filename, file=stream, userId=str(user["id"]))
        publish_message(data={"userId": str(user["id"]), "fileName": file.filename})
        session.add(Task(status="uploaded", user_id=str(user["id"])))
        return {
            "message": "File uploaded successfully",
            "data": {
                "userId": str(user["id"]),
                "id": str(user["id"]),
                "fileName": file.filename,
            },
        }
    except Exception as e:
        print(e)
        return e
    finally:
        file.file.close()


@router.get("", tags=["task"])
async def getTask(
    *,
    token: Annotated[str, Depends(OAuth2_scheme)],
    session: Session = Depends(get_session),
    fileName: str = "Ejemplo.mp4",
):
    try:
        user: User = await getUser(token=token, session=session)
        url = get_signed_url(
            userId=str(user["id"]), fileName=fileName
        )  # El filename puede pasar por parametro
        return {
            "message": "Task retrieved successfully",
            "data": {"url": url},
        }
    except Exception as e:
        print(e)
        return e
