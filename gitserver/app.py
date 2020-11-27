import secrets
import tempfile
from enum import Enum
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request
from starlette.responses import StreamingResponse

from gitserver.git import Git

TEMPDIR = tempfile.TemporaryDirectory()

app = FastAPI()
security = HTTPBasic()


class Service(Enum):
    receive = 'git-receive-pack'
    upload = 'git-upload-pack'


def auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """ Of course, this is just an example. Do not use this! """
    username = secrets.compare_digest(credentials.username, 'admin')
    password = secrets.compare_digest(credentials.password, 'admin')
    if not (username and password):
        raise HTTPException(status_code=401)
    return credentials.username


@app.get('/{path}/info/refs')
async def info(path: str, service: Service, user: str = Depends(auth)):
    path = Path(TEMPDIR.name, path)

    # Create repo if does does not exist
    repo = Git(path) if path.exists() else Git.init(path)

    # Fetch inforefs
    data = repo.inforefs(service.value)

    media = f'application/x-{service.value}-advertisement'
    return StreamingResponse(data, media_type=media)


@app.post('/{path}/{service}')
async def service(path: str, service: Service, req: Request):
    path = Path(TEMPDIR.name, path)
    repo = Git(path)

    # Load data to memory (be careful with huge repos)
    stream = req.stream()
    data = [data async for data in stream]
    data = b''.join(data)

    # Load service data
    data = repo.service(service.value, data)

    media = f'application/x-{service.value}-result'
    return StreamingResponse(data, media_type=media)
