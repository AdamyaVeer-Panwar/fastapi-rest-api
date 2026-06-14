from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from auth import create_access_token
from auth import decode_access_token

from exceptions import ProjectNotFoundException

from database import get_db

from user_repository import UserRepository
from project_repository import ProjectRepository

from project_service import ProjectService
from user_service import UserService

from schemas import ProjectCreate
from schemas import UserCreate

from task_repository import TaskRepository
from task_service import TaskService

from schemas import TaskCreate

from redis_client import redis_client

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
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

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_access_token(token)
    user_id = int(
        payload["sub"]
    )

    repository = UserRepository(db)

    user = await repository.get_by_id(
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@app.get("/profile")
async def profile(
    current_user = Depends(get_current_user)
):
    return current_user


@app.post("/projects")
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    repository = ProjectRepository(db)
    service = ProjectService(
        repository
    )

    return await service.create_project(
        name=project.name,
        user_id=project.user_id
    )


@app.get("/projects/{project_id}")
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = ProjectRepository(db)
    service = ProjectService(
        repository
    )

    project = await service.get_project(
        project_id
    )

    if not project:
        raise ProjectNotFoundException()

    return project


@app.get("/projects")
async def get_projects(
    db: AsyncSession = Depends(get_db)
):
    repository = ProjectRepository(db)
    service = ProjectService(
        repository
    )

    return await service.get_projects()


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


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

@app.post("/users")
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    repository = UserRepository(db)

    service = UserService(
        repository
    )

    return await service.create_user(
        name=user.name,
        email=user.email
    )


@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = UserRepository(db)

    service = UserService(
        repository
    )

    return await service.get_user(
        user_id
    )


@app.get("/users")
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    repository = UserRepository(db)

    service = UserService(
        repository
    )

    return await service.get_users()

@app.post("/tasks")
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    task_repository = TaskRepository(db)

    user_repository = UserRepository(db)

    project_repository = ProjectRepository(db)

    service = TaskService(
        task_repository,
        user_repository,
        project_repository
    )

    return await service.create_task(
        title=task.title,
        user_id=task.user_id,
        project_id=task.project_id
    )


@app.get("/tasks/{task_id}")
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db)
):
    repository = TaskRepository(db)

    service = TaskService(
        repository
    )

    return await service.get_task(
        task_id
    )


@app.get("/tasks")
async def get_tasks(
    db: AsyncSession = Depends(get_db)
):
    repository = TaskRepository(db)

    service = TaskService(
        repository
    )

    return await service.get_tasks()


@app.get("/redis-test")
async def redis_test():

    await redis_client.set(
        "hello",
        "world"
    )

    value = await redis_client.get(
        "hello"
    )

    return {
        "value": value
    }