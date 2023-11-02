from os import environ
from pathlib import Path
from csv import DictWriter
import logging

from labcrawler.gitlab.project_data_file import ProjectDataFile
from labcrawler.gitlab.gitlab_repository_files_extractor import \
    GitLabRepositoryFilesExtractor
from labcrawler.gitlab.gitlab_ci_config import GitLabCIConfig


class GitLabCIDataLoader:
    """Load includes (and later blames) from GitLab CI configs"""

    def __init__(self, config: GitLabCIConfig, project_id: int = None):
        self.config = config
        self.project_file = ProjectDataFile(self.config)
        if project_id:
            self.project_ids = [int(project_id)]
        else:
            self.project_ids = [p['id']
                                for p in self.project_file.projects_data]
        self.extractor = GitLabRepositoryFilesExtractor(
            gitlab_private_token=environ['GITLAB_PRIVATE_TOKEN'],
            gitlab_api_url=config['api_url'])

    def load_files(self):
        """Load the main CI config file and the local includes"""
        paths = []
        for project_id in self.project_ids:
            project_data = self.project_file.get_project_data(project_id)
            main_ci_config_path = project_data['ci_config_path'] or \
                '.gitlab-ci.yml'
            ci_config_file_content = self.extractor.extract_file_content(
                project_id=project_data['id'],
                branch=project_data['default_branch'],
                repo_path=main_ci_config_path)
            if ci_config_file_content:
                paths.append({'project_id': project_data['id'],
                              'main': main_ci_config_path})
                ci_config = GitLabCIConfig(ci_config_file_content)
                if ci_config.locals:
                    for localfile in ci_config.locals:
                        paths.append({'project_id': project_data['id'],
                                      'local_include': localfile})
        self.write_csv(paths, 'ci_config_paths',
                       ['project_id', 'main', 'local_include'])

    def load_blames(self):
        """Find committer information for main CI config file"""
        committers = []
        for project_id in self.project_ids:
            project_data = self.project_file.get_project_data(project_id)
            project_committers = self.extractor.extract_blamed_committers(
                project_id=project_data['id'],
                branch=project_data['default_branch'],
                repo_path=project_data['ci_config_path'] or '.gitlab-ci.yml')
            committers.extend(project_committers)
        self.write_csv(committers, 'ci_config_committers',
                       ['project_id', 'committer_name', 'committer_email'])

    def write_csv(self, rows: list, filename: str, fieldnames: list):
        path = Path(self.config['output_dir']) / 'gitlab' / (filename + '.csv')
        with open(path, 'w') as outfile:
            writer = DictWriter(outfile, fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
            logging.info(f"Wrote {len(rows)} rows to {str(path.absolute())}")
