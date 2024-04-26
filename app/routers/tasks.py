from fastapi import APIRouter, Depends
from typing import Annotated
from utils.auth_utils import OAuth2_scheme

router = APIRouter(
    prefix="/tasks",
)


@router.get("/{taskId}", tags=["task"])
async def getTasks(token: Annotated[str, Depends(OAuth2_scheme)]):
    return


@router.post("/", tags=["task"])
async def createTask(token: Annotated[str, Depends(OAuth2_scheme)]):
    return
