class ProjectRepository:
    def create(self,
               project: dict,
               projects:list
               ):
        
        projects.append(project)

        return project
    
    def get_by_id(
        self,
        project_id: int,
        projects: list
        ):
            for project in projects:
                if project["id"] == project_id:
                 return project

        
            return None
    
    def get_all(
    self,
    projects: list
    ):
    
        return projects
