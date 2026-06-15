from pydantic import BaseModel



class UserCreate(BaseModel):
    name: str
    email: str


class ProjectCreate(BaseModel):
    name: str
    user_id: int


class TaskCreate(BaseModel):
    title: str
    user_id: int
    project_id: int


class UserUpdate(BaseModel):
    name: str
    email: str


