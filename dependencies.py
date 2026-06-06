from fastapi import Depends
from project_repository import ProjectRepository
from project_service import ProjectService


def get_project_repository():

    return ProjectRepository()


def get_project_service(
    repository=Depends(
        get_project_repository
    )
):

    return ProjectService(
        repository
    )