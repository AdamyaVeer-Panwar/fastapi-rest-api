from project_repository import ProjectRepository
from exceptions import ProjectNotFoundException


class ProjectService:

    def __init__(
        self,
        repository: ProjectRepository
    ):
        self.repository = repository

    def create_project(
        self,
        name: str,
        projects: list
    ):

        project = {
            "id": len(projects) + 1,
            "name": name
        }

        return self.repository.create(
        project,
        projects
        )
    
    def get_project(
        self,
        project_id: int,
        projects: list
    ):

        project = self.repository.get_by_id(
        project_id,
        projects
    )

        if not project:
            raise ProjectNotFoundException()

        return project
    
    def get_projects(
    self,
    projects: list,
    skip: int,
    limit: int
):

        all_projects = self.repository.get_all(
        projects
    )

        return all_projects[
        skip : skip + limit
    ]
