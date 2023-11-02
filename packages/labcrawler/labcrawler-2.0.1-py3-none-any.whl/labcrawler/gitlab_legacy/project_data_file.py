from csv import DictReader
from pathlib import Path


class ProjectDataFile:
    """Specific to GitLab"""

    def __init__(self, config: dict):
        filepath = Path(config['output_dir']) / 'gitlab' / 'projects.csv'
        with open(filepath) as projects_file:
            self.projects_data = [p for p in DictReader(projects_file)]

    def get_project_data(self, project_id: int):
        return next((p for p in self.projects_data if p['id'] == str(project_id)),
                    None)
