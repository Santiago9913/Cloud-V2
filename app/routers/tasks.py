from fastapi import APIRouter, Depends, File, UploadFile
from typing import Annotated
from sqlmodel import Session
from utils.auth_utils import OAuth2_scheme
from utils.db_engine import get_session
from utils.pub_sub import publish_message
from utils.cloud_storage import upload_blob
from jose import jwt, JWTError
from .users import getUser
from models.models import User
import io
from models.models import Task

router = APIRouter(
    prefix="/tasks",
)


# @router.get("/{taskId}", tags=["task"])
# async def getTasks(
#     *,
#     token: Annotated[str, Depends(OAuth2_scheme)],
#     session: Session = Depends(get_session),
# ):
#     return


@router.post("", tags=["task"])
async def createTask(
    *,
    token: Annotated[str, Depends(OAuth2_scheme)],
    session: Session = Depends(get_session),
    file: UploadFile = File(...)
):
    try:
        user: User = await getUser(token=token, session=session)
        stream = io.BytesIO(file.file.read())
        upload_blob(blob_name=file.filename, file=stream, userId=str(user["id"]))
        publish_message(data={"userId": str(user["id"]), "fileName": file.filename})
        session.add(Task(status="uploaded", user_id=str(user["id"])))
        return {
            "message": "File uploaded successfully",
        }
    except Exception as e:
        print(e)
        return e
    finally:
        file.file.close()
