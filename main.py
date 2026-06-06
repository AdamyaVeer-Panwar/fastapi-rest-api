from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from exceptions import ProjectNotFoundException

from pydantic import BaseModel

from auth import create_access_token
from auth import decode_access_token

from user_repository import UserRepository

from project_repository import ProjectRepository
from project_service import ProjectService

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

repository = ProjectRepository()

service = ProjectService(
    repository
)

projects = []


class ProjectCreate(BaseModel):
    name: str


@app.post("/projects")
async def create_project(
    project: ProjectCreate
):
    return service.create_project(
        project.name,
        projects
    )


@app.post("/login")
async def login():

    token = create_access_token(
        user_id=1
    )

    return {
        "access_token": token,
        "token_type": "bearer"

    }


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):
    payload = decode_access_token(
        token
    )

    user_id = int(
        payload["sub"]
    )

    repository = UserRepository()

    user = repository.get_by_id(
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@app.get("/profile")
def profile(
    current_user=Depends(
        get_current_user
    )
):
    return current_user

@app.get("/projects/{project_id}")
def get_project(
    project_id: int
):
    return service.get_project(
        project_id,
        projects
    )

@app.exception_handler(
    ProjectNotFoundException
)
async def project_not_found_handler(
    request,
    exc
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Project not found"
        }
    )

@app.get("/projects")
def get_projects(
    skip: int = 0,
    limit: int = 10
):
    return service.get_projects(
        projects,
        skip,
        limit
    )